from checker import *
from copy import deepcopy

def in_array(e, arr):
    for i in arr:
        if e[0] == i[0] and e[1] == i[1]:
            return True
    return False

def in_marks(mark, arr):
    print(mark)
    print(arr)
    for i in arr:
        if mark[0] == i[0]:
            return True
    return False

def check_marks(marks):
    jmps = list(filter(lambda token: token[2][1] == 'jmp', marks))
    mark = list(filter(lambda token: token[2][1] == 'mark', marks))

    last = []
    for jmp in jmps:
        last = jmp
        ret = False
        for mrk in mark:
            if jmp[2][0] == mrk[2][0]:
                ret = True
        if not ret:
            print("Line {}: error mark \"{}\" not exist".format(last[2][2], last[2][0]))

    return True

def main():
    if error:
        return 0
    raw_lines = list_of_lexems
    variables = []
    marks = []
    definitions = []
    complete = []
    in_var  = 0
    in_def  = 0
    for token in raw_lines:
        i = raw_lines.index(token)
        if token[0] == 'Var':
            in_var = 1
        elif token[0] == 'Begin':
            in_var = 0
        if in_var and token[1] == '8':
            variables.append(token)
        if token[1] == '8' and not in_array(token, variables):
            if raw_lines[i + 2][1] == '7':
                print("Line {}: error variable {} wasn't declared".format(token[2], token[0]))
                return 0
            token[1] = 'mark'
            marks.append([i, len(definitions), token])
        if token[1] == 'jmp':
            marks.append([i, len(definitions), token])
        if token[1] == '8' and not in_def and not in_var:
            in_def = 1
            definitions.append([])
        elif token[0] == ';' and in_def:
            in_def = 0
        if in_def:
            definitions[-1].append(token)


    if not check_marks(marks):
        return 0

    num = []
    op  = []
    tmp = []
    minus = 0
    for expr in definitions:
        complete.append([])
        tmp.clear()
        num.clear()
        op.clear()
        while expr:
            token = expr.pop(0)
            print(op)
            print(num)
            print('\n')
            if token[1] == '8' or token[1] == '3':
                num.append(token)
            elif token[1] != '5':
                if not op:
                    op.append(token)
                else:
                    if token[1] == '21' or token[1] == '23':
                        if op[-1][1] == '21' or op[-1][1] == '23':
                            if order[token[0]] > order[op[-1][0]]:
                                op.append(token)
                            else:
                                while order[token[0]] <= order[op[-1][0]] and (op[-1][1] == '21' or op[-1][1] == '23'):
                                    tmp = [op.pop(), num.pop(-2), num.pop()]
                                    num.append(tmp)
                                op.append(token)

                        elif op[-1][1] == 'Minus':
                            tmp = [op.pop(), num.pop()]
                            num.append(tmp)
                            op.append(token)

                        else:
                            op.append(token)
                            
                    elif token[1] == '10':
                        op.append(token)
                    elif token[1] == '11':
                        while op[-1][0] != '(':
                            if op[-1][1] == 'Minus':
                                tmp = [op.pop(), num.pop()]
                            if op[-1][1] == '21' or op[-1][1] == '23':
                                tmp = [op.pop(), num.pop(-2), num.pop()]
                            num.append(tmp)
                        if op[-1][0] == '(':
                            op.pop()
                    elif token[1] == 'Minus':
                        op.append(token)
        if not expr:
            while len(num) != 1:
                tmp = [op.pop(), num.pop(-2), num.pop()]
                num.append(tmp)
        complete[-1] = deepcopy(num)

    index = 0
    while marks:
        complete.insert(marks[0][1] + index, marks.pop(0)[2])
        index += 1

    complete.insert(0, variables)
    for i in complete:
        print(i)

    f = open("main.asm", "w")
    f.write("format ELF64\n")
    f.write("public _start\n")
    f.write("section '.data' writable\n")

    for variable in complete.pop(0):
        f.write("\t{}\tdd\t0x00\n".format(variable[0]))

    f.write("section '.text' executable\n")
    f.write("_start:\n")

    for expr in complete:
        tmp = []
        if not (type(expr[0]) is list):
            if expr[1] != "jmp":
                f.write("{}:\n".format(expr[0]))
            else:
                f.write("jmp\t{}\n".format(expr[0]))
        else:
            get_flat_array(expr, tmp)
            tmp.reverse()
            declr = 0
            for token in tmp:
                if token[1] == '3' or token[1] == '8':
                    if token == tmp[-2]:
                        declr = 1
                    if not declr:
                        if token[1] == '8':
                            f.write("\tmov\teax,\t[{}]\n".format(token[0][0]))
                            f.write("\tpush\trax\n")
                        else:
                            f.write("\tpush\t{}\n".format(token[0]))
                elif token[1] == '21' or token[1] == '23':
                    f.write("\tpop\trax\n")
                    f.write("\tpop\trbx\n")
                    if token[0] == "+":     f.write("\tadd\trax,\trbx\n")
                    elif token[0] == "-":   f.write("\tsub\trax,\trbx\n")
                    elif token[0] == "*":   f.write("\timul\trax,\trbx\n")
                    elif token[0] == "/":   f.write("\tidiv\trbx\n")
                    f.write("\tpush\trax\n")
                elif token[1] == "Minus":
                    f.write("\tpop\trax\n")
                    f.write("\tneg\trax\n")
                    f.write("\tpush\trax\n")
                elif token[1] == '7':
                    f.write("\tpop\trax\n")
                    f.write("\tmov\t[{}],\teax\n".format(tmp[-2][0]))




    f.write("\tcall\texit\n")
    f.write("section '.exit' executable\n")
    f.write("exit:\n")
    f.write("\tmov\trax,\t1\n")
    f.write("\tmov\trbx,\t0\n")
    f.write("\tint\t0x80\n")

    f.close()

    return 0

def get_flat_array(multi_dim_array, tmp):
    for arr in multi_dim_array:
        if type(arr[0]) is list:
            get_flat_array(arr, tmp)
        else:
            tmp.append(arr)

order = {
        "=": 0,
        "+": 1,
        "-": 1,
        "*": 2,
        "/": 2,
        "(": 3,
        ")": 3
        }

if __name__ == "__main__":
    main()

