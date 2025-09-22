"""
相似度计算测试
"""

import unittest
from src.simhash_util import calculate_similarity

class TestSimhashSimilarity(unittest.TestCase):
    """Simhash相似度计算测试类"""

    def test_calculate_similarity(self):
        """测试相似度计算"""
        text1 = "这是一个测试文本，用于测试相似度计算功能。"
        text2 = "这是一个测试文本，用于测试相似度计算。"
        result = calculate_similarity(text1, text2)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_identical_text(self):
        """测试相同文本的相似度"""
        text = "这是一个完全相同的文本。"
        result = calculate_similarity(text, text)
        self.assertEqual(result, 1.0)

    def test_different_text(self):
        """测试完全不同文本的相似度"""
        text1 = "这是第一个文本内容。"
        text2 = "这是完全不同的第二个文本内容。"
        result = calculate_similarity(text1, text2)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

if __name__ == "__main__":
    unittest.main()