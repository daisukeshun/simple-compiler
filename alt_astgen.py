class Reader:
    def flag_reading(self, filename, before, after):
        f = open(filename, "r")

        array = []
        flag = False

        for line in f.readlines():
            if len(line.split()) and line.split()[0][0] != ':':
                if len(line.split()) > 1:
                    code = int(line.split()[1])
                else:
                    continue
                if code == before:
                    flag = True
                elif code == after:
                    flag = False
                if flag and  before != code != after:
                    array.append(line.split())
        f.close()
        return array

    def data_segment(self, filename):               #чтение объявления переменных
        return self.flag_reading(filename, 3, 4)

    def text_segment(self, filename):               #чтение основного текста программы
        return self.flag_reading(filename, 4, 5)

class VariableDeclarator:
    def __init__(self, var = None, init = None):
        self.type = "VariableDeclarator"
        self.id = var
        self.init = init
    def __repr__(self):
        return "%s %s %s " % (self.type, self.id, self.init)

class Literal:
    def __init__(self, value = None, raw = ""):
        self.type = "Literal"
        self.value = value
        self.raw = raw
    def __repr__(self):
        return "%s %s %s " % (self.type, self.value, self.raw)

class Identifier:
    def __init__(self, name = ""):
        self.type = "Identifier"
        self.name = name
    def __repr__(self):
        return "%s %s " % (self.type, self.name)

class BinaryExpression:
    def __init__(self, operator = None, left = None, right = None):
        self.type = "BinaryExpression"
        self.operator = operator
        self.left = left
        self.right = right
    def __repr__(self):
        return "%s %s %s %s " % (self.type, self.operator, self.left, self.right)

class UnaryExpression:
    def __init__(self, operator = "-", argument = None):
        self.type = "UnaryExpression"
        self.operator = operator
        self.argument = argument
    def __repr__(self):
        return "%s %s %s " % (self.type, self.operator, self.argument)

class Translator:
    def data(self, data):
        print("global _start")
        print("section .data")
        for i in data:
            if int(i[1]) == 1:
                print("%s\t dd 0x00" % i[0])

    def text(self, stakenize_text):
        print("section .text")
        print("_start:")

    def to_class(self, token):
        if is_operator(token):
            if token.code == 30:
                return VariableDeclarator()
            else:
                return BinaryExpression(token.value)
        elif token.code == 1:
            return Identifier(token.value)
        elif token.code == 2:
            return Literal(int(token.value), token.value)
        elif token.code == 37:
            return UnaryExpression()

    def to_dict(self, obj, classkey=None):
        if isinstance(obj, dict):
            data = {}
            for (k, v) in obj.items():
                data[k] = self.to_dict(v, classkey)
            return data
        elif hasattr(obj, "_ast"):
            return self.to_dict(obj._ast())
        elif hasattr(obj, "__iter__") and not isinstance(obj, str):
            return [self.to_dict(v, classkey) for v in obj]
        elif hasattr(obj, "__dict__"):
            data = dict([(key, self.to_dict(value, classkey))
                for key, value in obj.__dict__.items()
                if not callable(value) and not key.startswith('_')])
            if classkey is not None and hasattr(obj, "__class__"):
                data[classkey] = obj.__class__.__name__
            return data
        else:
            return obj

    def generate_ast(self, stakenized_lines):
        for expression in stakenized_lines:



class Token:                            #содержит в себе представление лексемы со вспомогательными свойствами
    def __init__(self, el):
        self.value = el[0]              #значение лексемы
        self.code = int(el[1])          #код
        if 30 <= self.code <= 32:
            self.order = 0              #порядок
        elif 33 <= self.code <= 34:
            self.order = 2              #порядок
        self.bracket = 0                #скобка, в которой эта лексема

    def __repr__(self):
        return "%s" % (self.value)
    def __str__(self):
        return self.value

def tokenize(arr):                  #переводит массив считанных лексем в токены
    ret = []
    for i in arr:
        ret.append(Token(i))
    return ret

def is_operator(token):             #вспомогательная функция для определения оператора
    if 30 <= token.code <= 34:
        return True
    else:
        return False

def find_min_order(text):           #выбираем токен с минимальным приоритетом
    mi = text[0].order
    arr = []
    for i in text:
        mi = min(mi, i.order)
    for i in text:
        if i.order == mi:
            arr.append(i)
    return arr

def find_bracket(text):             #находит первый токен открывающейся или закрывающейся скобки
    for i in text:
        if  35 <= i.code <= 36:
            return text.index(i)
    return False


def collect_brackets(text):         #собираем все скобки и их индексы в один массив
    arr = []
    for item in text:
        if 35 <= item.code <= 36:
            arr.append([item, text.index(item)])
    return arr

def find_last(arr):                 #находит повторяющиеся элементы в массиве
    example = arr[0]
    ret = []
    for i in arr:
        if example[0] == i[0]:
            ret.append(i)
    for i in ret:
        arr.remove(i)
    return ret

def close_bracket_fix(arr1, arr2):  #индексирует скобки в приоритете от вложенности
    current = []
    for i in range(1, len(arr1)):
        if arr1.count(arr1[i - 1]) == 1:
            current.append(arr1[i - 1])
    if not current:
        return False
    now = []
    for i in range(1, len(arr1)):       #супер хитрый алгоритм, завязанный на порядке открывающихся скобок и вложенности выражения
        if arr1[i - 1] == arr1[i]:
            if arr2[i - 1] > arr2[i]:
                now.append([arr1[i], i])
    now.reverse()
    last = find_last(now)
    b = current.pop()
    for i in last:
        arr1[i[1]] = b
    return True

def brackets_ordering(text):            #общая индексация скобок
    brackets = collect_brackets(text)

    counter = 0
    depth = 0
    in_bracket = 0
    arr1 = []
    arr2 = []

    for b in brackets:              #формирование массивов для close_bracket_fix
        if b[0].code == 35:
            counter+=1
            depth+=1
        arr1.append(counter)
        arr2.append(depth)
        if b[0].code == 36:
            depth-=1
        b[0].bracket = counter

    checker = True
    while checker:
        checker = close_bracket_fix(arr1, arr2)

    for i in range(len(arr1)):
        brackets[i][0].bracket = arr1[i]
    return brackets

def brackets_sort(ordered_brackets):    #сортировка скобок по порядку
    ret = []
    for i in ordered_brackets:
        if i[0].code == 35:
            ret.append([])
        ret[i[0].bracket - 1].append(i)
    return ret

def find_min_tokens(text):              #находит токены в скобке с минимальным индексом
    min_bracket = text[0].bracket
    for i in text:
        if i.bracket < min_bracket:
            min_bracket = i.bracket

    ret = []
    for i in text:
        if i.bracket == min_bracket:
            ret.append(i)
    return ret

def find_operator(chosen_tokens):       #находит предпочитаемый токен из уже выбранных токенов в скобке
    prefer = None
    for i in chosen_tokens:
        if i.code == 37 and chosen_tokens[chosen_tokens.index(i) + 1].code == 35:
            prefer = i
            break
        if not prefer:
            if is_operator(i):
                prefer = i
        elif prefer:
            if is_operator(i):
                if i.code <= prefer.code:
                    prefer = i
    if prefer:
        return chosen_tokens.index(prefer)
    else:
        return 0

def calculate(stack, chosen_tokens):
    for i in chosen_tokens:
        if not stack:
            if is_operator(i):
                stack.append(chosen_tokens.pop(chosen_tokens.index(i)))
        else:
            if stack[-1].code == 30:
                stack.append(chosen_tokens.pop(0))
            else:
                prefer = find_operator(chosen_tokens)           #выбираем приоритетный токен для включения в стек
                stack.append(chosen_tokens.pop(prefer))         #включаем приоритетный токен в стек
    if not stack:
        stack.append(chosen_tokens.pop())

def remove_brackets(text):              #удаляет скобки в выражении
    while 1:
        i = find_bracket(text)
        if i:
            text.pop(i)
        else:
            break
    for i in text:
        if i.code == 10:
            text.remove(i)

def prepare_token_brackets(text):           #индексирует токены в соответствии со скобками и порядком выполнения операций
    ordered_brackets = brackets_ordering(text)
    sorted_ordered_brackets = brackets_sort(ordered_brackets)
    buf = [0 for i in range(len(text))]
    for arr in sorted_ordered_brackets:
        for i in range(arr[0][1], arr[1][1]):
            buf[i] = arr[0][0].bracket
            if text[i - 1].code == 37:
                buf[i - 1] = arr[0][0].bracket
    for i in range(len(text)):
        text[i].bracket = buf[i]

def final_minus_sort(stack):
    for i in range(1, len(stack)):
        if stack[i].code == 37 and stack[i - 1].code == 37:
            buf = stack[i]
            stack[i] = stack[i + 1]
            stack[i + 1] = buf
            
def op_count(text):
    counter = 0
    for i in text:
        if is_operator(i):
            counter+=1
    return counter

def op_proc(op_arr):
    bracket = op_arr[0].bracket + 1
    for i in op_arr:
        if i.order == 2:
            i.bracket = bracket
            bracket+=1

def bracketing(text):
    operators = list(filter((lambda x: is_operator(x)), text))
    op_proc(operators)
    while operators:
        min_op = find_min_order(operators)
        for i in min_op:
            index = text.index(i)
            text[index].bracket = i.bracket
            text[index + 1].bracket = i.bracket
            text[index - 1].bracket = i.bracket
            operators.remove(i)
    unary_minus_detection(text)     #помечает унарные минусы

    checker = text[0].bracket
    br = []
    for i in range(1, len(text)):
        if checker != text[i].bracket:
            difference = abs(checker - text[i].bracket)
            while difference:
                if checker < text[i].bracket:
                    br.append([i, Token(['(', '35'])])
                elif checker > text[i].bracket:
                    br.append([i, Token([')', '36'])])
                difference-=1
            checker = text[i].bracket
    i = 0
    while br:
        el = br.pop(0)
        text.insert(el[0], el[1])
        for arr in br: 
            arr[0]+=1
    for i in text:
        i.bracket = 0


def stackenize_tokens(text):        #строит префиксную запись
    bracketing(text)
    prepare_token_brackets(text)    #индексирует скобки в выражении
    
    stack = []
    while text:
        chosen_tokens = find_min_tokens(text)       #выбирает приоритетное выражение, учитывая приоритет выполнения операций
        for i in chosen_tokens:
            text.remove(i)                          #удаляем уже обработанные токены
        while chosen_tokens:
            calculate(stack, chosen_tokens)         #формируем префиксную запись

    remove_brackets(stack)
    return stack

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
                text[i].bracket = text[i + 1].bracket

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

#класс проверки
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

def main():
    #global check
    program_checker = Checker("output.out")
    program_checker.var_begin_end()
    program_checker.invalid()
    program_checker.operators()
    program_checker.brackets()
    program_checker.equals()
    #global check end

    program_reader = Reader()
    data = program_reader.data_segment("output.out")
    program_translator = Translator()

    #program_translator.data(data)
    buf = program_reader.text_segment("output.out")

    text = [[]]
    i = 0
    for arr in buf:             #предварительная обработка считанных лексем для токенизации
        text[i].append(arr)
        if int(arr[1]) == 10:
            text.append([])
            i+=1
    text.remove([])
    
    stakenized_lines = []
    for line in text:
        tokenized_line = tokenize(line)             #переводит выражение из массива в токены
        stack = stackenize_tokens(tokenized_line)   #переводит массив из токенов в префиксную форму без сортировки унарных минусов
        final_minus_sort(stack)
        stack.reverse()
        stakenized_lines.append(stack)              #добавляет полученное выражение в stakenized_lines


    program_translator.generate_ast(stakenized_lines)
    return 0

if __name__ == "__main__":
    main()
