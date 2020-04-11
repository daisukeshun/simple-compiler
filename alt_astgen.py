from checker import *

def translate_data_segment(data_segment):
    print("section .data")
    for var_name in data_segment:
        if int(var_name[1]) == 1:
            print("\t%s:\tdd 0x00" % var_name[0])

    print("section .bss")

def calc_print(operator_token):
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
        print("\tmov\teax, %s" % operator_token)

def translate_code_segment(final_prefix_forms):
    print("section .text")
    print("\tglobal _start")
    print("_start:")
    print("\tpush ebp")
    print("\tmov ebp, esp")
    for prefix_form in final_prefix_forms:
        stack = []
        stored = []
        for i in range(len(prefix_form)):
            if is_operator(prefix_form[i]):
                if is_operator(prefix_form[i + 1]) or is_operator(prefix_form[i + 2]):
                    if not is_operator(prefix_form[i + 1]):   #думаю, вот это можно сделать куда более элегантно и лаконично
                        stack_counter=1
                    else:
                        stack_counter=2
                    stored.append(stack_counter)
                    stack.append(prefix_form[i])
        prefix_form.reverse()
        for i in range(len(prefix_form)):
            if is_operator(prefix_form[i]):
                if not is_operator(prefix_form[i - 1]) and not is_operator(prefix_form[i - 2]):
                    for j in range(1, 3):
                        calc_print(prefix_form[i - j])
                    calc_print(prefix_form[i])
                else:
                    in_stack = stored.pop()
                    if in_stack == 2:
                        print("\tpop\teax")
                    else:
                        for j in range(1, 3):
                            if not is_operator(prefix_form[i - j]):
                                calc_print(prefix_form[i - j])
                    print("\tpop\tebx")
                    calc_print(stack.pop())
                if stack:
                    print("\tpush\teax")
    print("\tmov\teax, 0")
    print("\tpop\tebp")
    print("\tret")


class Reader:
    def flag_reading(self, filename, before, after):
        f = open(filename, "r")
        array = []
        flag = False
        for line in f.readlines():
            if len(line.split()) and line.split()[0][0] != '::':
                if len(line.split()) > 1:
                    code = int(line.split()[1])
                else:
                    continue
                if code == before:
                    flag = True
                elif code == after:
                    flag = False
                if flag and  before != code != after:
                    array.append(line.split())
        f.close()
        return array

    def data_segment(self, filename):               #чтение объявления переменных
        return self.flag_reading(filename, 3, 4)

    def text_segment(self, filename):               #чтение основного текста программы
        return self.flag_reading(filename, 4, 5)

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

def is_bracket(token):
    if 35 <= token.code <= 36:
        return True
    return False

def brackets_ordering(tokens_array):
    bracket_array = list(filter((lambda x: is_bracket(x)), tokens_array))
    c1 = 1 
    c2 = 0
    layer_array = []
    shift_array = []
    for bracket in bracket_array:
        if bracket.code == 35:
            layer_array.append(c1)
            c1 += 1
            c2 += 1
        else:
            c1 -= 1
            layer_array.append(c1)
        shift_array.append(c2)

    unclosed_shift_brackets = list(filter((lambda x: shift_array.count(x) == 1), shift_array))
    for i in range(1, len(layer_array)):
        if (layer_array[i - 1] > layer_array[i] and 
            shift_array[i - 1] <= shift_array[i]):
            shift_array[i] = unclosed_shift_brackets.pop(0)
        bracket_array[i - 1].order = shift_array[i - 1]
        bracket_array[i].order = shift_array[i]

    for token in tokens_array:
        if is_bracket(token):
            token = bracket_array.pop(0)

def tokens_ordering_by_brackets(tokens_array):
    bracket = 0
    for token in tokens_array:
        token.bracket = bracket
        if is_bracket(token):
            bracket = token.order
            token.bracket = bracket
            if token.code == 36:
                bracket -= 1

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

def collect_tokens_by_bracket(tokens_array):

    Identifier = tokens_array.pop(0)
    VariableDeclarator = tokens_array.pop(0)

    max_br = max_bracket(tokens_array)
    tokens_in_brackets_array = []
    for i in range(max_br + 1):
        tokens_in_brackets_array.append(list(filter((lambda x: x.bracket == i and not is_bracket(x)), tokens_array)))
    
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

def collect_tokens_by_order(tokens_array):

    tokens_in_order_array = []
    for i in range(max_order(tokens_array) + 1):
        tokens_in_order_array.append([])
        for token in tokens_array:
            if token.order == i and not is_bracket(token):
                tokens_in_order_array[-1].append(token)
    for simple_expression in tokens_in_order_array:
        prefix_form_of_simple_expression(simple_expression)

    return tokens_in_order_array

def find_operator(tokens_array):
    for token in tokens_array:
        if is_operator(token):
            return token
    return None

def prefix_form_of_simple_expression(simple_expression):
    op = find_operator(simple_expression)
    if simple_expression:
        if simple_expression.index(op) and op:
            simple_expression.remove(op)
            simple_expression.insert(0, op)

def tokens_ordering_by_operators(tokens_array):
    for i in range(max_order(tokens_array) + 1):
        for token in tokens_array:
            if token.order == i and is_operator(token):
                index = tokens_array.index(token)
                tokens_array[index - 1].order = tokens_array[index + 1].order = i


def prefixation(text):
    prefix_form = []

    tokenized_text = []
    for array in text:
        tokenized_text.append([])
        for lexem in array:
            tokenized_text[-1].append(Token(lexem))

    final_prefix_forms = []
    for array in tokenized_text:
        array.pop()

        unary_minus_detection(array)
        brackets_ordering(array)
        tokens_ordering_by_brackets(array)
        expression_id_init = collect_tokens_by_bracket(array)
        tokens_ordering_by_operators(array)
        prefix_array_tokens_form = collect_tokens_by_order(array)

        i = 0
        final_prefix_form = [expression_id_init[1], expression_id_init[0]]
        for prefix_form in prefix_array_tokens_form:
            for token in prefix_form:
                final_prefix_form.append(token)
                i+=1
        final_prefix_forms.append(final_prefix_form)
    return final_prefix_forms

def main():
    #global check
    program_checker = Checker("output.out")
    program_checker.var_begin_end()
    program_checker.identifiers_and_literals()
    program_checker.operators()
    program_checker.brackets()
    program_checker.equals()
    program_checker.invalid()
    #global check end

    program_reader = Reader()
    data = program_reader.data_segment("output.out")
    buf = program_reader.text_segment("output.out")
    text = [[]]
    i = 0
    for arr in buf:             #предварительная обработка считанных лексем для токенизации
        text[i].append(arr)
        if int(arr[1]) == 10:
            text.append([])
            i+=1
    text.remove([])
    final_prefix_forms = prefixation(text)
    
    translate_data_segment(data)
    translate_code_segment(final_prefix_forms)

    return 0

if __name__ == "__main__":
    main()

