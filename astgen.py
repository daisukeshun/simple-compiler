class Operator:
    def __init__(self, code, value):
        if 30 <= code <= 34:
            self.code = code
            self.type = "math"
            self.value = value

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Operator\n code: %s\n type: %s\n value: %s\n" % (self.code, self.type, self.value)

class Identifier:
    def __init__(self, code, value):
        if 1 <= code <= 2:
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
    a = Identifier(2, "20")
    print(a)


if __name__ == "__main__":
    main()
