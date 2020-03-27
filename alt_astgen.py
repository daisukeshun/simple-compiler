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
        self.order = 0
        self.bracket = 0

    def __repr__(self):
        return "(value: '%s' bracket: %s)" % (self.value, self.bracket)
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

def find_min_order(text):
    mi = text[0].order
    arr = []
    for i in text:
        mi = min(mi, i.order)
    for i in text:
        if i.order == mi:
            arr.append(i)
    return arr

def find_bracket(text):
    for i in text:
        if  35 <= i.code <= 36:
            return text.index(i)
    return False


def collect_brackets(text):
    arr = []
    for item in text:
        if 35 <= item.code <= 36:
            arr.append([item, text.index(item)])
    return arr


def ordering(text):
    brackets = collect_brackets(text)

    counter = 0
    depth = 0
    in_bracket = 0
    arr1 = []
    arr2 = []

    for b in brackets:
        if b[0].code == 35:
            counter+=1
            depth+=1
        arr1.append(counter)
        arr2.append(depth)
        if b[0].code == 36:
            depth-=1
        b[0].bracket = counter

    before = 0
    current = []
    for i in range(1, len(arr1)):
        if not current.count(arr1[i - 1]):
            current.append(arr1[i - 1])
        else:
            current.remove(arr1[i - 1])
        if arr1[i - 1] == arr1[i]:
            if arr2[i - 1] > arr2[i]:
                arr1[i] = current.pop()

    for i in range(len(arr1)):
        brackets[i][0].bracket = arr1[i]

    return brackets



def main():
    program_reader = Reader()
    data = program_reader.data_segment("output.out")
    text = tokenize(program_reader.text_segment("output.out"))

    program_translator = Translator()
    program_translator.data(data)


    stack = []


    ordered_brackets = ordering(text)


    while 1:
        i = find_bracket(text)
        if i:
            text.pop(i)
        else:
            break
    text.pop(-1)

    return 0

if __name__ == "__main__":
    main()
