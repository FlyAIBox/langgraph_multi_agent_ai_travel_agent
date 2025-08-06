# AI旅行规划智能体 - Web版本

🌍 基于LangGraph框架、Google Gemini Flash-2.0和DuckDuckGo搜索的智能旅行规划Web应用

## 🎯 系统架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   FastAPI       │    │   LangGraph     │
│   前端界面      │◄──►│   后端API       │◄──►│   多智能体系统  │
│                 │    │                 │    │                 │
│ • 用户表单      │    │ • RESTful API   │    │ • 协调员智能体  │
│ • 进度显示      │    │ • 异步处理      │    │ • 旅行顾问      │
│ • 结果展示      │    │ • 状态管理      │    │ • 预算优化师    │
│ • 文件下载      │    │ • 文件服务      │    │ • 天气分析师    │
└─────────────────┘    └─────────────────┘    │ • 当地专家      │
                                              │ • 行程规划师    │
                                              └─────────────────┘
```

## 🚀 快速开始

### 1. 环境准备

确保您的系统已安装：
- Python 3.8+
- pip
- curl (用于健康检查)

### 2. 配置API密钥

创建 `.env` 文件并添加您的Google Gemini API密钥：

```bash
GEMINI_API_KEY=your_api_key_here
```

获取API密钥：https://makersuite.google.com/app/apikey

### 3. 启动系统

#### 方法一：使用启动脚本（推荐）

```bash
# 启动后端服务（在终端1中）
./start_backend.sh

# 启动前端应用（在终端2中）
./start_frontend.sh
```

#### 方法二：手动启动

**启动后端：**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python api_server.py
```

**启动前端：**
```bash
cd frontend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

### 4. 访问应用

- 🌐 **前端界面**: http://localhost:8501
- 📚 **API文档**: http://localhost:8000/docs
- 🔧 **健康检查**: http://localhost:8000/health

## 🎯 AI智能体团队

| 智能体 | 职责 | 功能 |
|--------|------|------|
| 🎯 协调员智能体 | 工作流编排与决策综合 | 统筹整个规划流程 |
| ✈️ 旅行顾问 | 目的地专业知识与实时搜索 | 提供目的地信息和建议 |
| 💰 预算优化师 | 成本分析与实时定价 | 优化预算分配和成本控制 |
| 🌤️ 天气分析师 | 天气情报与当前数据 | 提供天气预报和建议 |
| 🏠 当地专家 | 内部知识与实时本地信息 | 提供当地文化和实用信息 |
| 📅 行程规划师 | 日程优化与物流安排 | 制定详细的行程安排 |

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

## 📁 项目结构

```
langgraph_multi_agent_ai_travel_agent/
├── backend/                    # 后端服务
│   ├── api_server.py          # FastAPI服务器
│   ├── requirements.txt       # 后端依赖
│   ├── config/               # 配置文件
│   ├── agents/               # LangGraph智能体
│   ├── tools/                # 工具模块
│   ├── modules/              # 功能模块
│   └── utils/                # 工具函数
├── frontend/                  # 前端应用
│   ├── streamlit_app.py      # Streamlit主应用
│   └── requirements.txt      # 前端依赖
├── results/                  # 规划结果存储
├── start_backend.sh          # 后端启动脚本
├── start_frontend.sh         # 前端启动脚本
└── README_WEB.md            # 本文档
```

## 🔗 API接口

### 主要端点

- `GET /` - API信息
- `GET /health` - 健康检查
- `POST /plan` - 创建旅行规划任务
- `GET /status/{task_id}` - 获取任务状态
- `GET /download/{task_id}` - 下载规划结果
- `GET /tasks` - 列出所有任务

### 请求示例

```bash
# 创建规划任务
curl -X POST "http://localhost:8000/plan" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "北京",
    "start_date": "2025-08-18",
    "end_date": "2025-08-25",
    "budget_range": "中等预算",
    "group_size": 2,
    "interests": ["历史", "美食"]
  }'

# 查询任务状态
curl "http://localhost:8000/status/{task_id}"
```

## 🛠️ 开发指南

### 添加新的智能体

1. 在 `backend/agents/langgraph_agents.py` 中添加新的智能体方法
2. 在工作流图中注册新智能体
3. 更新状态转换逻辑

### 自定义前端界面

1. 修改 `frontend/streamlit_app.py` 中的表单组件
2. 添加新的显示组件
3. 更新样式和布局

### 扩展API功能

1. 在 `backend/api_server.py` 中添加新的端点
2. 定义相应的Pydantic模型
3. 更新API文档

## 🔍 故障排除

### 常见问题

1. **API服务无法启动**
   - 检查端口8000是否被占用
   - 确认GEMINI_API_KEY已正确设置

2. **前端无法连接后端**
   - 确认后端服务正在运行
   - 检查防火墙设置

3. **规划任务失败**
   - 检查API密钥是否有效
   - 查看后端日志获取详细错误信息

### 日志查看

```bash
# 查看后端日志
cd backend && python api_server.py

# 查看前端日志
cd frontend && streamlit run streamlit_app.py
```

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📞 支持

如有问题，请通过以下方式联系：
- 提交GitHub Issue
- 查看API文档：http://localhost:8000/docs
