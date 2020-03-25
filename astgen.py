
class Line:
    def __init__(self, num, arr):
        self.num = num
        self.element = arr

def read_lexers_file(filename):
    f = open(filename, "r")
    tokens = []
    for line in f:
        if len(line.split()) >= 1:
            tokens.append(line.split())
    f.close()
    line = []
    begin_flag = 0
    for i in tokens:
        if len(i) != 1:
            if int(i[1]) == 4:
                begin_flag = 1
            if begin_flag:
                line.append(i)
    line.pop(0);
    line.pop();
    return line




class Expression:
    def __init__(self, left, right, middle):
        self.left = left
        self.right = right
        self.middle = middle

        self.type = "EXP"

    def __repr__(self):
        return "Exp\n middle: %s\n left: %s\n right: %s\n" % (self.middle, self.left, self.right)
    def __str__(self):
        return self.__repr__()

class Operator:
    def __init__(self, code, value):
        self.value = value
        self.code = code
        if code > 11:
            self.type = "OPR"
        else:
            self.type = "SGN"
        if code == 30:
            self.order = 5
        elif 31<= code <= 32:
            self.order = 4
        elif 33 <= code <= 34:
            self.order = 3
        else:
            self.order = 2
    def __repr__(self):
        return "Op\n value: %s\n code: %s\n type: %s\n order: %s\n" % (self.value, self.code, self.type, self.order)
    def __str__(self):
        return self.__repr__()

class Identifier:
    def __init__(self, code, value):
        self.value = value
        self.code = code
        if code == 1:
            self.type = "VAR"
        elif code <= 2:
            self.type = "NUM"
    def __repr__(self):
        return "Id\n value: %s\n code: %s\n type: %s\n" % (self.value, self.code, self.type)
    def __str__(self):
        return self.__repr__()


def to_class(arr):
    if int(arr[1]) < 3:
        return Identifier(int(arr[1]), arr[0])
    elif 30 <= int(arr[1]) <= 36:
        return Operator(int(arr[1]), arr[0])
    elif 10 <= int(arr[1]) <= 11:
        return Operator(int(arr[1]), arr[0])


def main():
    raw_code_section = read_lexers_file("output.out")

    buf = []
    for i in raw_code_section:
        buf.append(to_class(i))

    exp = []
    for i in buf:
        if i.type == "OPR":
            l = buf[buf.index(i) - 1]
            r = buf[buf.index(i) + 1]
            m = i
            exp.append(Expression(l, r, m))

    convert(exp)
    return 0

def printer(e, var):
    if e.middle.code == 31:
        print("add %s rax" % (var.value))
        print("mov rax %s" % (e.right.value))
    elif e.middle.code == 32:
        print("add %s rax" % (var.value))
        print("mov rax %s" % (e.right.value))
    elif e.middle.code == 33:
        print("mul rax %s" % (e.right.value))
    elif e.middle.code == 34:
        print("div rax %s" % (e.right.value))
        
def convert(exp):
    var = exp[0].left
    for e in exp:
        if e.middle.code == 30:
            print("mov %s %s" %(e.left.value, e.right.value))
        elif 31 <= e.middle.code <= 34:
            printer(e, var)
            if exp.index(e) == len(exp) - 1:
                break
    print("add %s rax" % (var.value))


            


if __name__ == "__main__":
    main()
