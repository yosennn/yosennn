#!/usr/bin/env python3
"""
基于 Simhash 的重复检查工具模块
"""
import jieba
import re
from typing import List, Tuple
from collections import Counter

# 中文 stopwords
STOP_WORDS = {
    '的', '了', '是', '我', '你', '他', '她', '它', '们', '在', '有', '和', '就', '不', '人', '都', '一', '个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '那', '里', '就是', '还是', '这', '这个', '那个', '什么', '怎么', '为什么', '因为', '所以', '如果', '但是', '可是', '然而', '而且', '并且', '或者', '吗', '呢', '吧', '啊', '啦', '呀', '哦', '唉', '嘿', '哼', '喂', '嗯', '哦', '噢', '呵', '喔', '哟', '呜', '哗', '啪', '咚', '滴', '哒', '叮', '当', '哗啦', '咕咚', '滴答', '叮当', '啪嗒', '呼呼', '沙沙', '淅淅', '沥沥', '哗哗', '咚咚', '嘀嗒', '叮咚', '砰砰', '轰轰', '隆隆', '滴滴', '嘟嘟', '铃铃', '嗒嗒', '啪啪', '咣咣', '哐哐', '铛铛', '梆梆', '当当', '锵锵', '咚咚', '哐哐', '铛铛', '梆梆', '当当', '锵锵', '咚咚', '哐哐', '铛铛', '梆梆', '当当', '锵锵'
}


def _tokenize(text: str) -> List[Tuple[str, int]]:
    """
    对文本进行分词并返回带权重的特征

    Args:
        text: 原始文本字符串

    Returns:
        (特征, 权重)元组的列表
    """
    # 清理文本：移除标点符号和特殊字符
    text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    # 使用 jieba 进行中文分词
    words = jieba.lcut(text)

    # 过滤停用词和单个字符
    filtered_words = []
    for word in words:
        if (len(word) > 1 and word not in STOP_WORDS and
                not word.isdigit() and word.strip()):
            filtered_words.append(word)

    # 统计词频作为权重
    word_counts = Counter(filtered_words)

    # 返回 (单词, 权重) 元组的列表
    return list(word_counts.items())


class Simhash:
    """Simhash 计算类"""

    def __init__(self, features: List[Tuple[str, int]]):
        """
        使用特征初始化 Simhash

        Args:
            features: (特征, 权重)元组的列表
        """
        self.features = features
        self.hash_value = None

    def build(self) -> int:
        """
        从特征构建 Simhash 指纹

        Returns:
            64位整数指纹
        """
        # 初始化64维向量
        v = [0] * 64

        for feature, weight in self.features:
            # 将特征哈希为64位整数
            feature_hash = hash(feature)

            # 确保是64位无符号整数
            feature_hash = feature_hash & ((1 << 64) - 1)

            # 根据哈希位更新向量
            for i in range(64):
                if (feature_hash >> i) & 1:
                    v[i] += weight
                else:
                    v[i] -= weight

        # 构建最终指纹
        fingerprint = 0
        for i in range(64):
            if v[i] > 0:
                fingerprint |= (1 << i)

        self.hash_value = fingerprint
        return fingerprint


def hamming_distance(hash1: int, hash2: int) -> int:
    """
    计算两个哈希值之间的汉明距离

    Args:
        hash1: 第一个哈希值
        hash2: 第二个哈希值

    Returns:
        不同位的数量
    """
    xor_result = hash1 ^ hash2
    return bin(xor_result).count('1')


def calculate_similarity(text1: str, text2: str) -> float:
    """
    使用 Simhash 计算两个文本之间的相似度

    Args:
        text1: 第一个文本
        text2: 第二个文本

    Returns:
        0.0 到 1.0 之间的相似度分数
    """
    # 对两个文本进行分词
    features1 = _tokenize(text1)
    features2 = _tokenize(text2)

    # 构建 Simhash 指纹
    hash1 = Simhash(features1).build()
    hash2 = Simhash(features2).build()

    # 计算汉明距离
    distance = hamming_distance(hash1, hash2)

    # 转换为相似度分数
    similarity = (64 - distance) / 64

    return similarity