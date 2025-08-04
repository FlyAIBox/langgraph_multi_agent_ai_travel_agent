"""
多智能体AI旅行规划系统 - 主入口点

这是传统多智能体系统的主程序，展示了多个专业AI智能体协作进行旅行规划的完整流程。
该系统包含6个专业智能体，通过协调、通信和决策引擎实现智能协作。

主要功能：
- 多智能体系统初始化和管理
- 智能体间协作演示
- 用户输入收集和处理
- 协作式旅行规划执行
- 系统性能监控和报告

适用于大模型技术初级用户：
这个文件展示了如何构建一个完整的多智能体系统，
包含系统架构、协作机制和用户交互的最佳实践。
"""

import sys
import os
from datetime import datetime, timedelta
import json

# 将项目目录添加到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.multi_agent_orchestrator import MultiAgentTravelOrchestrator
from modules.user_input import UserInputHandler
from utils.helpers import display_header, save_to_file

def main():
    """
    多智能体旅行规划系统的主函数

    这是整个传统多智能体系统的核心控制流程，包括：
    1. 系统初始化和状态检查
    2. 智能体协作能力演示
    3. 用户输入收集和验证
    4. 多智能体协作规划执行
    5. 结果展示和文件保存
    6. 系统性能指标分析

    适用于大模型技术初级用户：
    这个函数展示了如何组织一个复杂AI系统的主要工作流程，
    包含错误处理、用户交互和系统监控的完整实现。
    """

    # 显示增强的系统标题
    display_multi_agent_header()

    try:
        # 初始化多智能体系统
        print("🚀 正在初始化多智能体旅行规划系统...")
        orchestrator = MultiAgentTravelOrchestrator()

        # 显示系统状态
        system_status = orchestrator.get_system_status()
        print(f"✅ 系统就绪: {system_status['active_agents']}/{system_status['total_agents']} 个智能体在线")
        print()

        # 演示智能体协作能力
        show_agent_collaboration_demo = input("您想查看多智能体协作演示吗？(y/n): ").lower().strip()
        if show_agent_collaboration_demo in ['y', 'yes', '是', '确认']:
            demonstrate_system_capabilities(orchestrator)

        # 获取用户输入
        print("\n" + "="*80)
        print("🎯 旅行规划输入")
        print("="*80)

        user_input_handler = UserInputHandler()
        user_data = user_input_handler.get_trip_details()

        if not user_data:
            print("❌ 旅行规划已取消。")
            return

        print("\n" + "="*80)
        print("🤖 多智能体协作规划")
        print("="*80)

        # 执行多智能体规划
        comprehensive_plan = orchestrator.plan_comprehensive_trip(user_data)

        # 显示结果
        display_multi_agent_results(comprehensive_plan)

        # 保存结果
        save_results = input("\n💾 将完整的多智能体报告保存到文件？(y/n): ").lower().strip()
        if save_results in ['y', 'yes', '是', '确认']:
            save_multi_agent_results(comprehensive_plan, user_data)

        # 显示系统性能指标
        show_metrics = input("\n📊 查看系统性能指标？(y/n): ").lower().strip()
        if show_metrics in ['y', 'yes', '是', '确认']:
            display_system_metrics(orchestrator, comprehensive_plan)

        print("\n🎉 多智能体旅行规划完成！")
        print("感谢您使用我们的协作式AI旅行规划系统！")

    except KeyboardInterrupt:
        print("\n\n❌ 多智能体规划被用户中断。")
    except Exception as e:
        print(f"\n❌ 多智能体系统发生错误: {str(e)}")
        print("请检查您的输入并重试。")

def display_multi_agent_header():
    """
    显示多智能体系统的增强标题

    这个函数展示系统的核心架构和能力，包括：
    1. 系统名称和主要功能
    2. 6个专业智能体的角色介绍
    3. 系统的增强能力说明
    4. 协作机制的特点

    适用于大模型技术初级用户：
    这个函数展示了如何为复杂系统设计清晰的用户界面，
    帮助用户理解系统的架构和能力。
    """
    print("\n" + "="*80)
    print("🤖 多智能体AI旅行规划师与费用计算器")
    print("="*80)
    print("🎯 协作智能: 6个专业AI智能体协同工作")
    print("="*80)
    print("\n🧠 AI智能体团队:")
    print("   🎯 协调员智能体     - 主编排和决策综合")
    print("   ✈️  旅行顾问        - 目的地专业知识与推荐")
    print("   💰 预算优化师      - 成本分析与省钱策略")
    print("   🌤️  天气分析师      - 天气情报与规划")
    print("   🏠 当地专家        - 内部知识与实时洞察")
    print("   📅 行程规划师      - 日程优化与物流")
    print("\n🚀 增强能力:")
    print("   • 基于智能体共识的协作决策")
    print("   • 多维度优化（成本、天气、物流）")
    print("   • 推荐间的实时冲突解决")
    print("   • 基于您优先级的自适应规划")
    print("   • 全面验证和质量保证")
    print("="*80)

def demonstrate_system_capabilities(orchestrator: MultiAgentTravelOrchestrator):
    """Demonstrate the multi-agent system capabilities"""
    print("\n" + "="*60)
    print("🎭 MULTI-AGENT COLLABORATION DEMONSTRATION")
    print("="*60)
    
    demo_data = orchestrator.demonstrate_agent_collaboration()
    
    print("\n🤖 AGENT NETWORK:")
    for agent_id, info in demo_data['agent_network'].items():
        print(f"   {agent_id.replace('_', ' ').title():<25} | Role: {info['role']:<15} | Capabilities: {len(info['capabilities'])}")
    
    print(f"\n📡 COMMUNICATION INFRASTRUCTURE:")
    comm_patterns = demo_data['communication_patterns']
    print(f"   • Registered Agents: {comm_patterns['hub_registered_agents']}")
    print(f"   • Message Types: {', '.join(comm_patterns['message_types_supported'])}")
    print(f"   • Features: {', '.join(comm_patterns['collaborative_features'])}")
    
    print(f"\n🧠 DECISION MAKING ENGINE:")
    decision_info = demo_data['decision_making_process']
    print(f"   • Engine: {decision_info['synthesis_engine']}")
    print(f"   • Consensus Methods: {', '.join(decision_info['consensus_mechanisms'])}")
    print(f"   • Quality Assurance: {', '.join(decision_info['quality_assurance'])}")
    
    print(f"\n✨ SYSTEM CAPABILITIES:")
    for capability in demo_data['system_capabilities']:
        print(f"   • {capability}")
    
    print("="*60)
    input("\nPress Enter to continue to trip planning...")

def display_multi_agent_results(comprehensive_plan: dict):
    """Display comprehensive multi-agent planning results"""
    print("\n" + "="*80)
    print("📋 MULTI-AGENT TRAVEL PLANNING RESULTS")
    print("="*80)
    
    # Trip Summary
    trip_summary = comprehensive_plan.get('trip_summary', {})
    print(f"🎯 TRIP OVERVIEW:")
    print(f"   Destination: {trip_summary.get('destination', 'N/A')}")
    print(f"   Duration: {trip_summary.get('duration', 'N/A')} days")
    print(f"   Dates: {trip_summary.get('dates', 'N/A')}")
    print(f"   Group Size: {trip_summary.get('group_size', 'N/A')} people")
    print(f"   Planning Method: {trip_summary.get('planning_approach', 'N/A')}")
    
    # Agent Contributions
    print(f"\n🤖 AI AGENT CONTRIBUTIONS:")
    agent_contributions = comprehensive_plan.get('agent_contributions', {})
    for agent_type, contribution in agent_contributions.items():
        print(f"   {agent_type.replace('_', ' ').title():<20}: {contribution}")
    
    # System Performance
    print(f"\n📊 SYSTEM PERFORMANCE:")
    performance = comprehensive_plan.get('system_performance', {})
    print(f"   Agents Consulted: {performance.get('agents_consulted', 0)}")
    print(f"   Consensus Level: {performance.get('consensus_achieved', 0):.1%}")
    print(f"   Confidence Score: {performance.get('confidence_score', 0):.1%}")
    print(f"   Processing: {performance.get('processing_time', 'N/A')}")
    
    # Multi-Agent Summary
    print(f"\n🎯 COLLABORATION SUMMARY:")
    ma_summary = comprehensive_plan.get('multi_agent_summary', {})
    print(f"   Coordination Success: {'✅' if ma_summary.get('coordination_success') else '❌'}")
    print(f"   All Agents Contributed: {'✅' if ma_summary.get('all_agents_contributed') else '❌'}")
    print(f"   Conflicts Resolved: {ma_summary.get('decision_conflicts_resolved', 0)}")
    print(f"   Recommendation Quality: {ma_summary.get('recommendation_quality', 'N/A')}")
    print(f"   Predicted Satisfaction: {ma_summary.get('user_satisfaction_prediction', 'N/A')}")
    
    # Detailed Insights
    detailed_insights = comprehensive_plan.get('detailed_insights', {})
    
    if detailed_insights.get('destination_highlights'):
        print(f"\n🏛️ DESTINATION HIGHLIGHTS:")
        for highlight in detailed_insights['destination_highlights']:
            print(f"   • {highlight}")
    
    if detailed_insights.get('budget_breakdown'):
        print(f"\n💰 BUDGET BREAKDOWN:")
        for category, percentage in detailed_insights['budget_breakdown'].items():
            print(f"   {category.title():<15}: {percentage}")
    
    if detailed_insights.get('weather_considerations'):
        print(f"\n🌤️ WEATHER INTELLIGENCE:")
        for consideration in detailed_insights['weather_considerations']:
            print(f"   • {consideration}")
    
    if detailed_insights.get('local_tips'):
        print(f"\n🏠 LOCAL EXPERT INSIGHTS:")
        for tip in detailed_insights['local_tips']:
            print(f"   • {tip}")
    
    if detailed_insights.get('optimized_itinerary'):
        print(f"\n📅 ITINERARY OPTIMIZATION:")
        for optimization in detailed_insights['optimized_itinerary']:
            print(f"   • {optimization}")
    
    if detailed_insights.get('contingency_plans'):
        print(f"\n🛡️ CONTINGENCY PLANNING:")
        for plan in detailed_insights['contingency_plans']:
            print(f"   • {plan}")

def save_multi_agent_results(comprehensive_plan: dict, user_data: dict):
    """Save multi-agent results to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    destination = user_data.get('destination', 'unknown').replace(' ', '_').lower()
    filename = f"multi_agent_trip_plan_{destination}_{timestamp}.txt"
    
    content = []
    content.append("="*80)
    content.append("MULTI-AGENT AI TRAVEL PLANNING REPORT")
    content.append("="*80)
    content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    content.append(f"Planning System: Multi-Agent Collaborative Intelligence")
    content.append("")
    
    # Trip Summary
    trip_summary = comprehensive_plan.get('trip_summary', {})
    content.append("TRIP OVERVIEW:")
    content.append("-" * 40)
    for key, value in trip_summary.items():
        content.append(f"{key.replace('_', ' ').title()}: {value}")
    content.append("")
    
    # Agent Contributions
    content.append("AI AGENT CONTRIBUTIONS:")
    content.append("-" * 40)
    agent_contributions = comprehensive_plan.get('agent_contributions', {})
    for agent_type, contribution in agent_contributions.items():
        content.append(f"{agent_type.replace('_', ' ').title()}: {contribution}")
    content.append("")
    
    # System Performance
    content.append("SYSTEM PERFORMANCE METRICS:")
    content.append("-" * 40)
    performance = comprehensive_plan.get('system_performance', {})
    for key, value in performance.items():
        if key != 'quality_metrics':
            content.append(f"{key.replace('_', ' ').title()}: {value}")
    
    # Quality Metrics
    quality_metrics = performance.get('quality_metrics', {})
    if quality_metrics:
        content.append("\nQuality Metrics:")
        for metric, score in quality_metrics.items():
            content.append(f"  {metric.replace('_', ' ').title()}: {score:.1%}")
    content.append("")
    
    # Detailed Insights
    detailed_insights = comprehensive_plan.get('detailed_insights', {})
    for section, items in detailed_insights.items():
        if items:
            content.append(f"{section.replace('_', ' ').upper()}:")
            content.append("-" * 40)
            if isinstance(items, list):
                for item in items:
                    content.append(f"• {item}")
            elif isinstance(items, dict):
                for key, value in items.items():
                    content.append(f"• {key.title()}: {value}")
            content.append("")
    
    # Multi-Agent Summary
    ma_summary = comprehensive_plan.get('multi_agent_summary', {})
    content.append("MULTI-AGENT COLLABORATION SUMMARY:")
    content.append("-" * 40)
    for key, value in ma_summary.items():
        content.append(f"{key.replace('_', ' ').title()}: {value}")
    content.append("")
    
    content.append("="*80)
    content.append("End of Multi-Agent Travel Planning Report")
    content.append("="*80)
    
    # Save to file
    try:
        full_content = "\n".join(content)
        save_to_file(full_content, filename)
        print(f"✅ Multi-agent report saved as: {filename}")
    except Exception as e:
        print(f"❌ Error saving file: {str(e)}")

def display_system_metrics(orchestrator: MultiAgentTravelOrchestrator, comprehensive_plan: dict):
    """Display detailed system performance metrics"""
    print("\n" + "="*60)
    print("📊 SYSTEM PERFORMANCE METRICS")
    print("="*60)
    
    system_status = orchestrator.get_system_status()
    
    print("🖥️ SYSTEM STATUS:")
    print(f"   Overall Status: {system_status['system_status'].title()}")
    print(f"   Active Agents: {system_status['active_agents']}/{system_status['total_agents']}")
    print(f"   Network Health: {system_status['agent_network_health']}")
    print(f"   Planning Sessions: {system_status['planning_sessions_completed']}")
    
    print("\n📡 COMMUNICATION HUB:")
    hub_status = system_status.get('communication_hub_status', {})
    print(f"   Total Agents: {hub_status.get('total_agents', 0)}")
    print(f"   Active Agents: {hub_status.get('active_agents', 0)}")
    print(f"   Messages Processed: {hub_status.get('total_messages', 0)}")
    
    print("\n🎯 PLANNING QUALITY:")
    performance = comprehensive_plan.get('system_performance', {})
    quality_metrics = performance.get('quality_metrics', {})
    for metric, score in quality_metrics.items():
        print(f"   {metric.replace('_', ' ').title()}: {score:.1%}")
    
    print("\n🤖 AGENT PERFORMANCE:")
    hub_agents = hub_status.get('agents', {})
    for agent_id, agent_info in hub_agents.items():
        print(f"   {agent_id.replace('_', ' ').title():<20}: "
              f"Active: {'✅' if agent_info.get('is_active') else '❌'} | "
              f"Connections: {len(agent_info.get('connected_agents', []))}")
    
    print("="*60)

if __name__ == "__main__":
    main()
