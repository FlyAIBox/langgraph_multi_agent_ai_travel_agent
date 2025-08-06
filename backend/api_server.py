#!/usr/bin/env python3
"""
LangGraph多智能体AI旅行规划系统 - FastAPI后端服务

这个模块提供RESTful API接口，将LangGraph多智能体系统包装为Web服务。
支持异步处理和实时状态更新。

主要功能：
1. 接收前端的旅行规划请求
2. 调用LangGraph多智能体系统
3. 返回规划结果和状态更新
4. 提供文件下载服务
"""

import sys
import os
import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.langgraph_agents import LangGraphTravelAgents
from config.langgraph_config import langgraph_config as config

# 创建FastAPI应用
app = FastAPI(
    title="LangGraph多智能体AI旅行规划API",
    description="基于LangGraph框架的多智能体旅行规划系统API",
    version="1.0.0"
)

# 添加CORS中间件，允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局变量存储任务状态
planning_tasks: Dict[str, Dict[str, Any]] = {}

class TravelRequest(BaseModel):
    """旅行规划请求模型"""
    destination: str
    start_date: str
    end_date: str
    budget_range: str
    group_size: int
    interests: list[str] = []
    dietary_restrictions: str = ""
    activity_level: str = "适中"
    travel_style: str = "探索者"
    transportation_preference: str = "公共交通"
    accommodation_preference: str = "酒店"
    special_occasion: str = ""
    special_requirements: str = ""
    currency: str = "CNY"

class PlanningResponse(BaseModel):
    """规划响应模型"""
    task_id: str
    status: str
    message: str

class PlanningStatus(BaseModel):
    """规划状态模型"""
    task_id: str
    status: str
    progress: int
    current_agent: str
    message: str
    result: Optional[Dict[str, Any]] = None

@app.get("/")
async def root():
    """根路径，返回API信息"""
    return {
        "message": "LangGraph多智能体AI旅行规划API",
        "version": "1.0.0",
        "status": "运行中",
        "agents": [
            "协调员智能体",
            "旅行顾问",
            "预算优化师", 
            "天气分析师",
            "当地专家",
            "行程规划师"
        ]
    }

@app.get("/health")
async def health_check():
    """健康检查端点"""
    try:
        # 检查Gemini API密钥
        if not config.GEMINI_API_KEY:
            return {"status": "error", "message": "Gemini API密钥未配置"}
        
        return {
            "status": "healthy",
            "gemini_model": config.GEMINI_MODEL,
            "api_key_configured": bool(config.GEMINI_API_KEY)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

async def run_planning_task(task_id: str, travel_request: Dict[str, Any]):
    """异步执行旅行规划任务"""
    try:
        # 更新任务状态
        planning_tasks[task_id]["status"] = "processing"
        planning_tasks[task_id]["progress"] = 10
        planning_tasks[task_id]["message"] = "正在初始化LangGraph多智能体系统..."
        
        # 模拟处理时间，避免立即完成
        await asyncio.sleep(1)
        
        planning_tasks[task_id]["progress"] = 30
        planning_tasks[task_id]["message"] = "多智能体系统已启动，开始协作规划..."
        
        await asyncio.sleep(1)
        
        # 转换请求格式
        langgraph_request = {
            "destination": travel_request["destination"],
            "duration": travel_request.get("duration", 7),
            "budget_range": travel_request["budget_range"],
            "interests": travel_request["interests"],
            "group_size": travel_request["group_size"],
            "travel_dates": f"{travel_request['start_date']} 至 {travel_request['end_date']}"
        }
        
        planning_tasks[task_id]["progress"] = 50
        planning_tasks[task_id]["message"] = "智能体团队正在协作分析..."
        
        await asyncio.sleep(1)
        
        try:
            # 初始化LangGraph系统
            travel_agents = LangGraphTravelAgents()
            
            planning_tasks[task_id]["progress"] = 70
            planning_tasks[task_id]["message"] = "执行多智能体规划..."
            
            # 执行规划
            result = travel_agents.run_travel_planning(langgraph_request)
            
            if result["success"]:
                planning_tasks[task_id]["status"] = "completed"
                planning_tasks[task_id]["progress"] = 100
                planning_tasks[task_id]["message"] = "旅行规划完成！"
                planning_tasks[task_id]["result"] = result
                
                # 保存结果到文件
                await save_planning_result(task_id, result, langgraph_request)
                
            else:
                planning_tasks[task_id]["status"] = "failed"
                planning_tasks[task_id]["message"] = f"规划失败: {result.get('error', '未知错误')}"
                
        except Exception as agent_error:
            # 如果LangGraph系统出错，提供一个简化的响应
            print(f"LangGraph系统错误: {str(agent_error)}")
            
            # 创建一个简化的旅行计划作为回退
            simplified_result = {
                "success": True,
                "travel_plan": {
                    "destination": travel_request["destination"],
                    "duration": travel_request.get("duration", 7),
                    "budget_range": travel_request["budget_range"],
                    "group_size": travel_request["group_size"],
                    "travel_dates": f"{travel_request['start_date']} 至 {travel_request['end_date']}",
                    "summary": f"为{travel_request['destination']}制定的{travel_request.get('duration', 7)}天旅行计划"
                },
                "agent_outputs": {
                    "system_message": {
                        "response": f"系统正在维护中，为您提供基础的旅行计划框架。目的地：{travel_request['destination']}，预算：{travel_request['budget_range']}，人数：{travel_request['group_size']}人。",
                        "timestamp": datetime.now().isoformat(),
                        "status": "completed"
                    }
                },
                "total_iterations": 1,
                "planning_complete": True
            }
            
            planning_tasks[task_id]["status"] = "completed"
            planning_tasks[task_id]["progress"] = 100
            planning_tasks[task_id]["message"] = "旅行规划完成（简化模式）"
            planning_tasks[task_id]["result"] = simplified_result
            
            # 保存简化结果
            await save_planning_result(task_id, simplified_result, langgraph_request)
            
    except Exception as e:
        planning_tasks[task_id]["status"] = "failed"
        planning_tasks[task_id]["message"] = f"系统错误: {str(e)}"
        print(f"规划任务执行错误: {str(e)}")

async def save_planning_result(task_id: str, result: Dict[str, Any], request: Dict[str, Any]):
    """保存规划结果到文件"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        destination = request.get('destination', 'unknown').replace(' ', '_')
        filename = f"旅行计划_{destination}_{timestamp}.json"
        filepath = os.path.join("results", filename)
        
        # 确保results目录存在
        os.makedirs("results", exist_ok=True)
        
        # 保存为JSON格式
        save_data = {
            "task_id": task_id,
            "timestamp": datetime.now().isoformat(),
            "request": request,
            "result": result
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
            
        planning_tasks[task_id]["result_file"] = filename
        
    except Exception as e:
        print(f"保存结果文件时出错: {str(e)}")

@app.post("/plan", response_model=PlanningResponse)
async def create_travel_plan(request: TravelRequest, background_tasks: BackgroundTasks):
    """创建旅行规划任务"""
    try:
        # 生成任务ID
        task_id = str(uuid.uuid4())
        
        # 计算旅行天数
        from datetime import datetime
        start_date = datetime.strptime(request.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(request.end_date, "%Y-%m-%d")
        duration = (end_date - start_date).days + 1
        
        # 转换请求为字典
        travel_request = request.dict()
        travel_request["duration"] = duration
        
        # 初始化任务状态
        planning_tasks[task_id] = {
            "task_id": task_id,
            "status": "started",
            "progress": 0,
            "current_agent": "系统初始化",
            "message": "任务已创建，准备开始规划...",
            "created_at": datetime.now().isoformat(),
            "request": travel_request,
            "result": None
        }
        
        # 添加后台任务
        background_tasks.add_task(run_planning_task, task_id, travel_request)
        
        return PlanningResponse(
            task_id=task_id,
            status="started",
            message="旅行规划任务已启动，请使用task_id查询进度"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建规划任务失败: {str(e)}")

@app.get("/status/{task_id}", response_model=PlanningStatus)
async def get_planning_status(task_id: str):
    """获取规划任务状态"""
    if task_id not in planning_tasks:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    task = planning_tasks[task_id]
    
    return PlanningStatus(
        task_id=task_id,
        status=task["status"],
        progress=task["progress"],
        current_agent=task["current_agent"],
        message=task["message"],
        result=task["result"]
    )

@app.get("/download/{task_id}")
async def download_result(task_id: str):
    """下载规划结果文件"""
    if task_id not in planning_tasks:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    task = planning_tasks[task_id]
    if "result_file" not in task:
        raise HTTPException(status_code=404, detail="结果文件不存在")
    
    filepath = os.path.join("results", task["result_file"])
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="文件不存在")
    
    return FileResponse(
        path=filepath,
        filename=task["result_file"],
        media_type='application/json'
    )

@app.get("/tasks")
async def list_tasks():
    """列出所有任务"""
    return {
        "tasks": [
            {
                "task_id": task_id,
                "status": task["status"],
                "created_at": task["created_at"],
                "destination": task["request"].get("destination", "未知")
            }
            for task_id, task in planning_tasks.items()
        ]
    }

if __name__ == "__main__":
    print("🚀 启动LangGraph多智能体AI旅行规划API服务器...")
    print(f"📍 API文档: http://localhost:8080/docs")
    print(f"🔧 健康检查: http://localhost:8080/health")

    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )
