import re
import math
import tkinter as tk
from tkinter import scrolledtext, messagebox
from PIL import Image, ImageTk

# Определения типов данных
DATA_TYPES = {"%", "!", "$"}
VARIABLE_PATTERN = r"([a-zA-Z_][a-zA-Z_0-9]*)"
RELATION_OPERATORS = {"<", ">", "<=", ">=", "==", "!="}
ADDITION_OPERATORS = {"+", "-"}
MULTIPLICATION_OPERATORS = {"*", "/"}
UNARY_OPERATORS = {"-"}

# Хранилище для значений переменных
variables = {}

# Функция для обработки описания переменных
def parse_declaration(declaration):
    parts = declaration.split()
    if len(parts) < 2:
        return "Ошибка: неполное описание переменных."

    var_type = parts[0]
    if var_type not in DATA_TYPES:
        return f"Ошибка: неизвестный тип данных '{var_type}'."

    # Проверка на использование "=" вместо "as"
    if "=" in declaration:
        return "Ошибка: для объявления переменных используйте только ключевое слово 'as', а не '='."

    # Получаем имена переменных и значения (если есть присваивание)
    declaration_content = ' '.join(parts[1:])
    var_declarations = [v.strip() for v in declaration_content.split(",")]

    for var_declaration in var_declarations:
        if " as " in var_declaration:
            var_name, var_value = var_declaration.split(" as ", 1)
            var_name = var_name.strip()
            var_value = var_value.strip()

            if not re.fullmatch(VARIABLE_PATTERN, var_name):
                return f"Ошибка: некорректное имя переменной '{var_name}'."

            # Вычисляем значение переменной и проверяем тип
            try:
                evaluated_value = eval(var_value, {"sqrt": math.sqrt}, {k: v["value"] for k, v in variables.items()})

                # Проверка, чтобы логические значения не присваивались целочисленным переменным
                if var_type == "%" and isinstance(evaluated_value, bool):
                    return f"Ошибка: значение '{var_value}' не может быть логическим для переменной типа '{var_type}'. Программа остановлена."

                if not validate_type(var_type, evaluated_value):
                    return f"Ошибка: значение '{var_value}' не соответствует типу данных '{var_type}'. Программа остановлена."

                variables[var_name] = {"type": var_type, "value": evaluated_value}
            except Exception as e:
                return f"Ошибка в инициализации переменной '{var_name}': {e}"
        else:
            var_name = var_declaration.strip()
            if not re.fullmatch(VARIABLE_PATTERN, var_name):
                return f"Ошибка: некорректное имя переменной '{var_name}'."
            variables[var_name] = {"type": var_type, "value": None}  # Инициализация значением None

    declared_vars = ', '.join(var.split(' as ')[0].strip() for var in var_declarations)
    return f"Переменные {declared_vars} типа {var_type} успешно объявлены."

def apply_operator(values, operator):
    if operator in ADDITION_OPERATORS:
        b, a = values.pop(), values.pop()
        values.append(a + b if operator == "+" else a - b)
    elif operator in MULTIPLICATION_OPERATORS:
        b, a = values.pop(), values.pop()
        values.append(a * b if operator == "*" else a / b)
    elif operator in RELATION_OPERATORS:
        b, a = values.pop(), values.pop()
        values.append(eval(f"a {operator} b"))

def precedence(op):
    if op in MULTIPLICATION_OPERATORS:
        return 2
    if op in ADDITION_OPERATORS:
        return 1
    if op in RELATION_OPERATORS:
        return 0
    return -1

# Функция для обработки выражений с учетом правил языка
def parse_expression(expression):
    try:
        tokens = re.split(
            rf"\s*({'|'.join(map(re.escape, RELATION_OPERATORS | ADDITION_OPERATORS | MULTIPLICATION_OPERATORS | UNARY_OPERATORS | {'(', ')'}))})\s*",
            expression)

        value_stack = []
        operator_stack = []

        for token in tokens:
            token = token.strip()
            if not token:
                continue

            # Обработка чисел в различных системах счисления
            try:
                parsed_number = parse_number(token)
                value_stack.append(parsed_number)
                continue
            except ValueError:
                pass  # Не число, идем дальше

            # Обработка констант pi и exp
            if token.lower() == "pi":
                value_stack.append(math.pi)
            elif token.lower() == "exp":
                value_stack.append(math.exp(1))
            elif token.lower() == "true":
                value_stack.append(True)
            elif token.lower() == "false":
                value_stack.append(False)
            elif validate_identifier(token):  # Идентификаторы
                if token in variables:
                    value_stack.append(variables[token]["value"])
                else:
                    raise ValueError(f"Переменная '{token}' не определена.")
            elif token == "(":
                operator_stack.append(token)
            elif token == ")":
                while operator_stack and operator_stack[-1] != "(":
                    apply_operator(value_stack, operator_stack.pop())
                operator_stack.pop()  # Убираем '('
            elif token in UNARY_OPERATORS:  # Унарные операторы
                if token == "-":
                    value_stack.append(-value_stack.pop())
            elif token in RELATION_OPERATORS | ADDITION_OPERATORS | MULTIPLICATION_OPERATORS:
                while (operator_stack and
                       precedence(operator_stack[-1]) >= precedence(token)):
                    apply_operator(value_stack, operator_stack.pop())
                operator_stack.append(token)
            else:
                raise ValueError(f"Некорректный токен '{token}'.")

        while operator_stack:
            apply_operator(value_stack, operator_stack.pop())

        return value_stack[0] if value_stack else None

    except Exception as e:
        return f"Ошибка в выражении '{expression}': {e}"

# Функция для обработки идентификаторов
def validate_identifier(identifier):
    return re.fullmatch(r"[a-zA-Z_][a-zA-Z_0-9]*", identifier) is not None

# Функция для обработки различных типов чисел
def parse_number(value):
    value = value.strip()

    # Проверка на двоичное (например, 1010B)
    if re.fullmatch(r"[01]+[Bb]", value):
        return int(value[:-1], 2)

    # Проверка на восьмеричное (например, 77O)
    elif re.fullmatch(r"[0-7]+[Oo]", value):
        return int(value[:-1], 8)

    # Проверка на десятичное (например, 1234D или 1234)
    elif re.fullmatch(r"\d+[Dd]?", value):
        return int(value.rstrip("Dd"))

    # Проверка на шестнадцатеричное (например, FFH)
    elif re.fullmatch(r"[0-9A-Fa-f]+[Hh]", value):
        return int(value[:-1], 16)

    # Проверка на действительное число с плавающей точкой (например, 1.23 или .456)
    elif re.fullmatch(r"\d*\.\d+([eE][+-]?\d+)?", value):
        return float(value)

    # Проверка на научную нотацию с опциональным знаком (например, 1.23E+5, .456E-3, 123e5)
    elif re.fullmatch(r"(\d+(\.\d*)?|\.\d+)[eE][+-]?\d+", value):
        return float(value)

    else:
        raise ValueError(f"Некорректное числовое значение '{value}' в разных системах счисления.")

# Функция для проверки соответствия значения типу данных
def validate_type(var_type, value):
    if var_type == "%" and isinstance(value, int):
        return True
    elif var_type == "!" and isinstance(value, float):
        return True
    elif var_type == "$" and isinstance(value, bool):
        return True
    return False

# Функция для выполнения и проверки выражений
def evaluate_expression(expression):
    try:
        # Вычисление выражения с использованием текущих значений переменных, а также pi и exp
        result = eval(expression, {"sqrt": math.sqrt, "pi": math.pi, "exp": math.exp(1)},
                      {k: v["value"] for k, v in variables.items()})
        return f"Результат: {result}" if not isinstance(result, bool) else ("Истина" if result else "Ложь")
    except Exception as e:
        return f"Ошибка в выражении: {e}"

# Функция для обработки выражений присваивания
def handle_assignment(expression):
    var_name, expr_value = expression.split(" as ", 1)
    var_name = var_name.strip()
    expr_value = expr_value.strip()

    if var_name not in variables:
        return f"Ошибка: переменная '{var_name}' не объявлена."

    var_type = variables[var_name]["type"]

    try:
        evaluated_value = parse_expression(expr_value)

        if var_type == "%" and not isinstance(evaluated_value, int):
            return f"Ошибка: значение '{expr_value}' должно быть целым числом для типа '%'."
        elif var_type == "!" and not isinstance(evaluated_value, float):
            return f"Ошибка: значение '{expr_value}' должно быть вещественным числом для типа '!'."
        elif var_type == "$" and not isinstance(evaluated_value, bool):
            return f"Ошибка: значение '{expr_value}' должно быть логическим для типа '$'."

        variables[var_name]["value"] = evaluated_value
        return f"{var_name} = {variables[var_name]['value']}"

    except Exception as e:
        return f"Ошибка в присваивании: {e}"

# Функция для обработки составного оператора
def handle_compound_operator(commands):
    for command in commands:
        command = command.strip()
        if command:
            parse_program(command)

# Функция для обработки операторов ввода
def handle_input(identifiers):
    for identifier in identifiers:
        identifier = identifier.strip()
        if identifier not in variables:
            return f"Ошибка: переменная '{identifier}' не объявлена."

        var_type = variables[identifier]["type"]
        value = input(f"Введите значение для {identifier} (тип {var_type}): ")

        # Попытка преобразовать ввод к нужному типу данных
        try:
            if var_type == "%":
                value = int(value)
            elif var_type == "!":
                value = float(value)
            elif var_type == "$":
                if value.lower() in ("true", "истина", "1"):
                    value = True
                elif value.lower() in ("false", "ложь", "0"):
                    value = False
                else:
                    raise ValueError("Неверное логическое значение")
        except ValueError:
            return f"Ошибка: введено некорректное значение для переменной '{identifier}' с типом '{var_type}'."

        # Сохраняем значение, если оно прошло проверку
        variables[identifier]["value"] = value

# Функция для обработки операторов вывода
def handle_output(expressions):
    for expression in expressions:
        expression = expression.strip()
        if expression:
            result = evaluate_expression(expression)
            output_text.insert(tk.END, result + "\n")  # Выводим результат в текстовое поле

# Функция для отображения задания
def show_task():
    task_text = """
    7 вариант 12311
    
    1. Операции языка
        1.1. Операции группы «отношение»
            1) <операции_группы_отношения>::= <> | = | < | <= | > | >=
        1.2. Операции группы «сложение»
            1) <операции_группы_сложения>::= + | - | or
        1.3. Операции группы «умножение»
            1) <операции_группы_умножения>::= * | / | and
        1.4. Унарная операция
            1) <унарная_операция>::= not
            
    2. Правила, определяющие структуру программы
        2.1. Структура программы
            2) <программа>::= «{» {/ (<описание> | <оператор>) ; /} «}»
            
    3. Правила, определяющие раздел описания переменных
        3.1. Синтаксис команд описания данных
            3) <описание>::= <тип> <идентификатор> { , <идентификатор> }
            
    4. Правила, определяющие типы данных
        4.1. Описание типов данных
            1) <тип>::= % | ! | $
            
    5. Правило, определяющее оператор программы
    <оператор>::= <составной> | <присваивания> | <условный> | <фиксированного_цикла> | <условного_цикла> | <ввода> | <вывода>
        5.1. Синтаксис составного оператора
            1) <составной>::= «[» <оператор> { ( : | перевод строки) <оператор> } «]»
        5.2. Синтаксис оператора присваивания
            1) <присваивания>::= <идентификатор> as <выражение>
        5.3. Синтаксис оператора условного перехода
            1) <условный>::= if <выражение> then <оператор> [ else <оператор>]
        5.4. Синтаксис оператора цикла с фиксированным числом повторений
            1) <фиксированного_цикла>::= for <присваивания> to <выражение> do <оператор>
        5.5. Синтаксис условного оператора цикла
            1) <условного_цикла>::= while <выражение> do <оператор>
        5.6. Синтаксис оператора ввода
            1) <ввода>::= read «(»<идентификатор> {, <идентификатор> } «)»
        5.7. Синтаксис оператора вывода
            1) <вывода>::= write «(»<выражение> {, <выражение> } «)»
            
    6. Многострочные комментарии в программе
        1) { … }
    
    
    Правила языка для всех вариантов:
    Выражения языка задаются правилами:
        1. <выражение>::= <операнд>{<операции_группы_отношения> <операнд>}
        2. <операнд>::= <слагаемое> {<операции_группы_сложения> <слагаемое>}
        3. <слагаемое>::= <множитель> {<операции_группы_умножения> <множитель>}
        4. <множитель>::= <идентификатор> | <число> | <логическая_константа> | <унарная_операция> <множитель> | «(»<выражение>«)»
        5. <число>::= <целое> | <действительное>
        6. <логическая_константа>::= true | false
        
    Правила, определяющие идентификатор, букву и цифру:
        7. <идентификатор>::= <буква> {<буква> | <цифра>}
        8. <буква>::= A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P | Q | R | S | T | U | V | W | X | Y | Z | a | b | c | d | e | f | g | h | i | j | k | l | m | n | o | p | q | r | s | t | u | v | w | x | y | z
        9. <цифра>::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
        
    Правила, определяющие целые числа:
        10. <целое>::= <двоичное> | <восьмеричное> | <десятичное> | <шестнадцатеричное>
        11. <двоичное>::= {/ 0 | 1 /} (B | b)
        12. <восьмеричное>::= {/ 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 /} (O | o)
        13. <десятичное>::= {/ <цифра> /} [D | d]
        14. <шестнадцатеричное>::= <цифра> {<цифра> | A | B | C | D | E | F | a | b | c | d | e | f} (H | h)
    
    Правила, описывающие действительные числа:
        15. <действительное>::= <числовая_строка> <порядок> | [<числовая_строка>] . <числовая_строка> [порядок]
        16. <числовая_строка>::= {/ <цифра> /}
        17. <порядок>::= ( E | e )[+ | -] <числовая_строка>

    """
    output_text.insert(tk.END, task_text + "\n")

# Функция для справки
def help_program():
    help_text = """
    Эта программа поддерживает выполнение различных операций, включая математические вычисления, 
    операции сравнения, логические операции, циклы и условные операторы, а также ввод и вывод значений.

    Основные правила и команды:

    1. Структура программы:
       Программа должна быть заключена в фигурные скобки `{}` и может содержать несколько операторов, 
       разделённых точкой с запятой `;`.

    2. Описание переменных и типы данных:
       Для объявления переменных используйте типы данных:
       - `%` - целочисленный тип (`int`)
       Пример: `% x, y;` - объявляет переменные `x` и `y` как целые числа.
       
       - `!` - вещественный тип (`float`)
       Пример: `! a as 5.5;` - объявляет переменную `a` как вещественное число и присваивает ей значение 5.5.
       
       - `$` - логический тип (`bool`)
       Пример: `$ flag as True;` - объявляет переменную `flag` как логическую и устанавливает значение `True`.

    3. Операторы:
       - Присваивание: `<идентификатор> as <выражение>`
         Пример: `x as 5 + 10;` - присваивает переменной `x` результат выражения `5 + 10`.

       - Составной оператор: `[...]`
         Пример: `[ x as 1 : y as x + 1 ]`

       - Условный оператор: `if <выражение> then <оператор> [else <оператор>]`
         Пример: `if x > y then write(x) else write(y);`

       - Цикл с фиксированным числом повторений: `for <присваивание> to <выражение> do <оператор>`
         Пример: `for x as 0 to 5 do write(x);`

       - Цикл с условием: `while <выражение> do <оператор>`
         Пример: `while x < 10 do [ x as x + 1 : write(x) ]`

       - Ввод значений: `read(<идентификатор>)`
         Пример: `read(x, y);`

       - Вывод значений: `write(<выражение>)`
         Пример: `write(x + y);`

    4. Логические операторы:
       - and: возвращает `Истина`, если оба операнда истинны.
         Пример: `x > 0 and y < 10`
         
       - or: возвращает `Истина`, если хотя бы один из операндов истинен.
         Пример: `x == 0 or y == 10`
         
       - not: возвращает `Истина`, если операнд ложен.
         Пример: `not x == 10`

    5. Дополнительные операторы:
       - Математический корень: `sqrt(<выражение>)`
         Пример: `write(sqrt(x));`
         
       - Возведение в степень: `**`
         Пример: `write(x ** 2);`

    6. Комментарии:
       Многострочные комментарии заключаются в фигурные скобки `{ ... }` и игнорируются при выполнении.
       Пример: `{ Это комментарий, он будет проигнорирован программой }`
       
    7. Системы счисления:
       Чтобы обозначить какую-либо систему счисления, в конце числа нужно добавить букву, 
       принадлежащую той или иной системе счисления
       - Двоичная система счисления: B или b
       Пример: binaryVar as 1101b; 
       
       - Восьмеричная система счисления: O или o
       Пример: octalVar as 17o;
       
       - Десятичная система счисления: D или d или ничего
       Пример: decimalVar as 42d;
       
       - Шестнадцатеричная система счисления: H или h
       Пример: hexVar as 2Fh;
       
    8. Константы 
        - pi 
        Пример: write(pi)
        
        - exp
        Пример: write(exp)
    """
    output_text.insert(tk.END, help_text + "\n")

def print_examples():
    examples = """
    Пример 1: Операции присваивания и арифметические операции.
    {
        % x, y;
        x as 10;
        y as 5;
        write(x + y);  { Вывод: 15 }
        write(x - y);  { Вывод: -5 }
        write(x * y);  { Вывод: 50 }
        write(y / x);  { Вывод: 2 }
    }

    Пример 2: Логические операторы (and, or, not) и операции сравнения.
    {
        $ a, b;
        a as (10 > 5) and (3 < 7);
        b as (10 == 10) or (5 > 10);
        write(a);  { Вывод: Истина }
        write(b);  { Вывод: Истина }
        write(not a); { Вывод: Ложь }
    }

    Пример 3: Использование if-then-else.
    {
        % x as 10;
        if x > 5 then write("x больше 5") else write("x меньше или равно 5");
        { Вывод: "x больше 5" }
    }

    Пример 4: Цикл с фиксированным числом повторений (for).
    {
        % i;
        for i as 0 to 3 do write(i);
        { Вывод: 0, 1, 2, 3 }
    }

    Пример 5: Условный цикл (while).
    {
        % x as 1;
        while x < 5 do [ write(x) : x as x + 1 ];
        { Вывод: 1, 2, 3, 4 }
    }

    Пример 6: Ввод и вывод значений.
    {
        % x, y;
        read(x, y);
        write("Введенные значения:", x, y);
    }

    Пример 7: Операции возведения в степень и корень.
    {
        ! a as 9.0;
        write(sqrt(a));  { Вывод: 3.0 }
        write(a ** 2);   { Вывод: 81.0 }
    }

    Пример 8: Объявление различных типов данных и работа с ними.
    {
        % x as 10;
        ! y as 3.5;
        $ flag as (x > y);
        write(x);  { Вывод: 10 }
        write(y);  { Вывод: 3.5 }
        write(flag);  { Вывод: Истина }
    }
    
    Примеры для 17 правил.
    
    Правило 1: <выражение>::= <операнд>{<операции_группы_отношения> <операнд>}
    {
        % a, b;
        a as 10;
        b as 5;
        c as 20;
        write(a + b > c)  { Вывод: Ложь }
    }
    
    Правило 2: <операнд>::= <слагаемое> {<операции_группы_сложения> <слагаемое>}
    {
        % a, b;
        a as 10;
        b as 5;
        c as 20;
        write(a - b + c)  { Вывод: 25 }
    }
    
    Правило 3: <слагаемое>::= <множитель> {<операции_группы_умножения> <множитель>}
    {
        write(3 * 4 / 2)  { Вывод: 6 }
    }
    
    Правило 4: <множитель>::= <идентификатор> | <число> | <логическая_константа> | <унарная_операция> <множитель> | «(»<выражение>«)»
    {
        % a;
        a as -5;
        write(-5);  { Вывод: -5 }
        write(a)  { Вывод: -5 }
    }
    
    Правило 5: <число>::= <целое> | <действительное>
    {
        write(42);  { Вывод: 42 }
        write(sqrt(25)); { Вывод: 5.0 }
        write(sqrt(2));  { Вывод: 1.4142135623730951 }
        write(3/2)  { Вывод: 1.5 }
    }
    Правило 6: <логическая_константа>::= true | false
    {
        $ a, b;
        a as false;
        b as true;
        write(a);  { Вывод: false }
        write(b)  { Вывод: true }
    }
    
    Правило 7: <идентификатор>::= <буква> {<буква> | <цифра>}
    { 
        % var1, var2, var3;
        var1 as 10;
        var2 as 20;
        var3 as var1 + var2; 
        write(var3);  { Вывод: 30 }
    }
    
    Правило 8: <буква>::= A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P | Q | R | S | T | U | V | W | X | Y | Z | a | b | c | d | e | f | g | h | i | j | k | l | m | n | o | p | q | r | s | t | u | v | w | x | y | z
    { 
        % x, y;
        x as 5;
        y as 15;
        write(x);  { Вывод: 5 }
        write(y);  { Вывод: 15 }
    }
    
    Правило 9: <цифра>::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
    { 
        % a1, b2;
        a1 as 8;
        b2 as 7;
        write(a1);  { Вывод: 8 }
        write(b2);  { Вывод: 7 }
    }
    
    Правило 10: <целое>::= <двоичное> | <восьмеричное> | <десятичное> | <шестнадцатеричное>
    { 
        % bin, oct, dec, hex;
        bin as 1010b;    { Двоичное 10 }
        oct as 12o;      { Восьмеричное 10 }
        dec as 10;       { Десятичное 10 }
        hex as 0Ah;       { Шестнадцатеричное 10 }
        write(bin);  { Вывод: 10 }
        write(oct);  { Вывод: 10 }
        write(dec);  { Вывод: 10 }
        write(hex);  { Вывод: 10 }
    }
    
    Правило 11: <двоичное>::= {/ 0 | 1 /} (B | b)
    { 
        % binaryVar;
        binaryVar as 1101b;  { Двоичное 13 в десятичном формате }
        write(binaryVar);  { Вывод: 13 }
    }
    
    Правило 12: <восьмеричное>::= {/ 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 /} (O | o)
    { 
        % octalVar;
        octalVar as 17o;  { Восьмеричное 15 в десятичном формате }
        write(octalVar);  { Вывод: 15 }
    }
    
    Правило 13: <десятичное>::= {/ <цифра> /} [D | d]
    { 
        % decimalVar;
        decimalVar as 42d;  { Десятичное 42 }
        write(decimalVar);  { Вывод: 42 }
    }
    
    Правило 14: <шестнадцатеричное>::= <цифра> {<цифра> | A | B | C | D | E | F |
a | b | c | d | e | f} (H | h)
    { 
        % hexVar;
        hexVar as 2Fh;  { Шестнадцатеричное 47 в десятичном формате }
        write(hexVar);  { Вывод: 47 }
    }
    
    Правило 15: <действительное>::= <числовая_строка> <порядок> | [<числовая_строка>] . <числовая_строка> [порядок]
    Правило 16: <числовая_строка>::= {/ <цифра> /}
    Правило 17: <порядок>::= ( E | e )[+ | -] <числовая_строка>
    { 
        ! expVar1 as 1.23E+3;
        ! expVar2 as 1.23E-3;
        write(expVar1)  { Вывод: 1230.0 };
        write(expVar2)  { Вывод: 0.00123 }
    }
    
    """
    output_text.insert(tk.END, examples + "\n")

# Основная функция для анализа программы
def parse_program(program):
    program = program.strip()

    if program.strip().lower() == "help":
        help_program()
        return

    if program.strip().lower() == "example":
        print_examples()
        return

    if program.strip().lower() == "task":
        print_examples()
        return

    if not (program.startswith("{") and program.endswith("}")):
        output_text.insert(tk.END, "Ошибка: программа должна начинаться с '{' и заканчиваться '}'.\n")
        return

    program = program[1:-1].strip()
    program = re.sub(r"\{.*?\}", "", program, flags=re.DOTALL).strip()
    commands = program.split(";")

    for command in commands:
        command = command.strip()
        if not command:
            continue

        if command.startswith("[") and command.endswith("]"):
            inner_commands = command[1:-1].strip().split(":")
            handle_compound_operator(inner_commands)
            continue

        if any(command.startswith(data_type) for data_type in DATA_TYPES):
            result = parse_declaration(command)
            output_text.insert(tk.END, result + "\n")
        elif " as " in command:
            result = handle_assignment(command)
            output_text.insert(tk.END, result + "\n")
        elif command.startswith("if "):
            if "then" in command:
                condition, action = command.split("then", 1)
                condition = condition[3:].strip()
                action = action.strip()
                if evaluate_expression(condition) == "Истина":
                    output_text.insert(tk.END, f"Выполняется действие: {action}\n")
                    handle_compound_operator([action])
            if "else" in command:
                _, else_action = action.split("else", 1)
                else_action = else_action.strip()
                if evaluate_expression(condition) != "Истина":
                    output_text.insert(tk.END, f"Выполняется действие else: {else_action}\n")
                    handle_compound_operator([else_action])
        elif command.startswith("for ") and "to" in command and "do" in command:
            loop_parts = command.split("to")
            loop_var, loop_end_part = loop_parts[0][4:].strip().split(" ", 1)
            loop_end, loop_action = loop_end_part.split("do", 1)
            loop_end = eval(loop_end.strip(), {"sqrt": math.sqrt}, {k: v["value"] for k, v in variables.items()})
            for i in range(0, loop_end):
                output_text.insert(tk.END, f"Итерация {i + 1}\n")
                handle_compound_operator([loop_action.strip()])
        elif command.startswith("while ") and "do" in command:
            condition, action = command[6:].split("do", 1)
            while evaluate_expression(condition.strip()) == "Истина":
                handle_compound_operator([action.strip()])
        elif command.startswith("read(") and command.endswith(")"):

            identifiers = command[5:-1].split(",")
            handle_input(identifiers)
        elif command.startswith("write(") and command.endswith(")"):
            expressions = command[6:-1].split(",")
            handle_output(expressions)

# Функция для переключения между дневным и ночным режимами
def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    if dark_mode:
        root.config(bg="gray15")  # Фон окна в темном режиме
        frame.config(bg="gray15")  # Фон рамки
        program_label.config(bg="gray15", fg="white")
        program_entry.config(bg="gray17", fg="white", insertbackground="white")
        output_text.config(bg="gray17", fg="white", insertbackground="white")
        run_button.config(bg="indigo", fg="white")
        help_button.config(bg="indigo", fg="white")
        task_button.config(bg="indigo", fg="white")
        example_button.config(bg="indigo", fg="white")
        theme_button.config(image=moon_image, bg="gray15")  # Кнопка темы и изображение "Луна"
        close_button.config(bg="indigo", fg="white")
    else:
        root.config(bg="gray95")  # Цвет фона главного окна
        frame.config(bg="gray95")  # Фон рамки
        program_label.config(bg="gray95", fg="black")  # Введите программу и фон
        program_entry.config(bg="white", fg="black", insertbackground="black")  # Ввод
        output_text.config(bg="white", fg="black", insertbackground="black")  # Вывод
        run_button.config(bg="green3", fg="black")  # Запуск
        help_button.config(bg="gray95", fg="black")  # Справка
        task_button.config(bg="gray95", fg="black")  # Задание
        example_button.config(bg="gray95", fg="black")  # Примеры
        theme_button.config(image=sun_image, bg="white")  # Кнопка темы и изображение "Солнце"
        close_button.config(bg="gray95", fg="black")  # Закрыть

# Функция для закрытия приложения
def close_window():
    root.quit()

def run_program():
    # Очистка поля вывода перед выполнением программы
    output_text.delete("1.0", tk.END)

    program = program_entry.get("1.0", tk.END).strip()
    if not program:
        output_text.insert(tk.END, "Ошибка: программа не введена.\n")
        return

    # Запуск функции анализа программы
    output_text.insert(tk.END, f"Запущенная программа:\n{program}\n\n")
    parse_program(program)

    # Обновление текстового поля, чтобы изменения отобразились сразу
    output_text.update()

# Создание главного окна
root = tk.Tk()
root.title("Распознаватель языка программирования")
root.geometry("1200x800")

# Загрузка изображений для кнопки темы
sun_image = ImageTk.PhotoImage(Image.open("../../Desktop/TFY kursovay GUI/sun.png").resize((30, 30)))  # Изображение солнца
moon_image = ImageTk.PhotoImage(Image.open("../../Desktop/TFY kursovay GUI/moon.png").resize((30, 30)))  # Изображение луны

dark_mode = False  # Начальный режим (дневной)

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Текстовое поле для ввода программы
program_label = tk.Label(frame, text="Введите программу:")
program_label.grid(row=0, column=0, sticky="w")

program_entry = scrolledtext.ScrolledText(frame, width=80, height=20)
program_entry.grid(row=1, column=0, columnspan=4, padx=5, pady=5)

# Кнопка для запуска программы
run_button = tk.Button(frame, text="Запуск", command=run_program)
run_button.grid(row=2, column=0, sticky="w", ipadx=4, ipady=4, padx=5, pady=5)

# Кнопка для справки по центру
help_button = tk.Button(frame, text="Справка", command=help_program)
help_button.grid(row=2, column=2, sticky="n", ipadx=4, ipady=4, padx=5, pady=5)

# Добавление кнопки "Задание" в интерфейс
task_button = tk.Button(frame, text="Задание", command=show_task)
task_button.grid(row=2, column=1, sticky="w", ipadx=4, ipady=4, padx=5, pady=5)

# Кнопка для примеров справа
example_button = tk.Button(frame, text="Примеры", command=print_examples)
example_button.grid(row=2, column=3, sticky="e", ipadx=4, ipady=4, padx=(5, 20), pady=5)

# Поле для вывода результатов
output_text = scrolledtext.ScrolledText(frame, width=80, height=20)
output_text.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

# Кнопка для смены темы
theme_button = tk.Button(frame, image=sun_image, command=toggle_theme, bd=0)
theme_button.grid(row=4, column=0, sticky="w", padx=5, pady=5)

# Кнопка для закрытия окна
close_button = tk.Button(frame, text="Закрыть", command=close_window)
close_button.grid(row=4, column=3, sticky="e", padx=5, pady=5)

# Запуск основного цикла приложения
root.mainloop()