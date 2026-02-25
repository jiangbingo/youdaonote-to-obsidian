"""
Obsidian Frontmatter 生成工具
"""
import re
from pathlib import Path
from datetime import datetime
from typing import List, Optional


def extract_title(content: str, filename: str) -> str:
    """
    从内容或文件名提取标题

    Args:
        content: 文件内容
        filename: 文件名

    Returns:
        提取的标题（最多100字符）
    """
    # 尝试从第一个标题提取
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()[:100]
    return Path(filename).stem[:100]


def extract_date_from_filename(filename: str) -> str:
    """
    从文件名提取日期

    Args:
        filename: 文件名

    Returns:
        日期字符串 (YYYY-MM-DD)
    """
    patterns = [
        r'(\d{4}[-_]\d{2}[-_]\d{2})',
        r'(\d{4}\d{2}\d{2})',
    ]

    for pattern in patterns:
        match = re.search(pattern, str(filename))
        if match:
            date_str = match.group(1)
            date_str = date_str.replace('_', '-')
            try:
                return datetime.strptime(date_str[:10], '%Y-%m-%d').strftime('%Y-%m-%d')
            except ValueError:
                continue

    return datetime.now().strftime('%Y-%m-%d')


def add_frontmatter(
    content: str,
    filepath: Path,
    tags: List[str] = None,
    is_converted: bool = False,
    is_short: bool = False,
    source: str = "有道云笔记",
    image_path_prefix: str = "../images/"
) -> str:
    """
    为内容添加 Obsidian frontmatter

    Args:
        content: 原始内容
        filepath: 文件路径
        tags: 额外的标签列表
        is_converted: 是否是从 .note 转换的
        is_short: 是否是短文件
        source: 来源标识
        image_path_prefix: 图片路径前缀

    Returns:
        添加了 frontmatter 的内容
    """
    # 检查是否已有 frontmatter
    if content.startswith('---\n'):
        return content

    title = extract_title(content, filepath.name)
    date = extract_date_from_filename(filepath.name)

    # 构建标签
    all_tags = ["有道云导入"]
    if tags:
        all_tags.extend(tags)
    if is_converted:
        all_tags.append("note转换")
    if is_short:
        all_tags.append("待审核")

    # 生成 frontmatter
    frontmatter = f"""---
title: "{title}"
created: {date}
tags:
{chr(10).join(f'  - {t}' for t in all_tags)}
source: {source}
---

"""

    # 修复图片链接
    content = re.sub(r'!\[([^\]]*)\]\(images/', f'![\\1]({image_path_prefix}', content)

    return frontmatter + content
