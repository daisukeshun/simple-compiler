
#TODO:: Запилить чтение из того, что нам выплюнул сишный лексер (output.out)
#       Считать переменные и числа в класс идентификаторов
#       Считать арифметические операторы в классы операторов
#       Можно сразу сделать заполнение data_segment'a в классе Program (просто напихать туда все переменные после Var и до Begin

def mincro_fabric(value, code):
    if 1 <= code <= 2:
        return Identifier(value, code)
    elif 30 <= code <= 34:
        return Operator(value, code)
    elif 10 <= code <= 11:
        return Sign(value, code)


class Sign:
    def __init__(self, value, code):
        self.code = code
        self.type = "sign"
        self.value = value
        if code == 10:
            self.type = "semicolon"
        elif code == 11:
            self.type = "comma"

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Sigh\n code: %s\n type: %s\n value: %s\n" % (self.code, self.type, self.value)

class Operator:
    def __init__(self, value, code):
        self.code = code
        self.value = value
        self.type = "operator"

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Operator\n code: %s\n type: %s\n value: %s\n" % (self.code, self.type, self.value)

class Identifier:
    def __init__(self, value, code):
        self.code = code
        self.value = value
        if code == 1:
            self.type = "variable"
        elif code == 2:
            self.type = "number"

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Identifier\n code: %s\n type: %s\n value: %s\n" % (self.code, self.type, self.value)

class Program:
    def __init__(self):
        self.data_section = []
        self.code_section = []

def main():
    token = "ab = 11 + 2 + 3 - 10 * 20 - a;"

    line = []
    line.append(mincro_fabric("ab", 1))
    line.append(mincro_fabric("=", 30))
    line.append(mincro_fabric("20", 2))
    line.append(mincro_fabric(";", 10))
    print(line)
    exp = [];

    i = 0
    while not exp.count(line[-1]):
        if len(line) == i:
            break

        exp.append(line[i].value)
        i+=1
        if(len(exp) == 3):
            print(exp)
            exp.pop()
            exp.pop()





if __name__ == "__main__":
    main()
