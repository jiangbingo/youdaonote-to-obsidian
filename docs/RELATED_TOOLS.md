# 其他笔记迁移方案

本文档整理了常见笔记应用迁移到 Obsidian 的方案。

## Obsidian Importer 插件（官方推荐）

**项目地址**: [obsidian-importer](https://github.com/obsidianmd/obsidian-importer)

这是 Obsidian 官方支持的社区插件，支持多种笔记应用的导入。

### 支持的来源

| 笔记应用 | 支持格式 | 说明 |
|----------|----------|------|
| **OneNote** | `.mht` / `.html` | 微软笔记应用 |
| **Evernote** | `.enex` | 经典笔记应用 |
| **Notion** | 导出文件 | 现代协作工具 |
| **Apple Notes** | 原生导出 | macOS/iOS 笔记 |
| **Google Keep** | Takeout 导出 | Google 笔记服务 |
| **Bear** | `.bear2bk` | Markdown 笔记应用 |
| **Roam Research** | JSON/Markdown | 双向链接笔记 |
| **HTML files** | `.html` | 通用格式 |

### 安装方法

```
Obsidian → 设置 → 社区插件 → 浏览 → 搜索 "Importer" → 安装并启用
```

---

## 各平台迁移指南

### OneNote → Obsidian

#### 方法一：使用 Obsidian Importer（推荐）

1. **导出 OneNote**
   - 打开 OneNote 桌面版
   - 文件 → 导出 → 页面/分区/笔记本
   - 选择格式：`.mht` 或 `.html`

2. **导入到 Obsidian**
   - 点击左侧边栏导入图标
   - 选择 OneNote 导出的文件
   - 设置输出文件夹
   - 点击 Import

#### 方法二：使用 OneNoteExporter

```bash
npx onenote-exporter --format markdown --output ./onenote-export
```

#### 参考文章

- [OneNote笔记迁移至Obsidian完全指南](https://m.blog.csdn.net/gitblog_00977/article/details/157538215)
- [Obsidian Importer插件OneNote导入完整指南](https://m.blog.csdn.net/gitblog_00318/article/details/156500830)

---

### Evernote → Obsidian

使用 Obsidian Importer 插件：

1. 在 Evernote 中导出为 `.enex` 格式
2. 在 Obsidian Importer 中选择 Evernote 导入
3. 选择 `.enex` 文件执行导入

---

### Notion → Obsidian

使用 Obsidian Importer 插件：

1. 在 Notion 中导出工作区（Settings → Export）
2. 选择 Markdown & CSV 格式
3. 在 Obsidian Importer 中选择 Notion 导入

---

### 有道云笔记 → Obsidian

**使用本项目**（youdaonote-to-obsidian）：

```bash
# 克隆项目
git clone https://github.com/jiangbingo/youdaonote-to-obsidian.git

# 执行迁移
make run SOURCE=/path/to/youdao-export TARGET=/path/to/obsidian-vault
```

**为什么需要本项目？**

- 有道云笔记没有官方 Obsidian 导入支持
- 导出格式（`.note`）需要特殊转换
- 目录结构需要智能映射

---

## 其他有用工具

### Pandoc - 通用文档转换

```bash
# Word 转 Markdown
pandoc input.docx -o output.md --extract-media=./images

# HTML 转 Markdown
pandoc input.html -o output.md
```

### 你需要哪个工具？

| 你的来源 | 推荐方案 |
|----------|----------|
| 有道云笔记 | **本项目** |
| OneNote | Obsidian Importer 插件 |
| Evernote | Obsidian Importer 插件 |
| Notion | Obsidian Importer 插件 |
| 其他 | 尝试 Obsidian Importer 或 Pandoc |

---

## 相关链接

- [Obsidian 官方文档](https://help.obsidian.md/)
- [Obsidian Importer 插件](https://github.com/obsidianmd/obsidian-importer)
- [Pandoc 文档](https://pandoc.org/)
- [youdaonote-pull](https://github.com/DeppWang/youdaonote-pull) - 有道云笔记导出工具
