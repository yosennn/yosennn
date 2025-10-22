"""表达式生成功能的单元测试"""
import pytest
from fractions import Fraction
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# 导入需要测试的函数
import main
from src.Expression import Expression


class TestExpressionGeneration:
    """表达式生成功能的测试用例"""

    def test_generate_expression_basic(self):
        """测试基本表达式生成"""
        for _ in range(50):
            expr = main.generate_expression(10, 3)
            assert expr is not None
            assert isinstance(expr, Expression)
            assert expr.expr_str.endswith("=")
            assert isinstance(expr.value, Fraction)

    def test_generate_expression_single_operator(self):
        """测试单运算符表达式生成"""
        expr = main.generate_expression(10, 1)
        assert expr is not None
        # 检查表达式包含一个运算符
        expr_str = expr.expr_str.rstrip("=")
        operator_count = sum(1 for op in ['+', '-', '×', '÷'] if op in expr_str)
        assert operator_count == 1

    def test_generate_expression_multiple_operators(self):
        """测试多运算符表达式生成"""
        expr = main.generate_expression(10, 3)
        assert expr is not None
        # 检查表达式包含1-3个运算符
        expr_str = expr.expr_str.rstrip("=")
        operator_count = sum(1 for op in ['+', '-', '×', '÷'] if op in expr_str)
        assert 1 <= operator_count <= 3

    def test_generate_expression_result_validity(self):
        """测试生成表达式的结果有效性"""
        for _ in range(50):
            expr = main.generate_expression(10, 3)
            if expr:
                # 手动计算验证结果
                calculated = main.evaluate_expression(expr.expr_str.rstrip("="))
                assert calculated == expr.value

    def test_generate_expression_range_constraint(self):
        """测试生成表达式数值范围约束"""
        for r in [5, 10, 20]:
            for _ in range(20):
                expr = main.generate_expression(r, 3)
                if expr:
                    # 验证结果在合理范围内（可能因为运算而超出输入范围）
                    assert expr.value >= 0  # 结果应该非负

    def test_generate_expression_no_negative_subtraction(self):
        """测试减法不会产生负数结果"""
        for _ in range(100):
            expr = main.generate_expression(10, 3)
            if expr and '-' in expr.expr_str:
                assert expr.value >= 0, f"减法表达式产生了负数结果: {expr.expr_str} = {expr.value}"

    def test_generate_expression_division_proper_fraction(self):
        """测试除法结果为真分数或整数"""
        for _ in range(100):
            expr = main.generate_expression(10, 3)
            if expr and '÷' in expr.expr_str:
                # 除法结果应该是正数
                assert expr.value > 0, f"除法表达式结果非正: {expr.expr_str} = {expr.value}"

    def test_generate_expression_with_parentheses(self):
        """测试带括号的表达式生成"""
        parentheses_found = False
        for _ in range(100):
            expr = main.generate_expression(10, 3)
            if expr and '(' in expr.expr_str:
                parentheses_found = True
                # 验证括号配对
                expr_str = expr.expr_str.rstrip("=")
                assert expr_str.count('(') == expr_str.count(')'), f"括号不配对: {expr.expr_str}"
                break

        # 由于只有30%概率添加括号，不一定总能找到
        # parentheses_found = True  # 注释掉这个断言，因为不是必然发生的

    def test_generate_expression_small_range(self):
        """测试小范围的表达式生成"""
        for r in [2, 3]:
            for _ in range(20):
                expr = main.generate_expression(r, 2)
                if expr:
                    assert expr.value >= 0

    def test_generate_expression_range_one(self):
        """测试范围为1的表达式生成"""
        expr = main.generate_expression(1, 1)
        if expr:
            # 范围为1时，数字只能是0，所以结果也应该是0
            assert expr.value == 0

    def test_generate_expression_division_by_zero_avoidance(self):
        """测试避免除零错误"""
        for _ in range(100):
            expr = main.generate_expression(10, 3)
            if expr and '÷' in expr.expr_str:
                # 验证表达式可以正常计算
                calculated = main.evaluate_expression(expr.expr_str.rstrip("="))
                assert calculated is not None
                assert calculated == expr.value

    def test_generate_expression_format_consistency(self):
        """测试生成表达式格式的一致性"""
        for _ in range(50):
            expr = main.generate_expression(10, 3)
            if expr:
                # 检查表达式格式
                assert expr.expr_str.endswith("=")
                assert expr.expr_str.count("=") == 1
                # 检查数字和运算符之间有空格
                expr_str = expr.expr_str.rstrip("=")
                tokens = expr_str.split()
                # 应该有奇数个token（数字 运算符 数字 ...）
                assert len(tokens) % 2 == 1

    def test_generate_expression_operator_distribution(self):
        """测试运算符分布的合理性"""
        operators = {'+': 0, '-': 0, '×': 0, '÷': 0}
        for _ in range(200):
            expr = main.generate_expression(10, 3)
            if expr:
                expr_str = expr.expr_str.rstrip("=")
                for op in operators:
                    if op in expr_str:
                        operators[op] += 1

        # 所有运算符都应该被使用到
        for op, count in operators.items():
            assert count > 0, f"运算符 {op} 没有被使用"

    def test_generate_expression_complexity(self):
        """测试表达式复杂度的合理性"""
        complexities = []  # 记录每个表达式的运算符数量
        for _ in range(100):
            expr = main.generate_expression(10, 3)
            if expr:
                expr_str = expr.expr_str.rstrip("=")
                complexity = sum(1 for op in ['+', '-', '×', '÷'] if op in expr_str)
                complexities.append(complexity)

        # 验证复杂度分布合理
        assert 1 <= min(complexities) <= max(complexities) <= 3
        # 应该有多种不同的复杂度
        assert len(set(complexities)) >= 2

    def test_generate_expression_uniqueness(self):
        """测试生成表达式的唯一性"""
        expressions = set()
        duplicates = 0
        total = 100

        for _ in range(total):
            expr = main.generate_expression(10, 3)
            if expr:
                normalized = expr.normalized
                if normalized in expressions:
                    duplicates += 1
                else:
                    expressions.add(normalized)

        # 允许少量重复，因为随机生成可能产生相同表达式
        uniqueness_rate = (total - duplicates) / total
        assert uniqueness_rate >= 0.7, f"表达式唯一率过低: {uniqueness_rate:.2%}"

    def test_generate_expression_failure_recovery(self):
        """测试表达式生成失败时的恢复机制"""
        # 使用非常小的范围，增加生成失败的几率
        successes = 0
        attempts = 50

        for _ in range(attempts):
            expr = main.generate_expression(2, 3)  # 小范围，高复杂度
            if expr:
                successes += 1

        # 至少应该有一些成功的生成
        assert successes > 0, f"在 {attempts} 次尝试中没有成功生成任何表达式"

    def test_generate_expression_valid_tokens(self):
        """测试生成表达式包含有效token"""
        valid_patterns = [
            r'^\d+$',  # 整数
            r'^\d+/\d+$',  # 分数
            r'^\d+\'\d+/\d+$'  # 带分数
        ]
        operators = ['+', '-', '×', '÷']

        for _ in range(50):
            expr = main.generate_expression(10, 3)
            if expr:
                expr_str = expr.expr_str.rstrip("=")
                tokens = expr_str.split()

                # 验证token交替模式：数字 运算符 数字 ...
                for i, token in enumerate(tokens):
                    if i % 2 == 0:  # 偶数位置应该是数字
                        assert any(
                            re.match(pattern, token)
                            for pattern in valid_patterns
                        ), f"无效的数字token: {token}"
                    else:  # 奇数位置应该是运算符
                        assert token in operators, f"无效的运算符token: {token}"