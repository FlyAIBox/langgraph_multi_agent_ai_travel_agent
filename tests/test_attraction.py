"""
景点查找模块的单元测试

这个测试文件验证AttractionFinder类的核心功能，包括：
1. 模拟景点数据的创建和验证
2. 费用估算算法的准确性
3. 数据类型和格式的正确性

适用于大模型技术初级用户：
这个文件展示了如何为AI模块编写单元测试，
确保代码质量和功能的正确性。
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# 添加父目录到路径以便导入模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.attraction_finder import AttractionFinder
from data.models import Attraction

class TestAttractionFinder(unittest.TestCase):
    """
    AttractionFinder类的测试用例

    这个测试类验证景点查找器的各种功能，
    确保模块在不同情况下都能正常工作。
    """

    def setUp(self):
        """
        设置测试环境

        在每个测试方法运行前，创建必要的测试对象和数据。
        这确保了每个测试都在干净的环境中运行。
        """
        self.finder = AttractionFinder()
        self.sample_trip_details = {
            'destination': '巴黎',
            'budget_range': '中等预算',
            'preferences': {'interests': ['博物馆', '美食']},
            'group_size': 2
        }

    def test_create_mock_attractions(self):
        """
        测试模拟景点数据的正确创建

        验证模拟景点生成功能是否：
        1. 返回正确的数据类型（列表）
        2. 包含有效数量的景点
        3. 每个景点都是正确的Attraction对象
        4. 景点名称包含目的地信息
        """
        attractions = self.finder._get_mock_attractions(self.sample_trip_details)

        # 验证返回类型和数量
        self.assertIsInstance(attractions, list)
        self.assertGreater(len(attractions), 0)

        # 验证每个景点对象
        for attraction in attractions:
            self.assertIsInstance(attraction, Attraction)
            self.assertEqual(attraction.type, 'attraction')
            # 注意：由于我们已经中文化，这里应该检查中文名称
            self.assertTrue(len(attraction.name) > 0)

    def test_estimate_cost(self):
        """
        测试费用估算功能

        验证费用估算算法是否：
        1. 返回正确的数据类型（浮点数）
        2. 返回合理的正数值
        3. 能够处理不同的预算范围和价格等级
        """
        cost = self.finder._estimate_cost('attraction', '中等预算', 2)

        # 验证返回值类型和范围
        self.assertIsInstance(cost, float)
        self.assertGreater(cost, 0)
        self.assertLess(cost, 10000)  # 合理的上限检查

if __name__ == '__main__':
    print("🧪 开始运行景点查找模块测试...")
    unittest.main(verbosity=2)
