#!/usr/bin/env python3
"""
Simhash-based duplicate checking utility module
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
    Tokenize text and return features with weights

    Args:
        text: Raw text string

    Returns:
        List of (feature, weight) tuples
    """
    # Clean text: remove punctuation and special characters
    text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    # Use jieba for Chinese word segmentation
    words = jieba.lcut(text)

    # Filter out stopwords and single characters
    filtered_words = []
    for word in words:
        if (len(word) > 1 and
            word not in STOP_WORDS and
            not word.isdigit() and
            word.strip()):
            filtered_words.append(word)

    # Count word frequencies as weights
    word_counts = Counter(filtered_words)

    # Return list of (word, weight) tuples
    return list(word_counts.items())

class Simhash:
    """Simhash calculation class"""

    def __init__(self, features: List[Tuple[str, int]]):
        """
        Initialize Simhash with features

        Args:
            features: List of (feature, weight) tuples
        """
        self.features = features
        self.hash_value = None

    def build(self) -> int:
        """
        Build Simhash fingerprint from features

        Returns:
            64-bit integer fingerprint
        """
        # Initialize 64-dimensional vector
        v = [0] * 64

        for feature, weight in self.features:
            # Hash feature to 64-bit integer
            feature_hash = hash(feature)

            # Ensure it's a 64-bit unsigned integer
            feature_hash = feature_hash & ((1 << 64) - 1)

            # Update vector based on hash bits
            for i in range(64):
                if (feature_hash >> i) & 1:
                    v[i] += weight
                else:
                    v[i] -= weight

        # Build final fingerprint
        fingerprint = 0
        for i in range(64):
            if v[i] > 0:
                fingerprint |= (1 << i)

        self.hash_value = fingerprint
        return fingerprint

def hamming_distance(hash1: int, hash2: int) -> int:
    """
    Calculate Hamming distance between two hashes

    Args:
        hash1: First hash value
        hash2: Second hash value

    Returns:
        Number of differing bits
    """
    xor_result = hash1 ^ hash2
    return bin(xor_result).count('1')

def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate similarity between two texts using Simhash

    Args:
        text1: First text
        text2: Second text

    Returns:
        Similarity score between 0.0 and 1.0
    """
    # Tokenize both texts
    features1 = _tokenize(text1)
    features2 = _tokenize(text2)

    # Build Simhash fingerprints
    hash1 = Simhash(features1).build()
    hash2 = Simhash(features2).build()

    # Calculate Hamming distance
    distance = hamming_distance(hash1, hash2)

    # Convert to similarity score
    similarity = (64 - distance) / 64

    return similarity