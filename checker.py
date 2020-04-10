class Token:                            #содержит в себе представление лексемы со вспомогательными свойствами
    def __init__(self, el):
        self.value = el[0]              #значение лексемы
        self.code = int(el[1])          #код
        if 30 <= self.code <= 32:
            self.order = 1              #порядок
        elif 33 <= self.code <= 34:
            self.order = 2              #порядок
        else:
            self.order = 0
        self.bracket = 0                #скобка, в которой эта лексема

    def __repr__(self):
        return "%s" % (self.value)
    def __str__(self):
        return self.value

def unary_minus_detection(text):
    for i in range(1, len(text)):               #унарный минус может стоять только перед открывающей скобкой, 
        if text[i].code == 32:                  #числом и переменной, при этом перед минусом должен быть оператор или открывающая скобка
            if ((text[i + 1].code == 1 or
                text[i + 1].code == 2 or
                text[i + 1].code == 35 or
                text[i - 1].code == 35) and
                (text[i - 1].code == 35 or
                is_operator(text[i - 1]))):
                text[i].code = 37
                text[i + 1].value = '-' + text[i + 1].value
    for i in text:
        if i.code == 37:
            text.remove(i)


def is_operator(token):
    if 30 <= token.code <= 34:
        return True
    return False

class Line:                                 #содержит в себе номер строки и саму строку
    def __init__(self, number, line):       #нужен для вывода синтаксических ошибок
        self.number = number
        self.line = line
    def __repr__(self):
        return "num: %s, line: %s" % (self.number, self.line)
    def __str__(self):
        self.string = str(self.number) + ": "
        for token in self.line:
            self.string+=token[0].value
        return self.string

class Checker:
    def __init__(self, filename):   #конструктор, в который мы передаем путь до файла с лексемами
        self.filename = filename
        self.lines = []             #массив с экземплярами класса Line
        self.tokens = []            #массив с экземплярами класса Token 

        f = open(self.filename, "r")#считывание файла с лексемами в два массива
        line_counter = 1
        token_counter = 0
        for line in f.readlines():
            if len(line.split()):
                if line[0] == ':' and len(line.split()) == 1:
                    self.lines.append(Line(line_counter, []))
                    line_counter+=1
                else:
                    if len(line.split()) > 1:
                        self.tokens.append(Token(line.split()))
                        self.lines[-1].line.append([Token(line.split()),token_counter])
                        token_counter+=1
                    else:
                        continue
        f.close()

    def var_begin_end(self):        #проверка на наличие Var, Begin, End
        flag = {
        "var": 0,
        "begin": 0,
        "end": 0
        }
        defined = []                #объявленные переменные
        used = []                   #использованные переменные
        for i in range(len(self.tokens)):
            if self.tokens[i].code == 3:
                if flag["var"]:
                    print("Error: Var is not expected")             #Если два раза встречается Var, то ошибка
                    print(self.get_line_by_token_id(i))
                flag["var"] = 1
                if self.tokens[i + 1].code != 1:
                    print("Error: expect identifier after Var")     #Если после Var не идет идентификатор
                    print(self.get_line_by_token_id(i + 1))
            elif self.tokens[i].code == 4:
                if flag["begin"]:
                    print("Error: Begin is not expected")           #Если два раза встречается Begin, то ошибка
                    print(self.get_line_by_token_id(i))
                flag["begin"] = 1
                if self.tokens[i + 1].code != 1:
                    print("Error: expect identifier after Begin")   #Если после Begin не идет идентификатор
                    print(self.get_line_by_token_id(i + 1))
            elif self.tokens[i].code == 5:
                if flag["end"]:
                    print("Error: End is not expected")             #Если два раза встречается End, то ошибка
                    print(self.get_line_by_token_id(i))
                flag["end"] = 1
                if self.tokens[i - 1].code != 10:
                    print("Error: expect semicolon before End")     #Если перед End нет ;
                    print(self.get_line_by_token_id(i - 1))
            else:
                if self.tokens[i].code == 1:                        #считывание в массив объявленных и используемых переменных
                    if not flag["begin"]:
                        defined.append([self.tokens[i], i])
                    elif flag["begin"]:
                        used.append([self.tokens[i], i])
        selected = []                                               #проверка на соответствие объявленных и используемых переменных
        if len(defined) >= len(used):
       	    for i in defined:
       	        for j in used:
       	            if i[0].value == j[0].value:
       	                selected.append(j)
        else:
       	    for i in used:
       	        for j in defined:
       	            if i[0].value == j[0].value:
       	                selected.append(i)
        if selected != used:
            for i in used:
                if i not in selected:
                    print("Error: variable is not defined")
                    print(self.get_line_by_token_id(i[1]))

        if not flag["var"]:                                         #проверка на наличие ключевых слов
            print("Var is not found")
        elif not flag["begin"]:
            print("Begin is not found")
        elif not flag["end"]:
            print("End not found")
        else:
            return 1
        return 0

    def invalid(self):                      #проверка на правильность имен переменных и операторов
        for n_line in self.lines:
            for token in n_line.line:
                if token[0].code == 20:
                    token[0].value = "{}"
                    print("Error: invalid identifier\n%s" % (n_line))
                if token[0].code == 0:
                    token[0].value = "{}"
                    print("Error: invalid operator\n%s" % (n_line))

    def get_line_by_token_id(self, token_id):#вспомогательный метод, который получает строку исходя из индекса Token'a
        for n_line in self.lines:
            for token_n in n_line.line:
                if token_n[1] == token_id:
                    token_n[0].value = "{}"
                    return n_line

    def operators(self):                    #проверка на правильность использования операторов
        unary_minus_detection(self.tokens)  #маркировка унарного минуса
        for i in range(len(self.tokens)):
            if is_operator(self.tokens[i]):
               if (is_operator(self.tokens[i - 1]) or
                   is_operator(self.tokens[i + 1]) or 
                   self.tokens[i + 1].code == 10):
                   print("Error: operators chain\n%s" % (self.get_line_by_token_id(i)))
            elif self.tokens[i].code == 37:
               if (self.tokens[i - 1].code == 37 or
                   self.tokens[i + 1].code == 37):
                   print("Error: operators chain\n%s" % (self.get_line_by_token_id(i)))

    def brackets(self):                     #проверка правильного использования скобок
        checker = 0                         #маркер замкнутости скобок
        last_bracket = 0                    #индекс последней пройденной скобки
        for i in range(len(self.tokens)):
            if self.tokens[i].code == 35:
                if is_operator(self.tokens[i + 1]) and self.tokens[i + 1].code != 37 and self.tokens[i + 1].code != 35:
                    print(self.tokens[i + 1].code)
                    print("Error: operator not expected\n%s" % (self.get_line_by_token_id(i + 1)))
                elif not is_operator(self.tokens[i - 1]) and self.tokens[i - 1].code != 37 and self.tokens[i - 1].code != 35:
                    print("Error: literal not expected\n%s" % (self.get_line_by_token_id(i - 1)))
                checker+=1
                last_bracket = i
            elif self.tokens[i].code == 36:
                if is_operator(self.tokens[i - 1]):
                    print("Error: operator not expected\n%s" % (self.get_line_by_token_id(i - 1)))
                elif not is_operator(self.tokens[i + 1]) and self.tokens[i + 1].code != 10 and self.tokens[i + 1].code != 36:
                    print("Error: literal not expected\n%s" % (self.get_line_by_token_id(i + 1)))
                checker-=1
                last_bracket = i
        if checker:
            if checker > 0:
                print("Error: close bracket not found\n%s" % (self.get_line_by_token_id(last_bracket)))
            else:
                print("Error: open bracket not found\n%s" % (self.get_line_by_token_id(last_bracket)))

    def equals(self):                   #проверка на несколько = в одном выражении
        checker = 0
        last_equal = 0
        in_exp = 0
        for i in range(len(self.tokens)):
            if self.tokens[i].code == 30:
                in_exp = 1
                checker+=1
                last_equal = i
            elif self.tokens[i].code == 10 and in_exp:
                in_exp = 0
                checker-=1

        if checker > 0:
            print("Error: equal is not expected")
            print(self.get_line_by_token_id(last_equal))
