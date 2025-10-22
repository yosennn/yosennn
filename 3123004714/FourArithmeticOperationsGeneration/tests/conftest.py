"""pytest配置文件，提供通用的测试工具和夹具"""
import pytest
import tempfile
import shutil
import os
import sys
from fractions import Fraction

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'src'))


@pytest.fixture
def temp_dir():
    """创建临时目录夹具"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_expressions():
    """提供示例表达式列表"""
    return [
        "1 + 2 =",
        "3 × 4 =",
        "5 - 2 =",
        "8 ÷ 2 =",
        "1/2 + 1/3 =",
        "1'1/2 × 2 =",
        "(1 + 2) × 3 =",
        "1 + 2 × 3 ="
    ]


@pytest.fixture
def sample_answers():
    """提供示例答案列表"""
    return [
        "3",
        "12",
        "3",
        "4",
        "5/6",
        "3",
        "9",
        "7"
    ]


@pytest.fixture
def sample_fraction_expressions():
    """提供包含分数的示例表达式"""
    return [
        "1/2 + 1/3 =",
        "1'1/2 + 2'1/4 =",
        "2/3 × 3/4 =",
        "1'1/2 ÷ 1/2 =",
        "(1/2 + 1/3) × 2 ="
    ]


@pytest.fixture
def sample_fraction_answers():
    """提供分数示例答案"""
    return [
        "5/6",
        "2'3/4",
        "1/2",
        "3",
        "5/3"
    ]


@pytest.fixture
def complex_expressions():
    """提供复杂表达式示例"""
    return [
        "(1 + 2) × (3 + 4) =",
        "1 + 2 × 3 - 4 ÷ 2 =",
        "(1'1/2 + 2'1/3) × 2 =",
        "((1 + 2) × 3) - 1 =",
        "1/2 + 2/3 × 3/4 - 1/6 ="
    ]


@pytest.fixture
def complex_answers():
    """提供复杂表达式的答案"""
    return [
        "21",
        "5",
        "7'2/3",
        "8",
        "1"
    ]


@pytest.fixture
def exercise_files(temp_dir, sample_expressions, sample_answers):
    """创建练习和答案文件的夹具"""
    exercise_file = os.path.join(temp_dir, "Exercises.txt")
    answer_file = os.path.join(temp_dir, "Answers.txt")

    with open(exercise_file, 'w', encoding='utf-8') as f:
        for expr in sample_expressions:
            f.write(f"{expr}\n")

    with open(answer_file, 'w', encoding='utf-8') as f:
        for ans in sample_answers:
            f.write(f"{ans}\n")

    return exercise_file, answer_file


@pytest.fixture
def fraction_exercise_files(temp_dir, sample_fraction_expressions, sample_fraction_answers):
    """创建分数练习和答案文件的夹具"""
    exercise_file = os.path.join(temp_dir, "FractionExercises.txt")
    answer_file = os.path.join(temp_dir, "FractionAnswers.txt")

    with open(exercise_file, 'w', encoding='utf-8') as f:
        for expr in sample_fraction_expressions:
            f.write(f"{expr}\n")

    with open(answer_file, 'w', encoding='utf-8') as f:
        for ans in sample_fraction_answers:
            f.write(f"{ans}\n")

    return exercise_file, answer_file


@pytest.fixture
def complex_exercise_files(temp_dir, complex_expressions, complex_answers):
    """创建复杂练习和答案文件的夹具"""
    exercise_file = os.path.join(temp_dir, "ComplexExercises.txt")
    answer_file = os.path.join(temp_dir, "ComplexAnswers.txt")

    with open(exercise_file, 'w', encoding='utf-8') as f:
        for expr in complex_expressions:
            f.write(f"{expr}\n")

    with open(answer_file, 'w', encoding='utf-8') as f:
        for ans in complex_answers:
            f.write(f"{ans}\n")

    return exercise_file, answer_file


@pytest.fixture
def mixed_answer_files(temp_dir, sample_expressions):
    """创建混合正确/错误答案的文件夹具"""
    exercise_file = os.path.join(temp_dir, "MixedExercises.txt")
    answer_file = os.path.join(temp_dir, "MixedAnswers.txt")

    with open(exercise_file, 'w', encoding='utf-8') as f:
        for expr in sample_expressions:
            f.write(f"{expr}\n")

    # 创建混合答案（一半正确，一半错误）
    mixed_answers = []
    for i, expr in enumerate(sample_expressions):
        if i % 2 == 0:
            # 偶数索引使用正确答案
            expr_str = expr.rstrip("=").strip()
            import main
            result = main.evaluate_expression(expr_str)
            if result:
                mixed_answers.append(main.format_number(result))
            else:
                mixed_answers.append("0")
        else:
            # 奇数索引使用错误答案
            mixed_answers.append("999")

    with open(answer_file, 'w', encoding='utf-8') as f:
        for ans in mixed_answers:
            f.write(f"{ans}\n")

    return exercise_file, answer_file, mixed_answers


@pytest.fixture(scope="session")
def test_random_seed():
    """为需要可重复结果的测试提供固定随机种子"""
    import random
    random.seed(42)
    yield
    # 恢复随机性
    random.seed()


def pytest_configure(config):
    """pytest配置钩子"""
    # 添加自定义标记
    config.addinivalue_line(
        "markers", "slow: 标记测试为慢速测试"
    )
    config.addinivalue_line(
        "markers", "integration: 标记为集成测试"
    )
    config.addinivalue_line(
        "markers", "unit: 标记为单元测试"
    )
    config.addinivalue_line(
        "markers", "generation: 标记为生成相关测试"
    )
    config.addinivalue_line(
        "markers", "evaluation: 标记为计算相关测试"
    )
    config.addinivalue_line(
        "markers", "grading: 标记为批改相关测试"
    )


def pytest_collection_modifyitems(config, items):
    """修改测试收集的钩子"""
    # 为没有标记的测试自动添加unit标记
    for item in items:
        if not any(item.iter_markers()):
            item.add_marker(pytest.mark.unit)


# 测试工具函数
def assert_fraction_equal(frac1, frac2):
    """断言两个Fraction相等"""
    assert isinstance(frac1, Fraction), f"第一个参数不是Fraction: {type(frac1)}"
    assert isinstance(frac2, Fraction), f"第二个参数不是Fraction: {type(frac2)}"
    assert frac1 == frac2, f"分数不相等: {frac1} != {frac2}"


def assert_expression_valid(expr_str):
    """断言表达式字符串有效"""
    assert isinstance(expr_str, str), "表达式必须是字符串"
    assert len(expr_str) > 0, "表达式不能为空"
    assert expr_str.endswith("="), "表达式必须以等号结尾"

    # 尝试计算表达式
    import main
    result = main.evaluate_expression(expr_str.rstrip("="))
    assert result is not None, f"无法计算表达式: {expr_str}"
    assert result >= 0, f"表达式结果为负数: {expr_str} = {result}"


def create_test_expression(expr_str, value):
    """创建测试用的Expression对象"""
    from src.Expression import Expression
    return Expression(expr_str, value)


def parse_number_safe(num_str):
    """安全解析数字字符串"""
    import main
    try:
        return main.parse_number(num_str)
    except Exception as e:
        pytest.fail(f"无法解析数字 '{num_str}': {e}")


def format_number_safe(frac):
    """安全格式化Fraction对象"""
    import main
    try:
        return main.format_number(frac)
    except Exception as e:
        pytest.fail(f"无法格式化分数 {frac}: {e}")