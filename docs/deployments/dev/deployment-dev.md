# Django 开发环境部署指南

## 项目结构说明

本项目采用多项目工作区结构：
```
website/                          # 工作区根目录
├── website-django/               # Django 后端项目
│   ├── venv/                    # Python 虚拟环境
│   ├── website/                 # Django 应用代码
│   ├── Makefile                 # 构建脚本
│   └── docs/                    # 文档
├── website-react/               # React 前端项目
├── website-gin/                 # Go 后端项目
└── website.code-workspace       # VS Code/Cursor 工作区配置
```

## 基于 Python venv 创建虚拟环境（推荐）

### 环境要求
- Python 3.9.0+
- MySQL 数据库（可选，默认使用 SQLite）
- VS Code 或 Cursor IDE

### 快速开始

1. **克隆项目并进入工作区根目录**
   ```bash
   git clone <repository-url>
   cd website
   ```

2. **进入 Django 项目目录**
   ```bash
   cd website-django
   ```

3. **创建 Python 虚拟环境**
   ```bash
   python3 -m venv venv
   ```

4. **安装依赖包**
   ```bash
   # 直接使用虚拟环境的 pip，无需激活
   venv/bin/pip install --upgrade pip
   venv/bin/pip install -r website/requirements.txt
   ```

5. **配置数据库（可选）**
   
   如果需要使用 MySQL 数据库：
   ```bash
   # 复制数据库配置示例文件
   cp website/settings/db.ini.example website/settings/db.ini
   
   # 编辑 db.ini 配置数据库连接信息
   # [default]
   # database = your_database_name
   # user = your_username
   # password = your_password
   # host = your_host
   # port = 3306
   ```
   
   如果使用默认的 SQLite 数据库，可以跳过此步骤。

6. **使用 Makefile 启动（推荐）**
   ```bash
   # 回到 website-django 根目录
   cd /path/to/website/website-django
   
   # 使用 make 命令启动开发环境（会自动检查数据库连接）
   make dev
   ```

7. **手动启动开发服务器**
   ```bash
   cd website
   ../venv/bin/python manage.py runserver 127.0.0.1:9798 --settings=website.settings.dev
   ```

8. **访问应用**
   
   打开浏览器访问：http://127.0.0.1:9798

## Cursor/VS Code IDE 配置

### 工作区配置

1. **打开工作区文件**
   
   使用 Cursor/VS Code 打开 `website.code-workspace` 文件，而不是直接打开文件夹。

2. **Python 解释器配置**
   
   工作区已自动配置 Python 解释器路径：
   ```json
   {
     "folders": [
       {
         "path": "."
       }
     ],
     "settings": {
       "python.defaultInterpreterPath": "./website-django/venv/bin/python",
       "python.terminal.activateEnvironment": true,
       "python.analysis.extraPaths": [
         "./website-django/website"
       ]
     }
   }
   ```

3. **手动设置解释器（如果自动配置失败）**
   
   - 按 `Cmd+Shift+P` (macOS) 或 `Ctrl+Shift+P` (Windows/Linux)
   - 输入 "Python: Select Interpreter"
   - 选择 "Enter interpreter path..."
   - 输入绝对路径：`/path/to/website/website-django/venv/bin/python`

### 解决常见 IDE 问题

**问题：无法解析导入 "rest_framework"**

解决方案：
1. 确保已正确设置 Python 解释器路径
2. 重启 Cursor/VS Code
3. 按 `Cmd+Shift+P` → "Developer: Reload Window"
4. 检查状态栏显示的 Python 解释器是否正确

**问题：模块路径无法识别**

确保 `.vscode/settings.json` 包含以下配置：
```json
{
  "python.defaultInterpreterPath": "./website-django/venv/bin/python",
  "python.terminal.activateEnvironment": true,
  "python.analysis.extraPaths": [
    "./website-django/website"
  ],
  "python.analysis.autoImportCompletions": true
}
```

### 调试和开发技巧

**1. 使用 Django Shell**
```bash
cd website
../venv/bin/python manage.py shell --settings=website.settings.dev
```

**2. 数据库迁移**
```bash
cd website
../venv/bin/python manage.py makemigrations --settings=website.settings.dev
../venv/bin/python manage.py migrate --settings=website.settings.dev
```

**3. 创建超级用户**
```bash
cd website
../venv/bin/python manage.py createsuperuser --settings=website.settings.dev
```

### 常见问题与解决方案

**数据库连接问题：**
- 确保 MySQL 服务器正在运行
- 检查 db.ini 中的连接信息是否正确
- 如果使用云数据库，确保 IP 地址在白名单中

**端口冲突：**
- 如果 9798 端口被占用，可以修改为其他端口：
  ```bash
  ../venv/bin/python manage.py runserver 127.0.0.1:9799 --settings=website.settings.dev
  ```

**虚拟环境问题：**
- 如果虚拟环境损坏，删除并重新创建：
  ```bash
  rm -rf venv
  python3 -m venv venv
  venv/bin/pip install -r website/requirements.txt
  ```

**Fish Shell 用户注意：**
- 不要使用 `source venv/bin/activate`
- 直接使用 `venv/bin/python` 和 `venv/bin/pip`

## 基于 conda 创建虚拟环境
```bash
conda --version
# 创建 conda 虚拟环境
conda create -n website-django python=3.9
conda activate website-django

# 安装依赖
cd website
pip install -r requirements.txt

# 运行项目
python manage.py runserver --settings=website.settings.dev
```

## 基于 docker 创建虚拟环境
```bash
# 构建开发镜像
docker-compose -f docker-compose.dev.yml build

# 启动开发环境
docker-compose -f docker-compose.dev.yml up
```