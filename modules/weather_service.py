"""
天气服务模块

这个模块负责获取和处理天气数据，包括：
- 当前天气信息获取
- 多日天气预报
- 天气数据的格式化和验证
- 模拟天气数据（当API不可用时）

适用于大模型技术初级用户：
这个模块展示了如何与外部API进行交互，
包括错误处理、数据转换和回退机制。
"""

import requests
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json

from ..config.api_config import api_config
from ..data.models import Weather

class WeatherService:
    """
    天气数据获取服务类

    这个类负责从OpenWeather API获取天气信息，包括：
    1. 当前天气状况查询
    2. 多日天气预报获取
    3. 天气数据的处理和格式化
    4. API错误处理和模拟数据回退

    适用于大模型技术初级用户：
    这个类展示了如何设计一个外部API服务的包装器，
    包含错误处理、数据验证和用户友好的接口。
    """

    def __init__(self):
        """
        初始化天气服务

        设置API密钥、基础URL和HTTP会话，
        为后续的天气数据请求做准备。
        """
        self.api_key = api_config.OPENWEATHER_API_KEY  # OpenWeather API密钥
        self.base_url = api_config.WEATHER_BASE_URL    # API基础URL
        self.session = requests.Session()              # HTTP会话对象，提高请求效率

    def get_current_weather(self, city: str) -> Optional[Weather]:
        """
        获取指定城市的当前天气

        从OpenWeather API获取实时天气数据，包括温度、
        天气描述、湿度、风速等信息。

        参数：
        - city: 城市名称（中文或英文）

        返回：Weather对象或None（如果获取失败）

        功能说明：
        1. 构建API请求参数
        2. 发送HTTP请求获取数据
        3. 解析JSON响应
        4. 创建Weather对象
        5. 错误处理和回退到模拟数据
        """
        try:
            # 构建API请求URL和参数
            url = f"{self.base_url}/weather"
            params = {
                'q': city,              # 城市名称
                'appid': self.api_key,  # API密钥
                'units': 'metric'       # 使用摄氏度
            }

            # 发送HTTP请求
            response = self.session.get(url, params=params)
            response.raise_for_status()  # 检查HTTP错误
            data = response.json()       # 解析JSON响应

            # 创建Weather对象
            return Weather(
                temperature=data['main']['temp'],                    # 温度
                description=data['weather'][0]['description'].title(), # 天气描述
                humidity=data['main']['humidity'],                   # 湿度
                wind_speed=data['wind'].get('speed', 0),            # 风速
                feels_like=data['main']['feels_like'],              # 体感温度
                date=datetime.now().strftime('%Y-%m-%d')            # 日期
            )

        except Exception as e:
            print(f"获取当前天气时出错: {e}")
            return self._get_mock_weather()  # 回退到模拟数据
    
    def get_weather_forecast(self, city: str, days: int = 5) -> List[Weather]:
        """Get weather forecast for multiple days"""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric',
                'cnt': min(days * 8, 40)  # 8 forecasts per day (3-hour intervals), max 40
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            daily_forecasts = []
            processed_dates = set()
            
            for item in data['list']:
                date_str = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                
                if date_str not in processed_dates:
                    weather = Weather(
                        temperature=item['main']['temp'],
                        description=item['weather'][0]['description'].title(),
                        humidity=item['main']['humidity'],
                        wind_speed=item['wind'].get('speed', 0),
                        feels_like=item['main']['feels_like'],
                        date=date_str
                    )
                    daily_forecasts.append(weather)
                    processed_dates.add(date_str)
                
                if len(daily_forecasts) >= days:
                    break
            
            return daily_forecasts
            
        except Exception as e:
            print(f"Error fetching weather forecast: {e}")
            return self._get_mock_forecast(days)
    
    def _get_mock_weather(self) -> Weather:
        """Return mock weather data when API fails"""
        return Weather(
            temperature=22.0,
            description="Partly Cloudy",
            humidity=65,
            wind_speed=5.2,
            feels_like=24.0,
            date=datetime.now().strftime('%Y-%m-%d')
        )
    
    def _get_mock_forecast(self, days: int) -> List[Weather]:
        """Return mock forecast data when API fails"""
        forecasts = []
        base_date = datetime.now()
        
        for i in range(days):
            date_str = (base_date + timedelta(days=i)).strftime('%Y-%m-%d')
            temp = 20 + (i % 10)  # Varying temperature
            
            weather = Weather(
                temperature=float(temp),
                description=["Sunny", "Partly Cloudy", "Cloudy", "Light Rain"][i % 4],
                humidity=60 + (i % 20),
                wind_speed=3.0 + (i % 5),
                feels_like=float(temp + 2),
                date=date_str
            )
            forecasts.append(weather)
        
        return forecasts
    
    def get_weather_summary(self, forecasts: List[Weather]) -> Dict[str, Any]:
        """Generate weather summary for the trip"""
        if not forecasts:
            return {}
        
        temps = [w.temperature for w in forecasts]
        
        return {
            'avg_temperature': round(sum(temps) / len(temps), 1),
            'min_temperature': min(temps),
            'max_temperature': max(temps),
            'conditions': [w.description for w in forecasts],
            'rainy_days': len([w for w in forecasts if 'rain' in w.description.lower()]),
            'recommendations': self._get_weather_recommendations(forecasts)
        }
    
    def _get_weather_recommendations(self, forecasts: List[Weather]) -> List[str]:
        """Generate weather-based recommendations"""
        recommendations = []
        temps = [w.temperature for w in forecasts]
        avg_temp = sum(temps) / len(temps)
        
        if avg_temp < 10:
            recommendations.append("Pack warm clothes - it will be cold!")
        elif avg_temp > 30:
            recommendations.append("Pack light, breathable clothing - it will be hot!")
        
        rainy_days = len([w for w in forecasts if 'rain' in w.description.lower()])
        if rainy_days > 0:
            recommendations.append(f"Pack an umbrella - rain expected on {rainy_days} day(s)")
        
        if any(w.wind_speed > 10 for w in forecasts):
            recommendations.append("Expect windy conditions - secure loose items")
        
        return recommendations# Weather fetching logic
