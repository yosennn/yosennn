"""Expression类的单元测试"""
import pytest
from fractions import Fraction
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from src.Expression import Expression


class TestExpression:
    """Expression类的测试用例"""

    def test_init_simple(self):
        """测试简单表达式的初始化"""
        expr = Expression("1 + 2 =", Fraction(3))
        assert expr.expr_str == "1 + 2 ="
        assert expr.value == Fraction(3)
        assert expr.normalized is not None

    def test_init_with_fraction(self):
        """测试包含分数的表达式初始化"""
        expr = Expression("1/2 + 1/3 =", Fraction(5, 6))
        assert expr.expr_str == "1/2 + 1/3 ="
        assert expr.value == Fraction(5, 6)

    def test_init_with_mixed_number(self):
        """测试包含带分数的表达式初始化"""
        expr = Expression("1'1/2 + 1/4 =", Fraction(7, 4))
        assert expr.expr_str == "1'1/2 + 1/4 ="
        assert expr.value == Fraction(7, 4)

    def test_tokenize_simple_numbers(self):
        """测试简单数字的分词"""
        expr = Expression("1 + 2 =", Fraction(3))
        tokens = expr.tokenize("1 + 2")
        expected = ["1", "+", "2"]
        assert tokens == expected

    def test_tokenize_fractions(self):
        """测试分数的分词"""
        expr = Expression("1/2 + 2/3 =", Fraction(7, 6))
        tokens = expr.tokenize("1/2 + 2/3")
        expected = ["1/2", "+", "2/3"]
        assert tokens == expected

    def test_tokenize_mixed_numbers(self):
        """测试带分数的分词"""
        expr = Expression("1'1/2 + 2'3/4 =", Fraction(17, 4))
        tokens = expr.tokenize("1'1/2 + 2'3/4")
        expected = ["1'1/2", "+", "2'3/4"]
        assert tokens == expected

    def test_tokenize_with_parentheses(self):
        """测试包含括号的表达式分词"""
        expr = Expression("(1 + 2) × 3 =", Fraction(9))
        tokens = expr.tokenize("(1 + 2) × 3")
        expected = ["(", "1", "+", "2", ")", "×", "3"]
        assert tokens == expected

    def test_tokenize_with_spaces(self):
        """测试包含空格的表达式分词"""
        expr = Expression(" 1 + 2 = ", Fraction(3))
        tokens = expr.tokenize(" 1 + 2 = ")
        expected = ["1", "+", "2"]
        assert tokens == expected

    def test_parse_simple_addition(self):
        """测试简单加法解析"""
        expr = Expression("1 + 2 =", Fraction(3))
        tokens = ["1", "+", "2"]
        ast = expr.parse(tokens)
        assert ast == ("+", "1", "2")

    def test_parse_multiplication(self):
        """测试乘法解析"""
        expr = Expression("2 × 3 =", Fraction(6))
        tokens = ["2", "×", "3"]
        ast = expr.parse(tokens)
        assert ast == ("×", "2", "3")

    def test_parse_mixed_operations(self):
        """测试混合运算解析（优先级）"""
        expr = Expression("1 + 2 × 3 =", Fraction(7))
        tokens = ["1", "+", "2", "×", "3"]
        ast = expr.parse(tokens)
        assert ast == ("+", "1", ("×", "2", "3"))

    def test_parse_with_parentheses(self):
        """测试括号改变优先级"""
        expr = Expression("(1 + 2) × 3 =", Fraction(9))
        tokens = ["(", "1", "+", "2", ")", "×", "3"]
        ast = expr.parse(tokens)
        assert ast == ("×", ("+", "1", "2"), "3")

    def test_normalize_simple_addition(self):
        """测试简单加法的标准化"""
        expr1 = Expression("1 + 2 =", Fraction(3))
        expr2 = Expression("2 + 1 =", Fraction(3))
        assert expr1.normalized == expr2.normalized

    def test_normalize_simple_multiplication(self):
        """测试简单乘法的标准化"""
        expr1 = Expression("2 × 3 =", Fraction(6))
        expr2 = Expression("3 × 2 =", Fraction(6))
        assert expr1.normalized == expr2.normalized

    def test_normalize_complex_expression(self):
        """测试复杂表达式的标准化"""
        expr1 = Expression("1 + 2 × 3 =", Fraction(7))
        expr2 = Expression("2 × 3 + 1 =", Fraction(7))
        # 这些应该不同，因为运算顺序不同
        assert expr1.normalized != expr2.normalized

    def test_normalize_with_parentheses(self):
        """测试包含括号的表达式标准化"""
        expr1 = Expression("(1 + 2) × 3 =", Fraction(9))
        expr2 = Expression("3 × (1 + 2) =", Fraction(9))
        # 乘法交换律，应该相同
        assert expr1.normalized == expr2.normalized

    def test_ast_to_string_simple(self):
        """测试简单AST转字符串"""
        expr = Expression("1 + 2 =", Fraction(3))
        ast = ("+", "1", "2")
        result = expr.ast_to_string(ast)
        assert result == "(1+2)"

    def test_ast_to_string_complex(self):
        """测试复杂AST转字符串"""
        expr = Expression("1 + 2 × 3 =", Fraction(7))
        ast = ("+", "1", ("×", "2", "3"))
        result = expr.ast_to_string(ast)
        assert result == "(1+(2×3))"

    def test_equality_same_expression(self):
        """测试相同表达式的相等性"""
        expr1 = Expression("1 + 2 =", Fraction(3))
        expr2 = Expression("1 + 2 =", Fraction(3))
        assert expr1 == expr2

    def test_equality_commutative_addition(self):
        """测试加法交换律的相等性"""
        expr1 = Expression("1 + 2 =", Fraction(3))
        expr2 = Expression("2 + 1 =", Fraction(3))
        assert expr1 == expr2

    def test_equality_commutative_multiplication(self):
        """测试乘法交换律的相等性"""
        expr1 = Expression("2 × 3 =", Fraction(6))
        expr2 = Expression("3 × 2 =", Fraction(6))
        assert expr1 == expr2

    def test_equality_different_expressions(self):
        """测试不同表达式的不相等性"""
        expr1 = Expression("1 + 2 =", Fraction(3))
        expr2 = Expression("1 + 3 =", Fraction(4))
        assert expr1 != expr2

    def test_equality_subtraction_not_commutative(self):
        """测试减法不满足交换律"""
        expr1 = Expression("3 - 1 =", Fraction(2))
        expr2 = Expression("1 - 3 =", Fraction(-2))
        # 减法不应该标准化
        assert expr1.normalized != expr2.normalized

    def test_equality_division_not_commutative(self):
        """测试除法不满足交换律"""
        expr1 = Expression("6 ÷ 2 =", Fraction(3))
        expr2 = Expression("2 ÷ 6 =", Fraction(1, 3))
        # 除法不应该标准化
        assert expr1.normalized != expr2.normalized

    def test_normalize_with_fractions(self):
        """测试包含分数的表达式标准化"""
        expr1 = Expression("1/2 + 1/3 =", Fraction(5, 6))
        expr2 = Expression("1/3 + 1/2 =", Fraction(5, 6))
        assert expr1.normalized == expr2.normalized

    def test_nested_expressions(self):
        """测试嵌套表达式的标准化"""
        expr1 = Expression("(1 + 2) + 3 =", Fraction(6))
        expr2 = Expression("3 + (1 + 2) =", Fraction(6))
        assert expr1.normalized == expr2.normalized

    def test_complex_nested_expressions(self):
        """测试复杂嵌套表达式"""
        expr1 = Expression("(1 + 2) × (3 + 4) =", Fraction(21))
        expr2 = Expression("(3 + 4) × (1 + 2) =", Fraction(21))
        assert expr1.normalized == expr2.normalized