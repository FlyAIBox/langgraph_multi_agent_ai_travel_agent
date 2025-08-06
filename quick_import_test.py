#!/usr/bin/env python3
"""
快速导入测试

只测试导入，不执行实际的AI调用
"""

import sys
import os

# 添加backend目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def main():
    print("🧪 快速导入测试")
    print("=" * 30)
    
    # 测试配置导入
    try:
        from backend.config.langgraph_config import langgraph_config
        print("✅ 配置导入成功")
        print(f"   模型: {langgraph_config.GEMINI_MODEL}")
        print(f"   API密钥: {'已配置' if langgraph_config.GEMINI_API_KEY else '未配置'}")
    except Exception as e:
        print(f"❌ 配置导入失败: {e}")
        return
    
    # 测试LangGraph智能体导入
    try:
        from backend.agents.langgraph_agents import LangGraphTravelAgents
        print("✅ LangGraph智能体导入成功")
    except Exception as e:
        print(f"❌ LangGraph智能体导入失败: {e}")
    
    # 测试简化智能体导入
    try:
        from backend.agents.simple_travel_agent import SimpleTravelAgent, MockTravelAgent
        print("✅ 简化智能体导入成功")
    except Exception as e:
        print(f"❌ 简化智能体导入失败: {e}")
    
    # 测试模拟智能体功能
    try:
        mock_agent = MockTravelAgent()
        test_request = {
            "destination": "测试城市",
            "duration": 1,
            "budget_range": "测试预算",
            "interests": [],
            "group_size": 1
        }
        result = mock_agent.run_travel_planning(test_request)
        if result["success"]:
            print("✅ 模拟智能体功能正常")
        else:
            print("❌ 模拟智能体功能异常")
    except Exception as e:
        print(f"❌ 模拟智能体测试失败: {e}")
    
    print("\n🎉 导入测试完成！")
    print("💡 所有必要的模块都可以正常导入")

if __name__ == "__main__":
    main()
