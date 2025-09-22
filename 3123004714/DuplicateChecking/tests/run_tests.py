#!/usr/bin/env python3
"""
Pytest 测试运行脚本
"""
import subprocess
import sys
from pathlib import Path

def run_pytest():
    """使用项目配置运行 pytest"""
    # 获取项目根目录
    project_root = Path(__file__).parent.parent

    # 切换到项目根目录
    original_dir = Path.cwd()
    try:
        import os
        os.chdir(project_root)

        # 运行 pytest
        cmd = [sys.executable, "-m", "pytest", "tests/", "-v"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        print("=== pytest输出 ===")
        print(result.stdout)
        if result.stderr:
            print("=== 错误信息 ===")
            print(result.stderr)

        return result.returncode
    finally:
        os.chdir(original_dir)

if __name__ == "__main__":
    exit_code = run_pytest()
    sys.exit(exit_code)