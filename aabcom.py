import hashlib
import os
import shutil
import zipfile
import numpy as np


def extract_aab(aab_file, extract_dir):
    """
    解压aab文件到指定目录
    :param aab_file: aab文件路径
    :param extract_dir: 解压目录
    """
    with zipfile.ZipFile(aab_file, 'r') as z:
        print(extract_dir)
        z.extractall(extract_dir)


def get_aab_feature(aab_dir):
    """
    提取aab文件的特征
    :param aab_dir: aab文件解压后的目录
    :return: 特征向量
    """
    feature = []
    print(aab_dir)
    for root, dirs, files in os.walk(aab_dir):
        for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    # 读取文件的前16个字节作为特征
                    feature.append(f.read(16))
    if feature:
        feature = np.vstack(feature)
        print(feature)
    else:
        feature = np.zeros((0,), dtype=np.uint8)
    return feature



def compare_aab_features(feature1, feature2):
    """
    比较两个aab文件的特征
    :param feature1: 第一个aab文件的特征向量
    :param feature2: 第二个aab文件的特征向量
    :return: 相似度分数，范围在0到1之间
    """
    # 计算两个特征向量的哈希值
    hash1 = hash(feature1.tobytes())
    hash2 = hash(feature2.tobytes())
    print("hash1: ", hash1)
    print("hash2: ", hash2)

    # 比较两个哈希值的汉明距离，返回相似度分数
    hamming_distance = bin(hash1 ^ hash2).count('1')
    print("hamming distance: ", hamming_distance)
    similarity = 1 - hamming_distance / max(feature1.size * 8, feature2.size * 8)
    return similarity


def compare_aab_files(aab_file_path1, aab_file_path2):
    """
    比较两个aab文件的相似度
    :param aab_file_path1: 第一个aab文件路径
    :param aab_file_path2: 第二个aab文件路径
    :return: 相似度分数，范围在0到1之间
    """
    try:
        # 解压第一个aab文件到临时目录
        aab_dir1 = 'tmp1'
        extract_aab(aab_file_path1, aab_dir1)
        feature1 = get_aab_feature(aab_dir1)
        shutil.rmtree(aab_dir1)

        # 解压第二个aab文件到临时目录
        aab_dir2 = 'tmp2'
        extract_aab(aab_file_path2, aab_dir2)
        feature2 = get_aab_feature(aab_dir2)
        shutil.rmtree(aab_dir2)

        # 比较两个aab文件的特征
        similarity = compare_aab_features(feature1, feature2)
        return similarity

    except (IOError, zipfile.BadZipFile, KeyError) as e:
        # 处理文件读写异常、文件格式错误等异常情况
        print(f"Error: {str(e)}")

if __name__ == '__main__':
        print(compare_aab_files("a.aab","b.aab"))
