"""
LangGraph智能体工具集

这个模块包含了LangGraph多智能体系统使用的所有搜索工具，包括：
- 目的地信息搜索
- 天气信息查询
- 景点发现
- 酒店搜索
- 餐厅查找
- 当地贴士获取
- 预算信息分析

适用于大模型技术初级用户：
这个模块展示了如何为AI智能体创建专门的工具，
每个工具都有特定的功能和搜索策略，通过DuckDuckGo
搜索引擎获取实时信息。
"""

import asyncio
from typing import List, Dict, Any, Optional
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from duckduckgo_search import DDGS
import json
import re
from datetime import datetime
from config.langgraph_config import langgraph_config as config

class TravelAgentTools:
    """
    旅行智能体工具集合类

    这个类包含了所有LangGraph旅行智能体使用的工具，
    每个工具都是一个专门的搜索功能，用于获取特定类型的
    旅行相关信息。

    主要功能：
    1. 初始化Google Gemini大语言模型
    2. 配置DuckDuckGo搜索参数
    3. 提供7个专业搜索工具
    4. 格式化搜索结果供智能体使用

    适用于大模型技术初级用户：
    这个类展示了如何为AI系统创建工具集，
    每个工具都有明确的职责和标准化的接口。
    """

    def __init__(self):
        """
        初始化旅行智能体工具集

        设置Google Gemini大语言模型和搜索配置，
        为各种搜索工具的使用做准备。
        """
        # 初始化Google Gemini大语言模型
        self.llm = ChatGoogleGenerativeAI(
            model=config.GEMINI_MODEL,           # 模型名称
            google_api_key=config.GEMINI_API_KEY, # API密钥
            temperature=config.TEMPERATURE,      # 生成随机性
            max_output_tokens=config.MAX_TOKENS, # 最大输出长度
            top_p=config.TOP_P,                 # 核采样参数
        )
        # 获取搜索配置
        self.search_config = config.get_search_config()

    @tool
    def search_destination_info(query: str) -> str:
        """
        使用DuckDuckGo搜索目的地信息

        这个工具专门用于搜索旅行目的地的综合信息，
        包括景点、旅游指南、文化背景等。

        参数：
        - query: 搜索查询字符串（目的地名称）

        返回：格式化的搜索结果字符串

        功能说明：
        1. 构建专门的搜索查询
        2. 使用DuckDuckGo进行搜索
        3. 格式化结果供智能体理解
        4. 处理搜索错误和异常情况
        """
        try:
            # 使用DuckDuckGo搜索引擎
            with DDGS() as ddgs:
                # 构建搜索查询，添加旅游相关关键词
                results = list(ddgs.text(
                    query + " 旅游目的地指南景点",  # 中文搜索关键词
                    max_results=config.DUCKDUCKGO_MAX_RESULTS,  # 最大结果数
                    region=config.DUCKDUCKGO_REGION,            # 搜索区域
                    safesearch=config.DUCKDUCKGO_SAFESEARCH     # 安全搜索级别
                ))

                # 检查是否有搜索结果
                if not results:
                    return f"未找到目的地搜索结果: {query}"

                # 格式化结果供智能体使用
                formatted_results = []
                for i, result in enumerate(results[:5], 1):  # 取前5个结果
                    formatted_results.append(
                        f"{i}. {result.get('title', '无标题')}\n"
                        f"   {result.get('body', '无描述')}\n"
                        f"   来源: {result.get('href', '无URL')}\n"
                    )

                return "\n".join(formatted_results)
        except Exception as e:
            return f"Error searching for destination info: {str(e)}"
    
    @tool
    def search_weather_info(destination: str, dates: str = "") -> str:
        """Search for weather information for a destination"""
        try:
            weather_query = f"{destination} weather forecast {dates} travel climate"
            with DDGS() as ddgs:
                results = list(ddgs.text(
                    weather_query,
                    max_results=5,
                    region=config.DUCKDUCKGO_REGION,
                    safesearch=config.DUCKDUCKGO_SAFESEARCH
                ))
                
                if not results:
                    return f"No weather information found for {destination}"
                
                weather_info = []
                for result in results[:3]:
                    weather_info.append(
                        f"• {result.get('title', 'Weather Info')}\n"
                        f"  {result.get('body', 'No details available')}\n"
                    )
                
                return f"Weather information for {destination}:\n" + "\n".join(weather_info)
        except Exception as e:
            return f"Error searching weather info: {str(e)}"
    
    @tool
    def search_attractions(destination: str, interests: str = "") -> str:
        """Search for attractions and activities in a destination"""
        try:
            attraction_query = f"{destination} top attractions activities {interests} must visit places"
            with DDGS() as ddgs:
                results = list(ddgs.text(
                    attraction_query,
                    max_results=8,
                    region=config.DUCKDUCKGO_REGION,
                    safesearch=config.DUCKDUCKGO_SAFESEARCH
                ))
                
                if not results:
                    return f"No attractions found for {destination}"
                
                attractions = []
                for i, result in enumerate(results[:6], 1):
                    attractions.append(
                        f"{i}. {result.get('title', 'Attraction')}\n"
                        f"   {result.get('body', 'No description')[:200]}...\n"
                    )
                
                return f"Top attractions in {destination}:\n" + "\n".join(attractions)
        except Exception as e:
            return f"Error searching attractions: {str(e)}"
    
    @tool
    def search_hotels(destination: str, budget: str = "mid-range") -> str:
        """Search for hotel information and pricing"""
        try:
            hotel_query = f"{destination} hotels {budget} best places to stay accommodation"
            with DDGS() as ddgs:
                results = list(ddgs.text(
                    hotel_query,
                    max_results=6,
                    region=config.DUCKDUCKGO_REGION,
                    safesearch=config.DUCKDUCKGO_SAFESEARCH
                ))
                
                if not results:
                    return f"No hotel information found for {destination}"
                
                hotels = []
                for i, result in enumerate(results[:4], 1):
                    hotels.append(
                        f"{i}. {result.get('title', 'Hotel')}\n"
                        f"   {result.get('body', 'No details')[:180]}...\n"
                    )
                
                return f"Hotel options in {destination} ({budget} budget):\n" + "\n".join(hotels)
        except Exception as e:
            return f"Error searching hotels: {str(e)}"
    
    @tool
    def search_restaurants(destination: str, cuisine: str = "") -> str:
        """Search for restaurants and dining options"""
        try:
            restaurant_query = f"{destination} best restaurants {cuisine} local food dining where to eat"
            with DDGS() as ddgs:
                results = list(ddgs.text(
                    restaurant_query,
                    max_results=6,
                    region=config.DUCKDUCKGO_REGION,
                    safesearch=config.DUCKDUCKGO_SAFESEARCH
                ))
                
                if not results:
                    return f"No restaurant information found for {destination}"
                
                restaurants = []
                for i, result in enumerate(results[:4], 1):
                    restaurants.append(
                        f"{i}. {result.get('title', 'Restaurant')}\n"
                        f"   {result.get('body', 'No details')[:180]}...\n"
                    )
                
                return f"Restaurant recommendations in {destination}:\n" + "\n".join(restaurants)
        except Exception as e:
            return f"Error searching restaurants: {str(e)}"
    
    @tool
    def search_local_tips(destination: str) -> str:
        """Search for local tips, culture, and insider information"""
        try:
            tips_query = f"{destination} local tips insider guide cultural etiquette what to know"
            with DDGS() as ddgs:
                results = list(ddgs.text(
                    tips_query,
                    max_results=5,
                    region=config.DUCKDUCKGO_REGION,
                    safesearch=config.DUCKDUCKGO_SAFESEARCH
                ))
                
                if not results:
                    return f"No local tips found for {destination}"
                
                tips = []
                for result in results[:3]:
                    tips.append(
                        f"• {result.get('title', 'Local Tip')}\n"
                        f"  {result.get('body', 'No details')[:200]}...\n"
                    )
                
                return f"Local tips for {destination}:\n" + "\n".join(tips)
        except Exception as e:
            return f"Error searching local tips: {str(e)}"
    
    @tool
    def search_budget_info(destination: str, duration: str = "") -> str:
        """Search for budget and cost information"""
        try:
            budget_query = f"{destination} travel budget cost daily expenses {duration} how much money"
            with DDGS() as ddgs:
                results = list(ddgs.text(
                    budget_query,
                    max_results=5,
                    region=config.DUCKDUCKGO_REGION,
                    safesearch=config.DUCKDUCKGO_SAFESEARCH
                ))
                
                if not results:
                    return f"No budget information found for {destination}"
                
                budget_info = []
                for result in results[:3]:
                    budget_info.append(
                        f"• {result.get('title', 'Budget Info')}\n"
                        f"  {result.get('body', 'No details')[:200]}...\n"
                    )
                
                return f"Budget information for {destination}:\n" + "\n".join(budget_info)
        except Exception as e:
            return f"Error searching budget info: {str(e)}"

# Create global tools instance
travel_tools = TravelAgentTools()

# Export individual tools for LangGraph
search_destination_info = travel_tools.search_destination_info
search_weather_info = travel_tools.search_weather_info
search_attractions = travel_tools.search_attractions
search_hotels = travel_tools.search_hotels
search_restaurants = travel_tools.search_restaurants
search_local_tips = travel_tools.search_local_tips
search_budget_info = travel_tools.search_budget_info

# List of all available tools
ALL_TOOLS = [
    search_destination_info,
    search_weather_info,
    search_attractions,
    search_hotels,
    search_restaurants,
    search_local_tips,
    search_budget_info
]
