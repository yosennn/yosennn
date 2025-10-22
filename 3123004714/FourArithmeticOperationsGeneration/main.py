import sys
import random
import re
from fractions import Fraction  # 用于分数计算，自动处理约分等
from src.Expression import Expression


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
        tokens = re.findall(r'\d+\'\d+/\d+|\d+/\d+|\d+|[+×÷\-()]', expr_str.replace(' ', ''))
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
        if re.match(r'^\d+\'\d+/\d+$|^\d+/\d+$|^\d+$', token):  # 数字直接入队
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
        if re.match(r'^\d+\'\d+/\d+$|^\d+/\d+$|^\d+$', token):
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
    """生成一个符合要求的四则运算表达式

    Args:
        r: 数值范围参数，用于控制生成数字的大小范围
        max_ops: 最大运算符数量，控制表达式的复杂度

    Returns:
        Expression对象: 包含表达式字符串和计算结果的对象，如果生成失败则返回None
    """
    max_attempts = 10  # 最大尝试次数

    for attempt in range(max_attempts):
        try:
            ops_count = random.randint(1, max_ops)
            ops = ['+', '-', '×', '÷']
            selected_ops = random.choices(ops, k=ops_count)
            numbers = [generate_number(r) for _ in range(ops_count + 1)]
            expr = numbers[0]  # 表达式字符串

            # 构建表达式
            for i in range(ops_count):
                op = selected_ops[i]
                next_num = numbers[i + 1]
                temp_expr = f"{expr} {op} {next_num}"
                value = evaluate_expression(temp_expr)
                if value is None:
                    break  # 跳出内层循环，重新尝试生成
                expr = temp_expr
            else:
                # 只有当所有运算都成功时才继续处理括号
                # 随机添加括号以增加复杂度
                if random.random() < 0.3 and ops_count > 1:
                    temp_expr_with_parens = add_parentheses(expr)
                    if temp_expr_with_parens:
                        final_value = evaluate_expression(temp_expr_with_parens)
                        if final_value is not None:
                            return Expression(f"{temp_expr_with_parens} =", final_value)

                # 不添加括号的情况
                value = evaluate_expression(expr)
                if value is not None:
                    return Expression(f"{expr} =", value)

        except:
            continue  # 尝试下一次生成

    return None


def add_parentheses(expr):
    """为表达式添加括号，如果成功则返回带括号的表达式，否则返回None"""
    try:
        start = random.randint(0, len(expr) // 2)
        end = start + random.randint(2, len(expr) - start)
        while start > 0 and expr[start - 1] not in ' +-×÷(':
            start -= 1
        while end < len(expr) and expr[end] not in ' +-×÷)':
            end += 1
        return expr[:start] + '(' + expr[start:end] + ')' + expr[end:]
    except:
        return None


def generate_exercises(n, r):
    """
        生成指定数量的不重复练习题
        param n: 练习题数量
        param r: 数字范围上限
    """
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
