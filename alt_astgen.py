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

class Poland:
    commands = [[4, 1, 1, 1, 1, 1, 5],
                [2, 2, 2, 1, 1, 1, 2],
                [2, 2, 2, 1, 1, 1, 2],
                [2, 2, 2, 2, 2, 1, 2],
                [2, 2, 2, 2, 2, 1, 2],
                [5, 1, 1, 1, 1, 1, 3]]
    poland = []
    texas = []
    count = 0

    def __init__(self, prePoland):
        self.prePoland = prePoland

    def indexOp(self, op):
        #print(op)
        if  op == '+': return 1
        if op == "-": return 2
        if op == "*": return 3
        if op == "/": return 4
        if op == "(": return 5
        if op == ")": return 6
        return 0
        
    def getLastTexas(self):
        return self.texas[-1]

    def getCom(self, indexLast, index):
        return self.commands[indexLast][index]

    def command(self, com):
        if com == 1:
            self.texas.append(self.prePoland[self.count])
            #self.count+=1
        elif com == 2:
            self.poland.append(self.getLastTexas())
            self.texas.pop()
            #self.texas.append(self.prePoland[self.count])
            #self.count+=1
        elif com == 3:
            self.texas.pop()
            #self.count+=1
        else:
            print("error Poland")
        #self.command(self.getCom(indexLast, index))
    
    def go(self):
        for c in self.prePoland:
            #print(c)
            index = self.indexOp(self.prePoland[self.count])
            #print(c + " "+ str(index))
            #print(self.count)
            if (index == 0):
                self.poland.append(self.prePoland[self.count])
                self.count+=1
                #print(self.count)
            else:
                if (self.texas != []):
                    #indexLast = self.indexOp(self.getLastTexas())
                    while (True):
                        indexLast = self.indexOp(self.getLastTexas())
                        #print("comand " + str(self.getCom(indexLast, index)))
                        self.command(self.getCom(indexLast, index))
                        #print("poland : " + str(self.poland))
                        #print("texas  : " + str(self.texas))
			if (self.getCom(indexLast, index) != 2): break
                    
                    self.count+=1
                else:
                    self.texas.append(self.prePoland[self.count])
                    self.count+=1
            #print("poland : " + str(self.poland))
            #print("texas  : " + str(self.texas))
            #print("prePo  : " + str(self.prePoland[self.count:]))
        self.poland.append(self.texas[0])
        self.texas.pop()
        #print("poland : " + str(self.poland))
        #print("texas  : " + str(self.texas))

    def get(self):
        return self.poland

    

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
            elif prefer.code < i.code:
                prefer = i
    if prefer:
        return text.index(prefer)
    else:
        return 0

def calc(stack, text):
    i = find_operator(text)
    #print(i)
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
    print(text) 
    prePoland = []

    for t in text:
        prePoland.append(t.value)

    poland = Poland(prePoland)
    poland.go()
    print(poland.get())

    while len(text) != 1:
        calc(stack, text)
    print(text)

    print(stack)
    #print(text)

    return 0

if __name__ == "__main__":
    main()
