# 🌍 LangGraph多智能体AI旅行规划师 - Web版本

基于LangGraph框架、Google Gemini Flash-2.0和DuckDuckGo搜索的智能旅行规划Web系统

## 🎯 系统概述

这是一个先进的多智能体AI旅行规划Web系统，包含：

- **🌐 Streamlit前端**: 用户友好的Web界面
- **⚡ FastAPI后端**: 高性能API服务
- **🤖 LangGraph智能体**: 多智能体协作系统
- **📊 实时监控**: 可视化进度跟踪
- **📥 文件服务**: 完整报告下载

## 🚀 快速开始

### 1. 环境准备
```bash
# 设置API密钥
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

### 2. 启动服务
```bash
# 启动后端 (终端1)
./start_backend.sh

# 启动前端 (终端2)
./start_frontend.sh
```

### 3. 访问应用
- 🌐 前端界面: http://localhost:8501
- 📚 API文档: http://localhost:8000/docs

## 🎯 AI智能体团队

| 智能体 | 职责 | 功能 |
|--------|------|------|
| 🎯 协调员智能体 | 工作流编排与决策综合 | 统筹整个规划流程 |
| ✈️ 旅行顾问 | 目的地专业知识与实时搜索 | 提供目的地信息和建议 |
| 💰 预算优化师 | 成本分析与实时定价 | 优化预算分配和成本控制 |
| 🌤️ 天气分析师 | 天气情报与当前数据 | 提供天气预报和建议 |
| 🏠 当地专家 | 内部知识与实时本地信息 | 提供当地文化和实用信息 |
| 📅 行程规划师 | 日程优化与物流安排 | 制定详细的行程安排 |

## 📁 项目结构

```
langgraph_multi_agent_ai_travel_agent/
├── 🌐 frontend/              # Streamlit前端
│   ├── streamlit_app.py      # 主应用
│   ├── requirements.txt      # 前端依赖
│   └── Dockerfile           # Docker配置
├── ⚡ backend/               # FastAPI后端
│   ├── api_server.py        # API服务器
│   ├── requirements.txt     # 后端依赖
│   ├── Dockerfile          # Docker配置
│   ├── agents/             # LangGraph智能体
│   ├── config/             # 配置文件
│   ├── modules/            # 功能模块
│   ├── tools/              # 工具模块
│   └── utils/              # 工具函数
├── 📊 results/              # 规划结果存储
├── 🚀 start_backend.sh      # 后端启动脚本
├── 🌐 start_frontend.sh     # 前端启动脚本
├── 🐳 docker-compose.yml    # Docker编排
├── 🎮 demo.py              # 演示脚本
└── 📚 文档文件
```

## 🔧 功能特性

### 前端功能
- 📋 **智能表单**: 用户友好的旅行规划输入界面
- 🔄 **实时进度**: 显示多智能体协作的实时进度
- 📊 **结果展示**: 结构化展示各智能体的专业建议
- 📥 **报告下载**: 支持下载完整的规划报告

### 后端功能
- 🚀 **异步处理**: 支持多个并发规划任务
- 📡 **RESTful API**: 标准化的API接口
- 💾 **状态管理**: 实时跟踪任务状态和进度
- 📁 **文件服务**: 自动保存和提供下载服务

### 智能体功能
- 🤖 **多智能体协作**: 基于LangGraph的状态图管理
- 🔍 **实时搜索**: 集成DuckDuckGo获取最新信息
- 🧠 **智能分析**: Google Gemini Flash-2.0驱动的AI分析
- 📈 **迭代优化**: 智能体间的协作和优化

## 🐳 Docker部署

```bash
# 一键启动所有服务
docker-compose up --build -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

## 🔗 API接口

### 主要端点

- `GET /` - API信息
- `GET /health` - 健康检查
- `POST /plan` - 创建旅行规划任务
- `GET /status/{task_id}` - 获取任务状态
- `GET /download/{task_id}` - 下载规划结果

### 使用示例

```python
import requests

# 创建规划任务
response = requests.post("http://localhost:8000/plan", json={
    "destination": "北京",
    "start_date": "2025-08-18",
    "end_date": "2025-08-25",
    "budget_range": "中等预算",
    "group_size": 2,
    "interests": ["历史", "美食"]
})

task_id = response.json()["task_id"]

# 查询进度
status = requests.get(f"http://localhost:8000/status/{task_id}")
```

## 🧪 测试和演示

```bash
# 运行完整演示
python demo.py
```

## 📚 文档

- 📖 **快速开始**: [QUICK_START.md](QUICK_START.md)
- 🚀 **部署指南**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- 🌐 **Web版说明**: [README_WEB.md](README_WEB.md)

## 🔧 环境要求

- Python 3.8+
- Google Gemini API密钥
- 8GB+ RAM (推荐)
- 网络连接 (用于实时搜索)

## 📄 许可证

本项目采用MIT许可证 - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 🎉 开始使用

```bash
# 克隆项目
git clone <repository-url>
cd langgraph_multi_agent_ai_travel_agent

# 设置API密钥
echo "GEMINI_API_KEY=your_api_key_here" > .env

# 启动服务
./start_backend.sh    # 终端1
./start_frontend.sh   # 终端2

# 访问: http://localhost:8501
```

祝您旅行愉快！🌍✈️
