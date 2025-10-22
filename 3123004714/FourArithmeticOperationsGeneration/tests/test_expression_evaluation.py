"""表达式计算功能的单元测试"""
import pytest
from fractions import Fraction
import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# 导入需要测试的函数
import main


class TestShuntingYard:
    """调度场算法的测试用例"""

    def test_shunting_yard_simple_addition(self):
        """测试简单加法的调度场算法"""
        tokens = ["1", "+", "2"]
        result = main.shunting_yard(tokens)
        assert result == ["1", "2", "+"]

    def test_shunting_yard_simple_subtraction(self):
        """测试简单减法的调度场算法"""
        tokens = ["5", "-", "2"]
        result = main.shunting_yard(tokens)
        assert result == ["5", "2", "-"]

    def test_shunting_yard_simple_multiplication(self):
        """测试简单乘法的调度场算法"""
        tokens = ["3", "×", "4"]
        result = main.shunting_yard(tokens)
        assert result == ["3", "4", "×"]

    def test_shunting_yard_simple_division(self):
        """测试简单除法的调度场算法"""
        tokens = ["8", "÷", "2"]
        result = main.shunting_yard(tokens)
        assert result == ["8", "2", "÷"]

    def test_shunting_yard_precedence(self):
        """测试运算符优先级处理"""
        tokens = ["1", "+", "2", "×", "3"]
        result = main.shunting_yard(tokens)
        assert result == ["1", "2", "3", "×", "+"]

        tokens = ["2", "×", "3", "+", "4"]
        result = main.shunting_yard(tokens)
        assert result == ["2", "3", "×", "4", "+"]

    def test_shunting_yard_parentheses(self):
        """测试括号处理"""
        tokens = ["(", "1", "+", "2", ")", "×", "3"]
        result = main.shunting_yard(tokens)
        assert result == ["1", "2", "+", "3", "×"]

    def test_shunting_yard_complex_expression(self):
        """测试复杂表达式"""
        tokens = ["(", "1", "+", "2", ")", "×", "(", "3", "-", "1", ")", "÷", "2"]
        result = main.shunting_yard(tokens)
        assert result == ["1", "2", "+", "3", "1", "-", "×", "2", "÷"]

    def test_shunting_yard_nested_parentheses(self):
        """测试嵌套括号"""
        tokens = ["(", "(", "1", "+", "2", ")", "×", "3", ")"]
        result = main.shunting_yard(tokens)
        assert result == ["1", "2", "+", "3", "×"]

    def test_shunting_yard_same_precedence(self):
        """测试相同优先级运算符（左结合）"""
        tokens = ["1", "-", "2", "-", "3"]
        result = main.shunting_yard(tokens)
        assert result == ["1", "2", "-", "3", "-"]

        tokens = ["8", "÷", "2", "÷", "2"]
        result = main.shunting_yard(tokens)
        assert result == ["8", "2", "÷", "2", "÷"]

    def test_shunting_yard_with_fractions(self):
        """测试包含分数的表达式"""
        tokens = ["1/2", "+", "1/3"]
        result = main.shunting_yard(tokens)
        assert result == ["1/2", "1/3", "+"]

    def test_shunting_yard_with_mixed_numbers(self):
        """测试包含带分数的表达式"""
        tokens = ["1'1/2", "+", "2'1/4"]
        result = main.shunting_yard(tokens)
        assert result == ["1'1/2", "2'1/4", "+"]


class TestPostfixEvaluation:
    """后缀表达式计算的测试用例"""

    def test_evaluate_postfix_simple_addition(self):
        """测试简单加法的后缀计算"""
        postfix = ["1", "2", "+"]
        result = main.evaluate_postfix(postfix)
        assert result == Fraction(3)

    def test_evaluate_postfix_simple_subtraction(self):
        """测试简单减法的后缀计算"""
        postfix = ["5", "2", "-"]
        result = main.evaluate_postfix(postfix)
        assert result == Fraction(3)

    def test_evaluate_postfix_simple_multiplication(self):
        """测试简单乘法的后缀计算"""
        postfix = ["3", "4", "×"]
        result = main.evaluate_postfix(postfix)
        assert result == Fraction(12)

    def test_evaluate_postfix_simple_division(self):
        """测试简单除法的后缀计算"""
        postfix = ["8", "2", "÷"]
        result = main.evaluate_postfix(postfix)
        assert result == Fraction(4)

    def test_evaluate_postfix_with_fractions(self):
        """测试包含分数的后缀计算"""
        postfix = ["1/2", "1/3", "+"]
        result = main.evaluate_postfix(postfix)
        assert result == Fraction(5, 6)

    def test_evaluate_postfix_complex_expression(self):
        """测试复杂表达式的后缀计算"""
        postfix = ["1", "2", "+", "3", "×"]
        result = main.evaluate_postfix(postfix)
        assert result == Fraction(9)

    def test_evaluate_postfix_mixed_operations(self):
        """测试混合运算的后缀计算"""
        postfix = ["1", "2", "3", "×", "+"]
        result = main.evaluate_postfix(postfix)
        assert result == Fraction(7)

    def test_evaluate_postfix_complex_with_fractions(self):
        """测试包含分数的复杂后缀计算"""
        postfix = ["1/2", "1/3", "+", "2", "×"]
        result = main.evaluate_postfix(postfix)
        assert result == Fraction(5, 3)

    def test_evaluate_postfix_division_by_zero(self):
        """测试除零错误处理"""
        postfix = ["1", "0", "÷"]
        with pytest.raises(ValueError, match="Division by zero"):
            main.evaluate_postfix(postfix)

    def test_evaluate_postfix_negative_subtraction(self):
        """测试减法产生负数的错误处理"""
        postfix = ["1", "5", "-"]
        with pytest.raises(ValueError, match="Negative result"):
            main.evaluate_postfix(postfix)

    def test_evaluate_postfix_invalid_expression(self):
        """测试无效后缀表达式"""
        # 操作数不足
        postfix = ["1", "+"]
        with pytest.raises(IndexError):
            main.evaluate_postfix(postfix)

    def test_evaluate_postfix_empty_expression(self):
        """测试空后缀表达式"""
        postfix = []
        result = main.evaluate_postfix(postfix)
        assert result is None


class TestExpressionEvaluation:
    """表达式整体计算的测试用例"""

    def test_evaluate_expression_simple_addition(self):
        """测试简单加法表达式计算"""
        result = main.evaluate_expression("1 + 2")
        assert result == Fraction(3)

    def test_evaluate_expression_simple_subtraction(self):
        """测试简单减法表达式计算"""
        result = main.evaluate_expression("5 - 2")
        assert result == Fraction(3)

    def test_evaluate_expression_simple_multiplication(self):
        """测试简单乘法表达式计算"""
        result = main.evaluate_expression("3 × 4")
        assert result == Fraction(12)

    def test_evaluate_expression_simple_division(self):
        """测试简单除法表达式计算"""
        result = main.evaluate_expression("8 ÷ 2")
        assert result == Fraction(4)

    def test_evaluate_expression_with_fractions(self):
        """测试包含分数的表达式计算"""
        result = main.evaluate_expression("1/2 + 1/3")
        assert result == Fraction(5, 6)

    def test_evaluate_expression_with_mixed_numbers(self):
        """测试包含带分数的表达式计算"""
        result = main.evaluate_expression("1'1/2 + 2'1/4")
        assert result == Fraction(15, 4)

    def test_evaluate_expression_with_parentheses(self):
        """测试包含括号的表达式计算"""
        result = main.evaluate_expression("(1 + 2) × 3")
        assert result == Fraction(9)

    def test_evaluate_expression_complex_with_parentheses(self):
        """测试复杂带括号表达式计算"""
        result = main.evaluate_expression("(1 + 2) × (3 - 1) ÷ 2")
        assert result == Fraction(3)

    def test_evaluate_expression_precedence(self):
        """测试运算符优先级"""
        # 乘法优先于加法
        result = main.evaluate_expression("1 + 2 × 3")
        assert result == Fraction(7)

        # 除法优先于减法
        result = main.evaluate_expression("10 - 6 ÷ 2")
        assert result == Fraction(7)

    def test_evaluate_expression_nested_parentheses(self):
        """测试嵌套括号"""
        result = main.evaluate_expression("((1 + 2) × 3) - 1")
        assert result == Fraction(8)

    def test_evaluate_expression_division_by_zero(self):
        """测试除零错误处理"""
        result = main.evaluate_expression("1 ÷ 0")
        assert result is None

    def test_evaluate_expression_negative_subtraction(self):
        """测试减法产生负数的错误处理"""
        result = main.evaluate_expression("1 - 5")
        assert result is None

    def test_evaluate_expression_invalid_syntax(self):
        """测试无效语法处理"""
        result = main.evaluate_expression("1 + + 2")
        assert result is None

    def test_evaluate_expression_mixed_types(self):
        """测试混合数字类型"""
        result = main.evaluate_expression("1 + 1/2 + 1'1/4")
        assert result == Fraction(11, 4)

    def test_evaluate_expression_spaces(self):
        """测试空格处理"""
        result1 = main.evaluate_expression("1+2")
        result2 = main.evaluate_expression("1 + 2")
        result3 = main.evaluate_expression(" 1   +   2 ")
        assert result1 == result2 == result3 == Fraction(3)

    def test_evaluate_expression_complex_fractions(self):
        """测试复杂分数运算"""
        result = main.evaluate_expression("1/2 + 2/3 × 3/4")
        # 2/3 × 3/4 = 1/2, 1/2 + 1/2 = 1
        assert result == Fraction(1)

    def test_evaluate_expression_mixed_complex(self):
        """测试混合复杂数字运算"""
        result = main.evaluate_expression("1'1/2 × 2 + 1/3")
        # 1'1/2 × 2 = 3, 3 + 1/3 = 10/3
        assert result == Fraction(10, 3)

    def test_evaluate_expression_zero_operations(self):
        """测试包含零的运算"""
        result = main.evaluate_expression("0 + 5")
        assert result == Fraction(5)

        result = main.evaluate_expression("5 × 0")
        assert result == Fraction(0)

        result = main.evaluate_expression("0 ÷ 5")
        assert result == Fraction(0)

    def test_evaluate_expression_single_number(self):
        """测试单个数字"""
        result = main.evaluate_expression("42")
        assert result == Fraction(42)

        result = main.evaluate_expression("1/2")
        assert result == Fraction(1, 2)

        result = main.evaluate_expression("1'1/2")
        assert result == Fraction(3, 2)

    def test_evaluate_expression_large_numbers(self):
        """测试大数字运算"""
        result = main.evaluate_expression("100 + 200")
        assert result == Fraction(300)

        result = main.evaluate_expression("50 × 60")
        assert result == Fraction(3000)

    def test_evaluate_expression_edge_cases(self):
        """测试边界情况"""
        # 最小非零分数
        result = main.evaluate_expression("1/100 + 1/100")
        assert result == Fraction(1, 50)

        # 大分数
        result = main.evaluate_expression("99/100")
        assert result == Fraction(99, 100)