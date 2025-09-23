# 论文查重系统 (Duplicate Checking System)

基于 Simhash 算法实现的论文查重系统，用于计算两个文本之间的相似度。

## 功能特性

- **Simhash 算法**: 使用局部敏感哈希 (LSH) 算法计算文本相似度
- **中文分词**: 基于 jieba 库的中文文本分词处理
- **停用词过滤**: 自动过滤常见中文停用词和单字符
- **汉明距离计算**: 通过计算两个文本 Simhash 值的汉明距离来判断相似度
- **命令行界面**: 简单易用的命令行接口

## 项目结构

```
DuplicateChecking/
├── main.py              # 主程序入口
├── src/
│   └── simhash_util.py # Simhash 核心实现
├── tests/
│   ├── test_similarity.py # 单元测试
│   ├── pytest.ini         # pytest 配置文件
│   └── run_tests.py       # 测试运行脚本
├── data/                # 测试数据文件
├── output/              # 输出结果目录
├── docs/                # 开发文档
├── .coveragerc          # 覆盖率配置文件
└── htmlcov/             # HTML 覆盖率报告目录
```

## 安装和使用

### 环境要求

- Python 3.7+
- jieba 库

### 安装依赖

```bash
pip install -r requirements.txt
```

### 使用方法

```bash
python main.py <原文文件路径> <抄袭文件路径> <输出文件路径>
```

**参数说明:**
- `原文文件路径`: 原始论文文件路径
- `抄袭文件路径`: 待检测的论文文件路径
- `输出文件路径`: 相似度结果输出路径

**示例:**

```bash
python main.py data/orig.txt data/orig_0.8_add.txt output/result.txt
```

### 输出结果

程序会在指定的输出文件中写入一个 0.00 到 1.00 之间的浮点数，表示两个文本的相似度：
- `1.00` 表示完全相同
- `0.00` 表示完全不同
- 数值越大表示相似度越高

## 算法原理

### Simhash 算法

1. **文本预处理**: 清理标点符号和特殊字符
2. **中文分词**: 使用 jieba 库进行中文分词
3. **停用词过滤**: 过滤常见停用词和单字符
4. **特征权重**: 统计词频作为特征权重
5. **哈希计算**: 将每个特征的哈希值加权叠加
6. **指纹生成**: 根据加权结果生成 64 位指纹

### 相似度计算

通过计算两个文本 Simhash 指纹的汉明距离来评估相似度：
```
相似度 = (64 - 汉明距离) / 64
```

## 单元测试

本项目使用 pytest 框架进行单元测试，提供了完整的测试覆盖。

### 测试框架
- **pytest**: 主要测试框架
- **pytest-cov**: 测试覆盖率工具
- **测试配置**: `tests/pytest.ini`
- **测试运行器**: `tests/run_tests.py`
- **覆盖率配置**: `.coveragerc`

### 测试用例

测试文件 `tests/test_similarity.py` 包含以下测试用例：

1. **`test_calculate_similarity`**: 测试基础相似度计算功能
2. **`test_identical_text`**: 测试相同文本的相似度（预期结果：1.0）
3. **`test_different_text`**: 测试不同文本的相似度
4. **`test_empty_text`**: 测试空文本的处理
5. **`test_short_text`**: 测试短文本的相似度计算
6. **`test_chinese_punctuation`**: 测试中文标点符号对相似度的影响

### 运行测试

```bash
# 运行所有测试
python -m pytest tests/

# 使用测试运行脚本
python tests/run_tests.py

# 运行单个测试文件
python -m pytest tests/test_similarity.py

# 运行单个测试方法
python -m pytest tests/test_similarity.py::TestSimhashSimilarity::test_identical_text

# 详细输出模式
python -m pytest tests/ -v

# 显示测试覆盖率
python -m pytest tests/ --cov=src

# 生成 HTML 覆盖率报告
python -m pytest tests/ --cov=src --cov-report=html

# 显示覆盖率明细（包含未覆盖行号）
python -m pytest tests/ --cov=src --cov-report=term-missing
```

### 测试配置

`tests/pytest.ini` 配置文件包含：
- 测试路径设置
- 测试文件命名规则
- 输出格式配置

`.coveragerc` 配置文件包含：
- 覆盖率源代码路径
- 忽略文件和目录配置
- 报告格式设置

### 预期结果

所有测试应该通过，确保：
- 相似度计算返回 0.0 到 1.0 之间的浮点数
- 相同文本的相似度为 1.0
- 不同文本的相似度合理
- 边界情况（空文本、短文本）正确处理

## 测试数据

项目包含多个测试文件用于验证系统准确性：
- `orig.txt`: 原始文本
- `orig_0.8_add.txt`: 添加内容的版本 (相似度约 0.8)
- `orig_0.8_del.txt`: 删除内容的版本 (相似度约 0.8)
- `orig_0.8_dis_X.txt`: 不同程度干扰的版本

## 开发日志

详细的开发过程记录请参考 `docs/开发日志.md`

## 技术栈

- **Python 3**: 主要开发语言
- **jieba**: 中文分词库
- **Simhash**: 局部敏感哈希算法
- **pytest**: 单元测试框架

## 许可证

本项目仅供学习和研究使用。