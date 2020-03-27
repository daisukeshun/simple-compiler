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


def main():
    prePoland = ['(', '8', '+', '2', '*', '5', ')', '/', '(','1', '+', '3', '*', '2', '-', '4', ')']
    #['a', '=', '(', '1', '+', '1', ')', '*', '2', ';']
    #print(prePoland)
    poland = Poland(prePoland)
    poland.go()
    print(poland.get())



main()
