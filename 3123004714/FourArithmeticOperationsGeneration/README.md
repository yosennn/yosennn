# 小学四则运算题目生成程序

一个用于生成小学四则运算练习题的Python程序，支持自然数、真分数和带分数的运算，并提供自动批改功能。

## 安装要求

- Python 3.13+
- pytest (用于测试，可选)

```bash
# 安装依赖
pip install pytest

# 或安装完整依赖（包括覆盖率工具）
pip install pytest pytest-cov
```

## 快速开始

### 生成练习题

```bash
# 生成10道题目，数值范围1-10
python main.py -n 10 -r 10

# 生成1000道题目，数值范围1-100
python main.py -n 1000 -r 100
```

### 批改练习题

```bash
# 批改练习题
python main.py -e Exercises.txt -a Answers.txt

# 查看批改结果
cat Grade.txt
```

## 程序规则

### 数值范围
- 通过 `-r` 参数指定数值范围上限
- 生成的数字在 `[0, r-1]` 范围内
- 分数分母在 `[2, r-1]` 范围内

### 运算规则
- **运算符限制**：每题最多3个运算符
- **减法规则**：确保结果非负（被减数 ≥ 减数）
- **除法规则**：结果为真分数（不是整数且大于0）
- **括号规则**：30%概率随机添加括号

### 去重机制
- 基于语法树标准化算法
- 处理加法、乘法交换律（如 `1+2` 和 `2+1` 视为重复）
- 确保生成的题目唯一性

## 输出文件

程序运行后会生成以下文件：

### Exercises.txt
练习题文件，每行一道题目：
```
1/2 + 2/3 × 3/4 =
(1 + 2) × 3 - 1 =
1'1/2 × 2 + 1/3 =
...
```

### Answers.txt
答案文件，每行对应一道题目的答案：
```
1
8
10/3
...
```

### Grade.txt
批改结果文件（仅在使用批改功能时生成）：
```
Correct: 7 (1, 2, 3, 5, 6, 8, 9)
Wrong: 3 (4, 7, 10)
```

## 使用示例

### 基础使用
```bash
# 生成50道题目，数值范围1-20
python main.py -n 50 -r 20

# 批改练习题
python main.py -e Exercises.txt -a Answers.txt
```

### 高级使用
```bash
# 大规模生成（性能测试）
python main.py -n 10000 -r 100

# 边界测试
python main.py -n 10 -r 1
```

## 错误处理

程序包含完善的错误处理机制：

- **参数错误**：检查命令行参数有效性
- **数值范围**：确保 `-r` 参数为自然数（≥1）
- **运算异常**：处理除零、负数等异常情况
- **文件操作**：处理文件读写错误

## 技术架构

### 核心模块

1. **主程序模块** (`main.py`)
   - 表达式生成引擎
   - 逆波兰式计算引擎
   - 批改系统
   - 命令行接口

2. **表达式模块** (`src/Expression.py`)
   - 表达式类定义
   - 语法树解析和标准化
   - 去重算法实现

3. **测试套件** (`tests/`)
   - 200+ 测试用例
   - 完整的功能覆盖
   - 性能测试验证

### 核心算法

- **调度场算法**：中缀表达式转后缀表达式
- **语法树标准化**：处理交换律去重
- **分数精确计算**：使用 Python Fraction 类

## 开发和测试

### 运行测试
```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_expression.py

# 生成覆盖率报告
pytest --cov=main --cov=src --cov-report=term-missing

# 运行性能测试
pytest -m slow
```

### 测试覆盖
- 单元测试：覆盖所有核心函数
- 集成测试：验证完整工作流
- 性能测试：确保大规模数据处理能力
- 边界测试：验证极端情况处理

## 性能分析

### 性能概况
- **生成速度**: 1000道题目约需22秒
- **成功率**: 表达式生成成功率约92%
- **内存使用**: 优化的分数计算和表达式存储

### 主要性能瓶颈
根据cProfile分析结果，主要性能消耗在：

1. **evaluate_postfix()** - 后缀表达式计算 (35.9% 累积时间)
2. **evaluate_expression()** - 表达式求值 (65.2% 累积时间)
3. **shunting_yard()** - 逆波兰式转换 (16.5% 累积时间)
4. **正则表达式操作** - 频繁的模式匹配和编译
5. **parse_number()** - 数字解析和Fraction创建

### 性能分析工具
```bash
# 运行完整性能分析
python performance/run_analysis.py run

# 查看生成的报告文件
python performance/run_analysis.py list

# 单独运行分析脚本
python performance/scripts/performance_analysis.py
python performance/scripts/performance_visualization.py
```

### 优化建议
- 预编译正则表达式模式
- 实现表达式计算结果缓存
- 优化Fraction对象创建和重用
- 考虑并行处理大规模生成任务

## 项目结构

```
FourArithmeticOperationsGeneration/
├── main.py                      # 主程序文件
├── src/                         # 源代码目录
│   ├── __init__.py             # 源代码包初始化
│   └── Expression.py           # 表达式类定义
├── tests/                      # 测试目录
│   ├── __init__.py             # 测试包初始化
│   ├── conftest.py             # pytest配置
│   ├── test_expression.py      # Expression类测试
│   ├── test_number_utils.py    # 数字工具测试
│   ├── test_expression_generation.py  # 表达式生成测试
│   ├── test_expression_evaluation.py  # 表达式计算测试
│   ├── test_deduplication.py   # 去重机制测试
│   ├── test_grading.py         # 批改系统测试
│   ├── test_integration.py     # 集成测试
│   └── test_run_all.py         # 测试运行脚本
├── performance/                # 性能分析目录
│   ├── README.md               # 性能分析模块说明
│   ├── run_analysis.py         # 性能分析运行脚本
│   ├── scripts/                # 分析脚本目录
│   │   ├── performance_analysis.py      # 基础性能分析
│   │   ├── performance_visualization.py # 性能可视化
│   │   └── optimization_examples.py    # 优化建议和示例
│   └── reports/                # 分析报告目录
│       ├── performance_stats.prof      # cProfile统计数据
│       ├── performance_report.html     # HTML格式报告
│       ├── performance_analysis.png    # 性能分析图表
│       └── bottleneck_analysis.md     # 瓶颈分析报告
├── docs/                       # 文档目录
│   └── 程序设计与实现文档.md     # 详细设计文档
├── pyproject.toml              # 项目配置
├── README.md                   # 项目说明
└── CLAUDE.md                   # Claude Code指导文件
```

## 生成的分析文件

运行性能分析后会在 `performance/reports/` 目录下生成以下文件：
- `performance_stats.prof` - cProfile性能统计文件
- `performance_report.html` - 详细性能分析报告（HTML格式）
- `performance_analysis.png` - 性能分析可视化图表
- `bottleneck_analysis.md` - 性能瓶颈分析报告（Markdown格式）
- `optimization_examples.py` - 优化建议和代码示例（在scripts目录）

