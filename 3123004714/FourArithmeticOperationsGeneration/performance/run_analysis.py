#!/usr/bin/env python3
"""
性能分析运行脚本
提供便捷的性能分析入口
"""

import os
import sys
import subprocess

def run_performance_analysis():
    """运行完整的性能分析"""
    print("开始运行性能分析...")

    # 脚本目录
    script_dir = os.path.join(os.path.dirname(__file__), 'scripts')
    reports_dir = os.path.join(os.path.dirname(__file__), 'reports')

    # 确保报告目录存在
    os.makedirs(reports_dir, exist_ok=True)

    # 运行性能分析脚本
    try:
        print("1. 运行基础性能分析...")
        result = subprocess.run([
            sys.executable,
            os.path.join(script_dir, 'performance_analysis.py')
        ], cwd=os.path.dirname(os.path.dirname(__file__)))

        if result.returncode != 0:
            print("性能分析脚本执行失败")
            return False

        print("2. 生成性能可视化...")
        result = subprocess.run([
            sys.executable,
            os.path.join(script_dir, 'performance_visualization.py')
        ], cwd=os.path.dirname(os.path.dirname(__file__)))

        if result.returncode != 0:
            print("性能可视化脚本执行失败")
            return False

        print("3. 移动报告文件到reports目录...")
        # 移动生成的报告文件
        for file in ['performance_stats.prof', 'performance_report.html',
                     'performance_analysis.png', 'bottleneck_analysis.md']:
            src = os.path.join(os.path.dirname(os.path.dirname(__file__)), file)
            dst = os.path.join(reports_dir, file)
            if os.path.exists(src):
                os.rename(src, dst)
                print(f"   已移动: {file} -> reports/")

        print("性能分析完成！")
        print(f"报告文件已保存到: {reports_dir}")

        return True

    except Exception as e:
        print(f"运行性能分析时出错: {e}")
        return False

def show_report_files():
    """显示生成的报告文件"""
    reports_dir = os.path.join(os.path.dirname(__file__), 'reports')

    if not os.path.exists(reports_dir):
        print("报告目录不存在")
        return

    files = os.listdir(reports_dir)
    if not files:
        print("没有找到报告文件")
        return

    print("可用的报告文件:")
    for i, file in enumerate(files, 1):
        file_path = os.path.join(reports_dir, file)
        size = os.path.getsize(file_path)
        print(f"{i}. {file} ({size} bytes)")

def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='四则运算生成程序性能分析工具')
    parser.add_argument('action', choices=['run', 'list'],
                       help='操作类型: run(运行分析) 或 list(列出报告文件)')

    args = parser.parse_args()

    if args.action == 'run':
        success = run_performance_analysis()
        sys.exit(0 if success else 1)
    elif args.action == 'list':
        show_report_files()

if __name__ == "__main__":
    main()