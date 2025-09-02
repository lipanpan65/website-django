# Makefile for Django Local Development Environment

.PHONY: help dev check-db check-network docker-dev docker-build docker-stop docker-clean

# 默认目标
help:
	@echo "🚀 Django本地开发环境管理"
	@echo ""
	@echo "可用命令:"
	@echo "  make dev           - 启动本地开发环境"
	@echo "  make check-db      - 检查数据库连接"
	@echo ""
	@echo "Docker 相关命令:"
	@echo "  make check-network - 检查/创建Docker网络"
	@echo "  make docker-build  - 构建Docker开发镜像"
	@echo "  make docker-dev    - 启动Docker开发环境"
	@echo "  make docker-stop   - 停止Docker开发环境"
	@echo "  make docker-clean  - 清理Docker开发环境"

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

# 检查/创建Docker网络
check-network:
	@echo "🌐 检查Docker网络 website-dev-network..."
	@if ! docker network ls | grep -q "website-dev-network"; then \
		echo "📡 创建Docker网络 website-dev-network..."; \
		docker network create website-dev-network --driver bridge; \
		echo "✅ Docker网络创建成功"; \
	else \
		echo "✅ Docker网络 website-dev-network 已存在"; \
	fi

# Docker开发环境相关命令
docker-build:
	@echo "🐳 构建Docker开发镜像..."
	@docker-compose -f docker-compose.dev.yml build

docker-dev: check-network
	@echo "🐳 启动Docker开发环境..."
	@echo "🌐 服务将在 http://localhost:9798 启动"
	@docker-compose -f docker-compose.dev.yml up

docker-stop:
	@echo "🛑 停止Docker开发环境..."
	@docker-compose -f docker-compose.dev.yml down

docker-clean:
	@echo "🧹 清理Docker开发环境（停止并删除容器、网络、镜像）..."
	@docker-compose -f docker-compose.dev.yml down --rmi all --volumes --remove-orphans