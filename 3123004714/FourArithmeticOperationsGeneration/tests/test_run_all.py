"""运行所有测试的便捷脚本"""
import pytest
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'src'))


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("四则运算题目生成程序 - 完整测试套件")
    print("=" * 60)

    # 运行测试并返回结果
    exit_code = pytest.main([
        'tests/',
        '-v',
        '--tb=short',
        '--color=yes',
        '--durations=10'
    ])

    if exit_code == 0:
        print("\n" + "=" * 60)
        print("✅ 所有测试通过！")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ 部分测试失败！")
        print("=" * 60)

    return exit_code


def run_unit_tests():
    """仅运行单元测试"""
    print("=" * 60)
    print("四则运算题目生成程序 - 单元测试")
    print("=" * 60)

    exit_code = pytest.main([
        'tests/',
        '-v',
        '-m', 'unit',
        '--tb=short',
        '--color=yes'
    ])

    return exit_code


def run_integration_tests():
    """仅运行集成测试"""
    print("=" * 60)
    print("四则运算题目生成程序 - 集成测试")
    print("=" * 60)

    exit_code = pytest.main([
        'tests/',
        '-v',
        '-m', 'integration',
        '--tb=short',
        '--color=yes'
    ])

    return exit_code


def run_specific_tests(test_pattern):
    """运行特定的测试"""
    print("=" * 60)
    print(f"四则运算题目生成程序 - 特定测试: {test_pattern}")
    print("=" * 60)

    exit_code = pytest.main([
        f'tests/{test_pattern}',
        '-v',
        '--tb=short',
        '--color=yes'
    ])

    return exit_code


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='运行测试套件')
    parser.add_argument('--unit', action='store_true', help='仅运行单元测试')
    parser.add_argument('--integration', action='store_true', help='仅运行集成测试')
    parser.add_argument('--pattern', type=str, help='运行特定模式的测试')
    parser.add_argument('--coverage', action='store_true', help='生成覆盖率报告')

    args = parser.parse_args()

    if args.coverage:
        # 运行带覆盖率的测试
        pytest_args = [
            'tests/',
            '--cov=main',
            '--cov=src',
            '--cov-report=html',
            '--cov-report=term-missing',
            '-v'
        ]
        exit_code = pytest.main(pytest_args)
    elif args.unit:
        exit_code = run_unit_tests()
    elif args.integration:
        exit_code = run_integration_tests()
    elif args.pattern:
        exit_code = run_specific_tests(args.pattern)
    else:
        exit_code = run_all_tests()

    sys.exit(exit_code)