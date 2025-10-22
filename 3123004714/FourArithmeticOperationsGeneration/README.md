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

## 项目结构

```
FourArithmeticOperationsGeneration/
├── main.py                    # 主程序文件
├── src/
│   ├── __init__.py           # 源代码包初始化
│   └── Expression.py         # 表达式类定义
├── tests/
│   ├── __init__.py           # 测试包初始化
│   ├── conftest.py           # pytest配置
│   ├── test_expression.py    # Expression类测试
│   ├── test_number_utils.py  # 数字工具测试
│   ├── test_expression_generation.py  # 表达式生成测试
│   ├── test_expression_evaluation.py  # 表达式计算测试
│   ├── test_deduplication.py # 去重机制测试
│   ├── test_grading.py       # 批改系统测试
│   ├── test_integration.py   # 集成测试
│   └── test_run_all.py       # 测试运行脚本
├── docs/
│   └── 程序设计与实现文档.md   # 详细设计文档
├── pyproject.toml            # 项目配置
├── README.md                 # 项目说明
```

