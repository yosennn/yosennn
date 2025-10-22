"""数字生成和解析工具的单元测试"""
import pytest
from fractions import Fraction
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# 导入需要测试的函数
import main


class TestNumberGeneration:
    """数字生成功能的测试用例"""

    def test_generate_number_range(self):
        """测试生成的数字在指定范围内"""
        for r in [5, 10, 20]:
            for _ in range(100):
                num_str = main.generate_number(r)
                num = main.parse_number(num_str)
                assert 0 <= num < r, f"生成的数字 {num} 不在范围 [0, {r}) 内"

    def test_generate_number_fraction_range(self):
        """测试生成的真分数在指定范围内"""
        for r in [5, 10, 20]:
            for _ in range(100):
                num_str = main.generate_number(r)
                num = main.parse_number(num_str)
                assert 0 <= num < r, f"生成的数字 {num} 不在范围 [0, {r}) 内"

    def test_generate_number_small_range(self):
        """测试小范围的数字生成"""
        # 范围为2时，分母只能为2
        for _ in range(20):
            num_str = main.generate_number(2)
            num = main.parse_number(num_str)
            assert 0 <= num < 2

    def test_generate_number_range_one(self):
        """测试范围为1的数字生成"""
        for _ in range(20):
            num_str = main.generate_number(1)
            num = main.parse_number(num_str)
            assert num == 0, "范围为1时只能生成数字0"

    def test_generate_number_types(self):
        """测试生成的数字类型覆盖"""
        found_integer = False
        found_fraction = False
        found_mixed = False

        for _ in range(200):
            num_str = main.generate_number(10)
            if "'" in num_str:
                found_mixed = True
            elif "/" in num_str:
                found_fraction = True
            else:
                found_integer = True

            if found_integer and found_fraction and found_mixed:
                break

        assert found_integer, "没有生成自然数"
        assert found_fraction, "没有生成真分数"
        assert found_mixed, "没有生成带分数"


class TestNumberParsing:
    """数字解析功能的测试用例"""

    def test_parse_integer(self):
        """测试解析整数"""
        assert main.parse_number("0") == Fraction(0, 1)
        assert main.parse_number("5") == Fraction(5, 1)
        assert main.parse_number("123") == Fraction(123, 1)

    def test_parse_proper_fraction(self):
        """测试解析真分数"""
        assert main.parse_number("1/2") == Fraction(1, 2)
        assert main.parse_number("3/4") == Fraction(3, 4)
        assert main.parse_number("7/8") == Fraction(7, 8)

    def test_parse_mixed_number(self):
        """测试解析带分数"""
        assert main.parse_number("1'1/2") == Fraction(3, 2)
        assert main.parse_number("2'3/4") == Fraction(11, 4)
        assert main.parse_number("5'1/3") == Fraction(16, 3)

    def test_parse_zero_mixed_number(self):
        """测试解析整数部分为0的带分数"""
        assert main.parse_number("0'1/2") == Fraction(1, 2)
        assert main.parse_number("0'3/4") == Fraction(3, 4)

    def test_parse_invalid_input(self):
        """测试解析无效输入"""
        with pytest.raises(Exception):
            main.parse_number("")  # 空字符串

        with pytest.raises(Exception):
            main.parse_number("abc")  # 非数字字符串

        with pytest.raises(Exception):
            main.parse_number("1/")  # 缺少分母

        with pytest.raises(Exception):
            main.parse_number("/2")  # 缺少分子

        with pytest.raises(Exception):
            main.parse_number("1''2")  # 格式错误

    def test_parse_fraction_zero_denominator(self):
        """测试分母为0的情况"""
        with pytest.raises(Exception):
            main.parse_number("1/0")

    def test_parse_mixed_number_zero_denominator(self):
        """测试带分数分母为0的情况"""
        with pytest.raises(Exception):
            main.parse_number("1'1/0")


class TestNumberFormatting:
    """数字格式化功能的测试用例"""

    def test_format_integer(self):
        """测试格式化整数"""
        assert main.format_number(Fraction(0, 1)) == "0"
        assert main.format_number(Fraction(5, 1)) == "5"
        assert main.format_number(Fraction(123, 1)) == "123"

    def test_format_proper_fraction(self):
        """测试格式化真分数"""
        assert main.format_number(Fraction(1, 2)) == "1/2"
        assert main.format_number(Fraction(3, 4)) == "3/4"
        assert main.format_number(Fraction(2, 3)) == "2/3"

    def test_format_improper_fraction(self):
        """测试格式化假分数（应该转为带分数）"""
        assert main.format_number(Fraction(3, 2)) == "1'1/2"
        assert main.format_number(Fraction(11, 4)) == "2'3/4"
        assert main.format_number(Fraction(16, 3)) == "5'1/3"

    def test_format_whole_number_from_fraction(self):
        """测试分数形式的整数格式化"""
        assert main.format_number(Fraction(4, 2)) == "2"
        assert main.format_number(Fraction(6, 3)) == "2"
        assert main.format_number(Fraction(9, 3)) == "3"

    def test_format_negative_numbers(self):
        """测试负数格式化"""
        # 注意：程序设计为不产生负数结果，但测试解析功能
        assert main.format_number(Fraction(-1, 2)) == "-1/2"
        assert main.format_number(Fraction(-3, 2)) == "-1'1/2"

    def test_roundtrip_conversion(self):
        """测试往返转换的一致性"""
        test_numbers = [
            "0", "1", "5", "10",
            "1/2", "3/4", "2/3",
            "1'1/2", "2'3/4", "5'1/3"
        ]

        for num_str in test_numbers:
            fraction = main.parse_number(num_str)
            formatted = main.format_number(fraction)
            # 对于某些情况，格式化结果可能与原始字符串不同但数值相同
            re_parsed = main.parse_number(formatted)
            assert re_parsed == fraction, f"往返转换失败: {num_str} -> {fraction} -> {formatted} -> {re_parsed}"


class TestNumberIntegration:
    """数字功能的集成测试"""

    def test_generate_parse_format_roundtrip(self):
        """测试生成-解析-格式化的完整流程"""
        for _ in range(100):
            # 生成数字
            num_str = main.generate_number(10)

            # 解析为Fraction
            fraction = main.parse_number(num_str)

            # 格式化回字符串
            formatted = main.format_number(fraction)

            # 验证数值一致性
            re_parsed = main.parse_number(formatted)
            assert re_parsed == fraction

    def test_generate_number_validity(self):
        """测试生成的数字都是有效的"""
        for _ in range(200):
            num_str = main.generate_number(20)
            try:
                fraction = main.parse_number(num_str)
                # 验证可以正常解析
                assert isinstance(fraction, Fraction)
            except Exception as e:
                pytest.fail(f"生成的数字 {num_str} 无法解析: {e}")

    def test_generate_proper_fractions(self):
        """测试生成的分数都是真分数"""
        proper_fractions_found = False

        for _ in range(200):
            num_str = main.generate_number(20)
            if "/" in num_str and "'" not in num_str:
                # 这是一个真分数
                fraction = main.parse_number(num_str)
                assert 0 < fraction < 1, f"生成的真分数 {num_str} 不在(0,1)范围内"
                proper_fractions_found = True

        assert proper_fractions_found, "没有找到真分数"

    def test_generate_mixed_numbers_validity(self):
        """测试生成的带分数都是有效的"""
        mixed_numbers_found = False

        for _ in range(200):
            num_str = main.generate_number(20)
            if "'" in num_str:
                # 这是一个带分数
                fraction = main.parse_number(num_str)
                integer_part = fraction.numerator // fraction.denominator
                remainder = fraction.numerator % fraction.denominator
                assert integer_part > 0, f"带分数 {num_str} 的整数部分应该大于0"
                assert 0 < remainder < fraction.denominator, f"带分数 {num_str} 的分数部分应该是真分数"
                mixed_numbers_found = True

        assert mixed_numbers_found, "没有找到带分数"