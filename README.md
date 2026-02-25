# 有道云笔记迁移到 Obsidian

将有道云笔记导出的数据迁移到 Obsidian vault，支持格式转换、去重、目录映射等功能。

## 功能特点

- **格式转换**: 自动将 `.note` 文件（HTML格式）转换为 Markdown
- **去重检测**: 基于 MD5 哈希检测并删除重复文件
- **目录映射**: 智能将有道云目录映射到 Obsidian PARA 结构
- **Frontmatter**: 自动添加 Obsidian 兼容的 YAML frontmatter
- **图片迁移**: 统一迁移图片到 `images/` 目录并修复链接
- **标签系统**: 自动添加迁移标签，标记需要审核的文件

## 快速开始

### 1. 安装依赖

```bash
# 克隆仓库
git clone https://github.com/jiangbingo/youdaonote-to-obsidian.git
cd youdaonote-to-obsidian

# 无需额外依赖，使用 Python 标准库
python3 --version  # 需要 Python 3.8+
```

### 2. 导出有道云笔记

1. 打开有道云笔记 PC 客户端
2. 选择要导出的笔记本
3. 右键 → 导出 → 选择 Markdown 格式
4. 保存到本地目录

### 3. 配置目录映射

编辑 `scripts/config.py`，修改 `DIRECTORY_MAPPING`：

```python
DIRECTORY_MAPPING = {
    "你的有道云目录": "Obsidian目标目录",
    "工作笔记": "6 工作",
    "学习资料": "5 职业技能",
    # ...
}
```

### 4. 执行迁移

```bash
# 预览模式（推荐先执行）
python3 scripts/migrate.py \
    --source /path/to/youdao-export \
    --target /path/to/obsidian-vault \
    --dry-run

# 正式迁移
python3 scripts/migrate.py \
    --source /path/to/youdao-export \
    --target /path/to/obsidian-vault
```

## 目录映射示例

### 有道云结构
```
youdaonote-export/
├── 1CPLANE/
├── 2工作/
├── 3提升/
├── 4理财投资/
└── 我的资源/
    ├── 微信收藏/
    └── 系统收藏/
```

### Obsidian PARA 结构
```
obsidian-vault/
├── 1 AI/
├── 2 投资/
├── 3 生活/
├── 4 career/
├── 5 职业技能/
├── 6 工作/
├── 文章/
│   └── 文摘/
└── images/
```

## 迁移效果

### 转换前 (.note 文件)
```html
<div style='font-size:18px'>
  <p>这是有道云笔记内容</p>
  <img src="http://note.youdao.com/yws/res/xxx" />
</div>
```

### 转换后 (Markdown)
```markdown
---
title: "笔记标题"
created: 2026-02-14
tags:
  - 有道云导入
  - note转换
source: 有道云笔记
---

这是有道云笔记内容

![](../images/xxx.png)
```

## 配置说明

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `YOUDAO_SOURCE_DIR` | 有道云导出目录 | `./youdaonote-export` |
| `OBSIDIAN_VAULT_DIR` | Obsidian vault 目录 | `./obsidian-vault` |
| `MIGRATION_LOG_FILE` | 日志文件路径 | `./migration.log` |

### 命令行参数

```
--source, -s     有道云导出目录
--target, -t     Obsidian vault 目录
--log, -l        日志文件路径
--dry-run        预览模式，不实际执行
--skip-duplicates 跳过重复文件检测
```

## 迁移后操作

1. **审核短文件**: 在 Obsidian 中搜索 `#待审核`
2. **检查转换文件**: 搜索 `#note转换`
3. **验证图片**: 检查图片是否正常显示
4. **调整分类**: 根据需要重新组织文件

## 项目结构

```
youdaonote-to-obsidian/
├── README.md
├── LICENSE
├── scripts/
│   ├── migrate.py        # 主迁移脚本
│   ├── config.py         # 配置文件
│   └── utils/
│       ├── __init__.py
│       ├── converter.py  # HTML→MD 转换
│       ├── dedup.py      # 去重工具
│       └── frontmatter.py # Frontmatter 生成
├── config/
│   └── config.example.yaml
├── docs/
│   └── MIGRATION_GUIDE.md
└── tests/
    └── test_converter.py
```

## 常见问题

### Q: 图片链接失效怎么办？
A: 检查 `images/` 目录下是否有对应图片，可能是有道云导出时未下载完整。

### Q: Note 文件转换乱码？
A: 部分复杂格式的 .note 文件可能需要手动调整，搜索 `#note转换` 逐个检查。

### Q: 如何处理重复文件？
A: 脚本默认保留第一个找到的文件，删除后续重复项。可以先用 `--dry-run` 预览。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 相关项目

- [Obsidian](https://obsidian.md/) - 知识管理工具
- [youdaonote-pull](https://github.com/DeppWang/youdaonote-pull) - 有道云笔记导出工具
