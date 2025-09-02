# Makefile for Django Local Development Environment

.PHONY: help dev check-db

# 默认目标
help:
	@echo "🚀 Django本地开发环境管理"
	@echo ""
	@echo "可用命令:"
	@echo "  make dev           - 启动本地开发环境"
	@echo "  make check-db      - 检查数据库连接"

# 检查数据库连接
check-db:
	@echo "🔍 检查数据库连接..."
	@if [ ! -f website/website/settings/db.ini ]; then \
		echo "❌ 数据库配置文件不存在: website/website/settings/db.ini"; \
		echo "请复制 db.ini.example 并配置数据库连接信息"; \
		exit 1; \
	fi
	@DB_HOST=$$(grep "^host" website/website/settings/db.ini | cut -d'=' -f2 | tr -d ' '); \
	DB_PORT=$$(grep "^port" website/website/settings/db.ini | cut -d'=' -f2 | tr -d ' '); \
	DB_USER=$$(grep "^user" website/website/settings/db.ini | cut -d'=' -f2 | tr -d ' '); \
	DB_PASSWORD=$$(grep "^password" website/website/settings/db.ini | cut -d'=' -f2 | tr -d ' '); \
	DB_NAME=$$(grep "^database" website/website/settings/db.ini | cut -d'=' -f2 | tr -d ' '); \
	echo "📡 测试数据库连接: $$DB_HOST:$$DB_PORT"; \
	if command -v nc >/dev/null 2>&1; then \
		nc -z $$DB_HOST $$DB_PORT >/dev/null 2>&1; \
		if [ $$? -eq 0 ]; then \
			echo "✅ 数据库端口连接正常"; \
		else \
			echo "❌ 无法连接到数据库端口"; \
			exit 1; \
		fi; \
	else \
		echo "⚠️  无法找到nc命令，跳过端口检查"; \
	fi
	@echo "🗄️  检查数据库是否存在..."
	@DB_HOST=$$(grep "^host" website/website/settings/db.ini | cut -d'=' -f2 | tr -d ' '); \
	DB_PORT=$$(grep "^port" website/website/settings/db.ini | cut -d'=' -f2 | tr -d ' '); \
	DB_USER=$$(grep "^user" website/website/settings/db.ini | cut -d'=' -f2 | tr -d ' '); \
	DB_PASSWORD=$$(grep "^password" website/website/settings/db.ini | cut -d'=' -f2 | tr -d ' '); \
	DB_NAME=$$(grep "^database" website/website/settings/db.ini | cut -d'=' -f2 | tr -d ' '); \
	if command -v mysql >/dev/null 2>&1; then \
		mysql -h$$DB_HOST -P$$DB_PORT -u$$DB_USER -p$$DB_PASSWORD -e "USE $$DB_NAME; SELECT 1;" >/dev/null 2>&1; \
		if [ $$? -eq 0 ]; then \
			echo "✅ 数据库 $$DB_NAME 存在且可访问"; \
		else \
			echo "❌ 数据库 $$DB_NAME 不存在或无法访问"; \
			exit 1; \
		fi; \
	elif command -v docker >/dev/null 2>&1; then \
		echo "📦 使用Docker MySQL客户端检查数据库..."; \
		docker run --rm mysql:8.0 mysql -h$$DB_HOST -P$$DB_PORT -u$$DB_USER -p$$DB_PASSWORD -e "USE $$DB_NAME; SELECT 'Database exists' as result;" >/dev/null 2>&1; \
		if [ $$? -eq 0 ]; then \
			echo "✅ 数据库 $$DB_NAME 存在且可访问"; \
		else \
			echo "❌ 数据库 $$DB_NAME 不存在或无法访问"; \
			exit 1; \
		fi; \
	else \
		echo "⚠️  未找到mysql客户端和Docker，跳过数据库检查"; \
	fi

# 启动本地开发环境
dev: check-db
	@echo "🚀 启动Django本地开发环境..."
	@if [ ! -d venv ]; then \
		echo "📦 创建Python虚拟环境..."; \
		python3 -m venv venv; \
	fi
	@echo "📦 安装依赖包..."
	@venv/bin/pip install -q -r website/requirements.txt
	@echo "🌐 启动开发服务器在端口9798..."
	@cd website && ../venv/bin/python manage.py runserver 127.0.0.1:9798 --settings=website.settings.dev