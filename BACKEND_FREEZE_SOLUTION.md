# 🔧 后端假死问题解决方案

## 🚨 问题分析

根据您提供的日志，问题出现在：
```
任务 b5c995bb-235b-4566-82b9-9f4159e20632: 执行旅行规划
```

这表明LangGraph的`travel_agents.run_travel_planning()`方法卡住了，导致整个后端进入假死状态。

## ✅ 立即解决方案

### 方案1: 重启后端服务（推荐）

```bash
# 使用重启脚本
./restart_backend.sh
```

### 方案2: 手动重启

```bash
# 1. 杀死后端进程
pkill -f api_server.py

# 2. 检查端口
lsof -i :8080

# 3. 强制释放端口（如果需要）
lsof -ti :8080 | xargs kill -9

# 4. 重新启动
cd backend
conda activate ai-travel-agents
python api_server.py
```

## 🛠️ 系统改进

我已经对系统进行了以下改进来防止假死：

### 1. 添加超时机制
- LangGraph执行超时：4分钟
- 使用线程池避免阻塞
- 超时后自动切换到简化版本

### 2. 备选方案
- **简化智能体**: 当LangGraph失败时自动使用
- **模拟智能体**: 用于快速测试

### 3. 新增API端点

```bash
# 简化版规划（推荐用于测试）
curl -X POST http://localhost:8080/simple-plan \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "北京",
    "start_date": "2025-08-20",
    "end_date": "2025-08-22",
    "budget_range": "中等预算",
    "group_size": 2,
    "interests": ["历史"]
  }'

# 模拟规划（立即返回结果）
curl -X POST http://localhost:8080/mock-plan \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "上海",
    "start_date": "2025-08-20",
    "end_date": "2025-08-22",
    "budget_range": "中等预算",
    "group_size": 1,
    "interests": ["文化"]
  }'
```

## 🎯 使用建议

### 当前任务处理

1. **重启后端服务**:
   ```bash
   ./restart_backend.sh
   ```

2. **检查之前的任务**:
   ```bash
   python check_task_status.py b5c995bb-235b-4566-82b9-9f4159e20632
   ```

3. **如果任务丢失，使用简化版本重新创建**:
   - 访问前端页面
   - 或使用`/simple-plan`端点

### 未来使用策略

1. **测试阶段**: 使用`/mock-plan`或`/simple-plan`
2. **生产使用**: 使用主要的`/plan`端点（已有超时保护）
3. **复杂规划**: 简化请求参数，减少兴趣爱好数量

## 🔍 问题预防

### 1. 简化请求
```json
{
  "destination": "北京",
  "start_date": "2025-08-20",
  "end_date": "2025-08-22",
  "budget_range": "中等预算",
  "group_size": 2,
  "interests": ["历史"]  // 限制1-2个兴趣
}
```

### 2. 监控日志
```bash
# 实时查看后端日志
cd backend
python api_server.py | tee backend.log
```

### 3. 使用任务监控页面
```bash
# 启动监控页面
./start_task_monitor.sh
# 访问: http://localhost:8502
```

## 📊 系统状态检查

### 检查后端健康
```bash
curl http://localhost:8080/health
```

### 检查所有任务
```bash
curl http://localhost:8080/tasks
```

### 测试基本功能
```bash
curl -X POST http://localhost:8080/mock-plan \
  -H "Content-Type: application/json" \
  -d '{"destination": "测试", "start_date": "2025-08-20", "end_date": "2025-08-22", "budget_range": "中等预算", "group_size": 1, "interests": []}'
```

## 🚀 推荐操作流程

### 立即操作：
1. 运行 `./restart_backend.sh`
2. 等待后端完全启动
3. 使用 `/simple-plan` 端点测试
4. 如果成功，再尝试正常的 `/plan` 端点

### 长期使用：
1. 优先使用简化版本进行测试
2. 对于复杂规划，逐步增加参数复杂度
3. 定期重启后端服务以保持稳定性
4. 使用任务监控页面跟踪长时间运行的任务

## 💡 技术说明

### 假死原因
- LangGraph的多智能体协作可能在某些情况下陷入无限循环
- Google API调用可能超时但没有正确处理
- 内存泄漏或资源竞争

### 解决机制
- 线程池隔离：避免主线程阻塞
- 超时保护：4分钟后自动终止
- 备选方案：简化智能体作为后备
- 错误恢复：自动切换到可用的方案

现在您可以重启后端并继续使用系统了！🎉
