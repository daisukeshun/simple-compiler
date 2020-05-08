f = open("output.out", "r")

list_of_lexems = []
for line in f.readlines():
    list_of_lexems.append(line.split())
f.close()

flag = {
        "section": 0,

        "var": 0,
        "begin": 0,
        "end": 0,

        "const": 0,
        "variable": 0,
        "declarator": 0,

        "semicolon": 0,
        "colon": 0,

        "operator": 0,
        "minus": 0,

        "goto": 0,
        "mark": 0,
        "double_dot": 0,

        "o_bracket": 0,
        "c_bracket": 0,

        }

def clear_flags(flag):
    for key in flag:
        if key != "section":
            flag[key] = 0

definition = 0
go = 0
for line in list_of_lexems:
    if line[0] == "Var":
        if flag["var"]:
            print("Line {}: error {} not expected".format(line[2], line[0]))
        line[1] = "Keyword"
        clear_flags(flag)
        flag["section"] = 0
        flag["var"] = 1

    elif line[0] == "Begin":
        line[1] = "Keyword"
        if not flag["semicolon"] or flag["begin"]:
                print("Line {}: error {} not expected".format(line[2], line[0]))
        clear_flags(flag)
        flag["section"] = 1
        flag["begin"] = 1

    elif line[0] == "End":
        line[1] = "Keyword"
        if not flag["semicolon"] or flag["end"]:
                print("Line {}: error {} not expected".format(line[2], line[0]))
        clear_flags(flag)
        flag["section"] = 2
        flag["end"] = 1

    elif line[0] == "GO":
        line[1] = "Keyword"
        if flag["section"] != 1:
            print("Line {}: error {} not expected".format(line[2], line[0]))
        else:
            if not (flag["semicolon"] +
                    flag["begin"]):
                print("Line {}: error {} not expecter".format(line[2], line[0]))
        clear_flags(flag)
        go = 1

    elif line[0] == "TO":
        line[1] = "Keyword"
        if flag["section"] != 1:
            print("Line {}: error {} not expecter".format(line[2], line[0]))
        else:
            if go:
                clear_flags(flag)
                flag["goto"] = 1
            else:
                clear_flags(flag)
                flag["variable"] = 1

    elif line[1] == "8" and line[0] != "GO" and line[0] != "TO":
        if flag["section"] == 0:
            if not (flag["var"] + flag["semicolon"] + flag["colon"]):
                print("Line {}: error {} not expecter".format(line[2], line[0]))

        elif flag["section"] == 1:
            if definition:
                if not (flag["o_bracket"] + 
                        flag["declarator"] + 
                        flag["operator"] + 
                        flag["minus"]):
                    print("Line {}: error {} not expecter".format(line[2], line[0]))
            elif not definition:
                if not (flag["begin"] + 
                        flag["semicolon"] + 
                        flag["goto"]):
                    print("Line {}: error {} not expecter".format(line[2], line[0]))
        if flag["goto"]:
            line[1] = "jmp"
        clear_flags(flag)
        flag["variable"] = 1

    elif line[0] == ",":
        if flag["section"]:
            print("Line {}: error {} not expecter".format(line[2], line[0]))
            if not flag["variable"]:
                print("Line {}: error {} not expecter".format(line[2], line[0]))
        clear_flags(flag)
        flag["colon"] = 1

    elif line[0] == ";":
        if flag["section"] == 0:
            if not flag["variable"]:
                print("Line {}: error {} not expecter".format(line[2], line[0]))
        elif flag["section"] == 1:
            if not (flag["variable"] + 
                    flag["const"] +
                    flag["double_dot"] +
                    flag["c_bracket"]):
                print("Line {}: error {} not expecter".format(line[2], line[0]))
        clear_flags(flag)
        flag["semicolon"] = 1
        definition = 0

    elif line[1] == "3":
        if flag["section"] != 1:
            print("Line {}: error {} not expecter".format(line[2], line[0]))
        elif flag["section"] == 1:
            if not (flag["operator"] +
                    flag["declarator"] +
                    flag["minus"] +
                    flag["o_bracket"]):
                print("Line {}: error {} not expecter".format(line[2], line[0]))
        clear_flags(flag)
        flag["const"] = 1

    elif line[1] == "5":
        if flag["section"] != 1:
            print("Line {}: error {} not expecter".format(line[2], line[0]))
        else:
            if not flag["variable"]:
                print("Line {}: error {} not expecter".format(line[2], line[0]))
        clear_flags(flag)
        flag["double_dot"] = 1

    elif line[0] == "=":
        if not flag["double_dot"]:
            print("Line {}: error {} not expecter".format(line[2], line[0]))
        clear_flags(flag)
        flag["declarator"] = 1
        definition = 1

    elif line[1] == "2":
        if flag["section"] != 1:
            print("Line {}: error {} not expecter".format(line[2], line[0]))
        else:
            unary = False
            if line[0] == "-":
                if not (flag["declarator"] +
                        flag["o_bracket"]):
                    unary = False
                else:
                    unary = True
            
            if not unary:
                if not (flag["c_bracket"] +
                        flag["const"] +
                        flag["variable"]):
                    print("Line {}: error {} not expecter".format(line[2], line[0]))

            clear_flags(flag)
            if unary:
                line[1] = "Minus"
                flag["minus"] = 1
            else:
                flag["operator"] = 1

    elif line[0] == "(":
        if flag["section"] != 1:
            print("Line {}: error {} not expecter".format(line[2], line[0]))
        else:
            if not (flag["operator"] +
                    flag["declarator"] +
                    flag["minus"] +
                    flag["o_bracket"]):
                print("Line {}: error {} not expecter".format(line[2], line[0]))
        clear_flags(flag)
        flag["o_bracket"] = 1

    elif line[0] == ")":
        if flag["section"] != 1:
            print("Line {}: error {} not expecter".format(line[2], line[0]))
        else:
            if not (flag["variable"] +
                    flag["const"] +
                    flag["c_bracket"]):
                print("Line {}: error {} not expecter".format(line[2], line[0]))
        clear_flags(flag)
        flag["c_bracket"] = 1
