#!/usr/bin/env python3
"""
任务状态检查工具

用于检查特定任务的状态和结果
"""

import requests
import json
import sys
from datetime import datetime

API_BASE_URL = "http://localhost:8080"

def check_task_status(task_id):
    """检查任务状态"""
    print(f"🔍 检查任务状态: {task_id}")
    print("-" * 50)
    
    try:
        response = requests.get(f"{API_BASE_URL}/status/{task_id}", timeout=10)
        if response.status_code == 200:
            status = response.json()
            
            print(f"✅ 任务状态获取成功")
            print(f"   状态: {status.get('status')}")
            print(f"   进度: {status.get('progress')}%")
            print(f"   消息: {status.get('message')}")
            print(f"   当前智能体: {status.get('current_agent')}")
            
            if status.get('status') == 'completed':
                print(f"\n🎉 任务已完成！")
                result = status.get('result')
                if result:
                    travel_plan = result.get('travel_plan', {})
                    print(f"   目的地: {travel_plan.get('destination')}")
                    print(f"   行程天数: {travel_plan.get('duration')}")
                    print(f"   团队人数: {travel_plan.get('group_size')}")
                    
                    # 尝试下载结果
                    download_result(task_id)
                    
            elif status.get('status') == 'failed':
                print(f"\n❌ 任务失败: {status.get('message')}")
                
            elif status.get('status') == 'processing':
                print(f"\n🔄 任务正在处理中...")
                print(f"   建议等待几分钟后再次检查")
                
            return status
            
        elif response.status_code == 404:
            print(f"❌ 任务不存在")
            return None
        else:
            print(f"❌ 状态查询失败: HTTP {response.status_code}")
            return None
            
    except requests.exceptions.Timeout:
        print(f"❌ 请求超时")
        return None
    except requests.exceptions.ConnectionError:
        print(f"❌ 无法连接到API服务器")
        print(f"   请确保后端服务正在运行: cd backend && python api_server.py")
        return None
    except Exception as e:
        print(f"❌ 检查失败: {str(e)}")
        return None

def download_result(task_id):
    """下载任务结果"""
    print(f"\n📥 尝试下载结果...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/download/{task_id}", timeout=15)
        if response.status_code == 200:
            filename = f"travel_plan_{task_id[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ 结果已下载到: {filename}")
            
            # 显示结果摘要
            try:
                data = json.loads(response.content)
                print(f"\n📋 结果摘要:")
                if 'result' in data and 'travel_plan' in data['result']:
                    plan = data['result']['travel_plan']
                    print(f"   目的地: {plan.get('destination', '未知')}")
                    print(f"   规划方法: {plan.get('planning_method', '未知')}")
                    
                if 'result' in data and 'agent_outputs' in data['result']:
                    agents = data['result']['agent_outputs']
                    print(f"   参与智能体: {len(agents)}个")
                    for agent_name in agents.keys():
                        print(f"     - {agent_name}")
                        
            except json.JSONDecodeError:
                print(f"   (无法解析结果内容)")
                
        else:
            print(f"❌ 下载失败: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ 下载异常: {str(e)}")

def list_all_tasks():
    """列出所有任务"""
    print(f"📋 获取所有任务列表...")
    print("-" * 50)
    
    try:
        response = requests.get(f"{API_BASE_URL}/tasks", timeout=10)
        if response.status_code == 200:
            data = response.json()
            tasks = data.get('tasks', [])
            
            if not tasks:
                print(f"📭 暂无任务")
                return
                
            print(f"✅ 找到 {len(tasks)} 个任务:")
            print()
            
            for i, task in enumerate(tasks, 1):
                task_id = task.get('task_id', 'unknown')
                status = task.get('status', 'unknown')
                created_at = task.get('created_at', 'unknown')
                destination = task.get('destination', 'unknown')
                
                print(f"{i}. 任务ID: {task_id[:8]}...")
                print(f"   状态: {status}")
                print(f"   目的地: {destination}")
                print(f"   创建时间: {created_at[:19] if created_at != 'unknown' else 'unknown'}")
                print()
                
        else:
            print(f"❌ 获取任务列表失败: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ 获取任务列表异常: {str(e)}")

def main():
    """主函数"""
    print("🔧 LangGraph任务状态检查工具")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print(f"  python {sys.argv[0]} <task_id>     # 检查特定任务")
        print(f"  python {sys.argv[0]} --list       # 列出所有任务")
        print()
        print("示例:")
        print(f"  python {sys.argv[0]} 521f1fcf-2591-4b1a-9bc3-c654ae09c690")
        print(f"  python {sys.argv[0]} --list")
        return
    
    if sys.argv[1] == "--list":
        list_all_tasks()
    else:
        task_id = sys.argv[1]
        check_task_status(task_id)

if __name__ == "__main__":
    main()
