class Expression:
    """表达式类，用于表示一个四则运算表达式及其相关属性"""
    def __init__(self, expr_str, value):
        self.expr_str: str = expr_str            # 表达式的字符串形式（如 "1 + 2 =")
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
            if s[i] in '()+-×÷':  # 运算符和括号
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
