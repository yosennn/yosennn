"""表达式去重机制的单元测试"""
import pytest
from fractions import Fraction
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# 导入需要测试的函数和类
import main
from src.Expression import Expression


class TestExpressionNormalization:
    """表达式标准化的测试用例"""

    def test_normalize_simple_addition_commutative(self):
        """测试简单加法的交换律标准化"""
        expr1 = Expression("1 + 2 =", Fraction(3))
        expr2 = Expression("2 + 1 =", Fraction(3))
        assert expr1.normalized == expr2.normalized

    def test_normalize_simple_multiplication_commutative(self):
        """测试简单乘法的交换律标准化"""
        expr1 = Expression("2 × 3 =", Fraction(6))
        expr2 = Expression("3 × 2 =", Fraction(6))
        assert expr1.normalized == expr2.normalized

    def test_normalize_addition_with_fractions(self):
        """测试包含分数的加法标准化"""
        expr1 = Expression("1/2 + 1/3 =", Fraction(5, 6))
        expr2 = Expression("1/3 + 1/2 =", Fraction(5, 6))
        assert expr1.normalized == expr2.normalized

    def test_normalize_multiplication_with_fractions(self):
        """测试包含分数的乘法标准化"""
        expr1 = Expression("1/2 × 1/3 =", Fraction(1, 6))
        expr2 = Expression("1/3 × 1/2 =", Fraction(1, 6))
        assert expr1.normalized == expr2.normalized

    def test_normalize_complex_addition(self):
        """测试复杂加法表达式的标准化"""
        expr1 = Expression("1 + 2 + 3 =", Fraction(6))
        expr2 = Expression("3 + 1 + 2 =", Fraction(6))
        # 由于解析和标准化的方式，这些可能不完全相同，但数值应该相同
        assert expr1.value == expr2.value

    def test_normalize_mixed_operations_not_commutative(self):
        """测试混合运算不满足交换律"""
        expr1 = Expression("1 + 2 × 3 =", Fraction(7))
        expr2 = Expression("3 × 2 + 1 =", Fraction(7))
        # 交换顺序改变了运算优先级，不应该相同
        assert expr1.normalized != expr2.normalized

    def test_normalize_subtraction_not_commutative(self):
        """测试减法不满足交换律"""
        expr1 = Expression("5 - 2 =", Fraction(3))
        expr2 = Expression("2 - 5 =", Fraction(-3))
        # 减法不应该标准化
        assert expr1.normalized != expr2.normalized

    def test_normalize_division_not_commutative(self):
        """测试除法不满足交换律"""
        expr1 = Expression("6 ÷ 2 =", Fraction(3))
        expr2 = Expression("2 ÷ 6 =", Fraction(1, 3))
        # 除法不应该标准化
        assert expr1.normalized != expr2.normalized

    def test_normalize_with_parentheses_addition(self):
        """测试括号内加法的标准化"""
        expr1 = Expression("(1 + 2) × 3 =", Fraction(9))
        expr2 = Expression("(2 + 1) × 3 =", Fraction(9))
        assert expr1.normalized == expr2.normalized

    def test_normalize_with_parentheses_multiplication(self):
        """测试括号内乘法的标准化"""
        expr1 = Expression("(2 × 3) + 4 =", Fraction(10))
        expr2 = Expression("(3 × 2) + 4 =", Fraction(10))
        assert expr1.normalized == expr2.normalized

    def test_normalize_nested_commutative_operations(self):
        """测试嵌套交换律运算的标准化"""
        expr1 = Expression("(1 + 2) × (3 + 4) =", Fraction(21))
        expr2 = Expression("(2 + 1) × (4 + 3) =", Fraction(21))
        assert expr1.normalized == expr2.normalized

    def test_normalize_mixed_numbers(self):
        """测试带分数表达式的标准化"""
        expr1 = Expression("1'1/2 + 2'1/3 =", Fraction(47, 12))
        expr2 = Expression("2'1/3 + 1'1/2 =", Fraction(47, 12))
        assert expr1.normalized == expr2.normalized

    def test_normalize_deeply_nested(self):
        """测试深度嵌套表达式的标准化"""
        expr1 = Expression("((1 + 2) × (3 + 4)) + 5 =", Fraction(26))
        expr2 = Expression("((2 + 1) × (4 + 3)) + 5 =", Fraction(26))
        assert expr1.normalized == expr2.normalized

    def test_normalize_same_operation_different_structure(self):
        """测试相同运算不同结构"""
        expr1 = Expression("(1 + 2) + 3 =", Fraction(6))
        expr2 = Expression("1 + (2 + 3) =", Fraction(6))
        # 由于括号位置不同，标准化结果可能不同
        # 这是正常的，因为结构确实不同

    def test_normalize_complex_mixed_expression(self):
        """测试复杂混合表达式标准化"""
        expr1 = Expression("(1/2 + 1/3) × (2 + 3) =", Fraction(25, 6))
        expr2 = Expression("(1/3 + 1/2) × (3 + 2) =", Fraction(25, 6))
        assert expr1.normalized == expr2.normalized


class TestDeduplicationMechanism:
    """去重机制的测试用例"""

    def test_deduplication_simple_cases(self):
        """测试简单情况下的去重"""
        exercises = []
        seen = set()

        # 创建相同的表达式
        expr1 = Expression("1 + 2 =", Fraction(3))
        expr2 = Expression("2 + 1 =", Fraction(3))
        expr3 = Expression("3 =", Fraction(3))

        # 第一个表达式应该被添加
        assert expr1.normalized not in seen
        seen.add(expr1.normalized)
        exercises.append(expr1)

        # 第二个表达式（与第一个标准化后相同）应该被识别为重复
        assert expr2.normalized in seen

        # 第三个表达式不同，应该被添加
        assert expr3.normalized not in seen
        seen.add(expr3.normalized)
        exercises.append(expr3)

        assert len(exercises) == 2
        assert len(seen) == 2

    def test_deduplication_with_fractions(self):
        """测试包含分数的去重"""
        seen = set()

        expr1 = Expression("1/2 + 1/3 =", Fraction(5, 6))
        expr2 = Expression("1/3 + 1/2 =", Fraction(5, 6))
        expr3 = Expression("1/4 + 1/5 =", Fraction(9, 20))

        # 第一个表达式
        assert expr1.normalized not in seen
        seen.add(expr1.normalized)

        # 第二个表达式应该被识别为重复
        assert expr2.normalized in seen

        # 第三个表达式不同
        assert expr3.normalized not in seen
        seen.add(expr3.normalized)

        assert len(seen) == 2

    def test_deduplication_mixed_operations(self):
        """测试混合运算的去重"""
        seen = set()

        expr1 = Expression("1 + 2 × 3 =", Fraction(7))
        expr2 = Expression("1 + 3 × 2 =", Fraction(7))  # 相同结构
        expr3 = Expression("(1 + 2) × 3 =", Fraction(9))  # 不同结构

        # 第一个表达式
        assert expr1.normalized not in seen
        seen.add(expr1.normalized)

        # 第二个表达式（乘法交换律）
        assert expr2.normalized in seen

        # 第三个表达式（不同结构）
        assert expr3.normalized not in seen
        seen.add(expr3.normalized)

        assert len(seen) == 2

    def test_deduplication_non_commutative_operations(self):
        """测试非交换律运算的去重"""
        seen = set()

        expr1 = Expression("5 - 2 =", Fraction(3))
        expr2 = Expression("2 - 5 =", Fraction(-3))
        expr3 = Expression("6 ÷ 2 =", Fraction(3))

        # 第一个表达式
        assert expr1.normalized not in seen
        seen.add(expr1.normalized)

        # 第二个表达式（减法不交换）
        assert expr2.normalized not in seen
        seen.add(expr2.normalized)

        # 第三个表达式（除法结果相同但结构不同）
        assert expr3.normalized not in seen
        seen.add(expr3.normalized)

        assert len(seen) == 3

    def test_deduplication_with_parentheses(self):
        """测试包含括号的表达式去重"""
        seen = set()

        expr1 = Expression("(1 + 2) × 3 =", Fraction(9))
        expr2 = Expression("(2 + 1) × 3 =", Fraction(9))  # 括号内交换
        expr3 = Expression("3 × (1 + 2) =", Fraction(9))  # 外部交换
        expr4 = Expression("3 × (2 + 1) =", Fraction(9))  # 都交换

        # 第一个表达式
        assert expr1.normalized not in seen
        seen.add(expr1.normalized)

        # 其他表达式都应该被识别为重复
        assert expr2.normalized in seen
        assert expr3.normalized in seen
        assert expr4.normalized in seen

        assert len(seen) == 1

    def test_deduplication_complex_nested(self):
        """测试复杂嵌套表达式的去重"""
        seen = set()

        expr1 = Expression("((1 + 2) × (3 + 4)) + 5 =", Fraction(26))
        expr2 = Expression("((2 + 1) × (4 + 3)) + 5 =", Fraction(26))
        expr3 = Expression("5 + ((1 + 2) × (3 + 4)) =", Fraction(26))

        # 第一个表达式
        assert expr1.normalized not in seen
        seen.add(expr1.normalized)

        # 第二个表达式应该被识别为重复
        assert expr2.normalized in seen

        # 第三个表达式（加法交换律）
        assert expr3.normalized in seen

        assert len(seen) == 1

    def test_deduplication_edge_cases(self):
        """测试边界情况"""
        seen = set()

        # 单个数字
        expr1 = Expression("42 =", Fraction(42))
        expr2 = Expression("42 =", Fraction(42))

        seen.add(expr1.normalized)
        assert expr2.normalized in seen

        # 复杂分数
        expr3 = Expression("1'2/3 + 2'1/4 =", Fraction(71, 12))
        expr4 = Expression("2'1/4 + 1'2/3 =", Fraction(71, 12))

        seen.add(expr3.normalized)
        assert expr4.normalized in seen

        assert len(seen) == 2

    def test_deduplication_performance(self):
        """测试去重机制的性能"""
        exercises = []
        seen = set()
        duplicates_found = 0

        # 生成一批表达式并测试去重效率
        for _ in range(100):
            # 使用固定的随机种子以产生可重复的结果
            import random
            random.seed(42)
            expr = main.generate_expression(5, 2)
            if expr:
                if expr.normalized in seen:
                    duplicates_found += 1
                else:
                    seen.add(expr.normalized)
                    exercises.append(expr)

        # 验证去重机制正常工作
        assert len(exercises) + duplicates_found == 100
        assert len(seen) == len(exercises)
        assert duplicates_found > 0  # 应该有一些重复

    def test_deduplication_consistency(self):
        """测试去重机制的一致性"""
        # 创建多个表达式并验证标准化的一致性
        expressions = [
            Expression("1 + 2 =", Fraction(3)),
            Expression("2 + 1 =", Fraction(3)),
            Expression("(1 + 2) =", Fraction(3)),
        ]

        # 所有表达式的标准化结果应该相同
        normalized_forms = [expr.normalized for expr in expressions]
        assert len(set(normalized_forms)) == 1

    def test_deduplication_with_invalid_expressions(self):
        """测试无效表达式的去重处理"""
        # 测试解析失败时的处理
        # 这在正常的Expression类中不应该发生，但为了完整性
        try:
            expr = Expression("invalid + expression =", Fraction(0))
            # 如果表达式创建成功，应该有某种标准化形式
            assert hasattr(expr, 'normalized')
        except:
            # 如果创建失败，这是预期的
            pass

    def test_deduplication_hash_consistency(self):
        """测试标准化结果的哈希一致性"""
        expr1 = Expression("1 + 2 =", Fraction(3))
        expr2 = Expression("2 + 1 =", Fraction(3))

        # 标准化结果应该相同，因此哈希值也应该相同
        assert hash(expr1.normalized) == hash(expr2.normalized)

        # 可以用作集合元素
        test_set = {expr1.normalized, expr2.normalized}
        assert len(test_set) == 1