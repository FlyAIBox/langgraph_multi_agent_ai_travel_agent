#!/usr/bin/env python3
"""
LangGraph智能体系统测试类

这个测试类用于验证LangGraph多智能体系统在没有可视化界面下是否正常工作。
包含单元测试、集成测试和性能测试。
"""

import sys
import os
import time
import json
from datetime import datetime
from typing import Dict, Any, List

# 添加backend目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langgraph_agents import LangGraphTravelAgents, TravelPlanState
from config.langgraph_config import langgraph_config as config

class LangGraphAgentsTest:
    """LangGraph智能体系统测试类"""
    
    def __init__(self):
        """初始化测试类"""
        self.test_results = []
        self.start_time = None
        self.agents = None
        
    def log_test(self, test_name: str, success: bool, message: str = "", duration: float = 0):
        """记录测试结果"""
        result = {
            "test_name": test_name,
            "success": success,
            "message": message,
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅" if success else "❌"
        duration_str = f" ({duration:.2f}s)" if duration > 0 else ""
        print(f"{status} {test_name}{duration_str}")
        if message:
            print(f"   {message}")
    
    def test_config_loading(self):
        """测试配置加载"""
        test_start = time.time()
        
        try:
            # 检查API密钥
            if not config.GEMINI_API_KEY:
                self.log_test("配置加载", False, "GEMINI_API_KEY未配置", time.time() - test_start)
                return False
            
            # 检查模型配置
            if not config.GEMINI_MODEL:
                self.log_test("配置加载", False, "GEMINI_MODEL未配置", time.time() - test_start)
                return False
            
            self.log_test("配置加载", True, f"模型: {config.GEMINI_MODEL}", time.time() - test_start)
            return True
            
        except Exception as e:
            self.log_test("配置加载", False, f"异常: {str(e)}", time.time() - test_start)
            return False
    
    def test_agents_initialization(self):
        """测试智能体系统初始化"""
        test_start = time.time()
        
        try:
            self.agents = LangGraphTravelAgents()
            
            # 检查图是否正确构建
            if not hasattr(self.agents, 'graph'):
                self.log_test("智能体初始化", False, "图对象未创建", time.time() - test_start)
                return False
            
            # 检查所有智能体方法是否存在（私有方法）
            required_methods = [
                '_coordinator_agent',
                '_travel_advisor_agent',
                '_weather_analyst_agent',
                '_budget_optimizer_agent',
                '_local_expert_agent',
                '_itinerary_planner_agent'
            ]

            for method_name in required_methods:
                if not hasattr(self.agents, method_name):
                    self.log_test("智能体初始化", False, f"缺少方法: {method_name}", time.time() - test_start)
                    return False
            
            self.log_test("智能体初始化", True, "所有智能体方法已加载", time.time() - test_start)
            return True
            
        except Exception as e:
            self.log_test("智能体初始化", False, f"异常: {str(e)}", time.time() - test_start)
            return False
    
    def test_state_structure(self):
        """测试状态结构"""
        test_start = time.time()
        
        try:
            # 创建测试状态
            test_state = TravelPlanState(
                messages=[],
                destination="测试目的地",
                duration=3,
                budget_range="中等预算",
                interests=["测试兴趣"],
                group_size=2,
                travel_dates="2025-08-20 至 2025-08-23",
                current_agent="",
                agent_outputs={},
                final_plan={},
                iteration_count=0
            )
            
            # 验证状态字段
            required_fields = [
                'messages', 'destination', 'duration', 'budget_range',
                'interests', 'group_size', 'travel_dates', 'current_agent',
                'agent_outputs', 'final_plan', 'iteration_count'
            ]
            
            for field in required_fields:
                if field not in test_state:
                    self.log_test("状态结构", False, f"缺少字段: {field}", time.time() - test_start)
                    return False
            
            self.log_test("状态结构", True, "所有必需字段存在", time.time() - test_start)
            return True
            
        except Exception as e:
            self.log_test("状态结构", False, f"异常: {str(e)}", time.time() - test_start)
            return False
    
    def test_router_logic(self):
        """测试路由逻辑"""
        test_start = time.time()
        
        try:
            if not self.agents:
                self.log_test("路由逻辑", False, "智能体未初始化", time.time() - test_start)
                return False
            
            # 测试协调员路由
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
            next_agent = self.agents._coordinator_router(test_state)
            
            if next_agent not in ["travel_advisor", "weather_analyst", "budget_optimizer", "local_expert", "itinerary_planner", "end"]:
                self.log_test("路由逻辑", False, f"无效的路由决策: {next_agent}", time.time() - test_start)
                return False
            
            self.log_test("路由逻辑", True, f"路由决策正常: {next_agent}", time.time() - test_start)
            return True
            
        except Exception as e:
            self.log_test("路由逻辑", False, f"异常: {str(e)}", time.time() - test_start)
            return False
    
    def test_simple_planning(self):
        """测试简单规划流程（不执行完整LangGraph）"""
        test_start = time.time()
        
        try:
            if not self.agents:
                self.log_test("简单规划", False, "智能体未初始化", time.time() - test_start)
                return False
            
            # 创建简单的测试请求
            test_request = {
                "destination": "北京",
                "duration": 2,
                "budget_range": "经济型",
                "interests": ["历史"],
                "group_size": 1,
                "travel_dates": "2025-08-20 至 2025-08-22"
            }
            
            # 测试单个智能体方法（不执行完整流程）
            test_state = TravelPlanState(
                messages=[],
                destination=test_request["destination"],
                duration=test_request["duration"],
                budget_range=test_request["budget_range"],
                interests=test_request["interests"],
                group_size=test_request["group_size"],
                travel_dates=test_request["travel_dates"],
                current_agent="coordinator",
                agent_outputs={},
                final_plan={},
                iteration_count=0
            )
            
            # 测试协调员智能体
            result_state = self.agents._coordinator_agent(test_state)
            
            if not result_state:
                self.log_test("简单规划", False, "协调员智能体返回空结果", time.time() - test_start)
                return False
            
            if "current_agent" not in result_state:
                self.log_test("简单规划", False, "结果状态缺少current_agent", time.time() - test_start)
                return False
            
            self.log_test("简单规划", True, f"协调员智能体正常工作", time.time() - test_start)
            return True
            
        except Exception as e:
            self.log_test("简单规划", False, f"异常: {str(e)}", time.time() - test_start)
            return False
    
    def test_mock_full_planning(self):
        """测试模拟完整规划流程（使用超时保护）"""
        test_start = time.time()
        
        try:
            if not self.agents:
                self.log_test("模拟完整规划", False, "智能体未初始化", time.time() - test_start)
                return False
            
            # 创建测试请求
            test_request = {
                "destination": "上海",
                "duration": 1,  # 使用最短时间
                "budget_range": "经济型",
                "interests": ["文化"],  # 只有一个兴趣
                "group_size": 1,
                "travel_dates": "2025-08-20"
            }
            
            print(f"   开始模拟规划: {test_request['destination']}")
            
            # 使用超时执行
            import concurrent.futures
            
            def run_planning():
                return self.agents.run_travel_planning(test_request)
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(run_planning)
                try:
                    # 设置30秒超时
                    result = future.result(timeout=30)
                    
                    if result and result.get("success"):
                        self.log_test("模拟完整规划", True, f"规划成功完成", time.time() - test_start)
                        return True
                    else:
                        error_msg = result.get("error", "未知错误") if result else "无返回结果"
                        self.log_test("模拟完整规划", False, f"规划失败: {error_msg}", time.time() - test_start)
                        return False
                        
                except concurrent.futures.TimeoutError:
                    self.log_test("模拟完整规划", False, "规划超时（30秒）", time.time() - test_start)
                    return False
                    
        except Exception as e:
            self.log_test("模拟完整规划", False, f"异常: {str(e)}", time.time() - test_start)
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🧪 LangGraph智能体系统测试")
        print("=" * 50)
        
        self.start_time = time.time()
        
        # 按顺序执行测试
        tests = [
            self.test_config_loading,
            self.test_agents_initialization,
            self.test_state_structure,
            self.test_router_logic,
            self.test_simple_planning,
            # self.test_mock_full_planning  # 可选：完整规划测试
        ]
        
        passed = 0
        total = len(tests)
        
        for test_func in tests:
            if test_func():
                passed += 1
        
        # 总结
        total_time = time.time() - self.start_time
        print("\n" + "=" * 50)
        print(f"📊 测试结果: {passed}/{total} 通过")
        print(f"⏱️  总耗时: {total_time:.2f}秒")
        
        if passed == total:
            print("🎉 所有测试通过！LangGraph系统工作正常")
            print("\n💡 建议:")
            print("   - 可以安全使用LangGraph智能体系统")
            print("   - 建议在生产环境中使用超时保护")
            print("   - 可以启动完整的API服务器")
        else:
            print("⚠️  部分测试失败")
            print("\n💡 建议:")
            print("   - 检查失败的测试项目")
            print("   - 确保API密钥配置正确")
            print("   - 考虑使用简化版智能体作为备选")
        
        return passed == total
    
    def save_test_report(self, filename: str = None):
        """保存测试报告"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"langgraph_test_report_{timestamp}.json"
        
        report = {
            "test_summary": {
                "total_tests": len(self.test_results),
                "passed_tests": sum(1 for r in self.test_results if r["success"]),
                "failed_tests": sum(1 for r in self.test_results if not r["success"]),
                "total_duration": time.time() - self.start_time if self.start_time else 0,
                "test_time": datetime.now().isoformat()
            },
            "test_details": self.test_results,
            "system_info": {
                "gemini_model": config.GEMINI_MODEL,
                "api_key_configured": bool(config.GEMINI_API_KEY),
                "python_version": sys.version
            }
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"\n📄 测试报告已保存: {filename}")
        except Exception as e:
            print(f"\n❌ 保存测试报告失败: {str(e)}")

def main():
    """主测试函数"""
    tester = LangGraphAgentsTest()
    
    # 运行所有测试
    success = tester.run_all_tests()
    
    # 保存测试报告
    tester.save_test_report()
    
    # 返回退出码
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
