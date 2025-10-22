# 性能分析模块

这个模块提供了四则运算生成程序的性能分析工具和报告。

## 目录结构

```
performance/
├── README.md                 # 本文件
├── run_analysis.py           # 性能分析运行脚本
├── scripts/                 # 分析脚本目录
│   ├── performance_analysis.py      # 基础性能分析
│   ├── performance_visualization.py # 性能可视化
│   └── optimization_examples.py    # 优化建议和示例
└── reports/                 # 分析报告目录
    ├── performance_stats.prof      # cProfile统计数据
    ├── performance_report.html     # HTML格式报告
    ├── performance_analysis.png    # 性能分析图表
    └── bottleneck_analysis.md     # 瓶颈分析报告
```

## 使用方法

### 运行完整性能分析

```bash
# 从项目根目录运行
python performance/run_analysis.py run

# 或从performance目录运行
python run_analysis.py run
```

### 查看生成的报告文件

```bash
# 列出所有可用的报告文件
python performance/run_analysis.py list
```

### 单独运行分析脚本

```bash
# 运行基础性能分析
python performance/scripts/performance_analysis.py

# 生成性能可视化图表
python performance/scripts/performance_visualization.py
```

## 报告说明

### 性能分析报告 (performance_report.html)
- 包含性能概览和主要瓶颈分析
- 提供优化建议和技术细节
- 浏览器友好的交互式报告

### 瓶颈分析报告 (bottleneck_analysis.md)
- 详细的性能瓶颈分析
- 按时间排序的函数列表
- 具体的优化建议

### 性能分析图表 (performance_analysis.png)
- 可视化的性能数据图表
- 包含函数时间分布、调用次数统计
- 主要性能瓶颈的饼图展示

### 优化建议 (optimization_examples.py)
- 具体的代码优化示例
- 预编译正则表达式、缓存机制等
- 性能优化最佳实践

### 原始数据 (performance_stats.prof)
- cProfile原始统计数据
- 可用其他工具进一步分析
- 支持自定义分析脚本

## 主要性能瓶颈

根据分析结果，程序的主要性能消耗在：

1. **evaluate_postfix()** - 后缀表达式计算 (~36%)
2. **evaluate_expression()** - 表达式求值 (~65%)
3. **shunting_yard()** - 逆波兰式转换 (~17%)
4. **正则表达式操作** - 频繁的模式匹配和编译
5. **parse_number()** - 数字解析和Fraction创建

## 优化建议

### 立即可实施
- 预编译正则表达式模式
- 实现表达式计算结果缓存
- 减少函数调用开销

### 中期优化
- 使用更高效的解析算法
- 优化数据结构设计
- 内存管理优化

### 长期优化
- 并行处理大规模任务
- C扩展核心计算逻辑
- 编译优化 (Cython)

## 性能基准

- **50道题目**: 约0.011秒
- **1000道题目**: 约22秒
- **优化潜力**: 50-70%性能提升预期