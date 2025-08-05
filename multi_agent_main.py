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
    """
    演示多智能体系统能力

    这个函数展示系统的核心架构和协作机制，包括：
    1. 智能体网络结构和角色分工
    2. 通信基础设施和消息类型
    3. 决策引擎和共识机制
    4. 系统的整体能力展示

    参数：
    - orchestrator: 多智能体编排器实例

    适用于大模型技术初级用户：
    这个函数展示了如何设计系统演示功能，
    帮助用户理解复杂系统的内部工作机制。
    """
    print("\n" + "="*60)
    print("🎭 多智能体协作演示")
    print("="*60)

    demo_data = orchestrator.demonstrate_agent_collaboration()

    print("\n🤖 智能体网络:")
    for agent_id, info in demo_data['agent_network'].items():
        agent_name = agent_id.replace('_', ' ').title()
        role = info['role']
        capabilities_count = len(info['capabilities'])
        print(f"   {agent_name:<25} | 角色: {role:<15} | 能力数: {capabilities_count}")

    print(f"\n📡 通信基础设施:")
    comm_patterns = demo_data['communication_patterns']
    print(f"   • 注册智能体: {comm_patterns['hub_registered_agents']}")
    print(f"   • 消息类型: {', '.join(comm_patterns['message_types_supported'])}")
    print(f"   • 协作特性: {', '.join(comm_patterns['collaborative_features'])}")

    print(f"\n🧠 决策引擎:")
    decision_info = demo_data['decision_making_process']
    print(f"   • 引擎: {decision_info['synthesis_engine']}")
    print(f"   • 共识方法: {', '.join(decision_info['consensus_mechanisms'])}")
    print(f"   • 质量保证: {', '.join(decision_info['quality_assurance'])}")

    print(f"\n✨ 系统能力:")
    for capability in demo_data['system_capabilities']:
        print(f"   • {capability}")

    print("="*60)
    input("\n按回车键继续旅行规划...")

def display_multi_agent_results(comprehensive_plan: dict):
    """
    显示全面的多智能体规划结果

    这个函数展示多智能体协作的完整结果，包括：
    1. 旅行概览和基本信息
    2. 各智能体的贡献内容
    3. 系统性能指标
    4. 协作总结和质量评估
    5. 详细的专业洞察

    参数：
    - comprehensive_plan: 包含完整规划结果的字典

    适用于大模型技术初级用户：
    这个函数展示了如何设计复杂系统的结果展示，
    包含多维度的信息组织和用户友好的格式化。
    """
    print("\n" + "="*80)
    print("📋 多智能体旅行规划结果")
    print("="*80)

    # 旅行概览
    trip_summary = comprehensive_plan.get('trip_summary', {})
    print(f"🎯 旅行概览:")
    print(f"   目的地: {trip_summary.get('destination', '未知')}")
    print(f"   时长: {trip_summary.get('duration', '未知')} 天")
    print(f"   日期: {trip_summary.get('dates', '未知')}")
    print(f"   团队人数: {trip_summary.get('group_size', '未知')} 人")
    print(f"   规划方法: {trip_summary.get('planning_approach', '未知')}")

    # 智能体贡献
    print(f"\n🤖 AI智能体贡献:")
    agent_contributions = comprehensive_plan.get('agent_contributions', {})
    for agent_type, contribution in agent_contributions.items():
        agent_name = agent_type.replace('_', ' ').title()
        print(f"   {agent_name:<20}: {contribution}")

    # 系统性能
    print(f"\n📊 系统性能:")
    performance = comprehensive_plan.get('system_performance', {})
    print(f"   咨询智能体数: {performance.get('agents_consulted', 0)}")
    print(f"   共识水平: {performance.get('consensus_achieved', 0):.1%}")
    print(f"   置信度分数: {performance.get('confidence_score', 0):.1%}")
    print(f"   处理时间: {performance.get('processing_time', '未知')}")

    # 多智能体协作总结
    print(f"\n🎯 协作总结:")
    ma_summary = comprehensive_plan.get('multi_agent_summary', {})
    print(f"   协调成功: {'✅' if ma_summary.get('coordination_success') else '❌'}")
    print(f"   所有智能体参与: {'✅' if ma_summary.get('all_agents_contributed') else '❌'}")
    print(f"   解决冲突数: {ma_summary.get('decision_conflicts_resolved', 0)}")
    print(f"   推荐质量: {ma_summary.get('recommendation_quality', '未知')}")
    print(f"   预测满意度: {ma_summary.get('user_satisfaction_prediction', '未知')}")

    # 详细洞察
    detailed_insights = comprehensive_plan.get('detailed_insights', {})

    if detailed_insights.get('destination_highlights'):
        print(f"\n🏛️ 目的地亮点:")
        for highlight in detailed_insights['destination_highlights']:
            print(f"   • {highlight}")

    if detailed_insights.get('budget_breakdown'):
        print(f"\n💰 预算分解:")
        for category, percentage in detailed_insights['budget_breakdown'].items():
            category_name = category.title()
            print(f"   {category_name:<15}: {percentage}")

    if detailed_insights.get('weather_considerations'):
        print(f"\n🌤️ 天气情报:")
        for consideration in detailed_insights['weather_considerations']:
            print(f"   • {consideration}")

    if detailed_insights.get('local_tips'):
        print(f"\n🏠 当地专家洞察:")
        for tip in detailed_insights['local_tips']:
            print(f"   • {tip}")

    if detailed_insights.get('optimized_itinerary'):
        print(f"\n📅 行程优化:")
        for optimization in detailed_insights['optimized_itinerary']:
            print(f"   • {optimization}")

    if detailed_insights.get('contingency_plans'):
        print(f"\n🛡️ 应急计划:")
        for plan in detailed_insights['contingency_plans']:
            print(f"   • {plan}")

def save_multi_agent_results(comprehensive_plan: dict, user_data: dict):
    """
    保存多智能体结果到文件

    这个函数将完整的多智能体规划结果保存为文本文件，包括：
    1. 生成带时间戳的文件名
    2. 格式化所有规划结果
    3. 组织多层次的信息结构
    4. 保存到本地文件系统

    参数：
    - comprehensive_plan: 完整的规划结果字典
    - user_data: 用户输入数据字典

    适用于大模型技术初级用户：
    这个函数展示了如何设计数据持久化功能，
    包含文件命名、内容格式化和错误处理。
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    destination = user_data.get('destination', '未知').replace(' ', '_').lower()
    filename = f"多智能体旅行计划_{destination}_{timestamp}.txt"

    content = []
    content.append("="*80)
    content.append("多智能体AI旅行规划报告")
    content.append("="*80)
    content.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    content.append(f"规划系统: 多智能体协作智能")
    content.append("")

    # 旅行概览
    trip_summary = comprehensive_plan.get('trip_summary', {})
    content.append("旅行概览:")
    content.append("-" * 40)
    for key, value in trip_summary.items():
        key_name = key.replace('_', ' ').title()
        content.append(f"{key_name}: {value}")
    content.append("")

    # 智能体贡献
    content.append("AI智能体贡献:")
    content.append("-" * 40)
    agent_contributions = comprehensive_plan.get('agent_contributions', {})
    for agent_type, contribution in agent_contributions.items():
        agent_name = agent_type.replace('_', ' ').title()
        content.append(f"{agent_name}: {contribution}")
    content.append("")

    # 系统性能指标
    content.append("系统性能指标:")
    content.append("-" * 40)
    performance = comprehensive_plan.get('system_performance', {})
    for key, value in performance.items():
        if key != 'quality_metrics':
            key_name = key.replace('_', ' ').title()
            content.append(f"{key_name}: {value}")

    # 质量指标
    quality_metrics = performance.get('quality_metrics', {})
    if quality_metrics:
        content.append("\n质量指标:")
        for metric, score in quality_metrics.items():
            metric_name = metric.replace('_', ' ').title()
            content.append(f"  {metric_name}: {score:.1%}")
    content.append("")

    # 详细洞察
    detailed_insights = comprehensive_plan.get('detailed_insights', {})
    for section, items in detailed_insights.items():
        if items:
            section_name = section.replace('_', ' ').upper()
            content.append(f"{section_name}:")
            content.append("-" * 40)
            if isinstance(items, list):
                for item in items:
                    content.append(f"• {item}")
            elif isinstance(items, dict):
                for key, value in items.items():
                    content.append(f"• {key.title()}: {value}")
            content.append("")

    # 多智能体协作总结
    ma_summary = comprehensive_plan.get('multi_agent_summary', {})
    content.append("多智能体协作总结:")
    content.append("-" * 40)
    for key, value in ma_summary.items():
        key_name = key.replace('_', ' ').title()
        content.append(f"{key_name}: {value}")
    content.append("")

    content.append("="*80)
    content.append("多智能体旅行规划报告结束")
    content.append("="*80)

    # 保存到文件
    try:
        full_content = "\n".join(content)
        save_to_file(full_content, filename)
        print(f"✅ 多智能体报告已保存为: {filename}")
    except Exception as e:
        print(f"❌ 保存文件时出错: {str(e)}")

def display_system_metrics(orchestrator: MultiAgentTravelOrchestrator, comprehensive_plan: dict):
    """
    显示详细的系统性能指标

    这个函数展示多智能体系统的运行状态和性能数据，包括：
    1. 系统整体状态和健康度
    2. 通信中心的运行情况
    3. 规划质量的评估指标
    4. 各智能体的性能表现

    参数：
    - orchestrator: 多智能体编排器实例
    - comprehensive_plan: 完整的规划结果字典

    适用于大模型技术初级用户：
    这个函数展示了如何设计系统监控和性能分析功能，
    帮助理解复杂系统的运行状态和优化方向。
    """
    print("\n" + "="*60)
    print("📊 系统性能指标")
    print("="*60)

    system_status = orchestrator.get_system_status()

    print("🖥️ 系统状态:")
    print(f"   整体状态: {system_status['system_status'].title()}")
    print(f"   活跃智能体: {system_status['active_agents']}/{system_status['total_agents']}")
    print(f"   网络健康度: {system_status['agent_network_health']}")
    print(f"   规划会话数: {system_status['planning_sessions_completed']}")

    print("\n📡 通信中心:")
    hub_status = system_status.get('communication_hub_status', {})
    print(f"   总智能体数: {hub_status.get('total_agents', 0)}")
    print(f"   活跃智能体数: {hub_status.get('active_agents', 0)}")
    print(f"   处理消息数: {hub_status.get('total_messages', 0)}")

    print("\n🎯 规划质量:")
    performance = comprehensive_plan.get('system_performance', {})
    quality_metrics = performance.get('quality_metrics', {})
    for metric, score in quality_metrics.items():
        metric_name = metric.replace('_', ' ').title()
        print(f"   {metric_name}: {score:.1%}")

    print("\n🤖 智能体性能:")
    hub_agents = hub_status.get('agents', {})
    for agent_id, agent_info in hub_agents.items():
        agent_name = agent_id.replace('_', ' ').title()
        is_active = '✅' if agent_info.get('is_active') else '❌'
        connections = len(agent_info.get('connected_agents', []))
        print(f"   {agent_name:<20}: "
              f"活跃: {is_active} | "
              f"连接数: {connections}")

    print("="*60)

if __name__ == "__main__":
    main()
