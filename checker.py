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
        self.result = True

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

    def clear_flags(self, flags):
        for key in flags:
            flags[key] = 0

    def var_begin_end(self):        #проверка на наличие Var, Begin, End
        flag = {
        "var": 0,
        "begin": 0,
        "end": 0,
        "variable": 0,
        "const": 0,
        "colon": 0,
        "semicolon": 0,
        "double_dot": 0,
        "declarator": 0,
        "minus": 0,
        "operator": 0,
        "open_bracket": 0,
        "close_bracket": 0,
        }

        in_section = 0
        var = 0
        begin = 0
        end = 0

        error = 0

        bracket_checker = 0
        last_checked_bracket = None

        defined = []                #объявленные переменные
        used = []                   #использованные переменные
        for i in range(len(self.tokens)):
            code = self.tokens[i].code

            if code == 1:
                if in_section == 3:
                    defined.append([self.tokens[i], i])
                    if not (flag["var"] + flag["colon"] + flag["semicolon"]):
                        self.result = False
                elif in_section == 4:
                    used.append([self.tokens[i], i])
                    if not (flag["begin"] + flag["operator"] + flag["minus"] + flag["semicolon"] + flag["open_bracket"] + flag["declarator"]):
                        self.result = False
                self.clear_flags(flag)
                flag["variable"] = 1

            elif code == 2:
                if in_section == 3:
                    self.result = False
                elif in_section == 4:
                    if not (flag["declarator"] + flag["operator"] + flag["minus"] + flag["open_bracket"]):
                        self.result = False
                self.clear_flags(flag)
                flag["const"] = 1

            elif code == 10:
                if in_section == 3:
                    if not flag["variable"]:
                        self.result = False
                elif in_section == 4:
                    if not (flag["variable"] + flag["const"] + flag["close_bracket"]):
                        self.result = False
                self.clear_flags(flag)
                flag["semicolon"] = 1

            elif code == 11:
                if in_section != 3:
                    self.result = False
                else:
                    if not (flag["variable"]):
                        self.result = False
                self.clear_flags(flag)
                flag["colon"] = 1

            elif code == 20:
                self.clear_flags(flag)
                flag["invalid"] = 1
                self.result = False

            elif code in [31, 33, 34]:
                if flag["close_bracket"] + flag["const"] + flag["variable"]:
                    self.clear_flags(flag)
                    flag["operator"] = 1

            elif code == 32:
                if flag["declarator"] + flag["open_bracket"]:
                    self.clear_flags(flag)
                    flag["minus"] = 1
                    self.tokens[i].code = 37
                    self.tokens[i].order = 0
                elif flag["close_bracket"] + flag["const"] + flag["variable"]:
                    self.clear_flags(flag)
                    flag["operator"] = 1
                else:
                    self.result = False

            elif code == 35:
                bracket_checker += 1
                last_checked_bracket = i
                if not (flag["operator"] + flag["open_bracket"] + flag["declarator"] + flag["minus"]):
                    self.result = False
                self.clear_flags(flag)
                flag["open_bracket"] = 1

            elif code == 36:
                bracket_checker -= 1
                last_checked_bracket = i
                if not (flag["variable"] + flag["const"] + flag["close_bracket"]):
                    self.result = False
                self.clear_flags(flag)
                flag["close_bracket"] = 1

            elif code == 38:
                if not (flag["variable"]):
                    self.result = False
                self.clear_flags(flag)
                flag["double_dot"] = 1

            elif code == 30:
                if flag["double_dot"]:
                    self.clear_flags(flag)
                    flag["declarator"] = 1

            elif code == 3:
                var = 1
                if in_section == 3:
                    self.result = False
                in_section = 3
                self.clear_flags(flag)
                flag["var"] = 1

            elif code == 4:
                begin = 1
                if not flag["semicolon"]:
                    self.result = False
                if in_section == 4:
                    self.result = False
                in_section = 4
                self.clear_flags(flag)
                flag["begin"] = 1

            elif code == 5:
                end = 1
                if not flag["semicolon"]:
                    self.result = False
                if in_section == 5:
                    self.result = False
                in_section = 5
                self.clear_flags(flag)
                flag["end"] = 1

            if not self.result:
                error = 1
                print(self.get_line_by_token_id(i))
                self.result = True

        if not var:
            print("Var not found")
        if not begin:
            print("Begin not found")
        if not end:
            print("End not found")

        if error:
            self.result = False

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
                    self.result = False
                    print("Error: variable is not defined")
                    print(self.get_line_by_token_id(i[1]))
                                                                    #конец проверки объявленных и используемых переменных
        if bracket_checker:
            print("Error: bracket not found")
            print(self.get_line_by_token_id(last_checked_bracket))



    def get_line_by_token_id(self, token_id):   #вспомогательный метод, который получает строку исходя из индекса Token'a
        for n_line in self.lines:
            for token_n in n_line.line:
                if token_n[1] == token_id:
                    token_n[0].value = "[]"
                    return n_line

