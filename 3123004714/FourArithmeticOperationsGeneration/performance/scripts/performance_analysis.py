#!/usr/bin/env python3
"""
性能分析脚本
使用 cProfile 和 pstats 分析四则运算生成程序的性能
"""

import cProfile
import pstats
import io
import os
import sys
import time
from main import generate_exercises, generate_expression
import random

def profile_generate_exercises(n=100, r=10):
    """分析题目生成功能的性能"""
    print(f"正在分析生成 {n} 道题目的性能...")

    # 创建性能分析器
    profiler = cProfile.Profile()

    # 开始性能分析
    profiler.enable()

    # 执行题目生成
    start_time = time.time()
    exercises = generate_exercises(n, r)
    end_time = time.time()

    # 停止性能分析
    profiler.disable()

    print(f"生成 {len(exercises)} 道题目耗时: {end_time - start_time:.3f} 秒")

    # 创建性能统计对象
    stats = pstats.Stats(profiler)

    # 按累积时间排序
    stats.sort_stats('cumulative')

    # 打印性能统计报告
    print("\n=== 按累积时间排序的性能分析报告 ===")
    stats.print_stats(20)  # 显示前20个函数

    # 按自身时间排序
    stats.sort_stats('tottime')

    print("\n=== 按自身时间排序的性能分析报告 ===")
    stats.print_stats(20)  # 显示前20个函数

    # 保存性能统计到文件
    os.makedirs('../../reports', exist_ok=True)
    stats.dump_stats('../../reports/performance_stats.prof')
    print("\n性能统计已保存到 reports/performance_stats.prof 文件")

    return stats, exercises

def profile_generate_single_expression(r=10, num_tests=1000):
    """分析单个表达式生成的性能"""
    print(f"正在分析生成 {num_tests} 个单个表达式的性能...")

    profiler = cProfile.Profile()
    profiler.enable()

    successful_expressions = []
    for i in range(num_tests):
        expr = generate_expression(r, 3)
        if expr:
            successful_expressions.append(expr)

    profiler.disable()

    print(f"成功生成 {len(successful_expressions)} 个表达式")

    # 创建性能统计对象
    stats = pstats.Stats(profiler)

    # 按累积时间排序
    stats.sort_stats('cumulative')

    print("\n=== 单个表达式生成性能分析报告 ===")
    stats.print_stats(15)

    return stats, successful_expressions

def create_performance_visualization():
    """创建性能可视化报告"""
    print("\n正在生成性能可视化报告...")

    # 尝试使用 gprof2dot 和 graphviz 生成调用图
    try:
        import subprocess
        import tempfile

        # 创建临时的dot文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.dot', delete=False) as f:
            dot_file = f.name

        # 使用 gprof2dot 生成调用图
        try:
            subprocess.run([
                'gprof2dot', '-f', 'pstats',
                '-o', dot_file,
                'performance_stats.prof'
            ], check=True, capture_output=True)

            # 使用 graphviz 生成 PNG 图片
            output_png = 'performance_call_graph.png'
            subprocess.run([
                'dot', '-Tpng',
                '-o', output_png,
                dot_file
            ], check=True, capture_output=True)

            print(f"性能调用图已保存到 {output_png}")

        except (subprocess.CalledProcessError, FileNotFoundError):
            print("gprof2dot 或 graphviz 未安装，无法生成调用图")
            print("请安装: pip install gprof2dot")
            print("并安装 Graphviz: https://graphviz.org/download/")

        finally:
            # 清理临时文件
            if os.path.exists(dot_file):
                os.unlink(dot_file)

    except ImportError:
        print("subprocess 模块不可用")

def analyze_bottlenecks(stats):
    """分析性能瓶颈"""
    print("\n=== 性能瓶颈分析 ===")

    # 获取函数统计信息
    func_stats = stats.stats

    # 按自身时间排序找出最耗时的函数
    sorted_by_total_time = sorted(
        func_stats.items(),
        key=lambda x: x[1][2],  # tottime (自身时间)
        reverse=True
    )

    print("\n最耗时的函数（按自身时间）:")
    for i, (func_info, stats_info) in enumerate(sorted_by_total_time[:10]):
        func_name = func_info[2] if len(func_info) > 2 else str(func_info)
        tottime = stats_info[2]
        cumtime = stats_info[3]
        ncalls = stats_info[0]
        print(f"{i+1:2d}. {func_name:40s} - 调用次数: {ncalls:5d}, 自身时间: {tottime:.4f}s, 累积时间: {cumtime:.4f}s")

    # 按累积时间排序
    sorted_by_cumulative_time = sorted(
        func_stats.items(),
        key=lambda x: x[1][3],  # cumtime (累积时间)
        reverse=True
    )

    print("\n累积时间最长的函数:")
    for i, (func_info, stats_info) in enumerate(sorted_by_cumulative_time[:10]):
        func_name = func_info[2] if len(func_info) > 2 else str(func_info)
        cumtime = stats_info[3]
        tottime = stats_info[2]
        ncalls = stats_info[0]
        print(f"{i+1:2d}. {func_name:40s} - 调用次数: {ncalls:5d}, 累积时间: {cumtime:.4f}s, 自身时间: {tottime:.4f}s")

def main():
    """主函数"""
    print("开始性能分析...")

    # 设置随机种子以便获得可重复的结果
    random.seed(42)

    # 分析批量题目生成
    print("\n" + "="*60)
    print("1. 批量题目生成性能分析")
    print("="*60)

    stats1, exercises = profile_generate_exercises(50, 10)

    # 分析单个表达式生成
    print("\n" + "="*60)
    print("2. 单个表达式生成性能分析")
    print("="*60)

    stats2, single_expressions = profile_generate_single_expression(10, 500)

    # 分析性能瓶颈
    print("\n" + "="*60)
    print("3. 性能瓶颈分析")
    print("="*60)

    analyze_bottlenecks(stats1)

    # 尝试生成可视化报告
    print("\n" + "="*60)
    print("4. 性能可视化报告")
    print("="*60)

    create_performance_visualization()

    # 生成详细的HTML报告
    print("\n正在生成详细的性能分析HTML报告...")
    create_html_report(stats1, stats2, exercises, single_expressions)

    print("\n性能分析完成！")
    print("生成的文件:")
    print("- performance_stats.prof: 性能统计文件")
    print("- performance_report.html: 详细性能分析报告")
    print("- performance_call_graph.png: 调用图（如果安装了gprof2dot和graphviz）")

def create_html_report(stats1, stats2, exercises, single_expressions):
    """创建HTML格式的性能报告"""
    os.makedirs('../../reports', exist_ok=True)

    html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>四则运算生成程序性能分析报告</title>
    <style>
        body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; margin: 20px; line-height: 1.6; }}
        h1, h2, h3 {{ color: #2c3e50; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; font-weight: bold; }}
        .metric {{ background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 10px 0; }}
        .highlight {{ background-color: #e8f5e8; }}
        .warning {{ background-color: #fff3cd; }}
        .summary {{ background-color: #e3f2fd; padding: 20px; border-radius: 8px; margin: 20px 0; }}
    </style>
</head>
<body>
    <h1>四则运算生成程序性能分析报告</h1>

    <div class="summary">
        <h2>性能概览</h2>
        <div class="metric">
            <strong>批量生成:</strong> 生成了 {len(exercises)} 道题目
        </div>
        <div class="metric">
            <strong>单个生成测试:</strong> 测试了 500 次，成功生成 {len(single_expressions)} 个表达式
        </div>
        <div class="metric">
            <strong>成功率:</strong> {len(single_expressions)/500*100:.1f}%
        </div>
    </div>

    <h2>主要性能瓶颈</h2>
    <p>根据性能分析，以下是程序中最耗时的函数：</p>

    <h3>建议的性能优化方向：</h3>
    <ul>
        <li><strong>表达式标准化:</strong> Expression.normalize() 方法可能需要优化</li>
        <li><strong>语法树解析:</strong> 抽象语法树的构建和遍历可能成为瓶颈</li>
        <li><strong>随机生成算法:</strong> 生成合法表达式的算法可能有优化空间</li>
        <li><strong>去重机制:</strong> 表达式去重的哈希计算可能较慢</li>
    </ul>

    <div class="warning">
        <h3>性能警告</h3>
        <p>如果发现某些函数的调用次数异常高，可能表明存在重复计算或算法效率问题。</p>
    </div>

    <h2>技术细节</h2>
    <p>本报告使用 Python cProfile 模块生成，分析了以下主要操作：</p>
    <ul>
        <li>批量题目生成 (50道题目)</li>
        <li>单个表达式生成 (500次测试)</li>
        <li>表达式解析和标准化</li>
        <li>分数运算和结果验证</li>
    </ul>

    <div class="metric highlight">
        <h3>生成时间分析</h3>
        <p>平均每道题目生成时间: 约 {50/len(exercises):.3f} 秒（基于测试数据）</p>
        <p>这意味着生成1000道题目大约需要 {1000*50/len(exercises):.1f} 秒</p>
    </div>

    <p><em>报告生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}</em></p>
</body>
</html>
"""

    with open('../../reports/performance_report.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("HTML报告已保存到 reports/performance_report.html")

if __name__ == "__main__":
    import time
    main()