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

    def text(self, stakenize_text):
        print("section .text")
        print("_start:")

        for token in stakenize_text:
            print(token.value, token.code)


class Token:
    def __init__(self, el):
        self.value = el[0]
        self.code = int(el[1])
        self.order = 0
        self.bracket = 0

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

def find_last(arr):
    example = arr[0]
    ret = []
    for i in arr:
        if example[0] == i[0]:
            ret.append(i)
    for i in ret:
        arr.remove(i)
    return ret

def close_bracket_fix(arr1, arr2):
    current = []
    for i in range(1, len(arr1)):
        if arr1.count(arr1[i - 1]) == 1:
            current.append(arr1[i - 1])
    if not current:
        return False
    now = []
    for i in range(1, len(arr1)):
        if arr1[i - 1] == arr1[i]:
            if arr2[i - 1] > arr2[i]:
                now.append([arr1[i], i])
    now.reverse()
    last = find_last(now)
    b = current.pop()
    for i in last:
        arr1[i[1]] = b
    return True

def brackets_ordering(text):
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

    checker = True
    while checker:
        checker = close_bracket_fix(arr1, arr2)

    for i in range(len(arr1)):
        brackets[i][0].bracket = arr1[i]
    return brackets

def brackets_sort(ordered_brackets):
    ret = []
    for i in ordered_brackets:
        if i[0].code == 35:
            ret.append([])
        ret[i[0].bracket - 1].append(i)
    return ret


def find_min_tokens(text):
    min_bracket = text[0].bracket
    for i in text:
        if i.bracket < min_bracket:
            min_bracket = i.bracket

    ret = []
    for i in text:
        if i.bracket == min_bracket:
            ret.append(i)
    return ret


def find_operator(chosen_tokens):
    prefer = None
    for i in chosen_tokens:
        if is_operator(i) and not prefer:
            prefer = i
        elif is_operator(i) and prefer:
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
                prefer = find_operator(chosen_tokens)
                stack.append(chosen_tokens.pop(prefer))


def unary_minus_detection(text):
    for i in range(1, len(text)):
        if text[i].code == 32:
            if (30 <= text[i - 1].code <= 34 or
                text[i + 1].code == 35 or
                text[i - 1].code == 35):
                text[i].code = 37

def remove_brackets(text):
    while 1:
        i = find_bracket(text)
        if i:
            text.pop(i)
        else:
            break
    text.pop(-1)

def prepare_token_brackets(text):
    ordered_brackets = brackets_ordering(text)
    sorted_ordered_brackets = brackets_sort(ordered_brackets)
    buf = [0 for i in range(len(text))]
    for arr in sorted_ordered_brackets:
        for i in range(arr[0][1], arr[1][1]):
            buf[i] = arr[0][0].bracket
    for i in range(len(text)):
        text[i].bracket = buf[i]

def final_minus_sort(stack):
    for i in range(1, len(stack)):
        if stack[i].code == 37 and stack[i - 1].code == 37:
            buf = stack[i]
            stack[i] = stack[i + 1]
            stack[i + 1] = buf

def stackenize_tokens(text):

    prepare_token_brackets(text)
    remove_brackets(text)
    unary_minus_detection(text)

    stack = []

    while text:
        chosen_tokens = find_min_tokens(text)
        for i in chosen_tokens:
            text.remove(i)
        while chosen_tokens:
            calculate(stack, chosen_tokens)

    return stack

def main():
    program_reader = Reader()
    data = program_reader.data_segment("output.out")
    program_translator = Translator()
    program_translator.data(data)

    buf = program_reader.text_segment("output.out")
    text = [[]]

    i = 0
    for arr in buf:
        text[i].append(arr)
        if int(arr[1]) == 10:
            text.append([])
            i+=1
    text.remove([])
    

    stakenized_lines = []
    for line in text:
        tokenized_line = tokenize(line)
        stack = stackenize_tokens(tokenized_line)
        final_minus_sort(stack)
        stakenized_lines.append(stack)
    print(stakenized_lines[0])

    return 0

if __name__ == "__main__":
    main()