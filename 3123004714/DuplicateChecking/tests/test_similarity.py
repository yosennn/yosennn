"""
相似度计算测试
"""

import pytest
from src.simhash_util import calculate_similarity

class TestSimhashSimilarity:
    """Simhash相似度计算测试类"""

    def test_calculate_similarity(self):
        """测试相似度计算"""
        text1 = "这是一个测试文本，用于测试相似度计算功能。"
        text2 = "这是一个测试文本，用于测试相似度计算。"
        result = calculate_similarity(text1, text2)
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0

    def test_identical_text(self):
        """测试相同文本的相似度"""
        text = "这是一个完全相同的文本。"
        result = calculate_similarity(text, text)
        assert result == 1.0

    def test_different_text(self):
        """测试完全不同文本的相似度"""
        text1 = "这是第一个文本内容。"
        text2 = "这是完全不同的第二个文本内容。"
        result = calculate_similarity(text1, text2)
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0

    def test_empty_text(self):
        """测试空文本的相似度"""
        text1 = ""
        text2 = "这是一个测试文本。"
        result = calculate_similarity(text1, text2)
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0

    def test_short_text(self):
        """测试短文本的相似度"""
        text1 = "测试"
        text2 = "测试"
        result = calculate_similarity(text1, text2)
        assert result == 1.0

    def test_chinese_punctuation(self):
        """测试中文标点符号的影响"""
        text1 = "这是一个测试文本。"
        text2 = "这是一个测试文本，用于测试。"
        result = calculate_similarity(text1, text2)
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0
