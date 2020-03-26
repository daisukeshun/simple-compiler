class Reader:
    def flag_reading(self, filename, before, after):
        f = open(filename, "r")

        array = []
        flag = False

        for line in f.readlines():
            if len(line.split()) and line.split()[0][0] != ':':
                code = int(line.split()[1])
                if code == before:
                    flag = True
                elif code == after:
                    flag = False
                if flag and  before != code != after:
                    array.append(line.split())
        f.close()
        return array

    def data_segment(self, filename):
        return self.flag_reading(filename, 3, 4)

    def text_segment(self, filename):
        return self.flag_reading(filename, 4, 5)


class Translator:
    def data(self, data):
        print("global _start")
        print("section .data")
        for i in data:
            if int(i[1]) == 1:
                print("%s\t dd 0x00" % i[0])

    def text(self, text):
        print("section .text")
        print("_start:")
        for i in text:
            if int(i[1]) == 1:
                print("%s\t dd 0x00" % i[0])

class Token:
    def __init__(self, el):
        self.value = el[0]
        self.code = int(el[1])

    def __repr__(self):
        return "(value: '%s' code: %s)" % (self.value, self.code)
    def __str__(self):
        return self.value

def tokenize(arr):
    ret = []
    for i in arr:
        ret.append(Token(i))
    return ret
        

def is_operator(token):
    if 30 <= token.code <= 34:
        return True
    else:
        return False

def find_operator(text):
    prefer = None
    for i in text:
        if is_operator(i):
            if prefer == None:
                prefer = i
            elif prefer.code > i.code:
                prefer = i
    if prefer:
        return text.index(prefer)
    else:
        return 0

def calc(stack, text):
    i = find_operator(text)
    if stack:
        if is_operator(stack[-1]):
            stack.append(text.pop(0))
        else:
            i = find_operator(text)
            stack.append(text.pop(i))
    else:
        stack.append(text.pop(i))


def main():
    program_reader = Reader()
    data = program_reader.data_segment("output.out")
    text = tokenize(program_reader.text_segment("output.out"))

    program_translator = Translator()
    program_translator.data(data)


    stack = []

    while len(text) != 1:
        calc(stack, text)

    print(stack)
    print(text)

    return 0

if __name__ == "__main__":
    main()
