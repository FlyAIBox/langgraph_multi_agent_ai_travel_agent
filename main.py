#!/usr/bin/env python3
"""
AI旅行助手与费用规划师
主应用程序入口点 - 现在支持多智能体！

这个模块是整个旅行规划系统的主入口，提供三种不同的规划模式：
1. 单智能体规划（经典版）- 传统的单一AI助手
2. 多智能体规划（传统框架）- 6个专业AI智能体协作
3. LangGraph多智能体（高级版）- 基于LangGraph框架的现代化系统

适用于大模型技术初级用户：
这个文件展示了如何构建一个完整的AI应用程序，包括：
- 模块化设计：每个功能都有专门的模块
- 用户交互：友好的命令行界面
- 错误处理：完善的异常处理机制
- 系统集成：多个AI系统的整合
"""

import sys
import os
from datetime import datetime

# 将当前目录添加到路径中以导入模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.user_input import UserInputHandler
from modules.weather_service import WeatherService
from modules.attraction_finder import AttractionFinder
from modules.hotel_estimator import HotelEstimator
from modules.currency_converter import CurrencyConverter
from modules.expense_calculator import ExpenseCalculator
from modules.itinerary_planner import ItineraryPlanner
from modules.trip_summary import TripSummaryGenerator

class TravelAgent:
    """
    主要的旅行助手编排器类（传统单智能体版本）

    这个类是单智能体系统的核心，它：
    1. 初始化所有服务模块
    2. 协调各个模块的工作流程
    3. 处理用户交互和结果展示
    4. 管理整个旅行规划过程

    适用于大模型技术初级用户：
    这个类展示了面向对象编程的设计模式，
    通过组合多个专门的服务类来实现复杂的功能。
    """

    def __init__(self):
        """
        初始化所有服务模块

        创建旅行规划所需的所有服务实例，包括：
        - 用户输入处理器
        - 天气服务
        - 景点查找器
        - 酒店估算器
        - 货币转换器
        - 费用计算器
        - 行程规划器
        - 旅行总结生成器
        """
        self.input_handler = UserInputHandler()        # 用户输入处理器
        self.weather_service = WeatherService()        # 天气服务
        self.attraction_finder = AttractionFinder()    # 景点查找器
        self.hotel_estimator = HotelEstimator()        # 酒店估算器
        self.currency_converter = CurrencyConverter()  # 货币转换器
        self.expense_calculator = ExpenseCalculator()  # 费用计算器
        self.itinerary_planner = ItineraryPlanner()    # 行程规划器
        self.summary_generator = TripSummaryGenerator() # 旅行总结生成器
    
    def run(self):
        """
        主应用程序流程

        这个方法执行完整的旅行规划流程，包括：
        1. 收集用户输入
        2. 获取天气信息
        3. 查找景点和活动
        4. 估算住宿费用
        5. 计算总费用
        6. 转换货币
        7. 生成行程安排
        8. 创建旅行总结

        适用于大模型技术初级用户：
        这个方法展示了如何将复杂的任务分解为
        多个简单的步骤，每个步骤都有明确的职责。
        """
        try:
            print("🤖 AI旅行助手与费用规划师（单智能体版本）")
            print("=" * 70)

            # 第1步：获取用户输入
            print("\n📝 第1步：收集行程详情...")
            trip_details = self.input_handler.get_trip_details()

            if not self.input_handler.confirm_details(trip_details):
                print("❌ 旅行规划已取消。")
                return

            print("\n🔍 第2步：规划您的完美旅程...")

            # 第2步：获取天气信息
            print("🌤️  获取天气预报...")
            weather_data = self.weather_service.get_weather_forecast(
                trip_details['destination'],
                trip_details['total_days']
            )

            # 第3步：查找景点、餐厅和活动
            print("🏛️  查找景点和活动...")
            attractions = self.attraction_finder.find_attractions(trip_details)
            restaurants = self.attraction_finder.find_restaurants(trip_details)
            activities = self.attraction_finder.find_activities(trip_details)

            # 第4步：估算酒店费用
            print("🏨 估算住宿费用...")
            hotels = self.hotel_estimator.find_hotels(trip_details)

            # 第5步：计算总费用
            print("💰 计算费用...")
            expense_breakdown = self.expense_calculator.calculate_total_expenses(
                trip_details, hotels, attractions, restaurants, activities
            )

            # 第6步：转换货币
            print("💱 转换货币...")
            converted_expenses = self.currency_converter.convert_expenses(
                expense_breakdown, trip_details['currency']
            )

            # 第7步：生成行程安排
            print("📅 创建您的行程...")
            itinerary = self.itinerary_planner.create_itinerary(
                trip_details, weather_data, attractions, restaurants, activities
            )

            # 第8步：生成最终总结
            print("📋 生成旅行总结...")
            final_summary = self.summary_generator.generate_summary(
                trip_details, weather_data, hotels, converted_expenses, itinerary
            )

            # 显示结果
            self._display_results(final_summary)

            # 提供保存选项
            self._offer_save_option(final_summary)

        except KeyboardInterrupt:
            print("\n\n❌ 用户中断了旅行规划。")
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
            print("请重试或联系支持。")
    
    def _display_results(self, summary):
        """
        显示完整的旅行总结

        这个方法将生成的旅行计划以用户友好的格式展示，
        包括基本信息、天气概览、酒店推荐和行程预览。

        参数：
        - summary: 包含所有旅行信息的总结对象
        """
        print("\n" + "="*60)
        print("🎉 您的完整旅行计划")
        print("="*60)

        # 基本行程信息
        print(f"\n🏖️  目的地: {summary.destination}")
        print(f"📅 日期: {summary.start_date} 至 {summary.end_date}")
        print(f"⏰ 时长: {summary.total_days} 天")
        print(f"💰 总费用: {summary.converted_total:.2f} {summary.currency}")
        print(f"📊 每日预算: {summary.daily_budget:.2f} {summary.currency}")

        # 天气总结
        if hasattr(summary, 'weather_summary'):
            print(f"\n🌤️  天气概览:")
            weather = summary.weather_summary
            print(f"   平均温度: {weather.get('avg_temperature', '不可用')}°C")
            print(f"   天气状况: {', '.join(set(weather.get('conditions', [])))}")

            if weather.get('recommendations'):
                print("   建议:")
                for rec in weather['recommendations']:
                    print(f"   • {rec}")

        # 酒店推荐
        if summary.hotels:
            print(f"\n🏨 推荐酒店:")
            for hotel in summary.hotels[:3]:  # 显示前3个
                print(f"   • {hotel.name} ({hotel.rating}⭐)")
                print(f"     ¥{hotel.price_per_night:.2f}/晚 - {hotel.address}")

        # 行程预览
        if summary.itinerary:
            print(f"\n📅 行程预览:")
            for day_plan in summary.itinerary[:3]:  # 显示前3天
                print(f"\n   第 {day_plan.day} 天 ({day_plan.date}):")
                print(f"   天气: {day_plan.weather}")

                if day_plan.attractions:
                    print("   景点:")
                    for attraction in day_plan.attractions[:2]:
                        print(f"   • {attraction.name}")

                if day_plan.restaurants:
                    print("   用餐:")
                    for restaurant in day_plan.restaurants[:1]:
                        print(f"   • {restaurant.name}")

                print(f"   每日费用: ¥{day_plan.daily_cost:.2f}")

        print("\n" + "="*60)
        print("✅ 旅行规划成功完成!")
        print("="*60)
    
    def _offer_save_option(self, summary):
        """
        提供保存旅行计划到文件的选项

        询问用户是否要将生成的旅行计划保存为文本文件，
        如果用户同意，则生成包含时间戳的文件名并保存。

        参数：
        - summary: 要保存的旅行总结对象
        """
        while True:
            save = input("\n💾 将旅行计划保存到文件? (y/n): ").lower().strip()
            if save in ['y', 'yes', '是', 'y']:
                filename = f"旅行计划_{summary.destination.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                try:
                    self.summary_generator.save_to_file(summary, filename)
                    print(f"✅ 旅行计划已保存到: {filename}")
                except Exception as e:
                    print(f"❌ 保存文件时出错: {e}")
                break
            elif save in ['n', 'no', '否', 'n']:
                print("👋 感谢您使用AI旅行助手!")
                break
            else:
                print("请输入 'y' 或 'n'。")

def choose_planning_mode():
    """
    让用户选择规划模式

    显示三种不同的旅行规划模式供用户选择：
    1. 单智能体规划（经典版）
    2. 多智能体规划（传统框架）
    3. LangGraph多智能体（高级版）

    返回：用户选择的模式编号（字符串）
    """
    print("\n" + "="*80)
    print("🤖 AI旅行规划系统")
    print("="*80)
    print("选择您的规划体验:")
    print()
    print("1. 🔧 单智能体规划（经典版）")
    print("   • 传统的单一AI智能体")
    print("   • 直接规划方法")
    print("   • 经过验证的可靠性")
    print()
    print("2. 🚀 多智能体规划（传统框架）")
    print("   • 6个专业AI智能体协同工作")
    print("   • 自定义多智能体框架")
    print("   • 增强的推荐功能")
    print()
    print("3. 🌟 LangGraph多智能体（高级版）")
    print("   • Google Gemini Flash-2.0驱动的智能体")
    print("   • DuckDuckGo实时搜索集成")
    print("   • LangGraph工作流编排")
    print("   • 最先进的多智能体协作")
    print()

    while True:
        choice = input("选择规划模式 (1, 2, 或 3): ").strip()
        if choice in ['1', '2', '3']:
            return choice
        else:
            print("请输入 1、2 或 3。")

def main():
    """
    应用程序入口点，包含模式选择

    这是整个程序的主入口函数，它：
    1. 让用户选择规划模式
    2. 根据选择启动相应的系统
    3. 处理各种错误情况和回退机制

    适用于大模型技术初级用户：
    这个函数展示了如何构建一个灵活的应用程序，
    支持多种运行模式和优雅的错误处理。
    """
    try:
        # 让用户选择规划模式
        mode = choose_planning_mode()

        if mode == '1':
            # 运行传统单智能体系统
            agent = TravelAgent()
            agent.run()

        elif mode == '2':
            # 导入并运行传统多智能体系统
            try:
                from multi_agent_main import main as multi_agent_main
                multi_agent_main()
            except ImportError as e:
                print(f"❌ 传统多智能体系统不可用: {e}")
                print("回退到单智能体规划...")
                agent = TravelAgent()
                agent.run()

        elif mode == '3':
            # 导入并运行LangGraph多智能体系统
            try:
                from langgraph_main import main as langgraph_main
                langgraph_main()
            except ImportError as e:
                print(f"❌ LangGraph系统不可用: {e}")
                print("请安装所需依赖:")
                print("pip install langgraph langchain-google-genai duckduckgo-search")
                print("\n回退到单智能体规划...")
                agent = TravelAgent()
                agent.run()
            except Exception as e:
                print(f"❌ LangGraph系统错误: {e}")
                print("回退到单智能体规划...")
                agent = TravelAgent()
                agent.run()

    except KeyboardInterrupt:
        print("\n\n❌ 用户中断了规划过程。")
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")
        print("请检查您的输入并重试。")

if __name__ == "__main__":
    main()
