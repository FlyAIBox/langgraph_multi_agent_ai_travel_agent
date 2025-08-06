# AI旅行规划智能体 - 部署指南

## 🚀 部署方式

### 方式一：本地开发部署（推荐用于开发和测试）

#### 1. 环境准备
```bash
# 克隆项目
git clone <repository-url>
cd langgraph_multi_agent_ai_travel_agent

# 创建环境变量文件
cp .env.example .env
# 编辑.env文件，添加您的API密钥
```

#### 2. 启动服务
```bash
# 启动后端（终端1）
./start_backend.sh

# 启动前端（终端2）
./start_frontend.sh
```

#### 3. 访问应用
- 前端界面: http://localhost:8501
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

### 方式二：Docker部署（推荐用于生产环境）

#### 1. 环境准备
```bash
# 确保安装了Docker和Docker Compose
docker --version
docker-compose --version

# 创建环境变量文件
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

#### 2. 构建和启动
```bash
# 构建并启动所有服务
docker-compose up --build -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

#### 3. 访问应用
- 前端界面: http://localhost:8501
- API文档: http://localhost:8000/docs

#### 4. 管理服务
```bash
# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 更新服务
docker-compose pull
docker-compose up -d
```

### 方式三：云平台部署

#### Heroku部署

1. **准备Heroku配置文件**
```bash
# 创建Procfile
echo "web: cd backend && python api_server.py" > Procfile
echo "worker: cd frontend && streamlit run streamlit_app.py --server.port=$PORT" >> Procfile
```

2. **部署到Heroku**
```bash
# 安装Heroku CLI
# 登录Heroku
heroku login

# 创建应用
heroku create your-app-name

# 设置环境变量
heroku config:set GEMINI_API_KEY=your_api_key_here

# 部署
git push heroku main
```

#### AWS部署

1. **使用AWS ECS**
```bash
# 构建Docker镜像
docker build -t travel-backend ./backend
docker build -t travel-frontend ./frontend

# 推送到ECR
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-west-2.amazonaws.com
docker tag travel-backend:latest <account-id>.dkr.ecr.us-west-2.amazonaws.com/travel-backend:latest
docker push <account-id>.dkr.ecr.us-west-2.amazonaws.com/travel-backend:latest
```

2. **配置ECS任务定义**
```json
{
  "family": "travel-planning-app",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "<account-id>.dkr.ecr.us-west-2.amazonaws.com/travel-backend:latest",
      "portMappings": [{"containerPort": 8000}],
      "environment": [
        {"name": "GEMINI_API_KEY", "value": "your_api_key_here"}
      ]
    }
  ]
}
```

## 🔧 配置说明

### 环境变量

| 变量名 | 描述 | 默认值 | 必需 |
|--------|------|--------|------|
| `GEMINI_API_KEY` | Google Gemini API密钥 | - | ✅ |
| `GEMINI_MODEL` | 使用的Gemini模型 | `gemini-2.0-flash` | ❌ |
| `API_BASE_URL` | 后端API地址 | `http://localhost:8000` | ❌ |
| `TEMPERATURE` | AI模型温度参数 | `0.7` | ❌ |
| `MAX_TOKENS` | 最大输出token数 | `4000` | ❌ |

### 端口配置

| 服务 | 端口 | 描述 |
|------|------|------|
| 后端API | 8000 | FastAPI服务器 |
| 前端Web | 8501 | Streamlit应用 |

## 🔍 监控和日志

### 健康检查

```bash
# 检查后端健康状态
curl http://localhost:8000/health

# 检查前端健康状态
curl http://localhost:8501/_stcore/health
```

### 日志查看

```bash
# 本地部署日志
tail -f backend/logs/app.log
tail -f frontend/logs/app.log

# Docker部署日志
docker-compose logs -f backend
docker-compose logs -f frontend

# 查看特定容器日志
docker logs <container-id>
```

### 性能监控

```bash
# 查看资源使用情况
docker stats

# 查看系统资源
htop
iostat
```

## 🛡️ 安全配置

### 1. API密钥安全
```bash
# 使用环境变量而不是硬编码
export GEMINI_API_KEY="your_secret_key"

# 在生产环境中使用密钥管理服务
# AWS Secrets Manager, Azure Key Vault, etc.
```

### 2. 网络安全
```bash
# 配置防火墙规则
ufw allow 8000/tcp
ufw allow 8501/tcp

# 使用HTTPS（生产环境）
# 配置SSL证书和反向代理
```

### 3. 访问控制
```python
# 在FastAPI中添加认证中间件
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # 限制允许的域名
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## 🔧 故障排除

### 常见问题

1. **端口冲突**
```bash
# 查看端口占用
lsof -i :8000
lsof -i :8501

# 杀死占用进程
kill -9 <PID>
```

2. **依赖安装失败**
```bash
# 清理pip缓存
pip cache purge

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

3. **API连接失败**
```bash
# 检查网络连接
ping localhost
telnet localhost 8000

# 检查防火墙设置
sudo ufw status
```

4. **内存不足**
```bash
# 增加虚拟内存
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### 调试模式

```bash
# 启用调试模式
export DEBUG=true

# 查看详细错误信息
python -u api_server.py

# 使用调试器
python -m pdb api_server.py
```

## 📊 性能优化

### 1. 后端优化
```python
# 使用异步处理
import asyncio
from concurrent.futures import ThreadPoolExecutor

# 配置连接池
from httpx import AsyncClient
client = AsyncClient(limits=httpx.Limits(max_connections=100))
```

### 2. 前端优化
```python
# 使用Streamlit缓存
@st.cache_data
def load_data():
    return expensive_computation()

# 优化页面加载
st.set_page_config(layout="wide")
```

### 3. 系统优化
```bash
# 调整系统参数
echo 'net.core.somaxconn = 1024' >> /etc/sysctl.conf
echo 'net.ipv4.tcp_max_syn_backlog = 1024' >> /etc/sysctl.conf
sysctl -p
```

## 📈 扩展部署

### 负载均衡

```nginx
# Nginx配置
upstream backend {
    server localhost:8000;
    server localhost:8001;
    server localhost:8002;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
    }
}
```

### 数据库集成

```python
# 添加数据库支持
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@localhost/dbname"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

### 缓存系统

```python
# 添加Redis缓存
import redis
r = redis.Redis(host='localhost', port=6379, db=0)

@app.middleware("http")
async def cache_middleware(request: Request, call_next):
    # 实现缓存逻辑
    pass
```
