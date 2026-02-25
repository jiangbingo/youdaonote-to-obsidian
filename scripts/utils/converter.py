"""
HTML 到 Markdown 转换器
"""
import re
import html
from pathlib import Path
from typing import Optional


def convert_html_to_markdown(html_content: str) -> str:
    """
    将 HTML 内容转换为 Markdown 格式

    Args:
        html_content: HTML 格式的内容

    Returns:
        转换后的 Markdown 内容
    """
    # 解码 HTML 实体
    text = html.unescape(html_content)

    # 移除 style 标签
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)

    # 转换常见标签
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'<p[^>]*>', '\n\n', text)
    text = re.sub(r'</p>', '', text)
    text = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', text, flags=re.DOTALL)
    text = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', text, flags=re.DOTALL)
    text = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1', text, flags=re.DOTALL)
    text = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1', text, flags=re.DOTALL)
    text = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1', text, flags=re.DOTALL)
    text = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', text, flags=re.DOTALL)
    text = re.sub(r'<pre[^>]*>(.*?)</pre>', r'```\n\1\n```', text, flags=re.DOTALL)

    # 处理图片
    text = re.sub(r'<img[^>]*src=["\']([^"\']+)["\'][^>]*>', r'![](\1)', text)

    # 处理链接
    text = re.sub(r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', r'[\2](\1)', text, flags=re.DOTALL)

    # 移除其他标签
    text = re.sub(r'<[^>]+>', '', text)

    # 清理多余空白
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()

    return text


def convert_note_to_md(note_path: Path) -> Optional[str]:
    """
    将 .note 文件转换为 Markdown

    Args:
        note_path: .note 文件路径

    Returns:
        转换后的 Markdown 内容，失败返回 None
    """
    try:
        with open(note_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查是否是 HTML 格式
        if '<div' in content or '<p' in content:
            markdown = convert_html_to_markdown(content)
        else:
            # 已经是纯文本
            markdown = content

        return markdown
    except Exception as e:
        print(f"转换失败 {note_path.name}: {e}")
        return None
