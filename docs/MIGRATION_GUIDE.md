# 迁移详细指南

本文档提供从有道云笔记迁移到 Obsidian 的详细步骤。

## 目录

1. [准备工作](#准备工作)
2. [导出有道云笔记](#导出有道云笔记)
3. [配置迁移脚本](#配置迁移脚本)
4. [执行迁移](#执行迁移)
5. [迁移后整理](#迁移后整理)
6. [常见问题](#常见问题)

---

## 准备工作

### 系统要求

- Python 3.8 或更高版本
- 足够的磁盘空间（导出数据 + Obsidian vault）

### 安装 Python

```bash
# macOS (使用 Homebrew)
brew install python3

# Ubuntu/Debian
sudo apt install python3

# Windows
# 从 https://www.python.org/downloads/ 下载安装
```

### 验证安装

```bash
python3 --version
# Python 3.8.x 或更高
```

---

## 导出有道云笔记

### 方法一：官方客户端导出

1. 打开有道云笔记 PC 客户端
2. 选择笔记本或单个笔记
3. 右键 → 导出
4. 选择 Markdown 格式
5. 保存到本地

### 方法二：使用第三方工具

推荐使用 [youdaonote-pull](https://github.com/DeppWang/youdaonote-pull)：

```bash
pip install youdaonote-pull
youdaonote-pull
```

### 导出目录结构

导出后的目录结构通常如下：

```
youdaonote-export/
├── 笔记本1/
│   ├── 笔记1.md
│   ├── 笔记2.note
│   └── images/
│       └── image1.png
├── 笔记本2/
│   └── ...
└── 我的资源/
    └── ...
```

---

## 配置迁移脚本

### 1. 下载脚本

```bash
git clone https://github.com/jiangbingo/youdaonote-to-obsidian.git
cd youdaonote-to-obsidian
```

### 2. 修改配置

编辑 `scripts/config.py`：

```python
# 目录映射 - 根据你的 Obsidian 结构修改
DIRECTORY_MAPPING = {
    "你的有道云目录名": "Obsidian目标目录",

    # 示例
    "工作笔记": "6 工作",
    "学习资料": "5 职业技能",
    "生活记录": "3 生活",

    # 默认分类
    "_default": "Inbox",
}
```

### 3. PARA 结构参考

| 有道云分类 | Obsidian PARA |
|-----------|---------------|
| 项目相关 | 1 Projects |
| 持续领域 | 2 Areas |
| 资源收藏 | 3 Resources |
| 已完成 | 4 Archives |

---

## 执行迁移

### 步骤 1: 预览模式

先运行预览模式，检查配置是否正确：

```bash
python3 scripts/migrate.py \
    --source ~/Downloads/youdaonote-export \
    --target ~/Documents/my-obsidian-vault \
    --dry-run
```

### 步骤 2: 备份

迁移前备份 Obsidian vault：

```bash
cp -r ~/Documents/my-obsidian-vault ~/Documents/my-obsidian-vault-backup
```

### 步骤 3: 正式迁移

```bash
python3 scripts/migrate.py \
    --source ~/Downloads/youdaonote-export \
    --target ~/Documents/my-obsidian-vault
```

### 步骤 4: 查看报告

迁移完成后，查看生成的报告：

```bash
cat ~/Documents/my-obsidian-vault/migration_report.md
```

---

## 迁移后整理

### 1. 审核短文件

在 Obsidian 中搜索：
```
tag:#待审核
```

检查内容不完整的笔记，决定保留或删除。

### 2. 检查转换文件

搜索：
```
tag:#note转换
```

检查 HTML 转换的笔记，修复格式问题。

### 3. 验证图片

检查图片是否正常显示，如有问题：
1. 确认图片在 `images/` 目录
2. 检查 Markdown 中的图片路径

### 4. 调整分类

根据需要重新组织文件：
1. 在 Obsidian 文件浏览器中拖拽
2. 或使用脚本批量移动

### 5. 添加标签

为迁移的笔记添加主题标签：
```markdown
---
tags:
  - 有道云导入
  - Python  # 添加主题标签
  - 教程
---
```

---

## 常见问题

### 图片无法显示

**原因**：图片链接路径不正确

**解决**：
1. 确认图片在 `images/` 目录
2. Markdown 中使用相对路径：`![](../images/xxx.png)`

### Note 文件转换乱码

**原因**：.note 文件格式复杂，正则转换不完全

**解决**：
1. 搜索 `#note转换` 找到问题文件
2. 手动编辑修复格式

### 重复文件问题

**原因**：有道云中存在相同内容的不同笔记

**解决**：
1. 迁移脚本自动删除 MD5 相同的文件
2. 检查日志确认删除的文件

### 目录映射不生效

**原因**：目录名称不匹配

**解决**：
1. 检查 `DIRECTORY_MAPPING` 中的键名
2. 确保与有道云导出的目录名完全一致

---

## 高级用法

### 使用环境变量

```bash
export YOUDAO_SOURCE_DIR=~/Downloads/youdaonote-export
export OBSIDIAN_VAULT_DIR=~/Documents/my-vault
python3 scripts/migrate.py
```

### 只迁移特定目录

修改 `scripts/migrate.py`，在 `migrate_markdown_files` 中添加过滤：

```python
for md_file in self.source.rglob("*.md"):
    # 只迁移特定目录
    if "工作笔记" not in str(md_file):
        continue
    # ...
```

### 自定义 Frontmatter

修改 `scripts/utils/frontmatter.py` 中的 `add_frontmatter` 函数。

---

## 联系支持

如有问题，请提交 [GitHub Issue](https://github.com/jiangbingo/youdaonote-to-obsidian/issues)。
