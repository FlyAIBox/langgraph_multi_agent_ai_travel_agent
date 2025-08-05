"""
AI旅行助手的数据模型

这个模块定义了旅行规划系统中使用的所有数据结构，包括：
- 天气信息模型
- 景点和活动模型
- 酒店住宿模型
- 行程计划模型
- 旅行总结模型

适用于大模型技术初级用户：
数据模型是程序中用来表示和组织信息的结构。
使用dataclass装饰器可以自动生成常用的方法，
让代码更简洁和易于维护。
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import date, datetime

@dataclass
class Weather:
    """
    特定日期的天气信息模型

    存储某一天的完整天气数据，包括温度、天气描述、
    湿度、风速等信息，用于生成旅行建议。

    属性说明：
    - temperature: 温度（摄氏度）
    - description: 天气描述（如"晴天"、"多云"等）
    - humidity: 湿度百分比
    - wind_speed: 风速（公里/小时）
    - feels_like: 体感温度（摄氏度）
    - date: 日期（YYYY-MM-DD格式）
    """
    temperature: float  # 温度（摄氏度）
    description: str    # 天气描述
    humidity: int       # 湿度百分比
    wind_speed: float   # 风速（公里/小时）
    feels_like: float   # 体感温度（摄氏度）
    date: str          # 日期（YYYY-MM-DD格式）

    def __str__(self) -> str:
        """返回天气信息的字符串表示"""
        return f"{self.description}, {self.temperature}°C (体感温度 {self.feels_like}°C)"

@dataclass
class Attraction:
    """
    旅游景点、餐厅或活动模型

    表示旅行中可以参与的各种活动，包括景点游览、
    餐厅用餐、娱乐活动等。

    属性说明：
    - name: 名称
    - type: 类型（'attraction'景点, 'restaurant'餐厅, 'activity'活动）
    - rating: 评分（1-5分制）
    - price_level: 价格等级（0-4级，类似Google Places风格）
    - address: 地址
    - description: 详细描述
    - estimated_cost: 预估费用（人民币）
    - duration: 预计游览时长（小时）
    """
    name: str               # 名称
    type: str              # 类型
    rating: float          # 评分（1-5分制）
    price_level: int       # 价格等级（0-4级）
    address: str           # 地址
    description: str       # 详细描述
    estimated_cost: float  # 预估费用（人民币）
    duration: int          # 预计时长（小时）

    def __str__(self) -> str:
        """返回景点信息的字符串表示"""
        return f"{self.name} ({self.rating}⭐) - ¥{self.estimated_cost}"

@dataclass
class Hotel:
    """
    酒店住宿选择模型

    表示可选的住宿选项，包括酒店的基本信息、
    价格、设施等。

    属性说明：
    - name: 酒店名称
    - rating: 评分（1-5分制）
    - price_per_night: 每晚价格（人民币）
    - address: 地址
    - amenities: 设施服务列表
    """
    name: str               # 酒店名称
    rating: float          # 评分（1-5分制）
    price_per_night: float # 每晚价格（人民币）
    address: str           # 地址
    amenities: List[str]   # 设施服务列表

    def calculate_total_cost(self, nights: int) -> float:
        """
        计算指定夜数的总费用

        参数：
        - nights: 住宿夜数

        返回：总住宿费用
        """
        return self.price_per_night * nights

    def __str__(self) -> str:
        """返回酒店信息的字符串表示"""
        return f"{self.name} ({self.rating}⭐) - ¥{self.price_per_night}/晚"

@dataclass
class Transportation:
    """
    地点间的交通选择模型

    表示不同地点之间的交通方式选项，包括费用、
    时长等信息，用于行程规划。

    属性说明：
    - mode: 交通方式（'步行', '公共交通', '出租车', '网约车'等）
    - estimated_cost: 预估费用（人民币）
    - duration: 预计时长（分钟）
    """
    mode: str               # 交通方式
    estimated_cost: float   # 预估费用（人民币）
    duration: int          # 预计时长（分钟）

    def __str__(self) -> str:
        """返回交通信息的字符串表示"""
        return f"{self.mode} - ¥{self.estimated_cost} ({self.duration}分钟)"

@dataclass
class DayPlan:
    """
    单日完整行程计划模型

    表示旅行中某一天的完整计划，包括景点、餐厅、
    活动、交通和费用等所有信息。

    属性说明：
    - day: 第几天
    - date: 日期（YYYY-MM-DD格式）
    - weather: 当天天气信息
    - attractions: 景点列表
    - restaurants: 餐厅列表
    - activities: 活动列表
    - transportation: 交通安排列表
    - daily_cost: 当日总费用
    """
    day: int                                    # 第几天
    date: str                                   # 日期（YYYY-MM-DD格式）
    weather: Weather                            # 当天天气信息
    attractions: List[Attraction] = None        # 景点列表
    restaurants: List[Attraction] = None        # 餐厅列表
    activities: List[Attraction] = None         # 活动列表
    transportation: List[Transportation] = None # 交通安排列表
    daily_cost: float = 0.0                    # 当日总费用

    def __post_init__(self):
        """初始化空列表（如果为None）"""
        if self.attractions is None:
            self.attractions = []
        if self.restaurants is None:
            self.restaurants = []
        if self.activities is None:
            self.activities = []
        if self.transportation is None:
            self.transportation = []

    def get_total_activities(self) -> int:
        """获取当天计划活动的总数量"""
        return len(self.attractions) + len(self.restaurants) + len(self.activities)

    def __str__(self) -> str:
        """返回日程计划的字符串表示"""
        return f"第{self.day}天 ({self.date}) - {self.get_total_activities()}个活动, ¥{self.daily_cost}"

@dataclass
class TripSummary:
    """
    完整旅行总结模型

    包含整个旅行的所有详细信息，是系统生成的
    最终旅行计划的完整表示。

    属性说明：
    - destination: 目的地
    - start_date: 开始日期
    - end_date: 结束日期
    - total_days: 总天数
    - total_cost: 总费用
    - daily_budget: 每日预算
    - currency: 货币类型
    - converted_total: 转换后的总费用
    - itinerary: 行程安排列表
    - hotels: 酒店选择列表
    - 其他摘要数据（由TripSummaryGenerator添加）
    """
    destination: str                            # 目的地
    start_date: date                           # 开始日期
    end_date: date                             # 结束日期
    total_days: int                            # 总天数
    total_cost: float                          # 总费用
    daily_budget: float                        # 每日预算
    currency: str                              # 货币类型
    converted_total: float                     # 转换后的总费用
    itinerary: List[DayPlan]                   # 行程安排列表
    hotels: List[Hotel]                        # 酒店选择列表

    # 额外的摘要数据（由TripSummaryGenerator添加）
    trip_overview: Dict[str, Any] = None       # 旅行概览
    weather_summary: Dict[str, Any] = None     # 天气摘要
    accommodation_summary: Dict[str, Any] = None # 住宿摘要
    expense_summary: Dict[str, Any] = None     # 费用摘要
    itinerary_highlights: Dict[str, Any] = None # 行程亮点
    recommendations: Dict[str, Any] = None     # 推荐建议
    travel_tips: List[str] = None              # 旅行贴士

    def __post_init__(self):
        """初始化空字典/列表（如果为None）"""
        if self.trip_overview is None:
            self.trip_overview = {}
        if self.weather_summary is None:
            self.weather_summary = {}
        if self.accommodation_summary is None:
            self.accommodation_summary = {}
        if self.expense_summary is None:
            self.expense_summary = {}
        if self.itinerary_highlights is None:
            self.itinerary_highlights = {}
        if self.recommendations is None:
            self.recommendations = {}
        if self.travel_tips is None:
            self.travel_tips = []

    def get_cost_per_person(self, group_size: int) -> float:
        """计算人均费用"""
        return self.converted_total / group_size if group_size > 0 else self.converted_total

    def get_average_daily_cost(self) -> float:
        """计算平均每日费用"""
        return self.converted_total / self.total_days if self.total_days > 0 else 0.0

    def __str__(self) -> str:
        """返回旅行摘要的字符串表示"""
        return f"{self.destination}之旅 ({self.total_days}天) - {self.currency} {self.converted_total:.2f}"

# 模型创建的工具函数
def create_mock_weather(temperature: float = 22.0, description: str = "多云", date_str: str = None) -> Weather:
    """
    创建模拟天气对象用于测试

    参数：
    - temperature: 温度（默认22.0°C）
    - description: 天气描述（默认"多云"）
    - date_str: 日期字符串（默认当前日期）

    返回：Weather对象
    """
    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')

    return Weather(
        temperature=temperature,
        description=description,
        humidity=65,
        wind_speed=10.0,
        feels_like=temperature + 2,
        date=date_str
    )

def create_mock_attraction(name: str = "示例景点", attraction_type: str = "attraction") -> Attraction:
    """
    创建模拟景点对象用于测试

    参数：
    - name: 景点名称（默认"示例景点"）
    - attraction_type: 景点类型（默认"attraction"）

    返回：Attraction对象
    """
    return Attraction(
        name=name,
        type=attraction_type,
        rating=4.2,
        price_level=2,
        address="示例地址",
        description="示例描述",
        estimated_cost=175.0,  # 调整为人民币价格
        duration=2
    )

def create_mock_hotel(name: str = "示例酒店") -> Hotel:
    """
    创建模拟酒店对象用于测试

    参数：
    - name: 酒店名称（默认"示例酒店"）

    返回：Hotel对象
    """
    return Hotel(
        name=name,
        rating=4.0,
        price_per_night=700.0,  # 调整为人民币价格
        address="示例酒店地址",
        amenities=["WiFi", "早餐", "游泳池"]
    )