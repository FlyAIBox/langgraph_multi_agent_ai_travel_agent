# 🚀 LangGraph多智能体AI旅行规划系统 - 快速开始

## 📋 系统概述

基于您现有的LangGraph多智能体旅行规划系统，我们已经创建了一个完整的Web版本，包含：

- **🌐 Streamlit前端**: 用户友好的Web界面
- **⚡ FastAPI后端**: 高性能的API服务
- **🤖 LangGraph智能体**: 原有的多智能体协作系统
- **📊 实时监控**: 规划进度和状态跟踪
- **📥 文件下载**: 完整的规划报告导出

## 🎯 智能体团队

| 智能体 | 职责 | 功能 |
|--------|------|------|
| 🎯 协调员智能体 | 工作流编排与决策综合 | 统筹整个规划流程 |
| ✈️ 旅行顾问 | 目的地专业知识与实时搜索 | 提供目的地信息和建议 |
| 💰 预算优化师 | 成本分析与实时定价 | 优化预算分配和成本控制 |
| 🌤️ 天气分析师 | 天气情报与当前数据 | 提供天气预报和建议 |
| 🏠 当地专家 | 内部知识与实时本地信息 | 提供当地文化和实用信息 |
| 📅 行程规划师 | 日程优化与物流安排 | 制定详细的行程安排 |

## ⚡ 5分钟快速启动

### 1. 环境准备
```bash
# 确保您有Google Gemini API密钥
# 获取地址: https://makersuite.google.com/app/apikey

# 创建环境变量文件
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

### 2. 启动系统
```bash
# 方法一：使用启动脚本（推荐）
# 终端1 - 启动后端
./start_backend.sh

# 终端2 - 启动前端
./start_frontend.sh
```

### 3. 访问应用
- 🌐 **前端界面**: http://localhost:8501
- 📚 **API文档**: http://localhost:8000/docs

### 4. 体验演示
```bash
# 运行完整演示
python demo.py
```

## 🎮 使用指南

### Web界面使用

1. **打开浏览器访问**: http://localhost:8501

2. **填写旅行信息**:
   - 📍 目的地城市
   - 📅 旅行日期
   - 💰 预算范围
   - 👥 旅行人数
   - 🎯 兴趣爱好

3. **点击"开始AI智能规划"**

4. **观看实时进度**:
   - 多智能体协作过程
   - 实时状态更新
   - 进度百分比显示

5. **查看规划结果**:
   - 行程概览
   - 各智能体专业建议
   - 详细规划内容

6. **下载完整报告**

### API接口使用

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

# 下载结果
result = requests.get(f"http://localhost:8000/download/{task_id}")
```

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
│   ├── config/             # 配置文件
│   ├── agents/             # LangGraph智能体
│   ├── tools/              # 工具模块
│   └── modules/            # 功能模块
├── 📊 results/              # 规划结果存储
├── 🚀 start_backend.sh      # 后端启动脚本
├── 🌐 start_frontend.sh     # 前端启动脚本
├── 🐳 docker-compose.yml    # Docker编排
├── 🎮 demo.py              # 演示脚本
└── 📚 文档文件
```

## 🔧 高级功能

### Docker部署
```bash
# 一键启动所有服务
docker-compose up --build -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 演示和测试
```bash
# 运行完整演示
python demo.py
```

### 自定义配置
```bash
# 编辑配置文件
vim backend/config/langgraph_config.py

# 修改智能体行为
vim backend/agents/langgraph_agents.py
```

## 🎯 功能特色

### 🌐 前端特色
- ✨ **现代化界面**: 基于Streamlit的响应式设计
- 📱 **移动友好**: 支持手机和平板访问
- 🔄 **实时更新**: 动态显示规划进度
- 📊 **可视化展示**: 图表和指标展示
- 💾 **一键下载**: 支持多种格式导出

### ⚡ 后端特色
- 🚀 **高性能**: 异步处理，支持并发
- 📡 **RESTful API**: 标准化接口设计
- 🔍 **实时监控**: 任务状态跟踪
- 📁 **文件管理**: 自动保存和下载
- 🛡️ **错误处理**: 完善的异常处理机制

### 🤖 智能体特色
- 🧠 **协作智能**: 多智能体协同工作
- 🔍 **实时搜索**: DuckDuckGo集成
- 🎯 **专业分工**: 每个智能体专注特定领域
- 📈 **迭代优化**: 智能体间相互优化
- 🌍 **全球支持**: 支持多种语言和地区

## 🆚 版本对比

| 功能 | 命令行版本 | Web版本 |
|------|------------|---------|
| 用户界面 | 命令行交互 | ✅ Web界面 |
| 实时进度 | 文本输出 | ✅ 可视化进度条 |
| 结果展示 | 文本格式 | ✅ 结构化展示 |
| 文件下载 | 本地保存 | ✅ Web下载 |
| 并发支持 | 单任务 | ✅ 多任务并发 |
| API接口 | 无 | ✅ RESTful API |
| 部署方式 | 本地运行 | ✅ 多种部署方式 |

## 🔗 相关链接

- 📚 **详细文档**: [README_WEB.md](README_WEB.md)
- 🚀 **部署指南**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- 🎮 **演示脚本**: [demo.py](demo.py)

## 💡 使用技巧

1. **首次使用**: 建议先运行演示脚本了解系统功能
2. **自定义规划**: 在Web界面中详细填写您的需求
3. **API集成**: 可以将API集成到您的其他应用中
4. **结果分析**: 下载的JSON文件包含完整的规划数据
5. **性能优化**: 可以通过配置文件调整智能体参数

## 🎉 开始体验

现在您可以开始体验这个强大的多智能体旅行规划系统了！

```bash
# 快速启动
./start_backend.sh    # 终端1
./start_frontend.sh   # 终端2

# 然后访问: http://localhost:8501
```

祝您旅行愉快！🌍✈️
