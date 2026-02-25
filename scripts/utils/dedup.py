"""
文件去重工具
"""
import hashlib
from pathlib import Path
from typing import Dict, List
from collections import defaultdict


def get_file_hash(filepath: Path) -> str:
    """
    计算文件的 MD5 哈希值

    Args:
        filepath: 文件路径

    Returns:
        MD5 哈希字符串
    """
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception:
        return None


def find_duplicates(directory: Path, extensions: List[str] = None) -> Dict[str, List[Path]]:
    """
    查找目录中的重复文件

    Args:
        directory: 要扫描的目录
        extensions: 要检查的文件扩展名列表，如 ['.md', '.txt']

    Returns:
        字典，键为哈希值，值为具有相同哈希的文件路径列表
    """
    if extensions is None:
        extensions = ['.md', '.txt', '.note']

    hash_map = defaultdict(list)

    for ext in extensions:
        for file_path in directory.rglob(f'*{ext}'):
            file_hash = get_file_hash(file_path)
            if file_hash:
                hash_map[file_hash].append(file_path)

    # 只返回有重复的
    return {h: files for h, files in hash_map.items() if len(files) > 1}


def remove_duplicates(directory: Path, keep: str = 'first', dry_run: bool = False) -> int:
    """
    删除重复文件

    Args:
        directory: 要处理的目录
        keep: 保留策略 - 'first' 保留第一个，'newest' 保留最新的
        dry_run: 是否只预览不实际删除

    Returns:
        删除的文件数量
    """
    duplicates = find_duplicates(directory)
    removed_count = 0

    for file_hash, files in duplicates.items():
        if keep == 'newest':
            # 按修改时间排序，保留最新的
            files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

        # 保留第一个，删除其余
        for file_to_remove in files[1:]:
            if dry_run:
                print(f"[预览] 将删除: {file_to_remove}")
            else:
                try:
                    file_to_remove.unlink()
                    print(f"已删除: {file_to_remove}")
                except Exception as e:
                    print(f"删除失败: {file_to_remove}: {e}")
                    continue
            removed_count += 1

    return removed_count
