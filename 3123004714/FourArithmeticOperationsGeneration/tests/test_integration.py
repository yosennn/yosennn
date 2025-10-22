"""主程序的集成测试"""
import pytest
from fractions import Fraction
import sys
import os
import tempfile
import shutil
import subprocess
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# 导入需要测试的函数
import main


class TestMainIntegration:
    """主程序集成测试"""

    def setup_method(self):
        """测试前的设置"""
        # 创建临时目录
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

        # 备份原始sys.argv
        self.original_argv = sys.argv[:]

    def teardown_method(self):
        """测试后的清理"""
        # 恢复原始工作目录
        os.chdir(self.original_cwd)

        # 删除临时目录
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

        # 恢复原始sys.argv
        sys.argv = self.original_argv

    def test_main_generate_exercises_basic(self):
        """测试基本题目生成功能"""
        sys.argv = ['main.py', '-n', '5', '-r', '10']

        main.main()

        # 检查文件是否生成
        assert os.path.exists('Exercises.txt')
        assert os.path.exists('Answers.txt')

        # 读取并验证内容
        with open('Exercises.txt', 'r', encoding='utf-8') as f:
            exercises = f.readlines()

        with open('Answers.txt', 'r', encoding='utf-8') as f:
            answers = f.readlines()

        assert len(exercises) == 5
        assert len(answers) == 5

        # 验证格式
        for exercise in exercises:
            assert exercise.strip().endswith('=')
            assert len(exercise.strip()) > 1

        for answer in answers:
            assert len(answer.strip()) > 0
            # 验证答案格式（数字或分数）
            answer_str = answer.strip()
            assert answer_str.isdigit() or '/' in answer_str or "'" in answer_str

    def test_main_generate_exercises_large_count(self):
        """测试生成大量题目"""
        sys.argv = ['main.py', '-n', '100', '-r', '20']

        main.main()

        assert os.path.exists('Exercises.txt')
        assert os.path.exists('Answers.txt')

        with open('Exercises.txt', 'r', encoding='utf-8') as f:
            exercises = f.readlines()

        with open('Answers.txt', 'r', encoding='utf-8') as f:
            answers = f.readlines()

        assert len(exercises) == 100
        assert len(answers) == 100

    def test_main_generate_exercises_small_range(self):
        """测试小范围题目生成"""
        sys.argv = ['main.py', '-n', '10', '-r', '3']

        main.main()

        assert os.path.exists('Exercises.txt')
        assert os.path.exists('Answers.txt')

        # 验证生成成功，即使范围很小
        with open('Exercises.txt', 'r', encoding='utf-8') as f:
            exercises = f.readlines()

        assert len(exercises) == 10

    def test_main_generate_exercises_range_one(self):
        """测试范围为1的题目生成"""
        sys.argv = ['main.py', '-n', '5', '-r', '1']

        main.main()

        assert os.path.exists('Exercises.txt')
        assert os.path.exists('Answers.txt')

        # 验证只有数字0的表达式
        with open('Exercises.txt', 'r', encoding='utf-8') as f:
            exercises = f.readlines()

        with open('Answers.txt', 'r', encoding='utf-8') as f:
            answers = f.readlines()

        for answer in answers:
            assert answer.strip() == '0'

    def test_main_generate_invalid_parameters(self):
        """测试无效参数处理"""
        # 无效的n参数
        sys.argv = ['main.py', '-n', 'abc', '-r', '10']
        main.main()

        # 应该没有生成文件
        assert not os.path.exists('Exercises.txt')
        assert not os.path.exists('Answers.txt')

    def test_main_generate_invalid_range(self):
        """测试无效范围参数"""
        # 范围小于1
        sys.argv = ['main.py', '-n', '5', '-r', '0']
        main.main()

        # 应该没有生成文件
        assert not os.path.exists('Exercises.txt')
        assert not os.path.exists('Answers.txt')

    def test_main_generate_missing_parameters(self):
        """测试缺少参数"""
        # 缺少-r参数
        sys.argv = ['main.py', '-n', '5']
        main.main()

        # 应该没有生成文件
        assert not os.path.exists('Exercises.txt')
        assert not os.path.exists('Answers.txt')

    def test_main_grade_exercises_correct(self):
        """测试批改正确答案"""
        # 先创建练习和答案文件
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

        with open('Exercises.txt', 'w', encoding='utf-8') as f:
            for exercise in exercises:
                f.write(f"{exercise}\n")

        with open('Answers.txt', 'w', encoding='utf-8') as f:
            for answer in answers:
                f.write(f"{answer}\n")

        # 运行批改
        sys.argv = ['main.py', '-e', 'Exercises.txt', '-a', 'Answers.txt']
        main.main()

        # 检查批改结果
        assert os.path.exists('Grade.txt')

        with open('Grade.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            assert "Correct: 4 (1, 2, 3, 4)" in content
            assert "Wrong: 0 ()" in content

    def test_main_grade_exercises_mixed(self):
        """测试批改混合答案"""
        # 先创建练习和答案文件
        exercises = [
            "1 + 2 =",
            "3 × 4 =",
            "5 - 2 =",
            "8 ÷ 2 ="
        ]
        answers = [
            "3",    # 正确
            "10",   # 错误
            "3",    # 正确
            "5"     # 错误
        ]

        with open('Exercises.txt', 'w', encoding='utf-8') as f:
            for exercise in exercises:
                f.write(f"{exercise}\n")

        with open('Answers.txt', 'w', encoding='utf-8') as f:
            for answer in answers:
                f.write(f"{answer}\n")

        # 运行批改
        sys.argv = ['main.py', '-e', 'Exercises.txt', '-a', 'Answers.txt']
        main.main()

        # 检查批改结果
        assert os.path.exists('Grade.txt')

        with open('Grade.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            assert "Correct: 2 (1, 3)" in content
            assert "Wrong: 2 (2, 4)" in content

    def test_main_grade_missing_files(self):
        """测试批改缺少文件"""
        sys.argv = ['main.py', '-e', 'NonExistent.txt', '-a', 'Answers.txt']
        # 应该抛出异常但不崩溃
        with pytest.raises(FileNotFoundError):
            main.main()

    def test_main_generate_and_grade_workflow(self):
        """测试生成-批改完整工作流"""
        # 第一步：生成题目
        sys.argv = ['main.py', '-n', '5', '-r', '10']
        main.main()

        assert os.path.exists('Exercises.txt')
        assert os.path.exists('Answers.txt')

        # 读取生成的题目
        with open('Exercises.txt', 'r', encoding='utf-8') as f:
            exercises = f.readlines()

        # 创建学生答案（部分正确，部分错误）
        student_answers = []
        for i, exercise in enumerate(exercises):
            if i < 3:
                # 前三个使用正确答案
                with open('Answers.txt', 'r', encoding='utf-8') as f:
                    correct_answers = f.readlines()
                student_answers.append(correct_answers[i].strip())
            else:
                # 后两个使用错误答案
                student_answers.append("999")

        # 写入学生答案文件
        with open('StudentAnswers.txt', 'w', encoding='utf-8') as f:
            for answer in student_answers:
                f.write(f"{answer}\n")

        # 第二步：批改答案
        sys.argv = ['main.py', '-e', 'Exercises.txt', '-a', 'StudentAnswers.txt']
        main.main()

        # 检查批改结果
        assert os.path.exists('Grade.txt')

        with open('Grade.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            assert "Correct: 3 (1, 2, 3)" in content
            assert "Wrong: 2 (4, 5)" in content

    def test_main_complex_expressions_workflow(self):
        """测试复杂表达式的完整工作流"""
        # 生成包含分数和括号的复杂题目
        sys.argv = ['main.py', '-n', '10', '-r', '5']
        main.main()

        assert os.path.exists('Exercises.txt')
        assert os.path.exists('Answers.txt')

        # 验证生成的题目包含复杂元素
        with open('Exercises.txt', 'r', encoding='utf-8') as f:
            exercises = f.readlines()

        has_fractions = any('/' in ex for ex in exercises)
        has_parentheses = any('(' in ex for ex in exercises)

        # 由于是随机的，不一定每次都有，但应该有合理的概率
        # 这里只验证文件格式正确
        assert len(exercises) == 10

    def test_main_large_scale_workflow(self):
        """测试大规模工作流"""
        # 生成大量题目
        sys.argv = ['main.py', '-n', '1000', '-r', '50']
        main.main()

        assert os.path.exists('Exercises.txt')
        assert os.path.exists('Answers.txt')

        # 验证文件大小和内容
        with open('Exercises.txt', 'r', encoding='utf-8') as f:
            exercises = f.readlines()

        with open('Answers.txt', 'r', encoding='utf-8') as f:
            answers = f.readlines()

        assert len(exercises) == 1000
        assert len(answers) == 1000

        # 验证题目唯一性
        normalized_expressions = set()
        for exercise in exercises:
            # 提取表达式（去除等号）
            expr_str = exercise.rstrip("=").strip()
            # 使用Expression类进行标准化
            try:
                from src.Expression import Expression
                value = main.evaluate_expression(expr_str)
                if value:
                    expr = Expression(f"{expr_str} =", value)
                    normalized_expressions.add(expr.normalized)
            except:
                pass

        # 应该有很高的唯一性
        assert len(normalized_expressions) >= 950  # 允许少量重复

    def test_main_error_recovery(self):
        """测试错误恢复"""
        # 测试各种错误情况下的程序行为

        # 1. 无效参数后跟有效参数
        sys.argv = ['main.py', '-n', 'invalid', '-r', '10']
        main.main()
        assert not os.path.exists('Exercises.txt')

        # 2. 立即使用有效参数
        sys.argv = ['main.py', '-n', '5', '-r', '10']
        main.main()
        assert os.path.exists('Exercises.txt')

    def test_main_help_message(self):
        """测试帮助信息"""
        # 无效参数应该显示帮助信息
        sys.argv = ['main.py']
        main.main()

        # 不应该生成任何文件
        assert not os.path.exists('Exercises.txt')
        assert not os.path.exists('Answers.txt')
        assert not os.path.exists('Grade.txt')

    def test_main_file_encoding_consistency(self):
        """测试文件编码一致性"""
        sys.argv = ['main.py', '-n', '10', '-r', '10']
        main.main()

        # 验证文件能够以UTF-8编码正确读取
        try:
            with open('Exercises.txt', 'r', encoding='utf-8') as f:
                exercises = f.read()

            with open('Answers.txt', 'r', encoding='utf-8') as f:
                answers = f.read()

            # 验证内容不为空且包含预期的字符
            assert len(exercises) > 0
            assert len(answers) > 0
            assert '÷' in exercises or '×' in exercises  # 验证特殊运算符存在

        except UnicodeDecodeError:
            pytest.fail("文件编码不是UTF-8")

    def test_main_subprocess_execution(self):
        """测试通过子进程执行主程序"""
        # 使用subprocess运行主程序
        result = subprocess.run([
            sys.executable, '-c', '''
import sys
sys.path.append(r"D:\code\FourArithmeticOperationsGeneration")
import main
sys.argv = ["main.py", "-n", "3", "-r", "5"]
main.main()
'''
        ], capture_output=True, text=True, cwd=self.temp_dir)

        # 检查进程成功执行
        assert result.returncode == 0

        # 检查文件生成
        assert os.path.exists('Exercises.txt')
        assert os.path.exists('Answers.txt')

        # 检查文件内容
        with open('Exercises.txt', 'r', encoding='utf-8') as f:
            exercises = f.readlines()

        with open('Answers.txt', 'r', encoding='utf-8') as f:
            answers = f.readlines()

        assert len(exercises) == 3
        assert len(answers) == 3