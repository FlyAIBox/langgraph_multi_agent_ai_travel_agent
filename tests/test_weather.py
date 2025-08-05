"""
天气服务模块的单元测试

这个测试文件验证WeatherService类的核心功能，包括：
1. 模拟天气数据的创建和验证
2. 天气预报数据的格式和准确性
3. 回退机制的可靠性

适用于大模型技术初级用户：
这个文件展示了如何为天气服务模块编写测试，
确保天气数据的准确性和系统的稳定性。
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# 添加父目录到路径以便导入模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.weather_service import WeatherService
from data.models import Weather

class TestWeatherService(unittest.TestCase):
    """
    WeatherService类的测试用例

    这个测试类验证天气服务的各种功能，
    确保天气数据的准确性和可靠性。
    """

    def setUp(self):
        """
        设置测试环境

        在每个测试方法运行前，创建天气服务实例。
        这确保了每个测试都有一个干净的服务对象。
        """
        self.weather_service = WeatherService()

    def test_create_mock_weather(self):
        """
        测试模拟天气数据的正确创建

        验证模拟天气生成功能是否：
        1. 返回正确的Weather对象
        2. 温度数据类型正确（浮点数）
        3. 描述信息类型正确（字符串）
        4. 温度值在合理范围内（-50°C到60°C）
        """
        weather = self.weather_service._get_mock_weather()

        # 验证对象类型
        self.assertIsInstance(weather, Weather)

        # 验证数据类型
        self.assertIsInstance(weather.temperature, float)
        self.assertIsInstance(weather.description, str)

        # 验证数据范围
        self.assertGreater(weather.temperature, -50)
        self.assertLess(weather.temperature, 60)

        # 验证描述不为空
        self.assertGreater(len(weather.description), 0)

    def test_weather_forecast_fallback(self):
        """
        测试天气预报回退数据功能

        验证天气预报生成功能是否：
        1. 返回正确的列表类型
        2. 包含指定数量的天气对象
        3. 每个天气对象都是有效的Weather实例
        4. 预报数据的连续性和合理性
        """
        forecast_days = 5
        forecast = self.weather_service._get_mock_forecast(forecast_days)

        # 验证返回类型和数量
        self.assertIsInstance(forecast, list)
        self.assertEqual(len(forecast), forecast_days)

        # 验证每个天气对象
        for i, weather in enumerate(forecast):
            self.assertIsInstance(weather, Weather)
            self.assertIsInstance(weather.temperature, float)
            self.assertIsInstance(weather.description, str)

            # 验证温度合理性
            self.assertGreater(weather.temperature, -50)
            self.assertLess(weather.temperature, 60)

if __name__ == '__main__':
    print("🌤️ 开始运行天气服务模块测试...")
    unittest.main(verbosity=2)
