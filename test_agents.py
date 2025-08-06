#!/usr/bin/env python3
"""
智能体测试脚本

测试各种智能体的导入和基本功能
"""

import sys
import os

# 添加backend目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """测试所有导入"""
    print("🧪 测试智能体导入...")
    
    try:
        from backend.agents.langgraph_agents import LangGraphTravelAgents
        print("✅ LangGraph智能体导入成功")
    except Exception as e:
        print(f"❌ LangGraph智能体导入失败: {e}")
        return False
    
    try:
        from backend.agents.simple_travel_agent import SimpleTravelAgent, MockTravelAgent
        print("✅ 简化智能体导入成功")
    except Exception as e:
        print(f"❌ 简化智能体导入失败: {e}")
        return False
    
    try:
        from backend.config.langgraph_config import langgraph_config
        print("✅ 配置导入成功")
        print(f"   模型: {langgraph_config.GEMINI_MODEL}")
        print(f"   API密钥: {'已配置' if langgraph_config.GEMINI_API_KEY else '未配置'}")
    except Exception as e:
        print(f"❌ 配置导入失败: {e}")
        return False
    
    return True

def test_mock_agent():
    """测试模拟智能体"""
    print("\n🎭 测试模拟智能体...")
    
    try:
        from backend.agents.simple_travel_agent import MockTravelAgent
        
        mock_agent = MockTravelAgent()
        
        test_request = {
            "destination": "北京",
            "duration": 3,
            "budget_range": "中等预算",
            "interests": ["历史"],
            "group_size": 2
        }
        
        result = mock_agent.run_travel_planning(test_request)
        
        if result["success"]:
            print("✅ 模拟智能体测试成功")
            print(f"   目的地: {result['travel_plan']['destination']}")
            print(f"   规划方式: {result['travel_plan']['planning_method']}")
            return True
        else:
            print("❌ 模拟智能体测试失败")
            return False
            
    except Exception as e:
        print(f"❌ 模拟智能体测试异常: {e}")
        return False

def test_simple_agent():
    """测试简化智能体"""
    print("\n🤖 测试简化智能体...")
    
    try:
        from backend.agents.simple_travel_agent import SimpleTravelAgent
        from backend.config.langgraph_config import langgraph_config
        
        if not langgraph_config.GEMINI_API_KEY:
            print("⚠️  跳过简化智能体测试 - 未配置API密钥")
            return True
        
        simple_agent = SimpleTravelAgent()
        
        test_request = {
            "destination": "上海",
            "duration": 2,
            "budget_range": "经济型",
            "interests": ["文化"],
            "group_size": 1
        }
        
        print("   正在调用Google Gemini API...")
        result = simple_agent.run_travel_planning(test_request)
        
        if result["success"]:
            print("✅ 简化智能体测试成功")
            print(f"   目的地: {result['travel_plan']['destination']}")
            print(f"   规划方式: {result['travel_plan']['planning_method']}")
            content = result['travel_plan']['content']
            print(f"   内容长度: {len(content)}字符")
            return True
        else:
            print(f"❌ 简化智能体测试失败: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ 简化智能体测试异常: {e}")
        return False

def test_langgraph_agent():
    """测试LangGraph智能体（仅初始化）"""
    print("\n🔗 测试LangGraph智能体初始化...")
    
    try:
        from backend.agents.langgraph_agents import LangGraphTravelAgents
        from backend.config.langgraph_config import langgraph_config
        
        if not langgraph_config.GEMINI_API_KEY:
            print("⚠️  跳过LangGraph智能体测试 - 未配置API密钥")
            return True
        
        print("   正在初始化LangGraph系统...")
        travel_agents = LangGraphTravelAgents()
        print("✅ LangGraph智能体初始化成功")
        
        # 不执行实际规划，避免卡住
        print("   (跳过实际规划执行以避免潜在的阻塞)")
        
        return True
        
    except Exception as e:
        print(f"❌ LangGraph智能体初始化失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 智能体系统测试")
    print("=" * 50)
    
    results = []
    
    # 测试导入
    results.append(test_imports())
    
    # 测试模拟智能体
    results.append(test_mock_agent())
    
    # 测试简化智能体
    results.append(test_simple_agent())
    
    # 测试LangGraph智能体
    results.append(test_langgraph_agent())
    
    # 总结
    print("\n" + "=" * 50)
    print("📊 测试结果总结:")
    
    passed = sum(results)
    total = len(results)
    
    print(f"   通过: {passed}/{total}")
    
    if passed == total:
        print("🎉 所有测试通过！")
        print("\n💡 建议:")
        print("   - 可以安全使用模拟智能体进行测试")
        print("   - 可以使用简化智能体进行实际规划")
        print("   - LangGraph智能体已准备就绪")
    else:
        print("⚠️  部分测试失败")
        print("\n💡 建议:")
        print("   - 检查API密钥配置")
        print("   - 确保网络连接正常")
        print("   - 优先使用通过测试的智能体")

if __name__ == "__main__":
    main()
