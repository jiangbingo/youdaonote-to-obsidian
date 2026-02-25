"""
有道云笔记迁移配置

通过环境变量或配置文件设置路径
"""
import os
from pathlib import Path

# 默认配置 - 可通过环境变量覆盖
SOURCE_DIR = Path(os.getenv("YOUDAO_SOURCE_DIR", "./youdaonote-export"))
TARGET_DIR = Path(os.getenv("OBSIDIAN_VAULT_DIR", "./obsidian-vault"))
LOG_FILE = Path(os.getenv("MIGRATION_LOG_FILE", "./migration.log"))

# 目录映射：有道云目录 -> Obsidian 目录
# 用户可以根据自己的 PARA 结构修改
DIRECTORY_MAPPING = {
    # 示例映射 - 请根据实际情况修改
    "1CPLANE": "4 career/CPLANE",
    "2工作": "6 工作",
    "3提升": "5 职业技能",
    "4理财投资": "2 投资",
    "1存档": "文章/文摘/存档",

    # 资源目录细分
    "我的资源/微信收藏": "文章/文摘/微信收藏",
    "我的资源/系统收藏": "文章/文摘/系统收藏",
    "我的资源/收藏笔记": "文章/文摘",

    # 默认分类
    "_default": "文章/待分类",
}

# 关键词映射：用于智能分类
# 格式: (关键词元组): "目标目录"
KEYWORD_MAPPING = {
    # AI 相关
    ("AI", "人工智能", "机器学习", "深度学习", "GPT", "Claude", "LLM"): "1 AI",

    # 投资相关
    ("股票", "基金", "理财", "投资", "财经", "金融", "交易"): "2 投资",

    # 职业技能
    ("Python", "Java", "JavaScript", "Go", "Rust", "Git", "Linux", "Docker"): "5 职业技能",
    ("测试", "自动化", "CI/CD", "DevOps", "架构"): "5 职业技能",

    # 工作
    ("工作", "项目", "会议", "报告", "复盘"): "6 工作",

    # 生活
    ("生活", "美食", "旅游", "健康", "运动"): "3 生活",
}

# 需要排除的文件/目录
EXCLUDE_PATTERNS = [
    "images/",
    "attachments/",
    ".DS_Store",
    "*.lock",
    "HUB_DIRECTORY",  # 有道云空目录
]

# 图片扩展名
IMAGE_EXTENSIONS = {'.jpeg', '.jpg', '.png', '.gif', '.webp', '.bmp', '.svg'}

# 短文件阈值（行数）
SHORT_FILE_THRESHOLD = 10

# 标签配置
DEFAULT_TAGS = ["有道云导入"]
CONVERTED_TAG = "note转换"
REVIEW_TAG = "待审核"
