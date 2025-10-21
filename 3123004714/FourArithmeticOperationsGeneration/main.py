import sys
import random
import re
from fractions import Fraction  # 用于分数计算，自动处理约分等

class Expression:
    """表达式类，用于表示一个四则运算表达式及其相关属性"""
    def __init__(self, expr_str, value):
        self.expr_str = expr_str            # 表达式的字符串形式（如 "1 + 2 =")
        self.value = value                  # 表达式的计算结果（Fraction类型）
        self.normalized = self.normalize()  # 用于去重的标准化形式

    def normalize(self):
        """将表达式标准化，考虑加法和乘法的交换律，用于判断题目是否重复"""
        tokens = self.tokenize(self.expr_str)
        if not tokens:
            return self.expr_str
        try:
            ast = self.parse(tokens)
            normalized_ast = self.normalize_ast(ast)
            return self.ast_to_string(normalized_ast)
        except:
            return self.expr_str

    def tokenize(self, s):
        """将表达式字符串拆分为令牌（数字、运算符、括号等）"""
        s = s.replace(' ', '').rstrip('=')  # 去除空格和等号
        tokens = []
        i = 0
        n = len(s)
        while i < n:
            if s[i] in '()+*-÷':  # 运算符和括号
                tokens.append(s[i])
                i += 1
            elif s[i].isdigit() or s[i] == '/':  # 数字（自然数或分数）
                j = i
                # 收集完整的数字（可能包含'/'或'''）
                while j < n and (s[j].isdigit() or s[j] in '/\''):
                    j += 1
                tokens.append(s[i:j])
                i = j
            else:
                i += 1
        return tokens

    def parse(self, tokens):
        """将令牌列表解析为抽象语法树（AST），处理运算符优先级"""
        def parse_expression(index):
            left, index = parse_term(index)
            # 处理加法和减法（优先级较低）
            while index < len(tokens) and tokens[index] in '+-':
                op = tokens[index]
                index += 1
                right, index = parse_term(index)
                left = (op, left, right)
            return left, index

        def parse_term(index):
            # 处理乘法和除法（优先级较高）
            left, index = parse_factor(index)
            while index < len(tokens) and tokens[index] in '×÷':
                op = tokens[index]
                index += 1
                right, index = parse_factor(index)
                left = (op, left, right)
            return left, index

        def parse_factor(index):
            if tokens[index] == '(': # 处理括号
                index += 1
                expr, index = parse_expression(index)
                if index < len(tokens) and tokens[index] == ')':
                    index += 1
                    return expr, index
                else:
                    return expr, index
            else: # 数字
                num = tokens[index]
                index += 1
                return num, index

        ast, _ = parse_expression(0)
        return ast

    def normalize_ast(self, ast):
        """标准化语法树，对于加法和乘法交换左右操作数，实现去重"""
        if not isinstance(ast, tuple):
            return ast
        op, left, right = ast
        left_norm = self.normalize_ast(left)
        right_norm = self.normalize_ast(right)
        if op in ('+', '×'):
            left_str = self.ast_to_string(left_norm)
            right_str = self.ast_to_string(right_norm)
            if left_str > right_str:
                left_norm, right_norm = right_norm, left_norm
        return (op, left_norm, right_norm)

    def ast_to_string(self, ast):
        """将抽象语法树转换回字符串形式"""
        if not isinstance(ast, tuple):
            return ast
        op, left, right = ast
        left_str = self.ast_to_string(left)
        right_str = self.ast_to_string(right)
        return f'({left_str}{op}{right_str})'

    def __eq__(self, other):
        """判断两个表达式是否相同（基于标准化形式）"""
        return self.normalized == other.normalized


def generate_number(r):
    """生成范围内的自然数或真分数"""
    is_fraction = random.choice([True, False])
    if is_fraction:
        # 生成分母（2到范围值-1之间）
        denominator = random.randint(2, r - 1) if r > 2 else 2
        # 生成分母（2到范围值-1之间）
        numerator = random.randint(1, denominator - 1)
        # 生成分母（2到范围值-1之间）
        integer_part = random.randint(0, (r - 1) * denominator - numerator) // denominator if r > 1 else 0
        if integer_part == 0:
            return f"{numerator}/{denominator}"  # 纯分数（如3/5）
        else:
            return f"{integer_part}'{numerator}/{denominator}"  # 带分数（如2'3/8）
    else:
        return str(random.randint(0, r - 1))  # 自然数


def parse_number(s):
    """将字符串形式的数字（自然数或分数）转换为Fraction对象"""
    if "'" in s:
        integer_part, frac_part = s.split("'", 1)
        num, den = map(int, frac_part.split('/'))
        return Fraction(int(integer_part) * den + num, den)
    elif '/' in s:
        num, den = map(int, s.split('/'))
        return Fraction(num, den)
    else:
        return Fraction(int(s), 1)


def format_number(f):
    """将Fraction对象转换为字符串形式（自然数或分数）"""
    if f.denominator == 1:
        return str(f.numerator)
    else:
        integer_part = f.numerator // f.denominator
        remainder = f.numerator % f.denominator
        if integer_part == 0:
            return f"{remainder}/{f.denominator}"
        else:
            return f"{integer_part}'{remainder}/{f.denominator}"


def evaluate_expression(expr_str):
    """计算表达式的值，返回Fraction对象，处理错误情况"""
    try:
        tokens = re.findall(r'\d+|\d+\'\d+/\d+|\d+/\d+|[+×÷\-()]', expr_str.replace(' ', ''))
        postfix = shunting_yard(tokens)
        result = evaluate_postfix(postfix)
        return result
    except:
        return None


def shunting_yard(tokens):
    """将中缀表达式转换为后缀表达式（逆波兰式），处理运算符优先级"""
    precedence = {'+': 1, '-': 1, '×': 2, '÷': 2}  # 运算符优先级
    output = []
    stack = []
    for token in tokens:
        if re.match(r'^\d+$|^\d+\'\d+/\d+$|^\d+/\d+$', token):  # 数字直接入队
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            while stack and stack[-1] != '(' and precedence[stack[-1]] >= precedence[token]:
                output.append(stack.pop())
            stack.append(token)
    while stack:
        output.append(stack.pop())
    return output


def evaluate_postfix(postfix):
    """计算后缀表达式（逆波兰式）的值"""
    stack = []
    for token in postfix:
        if re.match(r'^\d+$|^\d+\'\d+/\d+$|^\d+/\d+$', token):
            stack.append(parse_number(token))
        else:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                res = a + b
            elif token == '-':
                if a < b:
                    raise ValueError("Negative result")
                res = a - b
            elif token == '×':
                res = a * b
            elif token == '÷':
                if b == 0:
                    raise ValueError("Division by zero")
                res = a / b
                if res.denominator == 1 and res.numerator < 0:
                    raise ValueError("Negative result")
            else:
                raise ValueError("Unknown operator")
            stack.append(res)
    return stack[0] if stack else None


def generate_expression(r, max_ops):
    """生成一个符合要求的四则运算表达式"""
    ops_count = random.randint(1, max_ops)
    ops = ['+', '-', '×', '÷']
    selected_ops = random.choices(ops, k=ops_count)
    numbers = [generate_number(r) for _ in range(ops_count + 1)]
    expr = numbers[0]
    for i in range(ops_count):
        op = selected_ops[i]
        next_num = numbers[i + 1]
        temp_expr = f"{expr} {op} {next_num}"
        try:
            value = evaluate_expression(temp_expr)
            if value is None:
                return None
            expr = temp_expr
        except:
            return None
    if random.random() < 0.3 and ops_count > 1:
        start = random.randint(0, len(expr) // 2)
        end = start + random.randint(2, len(expr) - start)
        while start > 0 and expr[start - 1] not in ' +-×÷(':
            start -= 1
        while end < len(expr) and expr[end] not in ' +-×÷)':
            end += 1
        expr = expr[:start] + '(' + expr[start:end] + ')' + expr[end:]
    try:
        value = evaluate_expression(expr)
        if value is None:
            return None
        return Expression(f"{expr} =", value)
    except:
        return None


def generate_exercises(n, r):
    """生成指定数量的不重复练习题"""
    exercises = []
    seen = set()
    while len(exercises) < n:
        print(f"正在生成第 {len(exercises) + 1} 题...")  # 新增日志
        expr = generate_expression(r, 3)
        if expr and expr.normalized not in seen:
            seen.add(expr.normalized)
            exercises.append(expr)
    return exercises


def grade_exercises(exercise_file, answer_file):
    """批改练习题，生成Grade.txt文件"""
    with open(exercise_file, 'r', encoding='utf-8') as f:
        exercises = [line.strip() for line in f if line.strip()]
    with open(answer_file, 'r', encoding='utf-8') as f:
        answers = [line.strip() for line in f if line.strip()]
    correct = []
    wrong = []
    for i in range(min(len(exercises), len(answers))):
        expr_str = exercises[i].rstrip('=')
        try:
            expected = evaluate_expression(expr_str)
            if expected is None:
                wrong.append(i + 1)
                continue
        except:
            wrong.append(i + 1)
            continue
        user_ans = answers[i]
        try:
            user_frac = parse_number(user_ans)
        except:
            wrong.append(i + 1)
            continue
        if user_frac == expected:
            correct.append(i + 1)
        else:
            wrong.append(i + 1)
    with open('Grade.txt', 'w', encoding='utf-8') as f:
        f.write(f"Correct: {len(correct)} ({', '.join(map(str, correct))})\n")
        f.write(f"Wrong: {len(wrong)} ({', '.join(map(str, wrong))})\n")


def main():
    """程序主入口，处理命令行参数"""
    args = sys.argv[1:]
    if len(args) == 4 and args[0] == '-n' and args[2] == '-r':
        try:
            n = int(args[1])
            r = int(args[3])
            if r < 1:
                print("Error: -r must be a natural number (≥1)")
                return
            exercises = generate_exercises(n, r)
            with open('Exercises.txt', 'w', encoding='utf-8') as f:
                for expr in exercises:
                    f.write(f"{expr.expr_str}\n")
            with open('Answers.txt', 'w', encoding='utf-8') as f:
                for expr in exercises:
                    f.write(f"{format_number(expr.value)}\n")
        except ValueError:
            print("Error: -n and -r must be integers")
    elif len(args) == 4 and args[0] == '-e' and args[2] == '-a':
        exercise_file = args[1]
        answer_file = args[3]
        grade_exercises(exercise_file, answer_file)
    else:
        print("Usage:")
        print("Generate exercises: main.py -n <number> -r <range>")
        print("Grade exercises: main.py -e <exercisefile>.txt -a <answerfile>.txt")
        print("Note: -r must be provided and be a natural number (≥1)")


if __name__ == "__main__":
    main()
