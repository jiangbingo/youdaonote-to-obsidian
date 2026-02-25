#!/usr/bin/env python3
"""
有道云笔记迁移到 Obsidian 的主脚本

使用方法:
    python migrate.py --source /path/to/youdao-export --target /path/to/obsidian-vault

功能:
    1. 检测并删除重复文件
    2. 转换 .note 文件为 Markdown
    3. 添加 Obsidian frontmatter
    4. 修复图片链接
    5. 按目录映射迁移文件
"""
import argparse
import shutil
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent))

from config import (
    SOURCE_DIR, TARGET_DIR, LOG_FILE,
    DIRECTORY_MAPPING, KEYWORD_MAPPING,
    EXCLUDE_PATTERNS, IMAGE_EXTENSIONS,
    SHORT_FILE_THRESHOLD, DEFAULT_TAGS,
    CONVERTED_TAG, REVIEW_TAG
)
from utils import (
    convert_note_to_md,
    get_file_hash,
    add_frontmatter,
    extract_date_from_filename,
)


class MigrationStats:
    """迁移统计"""
    def __init__(self):
        self.md_files = 0
        self.note_files = 0
        self.note_converted = 0
        self.note_failed = 0
        self.images = 0
        self.duplicates_removed = 0
        self.short_files_tagged = 0
        self.errors: List[str] = []

    def summary(self) -> str:
        return f"""
## 迁移统计

| 项目 | 数量 |
|------|------|
| Markdown 文件 | {self.md_files} |
| Note 转换成功 | {self.note_converted} |
| Note 转换失败 | {self.note_failed} |
| 图片文件 | {self.images} |
| 重复文件删除 | {self.duplicates_removed} |
| 短文件（待审核） | {self.short_files_tagged} |
| 错误数 | {len(self.errors)} |
"""


class MigrationLogger:
    """迁移日志"""
    def __init__(self, log_file: Path):
        self.log_file = log_file
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def log(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] {message}"
        print(log_line)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_line + "\n")


class YoudaoMigrator:
    """有道云笔记迁移器"""

    def __init__(self, source: Path, target: Path, log_file: Path = None):
        self.source = source
        self.target = target
        self.logger = MigrationLogger(log_file or LOG_FILE)
        self.stats = MigrationStats()

    def get_target_path(self, source_path: Path) -> Path:
        """根据目录映射获取目标路径"""
        rel_path = source_path.relative_to(self.source)
        parts = list(rel_path.parts)

        # 查找匹配的目录映射
        for source_prefix, target_prefix in DIRECTORY_MAPPING.items():
            source_parts = source_prefix.split('/')
            if parts[:len(source_parts)] == source_parts:
                new_parts = target_prefix.split('/') + parts[len(source_parts):]
                return self.target / '/'.join(new_parts)

        # 尝试关键词匹配
        filename = source_path.stem
        for keywords, target_dir in KEYWORD_MAPPING.items():
            if any(kw in filename for kw in keywords):
                return self.target / target_dir / source_path.name

        # 默认放到待分类
        default_dir = DIRECTORY_MAPPING.get("_default", "文章/待分类")
        return self.target / default_dir / source_path.name

    def process_duplicates(self, dry_run: bool = False) -> int:
        """处理重复文件"""
        self.logger.log("开始处理重复文件...")

        hash_map: Dict[str, List[Path]] = {}

        # 收集所有 md 文件的 hash
        for md_file in self.source.rglob("*.md"):
            file_hash = get_file_hash(md_file)
            if file_hash:
                if file_hash not in hash_map:
                    hash_map[file_hash] = []
                hash_map[file_hash].append(md_file)

        # 删除重复文件
        for file_hash, files in hash_map.items():
            if len(files) > 1:
                for file_to_remove in files[1:]:
                    if dry_run:
                        self.logger.log(f"  [预览] 将删除重复: {file_to_remove.name}")
                    else:
                        try:
                            file_to_remove.unlink()
                            self.logger.log(f"  删除重复: {file_to_remove.name}")
                            self.stats.duplicates_removed += 1
                        except Exception as e:
                            self.logger.log(f"  删除失败: {e}")

        self.logger.log(f"重复文件处理完成，删除 {self.stats.duplicates_removed} 个")
        return self.stats.duplicates_removed

    def migrate_markdown_files(self):
        """迁移 Markdown 文件"""
        self.logger.log("开始迁移 Markdown 文件...")

        for md_file in self.source.rglob("*.md"):
            # 跳过排除模式
            if any(pattern in str(md_file) for pattern in EXCLUDE_PATTERNS):
                continue

            try:
                target_path = self.get_target_path(md_file)
                target_path.parent.mkdir(parents=True, exist_ok=True)

                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 检查是否是短文件
                is_short = len(content.split('\n')) < SHORT_FILE_THRESHOLD

                # 添加 frontmatter
                content = add_frontmatter(
                    content,
                    md_file,
                    is_short=is_short,
                    source="有道云笔记"
                )

                with open(target_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                self.stats.md_files += 1
                if is_short:
                    self.stats.short_files_tagged += 1

                if self.stats.md_files % 100 == 0:
                    self.logger.log(f"  已迁移 {self.stats.md_files} 个 Markdown 文件...")

            except Exception as e:
                self.stats.errors.append(f"{md_file}: {e}")
                self.logger.log(f"  错误: {md_file}: {e}")

        self.logger.log(f"Markdown 迁移完成: {self.stats.md_files} 个文件")

    def migrate_note_files(self):
        """迁移并转换 Note 文件"""
        self.logger.log("开始转换 Note 文件...")

        for note_file in self.source.rglob("*.note"):
            try:
                target_path = self.get_target_path(note_file).with_suffix('.md')
                target_path.parent.mkdir(parents=True, exist_ok=True)

                # 转换内容
                markdown = convert_note_to_md(note_file)

                if markdown:
                    is_short = len(markdown.split('\n')) < SHORT_FILE_THRESHOLD
                    markdown = add_frontmatter(
                        markdown,
                        note_file,
                        is_converted=True,
                        is_short=is_short,
                        source="有道云笔记"
                    )

                    with open(target_path, 'w', encoding='utf-8') as f:
                        f.write(markdown)

                    self.stats.note_files += 1
                    self.stats.note_converted += 1
                else:
                    self.stats.note_failed += 1

                if self.stats.note_files % 100 == 0:
                    self.logger.log(f"  已转换 {self.stats.note_files} 个 Note 文件...")

            except Exception as e:
                self.stats.errors.append(f"{note_file}: {e}")
                self.stats.note_failed += 1

        self.logger.log(f"Note 转换完成: {self.stats.note_converted} 成功, {self.stats.note_failed} 失败")

    def migrate_images(self):
        """迁移图片"""
        self.logger.log("开始迁移图片...")

        target_images = self.target / "images"
        target_images.mkdir(parents=True, exist_ok=True)

        for image_file in self.source.rglob("*"):
            if image_file.suffix.lower() in IMAGE_EXTENSIONS:
                try:
                    target_path = target_images / image_file.name

                    # 避免重名覆盖
                    if target_path.exists():
                        base = image_file.stem
                        ext = image_file.suffix
                        counter = 1
                        while target_path.exists():
                            target_path = target_images / f"{base}_{counter}{ext}"
                            counter += 1

                    shutil.copy2(image_file, target_path)
                    self.stats.images += 1

                    if self.stats.images % 500 == 0:
                        self.logger.log(f"  已迁移 {self.stats.images} 个图片...")

                except Exception as e:
                    self.stats.errors.append(f"{image_file}: {e}")

        self.logger.log(f"图片迁移完成: {self.stats.images} 个")

    def generate_report(self) -> str:
        """生成迁移报告"""
        report = f"""# 有道云笔记迁移报告

**迁移时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**源目录:** {self.source}
**目标目录:** {self.target}

{self.stats.summary()}

## 错误列表

"""
        if self.stats.errors:
            for error in self.stats.errors[:20]:
                report += f"- {error}\n"
            if len(self.stats.errors) > 20:
                report += f"\n... 还有 {len(self.stats.errors) - 20} 个错误\n"
        else:
            report += "无错误\n"

        report += """
## 后续操作建议

1. 在 Obsidian 中搜索 `#待审核` 查看需要审核的短文件
2. 搜索 `#note转换` 查看转换的 Note 文件
3. 检查图片链接是否正常显示
4. 根据需要调整分类

---
*迁移完成*
"""
        return report

    def run(self, dry_run: bool = False, skip_duplicates: bool = False):
        """执行迁移"""
        self.logger.log("=" * 50)
        self.logger.log("有道云笔记迁移开始")
        self.logger.log(f"源目录: {self.source}")
        self.logger.log(f"目标目录: {self.target}")
        self.logger.log("=" * 50)

        if not skip_duplicates:
            self.process_duplicates(dry_run)

        if not dry_run:
            self.migrate_markdown_files()
            self.migrate_note_files()
            self.migrate_images()

        report = self.generate_report()
        self.logger.log("=" * 50)
        self.logger.log("迁移完成!")
        self.logger.log("=" * 50)

        return report


def main():
    parser = argparse.ArgumentParser(
        description="有道云笔记迁移到 Obsidian",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本用法
  python migrate.py --source ./youdaonote-export --target ./my-vault

  # 预览模式（不实际执行）
  python migrate.py --source ./youdaonote-export --target ./my-vault --dry-run

  # 使用环境变量
  export YOUDAO_SOURCE_DIR=/path/to/export
  export OBSIDIAN_VAULT_DIR=/path/to/vault
  python migrate.py
        """
    )

    parser.add_argument(
        '--source', '-s',
        type=Path,
        default=SOURCE_DIR,
        help=f'有道云笔记导出目录 (默认: {SOURCE_DIR})'
    )
    parser.add_argument(
        '--target', '-t',
        type=Path,
        default=TARGET_DIR,
        help=f'Obsidian vault 目录 (默认: {TARGET_DIR})'
    )
    parser.add_argument(
        '--log', '-l',
        type=Path,
        default=LOG_FILE,
        help=f'日志文件路径 (默认: {LOG_FILE})'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='预览模式，不实际执行迁移'
    )
    parser.add_argument(
        '--skip-duplicates',
        action='store_true',
        help='跳过重复文件检测'
    )

    args = parser.parse_args()

    # 验证目录
    if not args.source.exists():
        print(f"错误: 源目录不存在: {args.source}")
        sys.exit(1)

    # 执行迁移
    migrator = YoudaoMigrator(
        source=args.source,
        target=args.target,
        log_file=args.log
    )

    report = migrator.run(
        dry_run=args.dry_run,
        skip_duplicates=args.skip_duplicates
    )

    print("\n" + report)

    # 保存报告
    report_path = args.target / "migration_report.md"
    if not args.dry_run:
        args.target.mkdir(parents=True, exist_ok=True)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n报告已保存: {report_path}")


if __name__ == "__main__":
    main()
