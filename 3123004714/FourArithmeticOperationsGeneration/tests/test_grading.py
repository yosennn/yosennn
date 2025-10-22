"""批改系统的单元测试"""
import pytest
from fractions import Fraction
import sys
import os
import tempfile
import shutil
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# 导入需要测试的函数
import main


class TestGradingSystem:
    """批改系统的测试用例"""

    def setup_method(self):
        """测试前的设置"""
        # 创建临时目录
        self.temp_dir = tempfile.mkdtemp()
        self.exercise_file = os.path.join(self.temp_dir, "test_exercises.txt")
        self.answer_file = os.path.join(self.temp_dir, "test_answers.txt")
        self.grade_file = os.path.join(self.temp_dir, "Grade.txt")

    def teardown_method(self):
        """测试后的清理"""
        # 删除临时目录
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def create_test_files(self, exercises, answers):
        """创建测试用的练习和答案文件"""
        with open(self.exercise_file, 'w', encoding='utf-8') as f:
            for exercise in exercises:
                f.write(f"{exercise}\n")

        with open(self.answer_file, 'w', encoding='utf-8') as f:
            for answer in answers:
                f.write(f"{answer}\n")

    def read_grade_file(self):
        """读取批改结果文件"""
        if os.path.exists(self.grade_file):
            with open(self.grade_file, 'r', encoding='utf-8') as f:
                return f.read()
        return None

    def test_grade_all_correct_simple(self):
        """测试全部正确的简单题目"""
        exercises = [
            "1 + 2 =",
            "3 × 4 =",
            "5 - 2 =",
            "8 ÷ 2 ="
        ]
        answers = [
            "3",
            "12",
            "3",
            "4"
        ]

        self.create_test_files(exercises, answers)
        main.grade_exercises(self.exercise_file, self.answer_file)

        grade_content = self.read_grade_file()
        assert "Correct: 4 (1, 2, 3, 4)" in grade_content
        assert "Wrong: 0 ()" in grade_content

    def test_grade_all_correct_fractions(self):
        """测试全部正确的分数题目"""
        exercises = [
            "1/2 + 1/3 =",
            "1'1/2 × 2 =",
            "2/3 ÷ 1/3 =",
            "1'1/4 - 1/4 ="
        ]
        answers = [
            "5/6",
            "3",
            "2",
            "1"
        ]

        self.create_test_files(exercises, answers)
        main.grade_exercises(self.exercise_file, self.answer_file)

        grade_content = self.read_grade_file()
        assert "Correct: 4 (1, 2, 3, 4)" in grade_content
        assert "Wrong: 0 ()" in grade_content

    def test_grade_all_wrong(self):
        """测试全部错误的题目"""
        exercises = [
            "1 + 2 =",
            "3 × 4 =",
            "5 - 2 =",
            "8 ÷ 2 ="
        ]
        answers = [
            "4",  # 错误
            "10",  # 错误
            "4",  # 错误
            "5"   # 错误
        ]

        self.create_test_files(exercises, answers)
        main.grade_exercises(self.exercise_file, self.answer_file)

        grade_content = self.read_grade_file()
        assert "Correct: 0 ()" in grade_content
        assert "Wrong: 4 (1, 2, 3, 4)" in grade_content

    def test_grade_mixed_correct_wrong(self):
        """测试混合正确和错误的题目"""
        exercises = [
            "1 + 2 =",
            "3 × 4 =",
            "5 - 2 =",
            "8 ÷ 2 =",
            "1/2 + 1/2 =",
            "2 × 3 ="
        ]
        answers = [
            "3",    # 正确
            "10",   # 错误
            "3",    # 正确
            "5",    # 错误
            "1",    # 正确
            "6"     # 正确
        ]

        self.create_test_files(exercises, answers)
        main.grade_exercises(self.exercise_file, self.answer_file)

        grade_content = self.read_grade_file()
        assert "Correct: 3 (1, 3, 5, 6)" in grade_content
        assert "Wrong: 2 (2, 4)" in grade_content

    def test_grade_fraction_answers_different_formats(self):
        """测试不同格式的分数答案"""
        exercises = [
            "1/2 + 1/2 =",
            "1 + 1/2 =",
            "2 ÷ 4 =",
            "3/2 ="
        ]
        answers = [
            "1",        # 正确：整数形式
            "1'1/2",    # 正确：带分数形式
            "1/2",      # 正确：分数形式
            "1'1/2"     # 正确：带分数形式
        ]

        self.create_test_files(exercises, answers)
        main.grade_exercises(self.exercise_file, self.answer_file)

        grade_content = self.read_grade_file()
        assert "Correct: 4 (1, 2, 3, 4)" in grade_content
        assert "Wrong: 0 ()" in grade_content

    def test_grade_invalid_answer_format(self):
        """测试无效答案格式"""
        exercises = [
            "1 + 2 =",
            "3 × 4 =",
            "5 - 2 ="
        ]
        answers = [
            "3",        # 正确
            "invalid",  # 无效格式
            "three"     # 无效格式
        ]

        self.create_test_files(exercises, answers)
        main.grade_exercises(self.exercise_file, self.answer_file)

        grade_content = self.read_grade_file()
        assert "Correct: 1 (1)" in grade_content
        assert "Wrong: 2 (2, 3)" in grade_content

    def test_grade_missing_answers(self):
        """测试答案数量不足"""
        exercises = [
            "1 + 2 =",
            "3 × 4 =",
            "5 - 2 =",
            "8 ÷ 2 ="
        ]
        answers = [
            "3",
            "12"
            # 缺少两个答案
        ]

        self.create_test_files(exercises, answers)
        main.grade_exercises(self.exercise_file, self.answer_file)

        grade_content = self.read_grade_file()
        # 应该只处理前两个题目
        assert "Correct: 2 (1, 2)" in grade_content
        assert "Wrong: 0 ()" in grade_content

    def test_grade_extra_answers(self):
        """测试答案数量过多"""
        exercises = [
            "1 + 2 =",
            "3 × 4 ="
        ]
        answers = [
            "3",
            "12",
            "5",    # 额外的答案
            "4"     # 额外的答案
        ]

        self.create_test_files(exercises, answers)
        main.grade_exercises(self.exercise_file, self.answer_file)

        grade_content = self.read_grade_file()
        # 应该只处理前两个题目
        assert "Correct: 2 (1, 2)" in grade_content
        assert "Wrong: 0 ()" in grade_content

    def test_grade_empty_files(self):
        """测试空文件"""
        self.create_test_files([], [])
        main.grade_exercises(self.exercise_file, self.answer_file)

        grade_content = self.read_grade_file()
        assert "Correct: 0 ()" in grade_content
        assert "Wrong: 0 ()" in grade_content

    def test_grade_complex_expressions(self):
        """测试复杂表达式"""
        exercises = [
            "(1 + 2) × 3 =",
            "1 + 2 × 3 =",
            "(4 ÷ 2) + 6 =",
            "1/2 + 1/3 + 1/6 ="
        ]
        answers = [
            "9",
            "7",
            "8",
            "1"
        ]

        self.create_test_files(exercises, answers)
        main.grade_exercises(self.exercise_file, self.answer_file)

        grade_content = self.read_grade_file()
        assert "Correct: 4 (1, 2, 3, 4)" in grade_content
        assert "Wrong: 0 ()" in grade_content

    def test_grade_decimal_equivalent_answers(self):
        """测试小数形式的答案（应该被拒绝）"""
        exercises = [
            "1/2 =",
            "1'1/2 =",
            "3 ÷ 2 ="
        ]
        answers = [
            "0.5",      # 小数形式（应该被拒绝）
            "1.5",      # 小数形式（应该被拒绝）
            "1'1/2"     # 正确的带分数形式
        ]

        self.create_test_files(exercises, answers)
        main.grade_exercises(self.exercise_file, self.answer_file)

        grade_content = self.read_grade_file()
        assert "Correct: 1 (3)" in grade_content
        assert "Wrong: 2 (1, 2)" in grade_content

    def test_grade_unreduced_fractions(self):
        """测试未约分的分数答案"""
        exercises = [
            "1/2 + 1/2 =",
            "2/4 =",
            "1/3 + 1/6 ="
        ]
        answers = [
            "2/2",      # 未约分但数值正确
            "1/2",      # 正确
            "1/2"       # 正确
        ]

        self.create_test_files(exercises, answers)
        main.grade_exercises(self.exercise_file, self.answer_file)

        grade_content = self.read_grade_file()
        assert "Correct: 3 (1, 2, 3)" in grade_content
        assert "Wrong: 0 ()" in grade_content

    def test_grade_file_encoding(self):
        """测试文件编码处理"""
        exercises = [
            "1 + 2 =",
            "3 × 4 =",
            "1/2 + 1/3 ="
        ]
        answers = [
            "3",
            "12",
            "5/6"
        ]

        self.create_test_files(exercises, answers)
        main.grade_exercises(self.exercise_file, self.answer_file)

        # 验证文件能够正确读取
        assert os.path.exists(self.grade_file)
        grade_content = self.read_grade_file()
        assert "Correct: 3 (1, 2, 3)" in grade_content

    def test_grade_whitespace_handling(self):
        """测试空白字符处理"""
        exercises = [
            "1 + 2 =",
            "3 × 4 =",
            " 5 - 2 = ",  # 带空格
            "",           # 空行
            "8 ÷ 2 ="
        ]
        answers = [
            "3",
            "12",
            "3",
            "ignore",    # 对应空行
            "4"
        ]

        self.create_test_files(exercises, answers)
        main.grade_exercises(self.exercise_file, self.answer_file)

        grade_content = self.read_grade_file()
        # 空行应该被忽略
        assert "Correct: 4 (1, 2, 3, 5)" in grade_content
        assert "Wrong: 0 ()" in grade_content

    def test_grade_large_dataset(self):
        """测试大数据集"""
        exercises = []
        answers = []

        for i in range(100):
            exercises.append(f"{i} + {i+1} =")
            answers.append(str(2*i + 1))

        self.create_test_files(exercises, answers)
        main.grade_exercises(self.exercise_file, self.answer_file)

        grade_content = self.read_grade_file()
        assert "Correct: 100" in grade_content
        assert "Wrong: 0 ()" in grade_content

    def test_grade_mixed_number_equivalence(self):
        """测试带分数等价性"""
        exercises = [
            "3 ÷ 2 =",
            "5 ÷ 2 =",
            "7 ÷ 4 ="
        ]
        answers = [
            "1'1/2",    # 正确
            "2'1/2",    # 正确
            "1'3/4"     # 正确
        ]

        self.create_test_files(exercises, answers)
        main.grade_exercises(self.exercise_file, self.answer_file)

        grade_content = self.read_grade_file()
        assert "Correct: 3 (1, 2, 3)" in grade_content
        assert "Wrong: 0 ()" in grade_content

    def test_grade_zero_results(self):
        """测试结果为0的情况"""
        exercises = [
            "5 × 0 =",
            "0 ÷ 5 =",
            "0 + 0 =",
            "0 - 0 ="
        ]
        answers = [
            "0",
            "0",
            "0",
            "0"
        ]

        self.create_test_files(exercises, answers)
        main.grade_exercises(self.exercise_file, self.answer_file)

        grade_content = self.read_grade_file()
        assert "Correct: 4 (1, 2, 3, 4)" in grade_content
        assert "Wrong: 0 ()" in grade_content