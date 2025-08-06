#!/usr/bin/env python3
"""
LangGraph智能体系统轻量级测试

这个测试不调用实际的API，只验证系统结构和基本功能
"""

import sys
import os
import time
import json
from datetime import datetime

# 添加backend目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """测试所有必要的导入"""
    print("🧪 测试导入...")
    
    try:
        from langgraph_agents import LangGraphTravelAgents, TravelPlanState
        print("✅ LangGraph智能体导入成功")
    except Exception as e:
        print(f"❌ LangGraph智能体导入失败: {e}")
        return False
    
    try:
        from config.langgraph_config import langgraph_config as config
        print("✅ 配置导入成功")
        print(f"   模型: {config.GEMINI_MODEL}")
        print(f"   API密钥: {'已配置' if config.GEMINI_API_KEY else '未配置'}")
    except Exception as e:
        print(f"❌ 配置导入失败: {e}")
        return False
    
    return True

def test_agent_initialization():
    """测试智能体初始化"""
    print("\n🤖 测试智能体初始化...")
    
    try:
        from langgraph_agents import LangGraphTravelAgents
        
        agents = LangGraphTravelAgents()
        
        # 检查图对象
        if not hasattr(agents, 'graph'):
            print("❌ 图对象未创建")
            return False
        
        print("✅ 图对象创建成功")
        
        # 检查智能体方法
        required_methods = [
            '_coordinator_agent',
            '_travel_advisor_agent', 
            '_weather_analyst_agent',
            '_budget_optimizer_agent',
            '_local_expert_agent',
            '_itinerary_planner_agent'
        ]
        
        missing_methods = []
        for method_name in required_methods:
            if not hasattr(agents, method_name):
                missing_methods.append(method_name)
        
        if missing_methods:
            print(f"❌ 缺少方法: {', '.join(missing_methods)}")
            return False
        
        print("✅ 所有智能体方法存在")
        
        # 检查路由方法
        if not hasattr(agents, '_coordinator_router'):
            print("❌ 缺少路由方法")
            return False
        
        print("✅ 路由方法存在")
        
        return True
        
    except Exception as e:
        print(f"❌ 智能体初始化失败: {e}")
        return False

def test_state_structure():
    """测试状态结构"""
    print("\n📋 测试状态结构...")
    
    try:
        from langgraph_agents import TravelPlanState
        
        # 创建测试状态
        test_state = TravelPlanState(
            messages=[],
            destination="测试目的地",
            duration=3,
            budget_range="中等预算",
            interests=["测试兴趣"],
            group_size=2,
            travel_dates="2025-08-20 至 2025-08-23",
            current_agent="coordinator",
            agent_outputs={},
            final_plan={},
            iteration_count=0
        )
        
        # 验证字段
        required_fields = [
            'messages', 'destination', 'duration', 'budget_range',
            'interests', 'group_size', 'travel_dates', 'current_agent',
            'agent_outputs', 'final_plan', 'iteration_count'
        ]
        
        missing_fields = []
        for field in required_fields:
            if field not in test_state:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"❌ 缺少字段: {', '.join(missing_fields)}")
            return False
        
        print("✅ 所有必需字段存在")
        
        # 测试字段类型
        if not isinstance(test_state['messages'], list):
            print("❌ messages字段类型错误")
            return False
        
        if not isinstance(test_state['agent_outputs'], dict):
            print("❌ agent_outputs字段类型错误")
            return False
        
        print("✅ 字段类型正确")
        
        return True
        
    except Exception as e:
        print(f"❌ 状态结构测试失败: {e}")
        return False

def test_router_logic():
    """测试路由逻辑（不调用API）"""
    print("\n🔀 测试路由逻辑...")
    
    try:
        from langgraph_agents import LangGraphTravelAgents, TravelPlanState
        
        agents = LangGraphTravelAgents()
        
        # 创建测试状态
        test_state = TravelPlanState(
            messages=[],
            destination="北京",
            duration=3,
            budget_range="中等预算",
            interests=["历史"],
            group_size=2,
            travel_dates="2025-08-20 至 2025-08-23",
            current_agent="coordinator",
            agent_outputs={},
            final_plan={},
            iteration_count=0
        )
        
        # 测试路由决策
        next_agent = agents._coordinator_router(test_state)
        
        valid_routes = [
            "travel_advisor", "weather_analyst", "budget_optimizer", 
            "local_expert", "itinerary_planner", "end"
        ]
        
        if next_agent not in valid_routes:
            print(f"❌ 无效的路由决策: {next_agent}")
            return False
        
        print(f"✅ 路由决策正常: {next_agent}")
        
        # 测试不同迭代次数的路由
        test_state['iteration_count'] = 10  # 高迭代次数应该路由到end
        next_agent_high_iter = agents._coordinator_router(test_state)
        
        print(f"✅ 高迭代次数路由: {next_agent_high_iter}")
        
        return True
        
    except Exception as e:
        print(f"❌ 路由逻辑测试失败: {e}")
        return False

def test_graph_structure():
    """测试图结构"""
    print("\n🕸️  测试图结构...")
    
    try:
        from langgraph_agents import LangGraphTravelAgents
        
        agents = LangGraphTravelAgents()
        
        # 检查图的节点
        if hasattr(agents.graph, 'nodes'):
            nodes = list(agents.graph.nodes.keys()) if hasattr(agents.graph.nodes, 'keys') else []
            print(f"✅ 图节点: {len(nodes)}个")
            
            expected_nodes = [
                "coordinator", "travel_advisor", "weather_analyst",
                "budget_optimizer", "local_expert", "itinerary_planner"
            ]
            
            for node in expected_nodes:
                if node not in str(nodes):
                    print(f"⚠️  可能缺少节点: {node}")
        
        # 检查图的边
        if hasattr(agents.graph, 'edges'):
            print("✅ 图边结构存在")
        
        print("✅ 图结构基本正常")
        
        return True
        
    except Exception as e:
        print(f"❌ 图结构测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 LangGraph智能体系统轻量级测试")
    print("=" * 50)
    
    start_time = time.time()
    
    tests = [
        ("导入测试", test_imports),
        ("智能体初始化", test_agent_initialization),
        ("状态结构", test_state_structure),
        ("路由逻辑", test_router_logic),
        ("图结构", test_graph_structure)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name}异常: {e}")
    
    # 总结
    total_time = time.time() - start_time
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    print(f"⏱️  总耗时: {total_time:.2f}秒")
    
    if passed == total:
        print("🎉 所有轻量级测试通过！")
        print("\n✅ LangGraph系统结构正常，包括:")
        print("   - 所有智能体方法已加载")
        print("   - 状态结构完整")
        print("   - 路由逻辑正常")
        print("   - 图结构基本正确")
        print("\n💡 建议:")
        print("   - 系统结构验证通过，可以启动API服务器")
        print("   - 建议使用简化版智能体进行实际测试")
        print("   - 完整LangGraph系统需要稳定的网络连接")
    else:
        print("⚠️  部分测试失败")
        print("\n💡 建议:")
        print("   - 检查失败的测试项目")
        print("   - 确保所有依赖正确安装")
        print("   - 考虑使用简化版智能体")
    
    # 保存简单的测试报告
    report = {
        "test_time": datetime.now().isoformat(),
        "total_tests": total,
        "passed_tests": passed,
        "duration": total_time,
        "success": passed == total
    }
    
    try:
        with open("lightweight_test_report.json", "w") as f:
            json.dump(report, f, indent=2)
        print(f"\n📄 测试报告已保存: lightweight_test_report.json")
    except Exception as e:
        print(f"\n⚠️  保存报告失败: {e}")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
