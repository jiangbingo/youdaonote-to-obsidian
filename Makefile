.PHONY: help install run run-dry test format lint clean check-all

# 默认配置
SOURCE ?= ./youdaonote-export
TARGET ?= ./obsidian-vault
PYTHON := python3

# 颜色输出
CYAN := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RESET := \033[0m

help: ## 显示帮助信息
	@echo "$(CYAN)有道云笔记迁移工具$(RESET)"
	@echo ""
	@echo "$(GREEN)使用方法:$(RESET)"
	@echo "  make run        # 执行迁移"
	@echo "  make run-dry    # 预览模式（不实际执行）"
	@echo ""
	@echo "$(GREEN)开发命令:$(RESET)"
	@echo "  make test       # 运行测试"
	@echo "  make format     # 格式化代码"
	@echo "  make lint       # 代码检查"
	@echo "  make check-all  # 运行所有检查"
	@echo ""
	@echo "$(GREEN)配置:$(RESET)"
	@echo "  SOURCE=$(SOURCE)"
	@echo "  TARGET=$(TARGET)"
	@echo ""
	@echo "$(YELLOW)自定义路径:$(RESET)"
	@echo "  make run SOURCE=/path/to/export TARGET=/path/to/vault"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; } /^[a-zA-Z_-]+:.*##/ { printf "  $(CYAN)%-12s$(RESET) %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

install: ## 安装依赖
	@echo "$(CYAN)安装依赖...$(RESET)"
	$(PYTHON) -m pip install --quiet black ruff pytest 2>/dev/null || true
	@echo "$(GREEN)依赖安装完成$(RESET)"

run: ## 执行迁移
	@echo "$(CYAN)开始迁移...$(RESET)"
	@echo "源目录: $(SOURCE)"
	@echo "目标目录: $(TARGET)"
	$(PYTHON) scripts/migrate.py --source "$(SOURCE)" --target "$(TARGET)"

run-dry: ## 预览模式（不实际执行）
	@echo "$(YELLOW)预览模式 - 不会修改任何文件$(RESET)"
	$(PYTHON) scripts/migrate.py --source "$(SOURCE)" --target "$(TARGET)" --dry-run

test: ## 运行测试
	@echo "$(CYAN)运行测试...$(RESET)"
	$(PYTHON) -m pytest tests/ -v --tb=short 2>/dev/null || $(PYTHON) tests/test_converter.py

format: ## 格式化代码
	@echo "$(CYAN)格式化代码...$(RESET)"
	@$(PYTHON) -m black scripts/ tests/ --quiet 2>/dev/null || \
		echo "$(YELLOW)提示: 安装 black 进行格式化: pip install black$(RESET)"
	@$(PYTHON) -m isort scripts/ tests/ --quiet 2>/dev/null || true
	@echo "$(GREEN)格式化完成$(RESET)"

lint: ## 代码检查
	@echo "$(CYAN)代码检查...$(RESET)"
	@$(PYTHON) -m ruff check scripts/ tests/ 2>/dev/null || \
		echo "$(YELLOW)提示: 安装 ruff 进行检查: pip install ruff$(RESET)"
	@$(PYTHON) -m py_compile scripts/migrate.py scripts/utils/*.py
	@echo "$(GREEN)检查完成$(RESET)"

type-check: ## 类型检查
	@echo "$(CYAN)类型检查...$(RESET)"
	@$(PYTHON) -m mypy scripts/ --ignore-missing-imports 2>/dev/null || \
		echo "$(YELLOW)提示: 安装 mypy 进行类型检查: pip install mypy$(RESET)"

check-all: format lint test ## 运行所有检查

clean: ## 清理临时文件
	@echo "$(CYAN)清理临时文件...$(RESET)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.log" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)清理完成$(RESET)"

# 快捷命令
preview: run-dry ## 预览迁移（run-dry 的别名）

quick: ## 快速迁移（跳过重复检测）
	$(PYTHON) scripts/migrate.py --source "$(SOURCE)" --target "$(TARGET)" --skip-duplicates

stats: ## 显示统计信息
	@echo "$(CYAN)统计信息$(RESET)"
	@echo "源目录文件数:"
	@find "$(SOURCE)" -type f -name "*.md" 2>/dev/null | wc -l | xargs echo "  Markdown:"
	@find "$(SOURCE)" -type f -name "*.note" 2>/dev/null | wc -l | xargs echo "  Note:"
	@find "$(SOURCE)" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.gif" \) 2>/dev/null | wc -l | xargs echo "  图片:"
