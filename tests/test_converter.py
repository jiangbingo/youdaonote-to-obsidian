"""
转换器测试
"""
import sys
from pathlib import Path

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from utils.converter import convert_html_to_markdown


def test_convert_paragraphs():
    """测试段落转换"""
    html = "<p>这是第一段</p><p>这是第二段</p>"
    result = convert_html_to_markdown(html)
    assert "这是第一段" in result
    assert "这是第二段" in result


def test_convert_headers():
    """测试标题转换"""
    html = "<h1>一级标题</h1><h2>二级标题</h2><h3>三级标题</h3>"
    result = convert_html_to_markdown(html)
    assert "# 一级标题" in result
    assert "## 二级标题" in result
    assert "### 三级标题" in result


def test_convert_formatting():
    """测试格式转换"""
    html = "<strong>粗体</strong>和<em>斜体</em>"
    result = convert_html_to_markdown(html)
    assert "**粗体**" in result
    assert "*斜体*" in result


def test_convert_images():
    """测试图片转换"""
    html = '<img src="http://example.com/image.png" alt="图片">'
    result = convert_html_to_markdown(html)
    assert "![](http://example.com/image.png)" in result


def test_convert_links():
    """测试链接转换"""
    html = '<a href="http://example.com">链接文本</a>'
    result = convert_html_to_markdown(html)
    assert "[链接文本](http://example.com)" in result


def test_convert_code():
    """测试代码转换"""
    html = "<code>inline code</code>"
    result = convert_html_to_markdown(html)
    assert "`inline code`" in result


def test_convert_code_block():
    """测试代码块转换"""
    html = "<pre>code block</pre>"
    result = convert_html_to_markdown(html)
    assert "```" in result
    assert "code block" in result


def test_html_entities():
    """测试 HTML 实体解码"""
    html = "&lt;tag&gt; &amp; &quot;quote&quot;"
    result = convert_html_to_markdown(html)
    assert "<tag>" in result
    assert "&" in result
    assert '"quote"' in result


if __name__ == "__main__":
    # 运行测试
    test_convert_paragraphs()
    test_convert_headers()
    test_convert_formatting()
    test_convert_images()
    test_convert_links()
    test_convert_code()
    test_convert_code_block()
    test_html_entities()
    print("所有测试通过!")
