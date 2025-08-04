"""
酒店搜索和住宿费用估算模块

这个模块负责查找和推荐酒店，以及估算住宿费用，包括：
- 酒店搜索和筛选
- 基于预算的价格估算
- 城市价格系数调整
- Google Places API集成
- 模拟酒店数据生成
- 住宿费用计算和优化

适用于大模型技术初级用户：
这个模块展示了如何构建一个智能的酒店推荐系统，
包含价格预测、地区调整和用户偏好匹配。
"""

import requests
import json
from typing import List, Dict, Any, Optional
import random
from ..data.models import Hotel
from ..config.api_config import api_config

class HotelEstimator:
    """
    酒店查找和住宿费用估算服务类

    这个类负责处理所有与酒店住宿相关的功能，包括：
    1. 基于目的地的酒店搜索
    2. 根据预算范围筛选酒店
    3. 住宿费用的精确估算
    4. 城市价格差异的调整
    5. API集成和数据处理
    6. 模拟数据生成和回退

    主要功能：
    - Google Places API集成
    - 智能价格预测
    - 预算匹配算法
    - 地区价格调整

    适用于大模型技术初级用户：
    这个类展示了如何设计一个复杂的推荐系统，
    包含多维度的数据处理和智能筛选算法。
    """

    def __init__(self):
        """
        初始化酒店估算服务

        设置API配置、价格范围、城市倍数等参数，
        为酒店搜索和费用估算做准备。
        """
        # API配置
        self.api_key = api_config.GOOGLE_PLACES_API_KEY  # Google Places API密钥
        self.base_url = api_config.PLACES_BASE_URL       # API基础URL
        self.session = requests.Session()                # HTTP会话对象

        # 不同预算类别的基础价格范围（每晚，人民币）
        self.budget_price_ranges = {
            '经济型': {'min': 200, 'max': 560, 'avg': 350},      # 经济型酒店
            '中等预算': {'min': 560, 'max': 1400, 'avg': 910},   # 中档酒店
            '豪华型': {'min': 1400, 'max': 3500, 'avg': 2100}   # 豪华酒店
        }

        # 城市价格倍数（根据目的地生活成本调整）
        self.city_multipliers = {
            '北京': 1.6,      # 一线城市，价格较高
            '上海': 1.7,      # 一线城市，价格最高
            '广州': 1.4,      # 一线城市
            '深圳': 1.5,      # 一线城市
            '杭州': 1.3,      # 新一线城市
            '成都': 1.2,      # 新一线城市
            '西安': 1.1,      # 新一线城市
            '南京': 1.2,      # 新一线城市
            'default': 1.0    # 默认倍数
        }
    
    def find_hotels(self, trip_details: Dict[str, Any]) -> List[Hotel]:
        """
        根据旅行要求查找酒店

        这个方法负责搜索和推荐适合的酒店，包括：
        1. 使用Google Places API搜索真实酒店
        2. 根据预算范围筛选合适选项
        3. 应用城市价格调整
        4. 提供模拟数据作为回退方案

        参数：
        - trip_details: 包含目的地、预算等信息的旅行详情字典

        返回：Hotel对象列表，按推荐度排序

        功能说明：
        1. 提取目的地和预算信息
        2. 尝试API搜索获取真实酒店数据
        3. 处理和筛选搜索结果
        4. 回退到模拟数据（如果需要）
        """
        try:
            hotels = []
            destination = trip_details['destination']                    # 目的地
            budget_range = trip_details.get('budget_range', '中等预算')  # 预算范围

            # 首先尝试API搜索
            if self.api_key:
                hotels_data = self._search_hotels_api(destination)
                hotels = self._process_hotels_data(hotels_data, trip_details)

            # 如果API失败，回退到模拟数据
            if not hotels:
                hotels = self._generate_mock_hotels(trip_details)
            
            # Sort by rating and price appropriateness
            hotels = self._rank_hotels(hotels, budget_range)
            
            return hotels[:6]  # Return top 6 options
            
        except Exception as e:
            print(f"Error finding hotels: {e}")
            return self._generate_mock_hotels(trip_details)
    
    def _search_hotels_api(self, destination: str) -> List[Dict]:
        """Search for hotels using Google Places API"""
        try:
            url = f"{self.base_url}/textsearch/json"
            params = {
                'query': f'hotels in {destination}',
                'key': self.api_key,
                'type': 'lodging'
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            return data.get('results', [])
            
        except Exception as e:
            print(f"Hotel API search failed: {e}")
            return []
    
    def _process_hotels_data(self, hotels_data: List[Dict], trip_details: Dict) -> List[Hotel]:
        """Process Google Places API response into Hotel objects"""
        hotels = []
        destination = trip_details['destination']
        budget_range = trip_details.get('budget_range', 'mid-range')
        
        for hotel_data in hotels_data:
            try:
                name = hotel_data.get('name', 'Unknown Hotel')
                rating = hotel_data.get('rating', 4.0)
                address = hotel_data.get('formatted_address', f'{destination} City Center')
                price_level = hotel_data.get('price_level', 2)
                
                # Estimate price per night
                price_per_night = self._estimate_hotel_price(destination, budget_range, price_level, rating)
                
                # Generate amenities based on price level and rating
                amenities = self._generate_amenities(price_level, rating)
                
                hotel = Hotel(
                    name=name,
                    rating=rating,
                    price_per_night=price_per_night,
                    address=address,
                    amenities=amenities
                )
                
                hotels.append(hotel)
                
            except Exception as e:
                print(f"Error processing hotel data: {e}")
                continue
        
        return hotels
    
    def _estimate_hotel_price(self, destination: str, budget_range: str, price_level: int, rating: float) -> float:
        """Estimate hotel price per night"""
        # Get base price range
        base_range = self.budget_price_ranges.get(budget_range, self.budget_price_ranges['mid-range'])
        base_price = base_range['avg']
        
        # Apply city multiplier
        city_key = destination.lower()
        multiplier = self.city_multipliers.get(city_key, self.city_multipliers['default'])
        
        # Adjust for price level (0-4 scale from Google Places)
        price_level_multipliers = {0: 0.6, 1: 0.8, 2: 1.0, 3: 1.3, 4: 1.8}
        price_multiplier = price_level_multipliers.get(price_level, 1.0)
        
        # Adjust for rating (higher rated hotels tend to be more expensive)
        if rating >= 4.5:
            rating_multiplier = 1.2
        elif rating >= 4.0:
            rating_multiplier = 1.1
        elif rating < 3.5:
            rating_multiplier = 0.9
        else:
            rating_multiplier = 1.0
        
        final_price = base_price * multiplier * price_multiplier * rating_multiplier
        
        # Add some randomness for variety
        final_price *= random.uniform(0.9, 1.1)
        
        return round(final_price, 2)
    
    def _generate_amenities(self, price_level: int, rating: float) -> List[str]:
        """Generate amenities based on price level and rating"""
        basic_amenities = ['Free WiFi', 'Air Conditioning', '24/7 Reception']
        
        mid_range_amenities = [
            'Restaurant', 'Room Service', 'Fitness Center', 'Business Center',
            'Laundry Service', 'Parking', 'Breakfast Included'
        ]
        
        luxury_amenities = [
            'Spa', 'Pool', 'Concierge Service', 'Airport Shuttle',
            'Multiple Restaurants', 'Bar/Lounge', 'Valet Parking',
            'Premium Bedding', 'Mini Bar', 'Balcony/View'
        ]
        
        amenities = basic_amenities.copy()
        
        if price_level >= 2:
            amenities.extend(random.sample(mid_range_amenities, min(4, len(mid_range_amenities))))
        
        if price_level >= 3 or rating >= 4.5:
            amenities.extend(random.sample(luxury_amenities, min(3, len(luxury_amenities))))
        
        return list(set(amenities))  # Remove duplicates
    
    def _generate_mock_hotels(self, trip_details: Dict) -> List[Hotel]:
        """Generate mock hotel data when API is unavailable"""
        destination = trip_details['destination']
        budget_range = trip_details.get('budget_range', 'mid-range')
        
        mock_hotels_data = [
            {
                'name': f'Grand {destination} Hotel',
                'rating': 4.5,
                'price_level': 3,
                'address': f'{destination} City Center'
            },
            {
                'name': f'{destination} Plaza',
                'rating': 4.3,
                'price_level': 3,
                'address': f'Downtown {destination}'
            },
            {
                'name': f'Budget Stay {destination}',
                'rating': 4.0,
                'price_level': 1,
                'address': f'{destination} Tourist District'
            },
            {
                'name': f'Comfort Inn {destination}',
                'rating': 4.1,
                'price_level': 2,
                'address': f'{destination} Central'
            },
            {
                'name': f'{destination} Luxury Resort',
                'rating': 4.7,
                'price_level': 4,
                'address': f'{destination} Premium District'
            },
            {
                'name': f'Business Hotel {destination}',
                'rating': 4.2,
                'price_level': 2,
                'address': f'{destination} Business District'
            },
            {
                'name': f'Boutique {destination}',
                'rating': 4.4,
                'price_level': 3,
                'address': f'{destination} Historic Quarter'
            },
            {
                'name': f'Extended Stay {destination}',
                'rating': 3.9,
                'price_level': 1,
                'address': f'{destination} Residential Area'
            }
        ]
        
        hotels = []
        for hotel_data in mock_hotels_data:
            price_per_night = self._estimate_hotel_price(
                destination, budget_range, hotel_data['price_level'], hotel_data['rating']
            )
            
            amenities = self._generate_amenities(hotel_data['price_level'], hotel_data['rating'])
            
            hotel = Hotel(
                name=hotel_data['name'],
                rating=hotel_data['rating'],
                price_per_night=price_per_night,
                address=hotel_data['address'],
                amenities=amenities
            )
            
            hotels.append(hotel)
        
        return hotels
    
    def _rank_hotels(self, hotels: List[Hotel], budget_range: str) -> List[Hotel]:
        """Rank hotels based on budget range and quality"""
        target_range = self.budget_price_ranges.get(budget_range, self.budget_price_ranges['mid-range'])
        
        scored_hotels = []
        for hotel in hotels:
            score = 0
            
            # Score based on rating
            score += hotel.rating * 10
            
            # Score based on price appropriateness for budget
            price_diff = abs(hotel.price_per_night - target_range['avg'])
            max_diff = target_range['max'] - target_range['min']
            price_score = max(0, 10 - (price_diff / max_diff * 10))
            score += price_score
            
            # Bonus for being within budget range
            if target_range['min'] <= hotel.price_per_night <= target_range['max']:
                score += 5
            
            # Bonus for good amenities
            score += len(hotel.amenities) * 0.5
            
            scored_hotels.append((hotel, score))
        
        # Sort by score (descending)
        scored_hotels.sort(key=lambda x: x[1], reverse=True)
        return [hotel for hotel, score in scored_hotels]
    
    def calculate_accommodation_cost(self, hotels: List[Hotel], nights: int, budget_range: str) -> Dict[str, Any]:
        """Calculate total accommodation costs"""
        if not hotels:
            return {'total_cost': 0, 'cost_per_night': 0, 'recommended_hotel': None}
        
        # Get the best hotel within budget
        target_range = self.budget_price_ranges.get(budget_range, self.budget_price_ranges['mid-range'])
        
        suitable_hotels = [h for h in hotels if target_range['min'] <= h.price_per_night <= target_range['max']]
        recommended_hotel = suitable_hotels[0] if suitable_hotels else hotels[0]
        
        total_cost = recommended_hotel.calculate_total_cost(nights)
        
        return {
            'total_cost': total_cost,
            'cost_per_night': recommended_hotel.price_per_night,
            'recommended_hotel': recommended_hotel,
            'alternatives': hotels[:3]  # Top 3 alternatives
        }
    
    def get_hotel_suggestions_by_group_size(self, hotels: List[Hotel], group_size: int) -> List[Dict[str, Any]]:
        """Suggest hotel arrangements based on group size"""
        suggestions = []
        
        for hotel in hotels[:3]:  # Top 3 hotels
            if group_size <= 2:
                # Single room
                arrangement = {
                    'hotel': hotel,
                    'rooms': 1,
                    'room_type': 'Double Room',
                    'total_per_night': hotel.price_per_night,
                    'cost_per_person': hotel.price_per_night / group_size
                }
            elif group_size <= 4:
                # Two rooms or suite
                arrangement = {
                    'hotel': hotel,
                    'rooms': 2,
                    'room_type': '2 Double Rooms',
                    'total_per_night': hotel.price_per_night * 2,
                    'cost_per_person': (hotel.price_per_night * 2) / group_size
                }
            else:
                # Multiple rooms
                rooms_needed = (group_size + 1) // 2  # 2 people per room
                arrangement = {
                    'hotel': hotel,
                    'rooms': rooms_needed,
                    'room_type': f'{rooms_needed} Double Rooms',
                    'total_per_night': hotel.price_per_night * rooms_needed,
                    'cost_per_person': (hotel.price_per_night * rooms_needed) / group_size
                }
            
            suggestions.append(arrangement)
        
        return suggestions