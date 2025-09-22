"""
SimHash算法测试
"""

import unittest
from src.simhash import SimHash

class TestSimHash(unittest.TestCase):
    """SimHash测试类"""

    def setUp(self):
        self.simhash = SimHash()

    def test_compute(self):
        """测试SimHash计算"""
        result = self.simhash.compute("test text")
        self.assertIsInstance(result, int)

if __name__ == "__main__":
    unittest.main()