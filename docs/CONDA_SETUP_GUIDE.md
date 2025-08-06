# 🐍 Conda环境设置指南

## 📋 概述

本项目使用Conda进行Python环境管理，确保依赖的一致性和隔离性。

## 🚀 快速开始

### 方法一：自动设置（推荐）

```bash
# 一键设置环境和依赖
./setup_environment.sh

# 编辑API密钥
nano .env  # 或使用其他编辑器

# 启动服务
conda activate ai-travel-agents
./start_backend.sh    # 终端1
./start_frontend.sh   # 终端2
```

### 方法二：手动设置

```bash
# 1. 创建conda环境
conda create -n ai-travel-agents python=3.10

# 2. 激活环境
conda activate ai-travel-agents

# 3. 安装后端依赖
cd backend
pip install -r requirements.txt

# 4. 安装前端依赖
cd ../frontend
pip install -r requirements.txt

# 5. 返回根目录
cd ..

# 6. 创建环境变量文件
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

## 🔧 环境管理

### 激活环境
```bash
conda activate ai-travel-agents
```

### 停用环境
```bash
conda deactivate
```

### 查看环境列表
```bash
conda env list
```

### 删除环境（如需重建）
```bash
conda env remove -n ai-travel-agents
```

### 导出环境配置
```bash
conda activate ai-travel-agents
conda env export > environment.yml
```

### 从配置文件创建环境
```bash
conda env create -f environment.yml
```

## 📦 依赖管理

### 查看已安装包
```bash
conda activate ai-travel-agents
pip list
```

### 更新依赖
```bash
conda activate ai-travel-agents
pip install --upgrade -r backend/requirements.txt
pip install --upgrade -r frontend/requirements.txt
```

### 添加新依赖
```bash
conda activate ai-travel-agents
pip install package_name
pip freeze > backend/requirements.txt  # 更新依赖文件
```

## 🔑 环境变量配置

### .env文件格式
```bash
# Google API密钥 (必需)
GOOGLE_API_KEY=your_google_api_key_here

# 可选配置
GEMINI_MODEL=gemini-2.0-flash
TEMPERATURE=0.7
MAX_TOKENS=4000
TOP_P=0.9
```

### 获取Google API密钥
1. 访问：https://makersuite.google.com/app/apikey
2. 登录Google账户
3. 创建新的API密钥
4. 复制密钥到.env文件

## 🚀 启动服务

### 后端服务
```bash
conda activate ai-travel-agents
./start_backend.sh
```

### 前端服务
```bash
conda activate ai-travel-agents
./start_frontend.sh
```

### 演示脚本
```bash
conda activate ai-travel-agents
python demo.py
```

## 🐳 Docker替代方案

如果不想使用Conda，也可以使用Docker：

```bash
# 使用Docker Compose
docker-compose up --build -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 🔍 故障排除

### 常见问题

1. **Conda命令未找到**
   ```bash
   # 安装Miniconda
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   bash Miniconda3-latest-Linux-x86_64.sh
   ```

2. **环境激活失败**
   ```bash
   # 初始化conda
   conda init bash
   source ~/.bashrc
   ```

3. **依赖安装失败**
   ```bash
   # 清理pip缓存
   pip cache purge
   
   # 使用国内镜像
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
   ```

4. **API密钥错误**
   ```bash
   # 检查.env文件
   cat .env
   
   # 确保没有多余空格
   GOOGLE_API_KEY=your_key_without_spaces
   ```

## 💡 最佳实践

1. **始终在激活环境后工作**
   ```bash
   conda activate ai-travel-agents
   # 然后执行其他命令
   ```

2. **定期更新依赖**
   ```bash
   pip list --outdated
   pip install --upgrade package_name
   ```

3. **备份环境配置**
   ```bash
   conda env export > environment_backup.yml
   ```

4. **使用不同环境进行开发和生产**
   ```bash
   conda create -n ai-travel-dev python=3.10
   conda create -n ai-travel-prod python=3.10
   ```

## 📚 相关资源

- [Conda官方文档](https://docs.conda.io/)
- [Miniconda下载](https://docs.conda.io/en/latest/miniconda.html)
- [Google AI Studio](https://makersuite.google.com/)
- [项目README](README.md)
- [快速开始指南](QUICK_START.md)
