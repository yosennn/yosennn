#!/usr/bin/env python3
import sys
import logging
from pathlib import Path
from src.simhash_util import calculate_similarity

def validate_args(args):
    """验证命令行参数"""
    if len(args) != 4:
        raise ValueError("需要3个参数：原文的文件路径 抄袭文的文件路径 输出路径")

    orig_path = Path(args[1])
    copy_path = Path(args[2])
    output_path = Path(args[3])

    # 检查路径是否为有效地址（相对或绝对）
    for path, name in [(orig_path, "原文路径"), (copy_path, "抄袭文件路径"), (output_path, "输出路径")]:
        # 检查路径字符串是否有效（非空且不是纯分隔符）
        if not str(path).strip() or str(path).strip() in ['/', '\\']:
            raise ValueError(f"{name}不是有效地址：{path}")
        # 检查路径格式是否有效
        try:
            path.resolve()  # 尝试解析路径
        except Exception:
            raise ValueError(f"{name}不是有效地址：{path}")


    return orig_path, copy_path, output_path

def main():
    try:
        orig_path, copy_path, output_path = validate_args(sys.argv)

        # 读取文件内容
        with open(orig_path, 'r', encoding='utf-8') as f:
            text1 = f.read()
        with open(copy_path, 'r', encoding='utf-8') as f:
            text2 = f.read()

        # 计算相似度
        similarity = calculate_similarity(text1, text2)

        # 写入结果
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"{similarity:.2f}")

        print(f"查重完成，相似度：{similarity:.2f}，结果已写入 {output_path}")

    except Exception as e:
        logging.error(f"程序错误：{e}")
        sys.exit(1)

if __name__ == '__main__':
    main()