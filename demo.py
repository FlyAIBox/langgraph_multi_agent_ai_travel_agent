#!/usr/bin/env python3
"""
LangGraph多智能体AI旅行规划系统 - 演示脚本

这个脚本演示如何使用Web版本的API接口进行旅行规划。
"""

import requests
import json
import time
import sys
from datetime import datetime, date, timedelta

def print_header():
    """打印演示标题"""
    print("🌍" + "="*60 + "🌍")
    print("    LangGraph多智能体AI旅行规划系统 - Web版演示")
    print("🌍" + "="*60 + "🌍")
    print()

def check_services():
    """检查服务状态"""
    print("🔍 检查服务状态...")
    
    # 检查后端API
    try:
        response = requests.get("http://localhost:8080/health", timeout=5)
        if response.status_code == 200:
            print("✅ 后端API服务: 正常运行")
            health_data = response.json()
            print(f"   模型: {health_data.get('gemini_model', '未知')}")
            print(f"   API密钥: {'已配置' if health_data.get('api_key_configured') else '❌ 未配置'}")
        else:
            print("❌ 后端API服务: 异常")
            return False
    except Exception as e:
        print("❌ 后端API服务: 无法连接")
        print(f"   错误: {str(e)}")
        print("   请运行: ./start_backend.sh")
        return False
    
    # 检查前端服务
    try:
        response = requests.get("http://localhost:8501/_stcore/health", timeout=5)
        if response.status_code == 200:
            print("✅ 前端Web服务: 正常运行")
        else:
            print("⚠️  前端Web服务: 可能异常")
    except Exception as e:
        print("⚠️  前端Web服务: 无法连接")
        print("   请运行: ./start_frontend.sh")
    
    print()
    return True

def create_demo_plan():
    """创建演示旅行规划"""
    print("🚀 创建演示旅行规划...")
    
    # 演示数据
    demo_data = {
        "destination": "北京",
        "start_date": (date.today() + timedelta(days=30)).strftime("%Y-%m-%d"),
        "end_date": (date.today() + timedelta(days=37)).strftime("%Y-%m-%d"),
        "budget_range": "中等预算",
        "group_size": 2,
        "interests": ["历史", "文化", "美食", "建筑"],
        "dietary_restrictions": "",
        "activity_level": "适中",
        "travel_style": "探索者",
        "transportation_preference": "公共交通",
        "accommodation_preference": "酒店",
        "special_requirements": "希望体验当地文化",
        "currency": "CNY"
    }
    
    print("📋 规划参数:")
    print(f"   目的地: {demo_data['destination']}")
    print(f"   日期: {demo_data['start_date']} 至 {demo_data['end_date']}")
    print(f"   人数: {demo_data['group_size']} 人")
    print(f"   预算: {demo_data['budget_range']}")
    print(f"   兴趣: {', '.join(demo_data['interests'])}")
    print()
    
    try:
        response = requests.post("http://localhost:8080/plan", json=demo_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            task_id = result["task_id"]
            print(f"✅ 任务创建成功!")
            print(f"   任务ID: {task_id}")
            print(f"   状态: {result['status']}")
            return task_id
        else:
            print(f"❌ 任务创建失败: {response.status_code}")
            print(f"   错误: {response.text}")
            return None
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")
        return None

def monitor_progress(task_id):
    """监控规划进度"""
    print(f"🔄 监控规划进度...")
    print("   多智能体协作中，请稍候...")
    print()
    
    max_attempts = 120  # 最多等待2分钟
    attempt = 0
    last_progress = -1
    
    while attempt < max_attempts:
        try:
            response = requests.get(f"http://localhost:8080/status/{task_id}", timeout=5)
            if response.status_code == 200:
                status = response.json()
                progress = status['progress']
                current_status = status['status']
                message = status['message']
                
                # 只在进度变化时打印
                if progress != last_progress:
                    print(f"📊 进度: {progress:3d}% | 状态: {current_status:10s} | {message}")
                    last_progress = progress
                
                if current_status == 'completed':
                    print()
                    print("🎉 规划完成!")
                    return status
                elif current_status == 'failed':
                    print()
                    print(f"❌ 规划失败: {message}")
                    return None
                    
            time.sleep(2)
            attempt += 1
            
        except Exception as e:
            print(f"❌ 状态查询失败: {str(e)}")
            return None
    
    print("⏰ 规划超时")
    return None

def display_results(result):
    """显示规划结果"""
    if not result or not result.get('result'):
        return
    
    print("📋 规划结果摘要:")
    print("="*50)
    
    travel_plan = result['result'].get('travel_plan', {})
    agent_outputs = result['result'].get('agent_outputs', {})
    
    # 基本信息
    print(f"🌍 目的地: {travel_plan.get('destination', '未知')}")
    print(f"📅 行程: {travel_plan.get('duration', 0)} 天")
    print(f"👥 人数: {travel_plan.get('group_size', 0)} 人")
    print(f"💰 预算: {travel_plan.get('budget_range', '未知')}")
    print(f"🎯 兴趣: {', '.join(travel_plan.get('interests', []))}")
    print()
    
    # 智能体贡献
    print("🤖 智能体贡献:")
    print("-"*30)
    
    agent_names = {
        'travel_advisor': '🏛️ 旅行顾问',
        'weather_analyst': '🌤️ 天气分析师',
        'budget_optimizer': '💰 预算优化师',
        'local_expert': '🏠 当地专家',
        'itinerary_planner': '📅 行程规划师'
    }
    
    for agent_name, output in agent_outputs.items():
        display_name = agent_names.get(agent_name, agent_name)
        status = output.get('status', '未知')
        response = output.get('response', '无输出')
        
        print(f"{display_name}: {status.upper()}")
        
        # 显示前200个字符的建议
        if response and len(response) > 200:
            preview = response[:200] + "..."
        else:
            preview = response
            
        print(f"   建议: {preview}")
        print()

def download_result(task_id):
    """下载规划结果"""
    print("📥 下载完整规划报告...")
    
    try:
        response = requests.get(f"http://localhost:8080/download/{task_id}", timeout=10)
        if response.status_code == 200:
            filename = f"demo_travel_plan_{task_id[:8]}.json"
            with open(f"results/{filename}", 'wb') as f:
                f.write(response.content)
            print(f"✅ 报告已保存到: results/{filename}")
            return True
        else:
            print(f"❌ 下载失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 下载失败: {str(e)}")
        return False

def show_access_info():
    """显示访问信息"""
    print("🌐 Web界面访问信息:")
    print("="*40)
    print("📱 前端界面: http://localhost:8501")
    print("📚 API文档:  http://localhost:8080/docs")
    print("🔧 健康检查: http://localhost:8080/health")
    print()
    print("💡 提示:")
    print("   - 在浏览器中打开前端界面进行交互式规划")
    print("   - 查看API文档了解所有可用接口")
    print("   - 使用健康检查监控服务状态")

def main():
    """主演示函数"""
    print_header()
    
    # 1. 检查服务状态
    if not check_services():
        print("❌ 服务检查失败，请确保后端服务正在运行")
        sys.exit(1)
    
    # 2. 创建演示规划
    task_id = create_demo_plan()
    if not task_id:
        print("❌ 无法创建演示任务")
        sys.exit(1)
    
    # 3. 监控进度
    result = monitor_progress(task_id)
    if not result:
        print("❌ 规划过程失败")
        sys.exit(1)
    
    # 4. 显示结果
    display_results(result)
    
    # 5. 下载报告
    download_result(task_id)
    
    # 6. 显示访问信息
    show_access_info()
    
    print()
    print("🎉 演示完成! 现在您可以:")
    print("   1. 访问Web界面进行自定义规划")
    print("   2. 查看API文档了解更多功能")
    print("   3. 查看results目录中的规划报告")

if __name__ == "__main__":
    main()
