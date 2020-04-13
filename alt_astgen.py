from checker import *

def translate_data_segment(data_segment):
    print("section .data")
    for var in data_segment:
        if var.code == 1:
            print("\t%s:\tdd 0x00" % var)

    print("section .bss")

def calc_print(operator_token, register = "eax"):
    if operator_token.code == 31:
        print("\tadd\teax, ebx")
    elif operator_token.code == 32:
        print("\tsub\teax, ebx")
    elif operator_token.code == 33:
        print("\tmul\tebx")
    elif operator_token.code == 34:
        print("\tdiv\tebx")
    elif operator_token.code == 30:
        print("\tmov\t[eax], ebx")
    elif operator_token.code == 1:
        print("\tmov\teax, [%s]" % operator_token)
    else:
        print("\tmov\t%s, %s" % (register, operator_token))
        
def translate_code_segment(final_prefix_forms):
    print("section .text")
    print("\tglobal _start")
    print("_start:")
    print("\tpush\tebp")
    print("\tmov\tebp, esp")
    for prefix_form in final_prefix_forms:
        stack = []
        stored = []

        eax = 0

        prefix_form_without_minus = list(filter((lambda x: x.code != 37), prefix_form))
        for i in range(len(prefix_form_without_minus)):
            if is_operator(prefix_form_without_minus[i]):
                if is_operator(prefix_form_without_minus[i + 1]) or is_operator(prefix_form_without_minus[i + 2]):
                    if not is_operator(prefix_form_without_minus[i + 1]):   #думаю, вот это можно сделать куда более лаконично
                        stack_counter=1
                    else:
                        stack_counter=2
                    stored.append(stack_counter)
                else:
                    stack_counter = 0
                    stored.append(stack_counter)
        prefix_form.reverse()

        for token in prefix_form:
            in_stack = 0
            if is_operator(token):
                in_stack = stored.pop()
                if in_stack == 2:
                    print("\tpop\teax")
                    print("\tpop\tebx")
                elif in_stack == 1:
                    print("\tpop\tebx")
                calc_print(token)
                if token.code != 30:
                    print("\tpush\teax")
            elif not is_operator(token) and token.code != 37:
                if eax:
                    calc_print(token, "ebx")
                    eax = 0
                elif not eax:
                    calc_print(token, "eax")
                    eax = 1

            elif token.code == 37:
                print("\tpop\tebx")
                print("\tneg\tebx")
                print("\tpush\tebx")



    print("\tmov\teax, 0")
    print("\tpop\tebp")
    print("\tret")

#вспомогательные функции
def min_order(tokens_array):
    minimal_order = tokens_array[0].order
    for i in tokens_array:
        minimal_order = min(minimal_order, i.order)
    return minimal_order

def max_order(tokens_array):
    maximal_order = tokens_array[0].order
    for i in tokens_array:
        maximal_order = max(maximal_order, i.order)
    return maximal_order

def min_bracket(tokens_array):
    minimal_bracket = tokens_array[0].bracket
    for i in tokens_array:
        minimal_bracket = min(minimal_bracket, i.bracket)
    return minimal_bracket

def max_bracket(tokens_array):
    maximal_bracket = tokens_array[0].bracket
    for i in tokens_array:
        maximal_bracket = max(maximal_bracket, i.bracket)
    return maximal_bracket

def max_bracket_order(tokens_array):
    max_br_ordr = tokens_array[0].bracket + tokens_array[0].order
    ret = None
    for i in tokens_array:
        max_br_ordr = max(max_br_ordr, i.bracket + i.order)
        ret = i
    return ret

def select_min_ordered_tokens(tokens_array):
    minimal_order = min_order(tokens_array)

    min_ordered_tokens = []
    for token in tokens_array:
        if token.order == minimal_order:
            min_ordered_tokens.append(token)
    return min_ordered_tokens

def select_max_ordered_tokens(tokens_array):
    maximal_order = max_order(tokens_array)

    max_ordered_tokens = []
    for token in tokens_array:
        if token.order == maximal_order:
            max_ordered_tokens.append(token)
    return max_ordered_tokens

def min_ordered_operator(tokens_array):
    m = 6
    ret = None
    for token in tokens_array:
        if token.order < m and is_operator(token):
            m = token.order
            ret = token
    return ret

def min_ordered_token(tokens_array):
    m = 6
    ret = None
    for token in tokens_array:
        if token.order < m:
            m = token.order
            ret = token
    return ret

def is_bracket(token):
    if 35 <= token.code <= 36:
        return True
    return False


def find_operator(tokens_array):
    for token in tokens_array:
        if is_operator(token):
            return token
    return None

def find_minus(tokens_array):
    for token in tokens_array:
        if token.code == 37:
            return token
    return None
#Конец вспомогательных функций


def brackets_ordering(tokens_array):
    bracket_array = list(filter((lambda x: is_bracket(x)), tokens_array))   #выбираем все скобки в один массив
    c1 = 1 
    c2 = 0
    layer_array = []                #массив для показания вложенности скобок
    shift_array = []                #массив для показания накопленности открывающих скобок
    for bracket in bracket_array:   #составление массивов вложенности и накапливающиего открывающие скобки
        if bracket.code == 35:
            layer_array.append(c1)
            c1 += 1
            c2 += 1
        else:
            c1 -= 1
            layer_array.append(c1)
        shift_array.append(c2)

    unclosed_shift_brackets = list(filter((lambda x: shift_array.count(x) == 1), shift_array)) #массив для открывающих скобок, индекс которых в накапливающем массиве встречается 1 раз
    
    for i in range(1, len(layer_array)):                    #формируем номера для скобок
        if (layer_array[i - 1] > layer_array[i] and         #выбираем номер для закрывающей скобки,
            shift_array[i - 1] <= shift_array[i]):          #которая является парой для открывающей скобки в unclosed_shift_brackets
            shift_array[i] = unclosed_shift_brackets.pop()
        bracket_array[i - 1].order = shift_array[i - 1]
        bracket_array[i].order = shift_array[i]

    #print(layer_array)
    #print(shift_array)

    for token in tokens_array:              #замещаем скобки в исходном выражении на пронумерованные
        if is_bracket(token):
            token = bracket_array.pop(0)

        if 1 <= token.code <= 2:            #удаляем скобки если в них заключена константа или переменная
            i = tokens_array.index(token)
            if is_bracket(tokens_array[i - 1]) and is_bracket(tokens_array[i + 1]):
                tokens_array.pop(tokens_array.index(token) - 1)
                tokens_array.pop(tokens_array.index(token) + 1)

def tokens_ordering_by_brackets(tokens_array):
    bracket = 0
    for token in tokens_array:
        token.bracket = bracket
        if is_bracket(token):
            bracket = token.order   #в токене скобки номер скобки содержится в свойстве order
            token.bracket = bracket
            if token.code == 36:
                bracket -= 1

def collect_tokens_by_bracket(tokens_array):
    Identifier = tokens_array.pop(0)            #удаляем
    Semicolon = tokens_array.pop(0)             #объявление
    VariableDeclarator = tokens_array.pop(0)    #переменной
    VariableDeclarator.value = Semicolon.value + VariableDeclarator.value

    #объединяем все токены в одной скобке в массив
    max_br = max_bracket(tokens_array)
    tokens_in_brackets_array = []
    for i in range(max_br + 1):
        tokens_in_brackets_array.append(list(filter((lambda x: x.bracket == i and not is_bracket(x)), tokens_array))) 
    
    #нумеруем подряд все операторы, исходя из номера скобок
    op_order_in_brackets = 1
    for array in tokens_in_brackets_array:
        while array:
            op = min_ordered_operator(array)
            if op:
                array.remove(op)
                op.order = op_order_in_brackets
                op_order_in_brackets+=1
            else:
                array.pop()
                
    return [Identifier, VariableDeclarator]

def unary_minus_processing(tokens_array):   #обрабатываем унарные минусы так
    before_bracket = []                     #что все унарные минусы перед переменными или константами объединяем
    minus = 0                               #в итоге остаются только унарные минусы перед скобками
    for token in tokens_array:
        i = tokens_array.index(token)
        if token.code == 37:
            minus = 1
        elif token.code in [1, 2]:
            if minus:
                token.value = '-' + token.value;
                minus = 0
                tokens_array.pop(i - 1)
        elif token.code == 35:
            if minus:
                before_bracket.append(i)
                minus = 0
    while before_bracket:
        i = before_bracket.pop()
        tokens_array[i - 1].order = 0

def collect_tokens_by_order(tokens_array):              #собирает в массивы все токены с одним order'ом
    tokens_in_order_array = []
    for i in range(max_order(tokens_array) + 1):
        tokens_in_order_array.append([])
        for token in tokens_array:
            if token.order == i and not is_bracket(token):
                tokens_in_order_array[-1].append(token)

    for simple_expression in tokens_in_order_array:         #построение префиксной формы для каждого простого выражения
        prefix_form_of_simple_expression(simple_expression)

    return tokens_in_order_array

def prefix_form_of_simple_expression(simple_expression):    #создаем префиксную форму простого выражения
    op = find_operator(simple_expression)
    minus = find_minus(simple_expression)
    if simple_expression:
        if op:
            simple_expression.remove(op)
            simple_expression.insert(0, op)
        if minus:
            simple_expression.remove(minus)
            simple_expression.append(minus)

def tokens_ordering_by_operators(tokens_array):         #нумерация констант и переменных в соответствии с оператором
    max_order_in_bracket = 0
    max_orders = []
    for token in tokens_array:
        i = tokens_array.index(token)
        if token.code == 34 and is_bracket(tokens_array[i - 1]):
            br = tokens_array[i - 1].bracket
            in_bracket = 0
            for j in tokens_array:
                if j.bracket == br:
                    if j.code == 35:
                        in_bracket = 1
                    elif j.code == 36:
                        in_bracket = 0
                if in_bracket and is_operator(j):
                    max_order_in_bracket = max(max_order_in_bracket, j.order)
            max_orders.append(max_order_in_bracket)

    for i in range(max_order(tokens_array) + 1):
        for token in tokens_array:
            if token.order == i and is_operator(token):
                index = tokens_array.index(token)
                if not is_bracket(tokens_array[index - 1]):
                    tokens_array[index - 1].order = i
                if not is_bracket(tokens_array[index + 1]):
                    tokens_array[index + 1].order = i
                if token.code == 34 and is_bracket(tokens_array[index - 1]):
                    tokens_array[index + 1].order = max_orders.pop(0)

    buf = list(filter((lambda x: not is_bracket(x)), tokens_array))
    return buf

def prefixation(text):                  #основная функция для построения префиксной/постфиксной формы
    prefix_form = []

    tokenized_text = []
    for array in text:              
        tokenized_text.append([])   
        for lexem in array:
            tokenized_text[-1].append(lexem)

    final_prefix_forms = []             #массив для префиксных форм выражений
    for array in tokenized_text:
        array.pop()

        unary_minus_processing(array)                                       #обрабатываем унарные минусы
        brackets_ordering(array)                                            #нумеруем порядок скобок
        tokens_ordering_by_brackets(array)                                  #нумеруем токены в соответствии со скобками
        expression_id_init = collect_tokens_by_bracket(array)               #собираем в массивы токены в скобках
        ordered_by_ops = tokens_ordering_by_operators(array)                #нумеруем операторы в соответствии с порядком и скобками
        prefix_array_tokens_form = collect_tokens_by_order(ordered_by_ops)  #собираем токены в массивы простых выражений

        final_prefix_form = [expression_id_init[1], expression_id_init[0]]  #добавляем в префиксную форму объявление переменной

        i = 0
        minus_found = 0
        for prefix_form in prefix_array_tokens_form:            #все унарные минусы, которые присутствуют 
            if find_minus(prefix_array_tokens_form[0]):         #в префиксных формах из простых выражений являются минусами
                minus_found = True
                for minus in prefix_array_tokens_form[0]:       #перед скобками
                    if prefix_form[0].bracket == minus.bracket + 1: #в таких унарных минусах содержится номер скобки, перед которой они стоят
                        prefix_form.insert(0,minus)                 #вставляем перед простой префиксной формой минус
                        prefix_array_tokens_form[0].remove(minus)   #удаляем используемый минус

            if not minus_found:
                for token in prefix_form:
                    final_prefix_form.append(token)                 #добавляем токены в финальную префиксную форму
            else:
                if prefix_array_tokens_form.index(prefix_form):
                    for token in prefix_form:
                        final_prefix_form.append(token)                 #добавляем токены в финальную префиксную форму

        final_prefix_forms.append(final_prefix_form)                #в список префиксных форм добавляем обработанный результат
        postfix_form = final_prefix_form.copy()
        postfix_form.reverse()                                      #постфиксная форма выражения
        print(postfix_form)
    return final_prefix_forms

def main():
    #проверка программы на синтаксическую правильность
    program_checker = Checker("output.out")
    program_checker.var_begin_end()
    if not program_checker.result:  #выход из программы в случае если выявлена ошибка при проверке
        return 0
    

    data = []           #в массив будут складываться объявленные переменные
    buf = []            #для всех токенов в основном тексте программы
    in_section = 0      #маркер для секции
    for token in program_checker.tokens:
        if token.code == 3 or token.code == 4:
            in_section = token.code             #маркировка секции
            
        if in_section == 3:
            if token.code == 1 and token.code != 4:
                data.append(token)
        elif in_section == 4:
            if token.code != 5 and token.code != 4:
                buf.append(token)

    text = [[]]
    i = 0
    for arr in buf:                #разбиение массива из токенов на массивы из выражений
        text[i].append(arr)
        if arr.code == 10:
            text.append([])
            i+=1
    text.remove([])                             #удаление пустого массива в конце буфера (несовершеннство алгоритма)
    final_prefix_forms = prefixation(text)      #строим префиксную форму для массива с выражениями
    
    translate_data_segment(data)                #перевод в ассемблер объявленных переменных
    translate_code_segment(final_prefix_forms)  #перевод выражений в префиксной форме

    return 0

if __name__ == "__main__":
    main()

