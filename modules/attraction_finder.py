"""
景点、餐厅和活动查找模块

这个模块负责查找和推荐旅行相关的各种场所和活动，包括：
- 旅游景点发现和评估
- 餐厅推荐和筛选
- 娱乐活动搜索
- 价格估算和预算匹配
- Google Places API集成和模拟数据回退

适用于大模型技术初级用户：
这个模块展示了如何与外部API集成，处理不同类型的数据，
以及如何根据用户预算和偏好进行智能推荐。
"""

import requests
import json
from typing import List, Dict, Any, Optional
import random
from ..data.models import Attraction
from ..config.api_config import api_config
from ..config.app_config import app_config

class AttractionFinder:
    """
    景点和活动查找服务类

    这个类负责查找和推荐各种旅行相关的场所和活动，包括：
    1. 旅游景点的搜索和筛选
    2. 餐厅的发现和推荐
    3. 娱乐活动的查找
    4. 基于预算的价格估算
    5. API集成和数据处理

    主要功能：
    - Google Places API集成
    - 智能预算匹配
    - 多类型场所搜索
    - 模拟数据回退机制

    适用于大模型技术初级用户：
    这个类展示了如何设计一个复杂的推荐系统，
    包含API集成、数据处理和智能筛选功能。
    """

    def __init__(self):
        """
        初始化景点查找服务

        设置API配置、价格映射和成本估算规则，
        为各种类型的场所搜索做准备。
        """
        # API配置
        self.api_key = api_config.GOOGLE_PLACES_API_KEY  # Google Places API密钥
        self.base_url = api_config.PLACES_BASE_URL       # API基础URL
        self.session = requests.Session()                # HTTP会话对象

        # 不同预算范围的价格映射
        self.budget_price_mapping = {
            '经济型': {'min': 0, 'max': 2, 'multiplier': 0.7},    # 经济型：价格较低
            '中等预算': {'min': 1, 'max': 3, 'multiplier': 1.0},   # 中等：标准价格
            '豪华型': {'min': 2, 'max': 4, 'multiplier': 1.5}     # 豪华：价格较高
        }

        # 不同类型场所的成本估算（基础费用，人民币）
        self.cost_estimates = {
            'attraction': {'经济型': 100, '中等预算': 180, '豪华型': 320},  # 景点门票
            'restaurant': {'经济型': 150, '中等预算': 280, '豪华型': 560}, # 餐厅用餐
            'activity': {'经济型': 200, '中等预算': 420, '豪华型': 840}   # 娱乐活动
        }
    
    def find_attractions(self, trip_details: Dict[str, Any]) -> List[Attraction]:
        """
        根据旅行详情查找旅游景点

        这个方法负责搜索和推荐适合的旅游景点，包括：
        1. 使用Google Places API搜索实际景点
        2. 根据用户预算和偏好筛选
        3. 提供模拟数据作为回退方案
        4. 返回排序后的景点列表

        参数：
        - trip_details: 包含目的地、预算等信息的旅行详情字典

        返回：Attraction对象列表，按推荐度排序

        功能说明：
        1. 构建搜索查询
        2. 尝试API调用获取真实数据
        3. 处理和筛选搜索结果
        4. 回退到模拟数据（如果需要）
        """
        try:
            attractions = []
            query = f"{trip_details['destination']} 旅游景点"  # 中文搜索查询

            # 首先尝试API调用
            if self.api_key:
                places_data = self._search_places(query, 'tourist_attraction')
                attractions = self._process_places_data(places_data, 'attraction', trip_details)

            # 如果API失败或无密钥，回退到模拟数据
            if not attractions:
                attractions = self._get_mock_attractions(trip_details)

            # 返回限定数量的景点
            return attractions[:app_config.MAX_ATTRACTIONS]

        except Exception as e:
            print(f"查找景点时出错: {e}")
            return self._get_mock_attractions(trip_details)
    
    def find_restaurants(self, trip_details: Dict[str, Any]) -> List[Attraction]:
        """Find restaurants based on trip details"""
        try:
            restaurants = []
            query = f"restaurants in {trip_details['destination']}"
            
            # Try API call first
            if self.api_key:
                places_data = self._search_places(query, 'restaurant')
                restaurants = self._process_places_data(places_data, 'restaurant', trip_details)
            
            # Fallback to mock data
            if not restaurants:
                restaurants = self._get_mock_restaurants(trip_details)
            
            return restaurants[:app_config.MAX_RESTAURANTS]
            
        except Exception as e:
            print(f"Error finding restaurants: {e}")
            return self._get_mock_restaurants(trip_details)
    
    def find_activities(self, trip_details: Dict[str, Any]) -> List[Attraction]:
        """Find activities based on trip details and preferences"""
        try:
            activities = []
            
            # Build query based on preferences
            interests = trip_details.get('preferences', {}).get('interests', [])
            if interests:
                query = f"{' '.join(interests)} activities in {trip_details['destination']}"
            else:
                query = f"things to do activities in {trip_details['destination']}"
            
            # Try API call first
            if self.api_key:
                places_data = self._search_places(query, 'point_of_interest')
                activities = self._process_places_data(places_data, 'activity', trip_details)
            
            # Fallback to mock data
            if not activities:
                activities = self._get_mock_activities(trip_details)
            
            return activities[:app_config.MAX_ACTIVITIES]
            
        except Exception as e:
            print(f"Error finding activities: {e}")
            return self._get_mock_activities(trip_details)
    
    def _search_places(self, query: str, place_type: str) -> List[Dict]:
        """Search places using Google Places API"""
        try:
            url = f"{self.base_url}/textsearch/json"
            params = {
                'query': query,
                'key': self.api_key,
                'type': place_type
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            return data.get('results', [])
            
        except Exception as e:
            print(f"API search failed: {e}")
            return []
    
    def _process_places_data(self, places_data: List[Dict], place_type: str, trip_details: Dict) -> List[Attraction]:
        """Process Google Places API response into Attraction objects"""
        attractions = []
        budget_range = trip_details.get('budget_range', 'mid-range')
        
        for place in places_data:
            try:
                # Extract basic information
                name = place.get('name', 'Unknown')
                rating = place.get('rating', 4.0)
                price_level = place.get('price_level', 2)
                address = place.get('formatted_address', 'Address not available')
                
                # Estimate cost based on type and budget
                estimated_cost = self._estimate_cost(place_type, budget_range, price_level)
                
                # Determine duration based on type
                duration = self._get_duration_by_type(place_type)
                
                attraction = Attraction(
                    name=name,
                    type=place_type,
                    rating=rating,
                    price_level=price_level,
                    address=address,
                    description=self._generate_description(place, place_type),
                    estimated_cost=estimated_cost,
                    duration=duration
                )
                
                attractions.append(attraction)
                
            except Exception as e:
                print(f"Error processing place data: {e}")
                continue
        
        return attractions
    
    def _estimate_cost(self, place_type: str, budget_range: str, price_level: int) -> float:
        """Estimate cost based on place type, budget range, and price level"""
        base_cost = self.cost_estimates.get(place_type, {}).get(budget_range, 30)
        
        # Adjust based on price level (0-4 scale from Google)
        price_multipliers = {0: 0.5, 1: 0.7, 2: 1.0, 3: 1.3, 4: 1.8}
        multiplier = price_multipliers.get(price_level, 1.0)
        
        return round(base_cost * multiplier, 2)
    
    def _get_duration_by_type(self, place_type: str) -> int:
        """Get typical duration in hours for different place types"""
        durations = {
            'attraction': 2,
            'restaurant': 1,
            'activity': 3
        }
        return durations.get(place_type, 2)
    
    def _generate_description(self, place: Dict, place_type: str) -> str:
        """Generate a description for the place"""
        types = place.get('types', [])
        rating = place.get('rating', 0)
        
        description_parts = []
        
        if rating >= 4.5:
            description_parts.append("Highly rated")
        elif rating >= 4.0:
            description_parts.append("Well-reviewed")
        
        if 'museum' in types:
            description_parts.append("cultural attraction")
        elif 'park' in types:
            description_parts.append("outdoor space")
        elif 'restaurant' in types:
            description_parts.append("dining establishment")
        elif 'shopping_mall' in types:
            description_parts.append("shopping destination")
        
        return " ".join(description_parts) if description_parts else f"Popular {place_type}"
    
    def _get_mock_attractions(self, trip_details: Dict) -> List[Attraction]:
        """Generate mock attraction data when API is unavailable"""
        destination = trip_details['destination']
        budget_range = trip_details.get('budget_range', 'mid-range')
        
        mock_attractions = [
            {
                'name': f'{destination} Historical Museum',
                'rating': 4.3,
                'price_level': 2,
                'description': 'Learn about local history and culture',
                'duration': 2
            },
            {
                'name': f'{destination} Central Park',
                'rating': 4.5,
                'price_level': 0,
                'description': 'Beautiful public park perfect for relaxation',
                'duration': 2
            },
            {
                'name': f'{destination} Art Gallery',
                'rating': 4.2,
                'price_level': 2,
                'description': 'Contemporary and classical art exhibitions',
                'duration': 2
            },
            {
                'name': f'{destination} Old Town District',
                'rating': 4.6,
                'price_level': 1,
                'description': 'Historic architecture and charming streets',
                'duration': 3
            },
            {
                'name': f'{destination} Observatory',
                'rating': 4.4,
                'price_level': 2,
                'description': 'Panoramic city views and astronomical exhibits',
                'duration': 2
            },
            {
                'name': f'{destination} Cultural Center',
                'rating': 4.1,
                'price_level': 2,
                'description': 'Local performances and cultural events',
                'duration': 2
            },
            {
                'name': f'{destination} Botanical Gardens',
                'rating': 4.7,
                'price_level': 1,
                'description': 'Diverse plant collections and peaceful walkways',
                'duration': 2
            },
            {
                'name': f'{destination} Waterfront Promenade',
                'rating': 4.5,
                'price_level': 0,
                'description': 'Scenic waterfront walks and recreational activities',
                'duration': 2
            }
        ]
        
        attractions = []
        for mock in mock_attractions:
            cost = self._estimate_cost('attraction', budget_range, mock['price_level'])
            
            attraction = Attraction(
                name=mock['name'],
                type='attraction',
                rating=mock['rating'],
                price_level=mock['price_level'],
                address=f"{destination} City Center",
                description=mock['description'],
                estimated_cost=cost,
                duration=mock['duration']
            )
            attractions.append(attraction)
        
        return attractions
    
    def _get_mock_restaurants(self, trip_details: Dict) -> List[Attraction]:
        """Generate mock restaurant data"""
        destination = trip_details['destination']
        budget_range = trip_details.get('budget_range', 'mid-range')
        
        mock_restaurants = [
            {
                'name': f'The Local Bistro - {destination}',
                'rating': 4.4,
                'price_level': 2,
                'description': 'Traditional local cuisine with modern twist'
            },
            {
                'name': f'{destination} Street Food Market',
                'rating': 4.2,
                'price_level': 1,
                'description': 'Authentic street food and local delicacies'
            },
            {
                'name': 'Fine Dining Restaurant',
                'rating': 4.6,
                'price_level': 3,
                'description': 'Upscale dining experience with seasonal menu'
            },
            {
                'name': 'Rooftop Cafe',
                'rating': 4.3,
                'price_level': 2,
                'description': 'Great views with coffee and light meals'
            },
            {
                'name': 'Family Restaurant',
                'rating': 4.1,
                'price_level': 2,
                'description': 'Comfortable atmosphere with international cuisine'
            },
            {
                'name': 'Vegetarian Haven',
                'rating': 4.5,
                'price_level': 2,
                'description': 'Plant-based cuisine with fresh local ingredients'
            },
            {
                'name': 'Seafood Speciality',
                'rating': 4.4,
                'price_level': 3,
                'description': 'Fresh seafood with harbor views'
            }
        ]
        
        restaurants = []
        for mock in mock_restaurants:
            cost = self._estimate_cost('restaurant', budget_range, mock['price_level'])
            
            restaurant = Attraction(
                name=mock['name'],
                type='restaurant',
                rating=mock['rating'],
                price_level=mock['price_level'],
                address=f"{destination} Downtown",
                description=mock['description'],
                estimated_cost=cost,
                duration=1
            )
            restaurants.append(restaurant)
        
        return restaurants
    
    def _get_mock_activities(self, trip_details: Dict) -> List[Attraction]:
        """Generate mock activity data"""
        destination = trip_details['destination']
        budget_range = trip_details.get('budget_range', 'mid-range')
        interests = trip_details.get('preferences', {}).get('interests', [])
        
        # Base activities
        mock_activities = [
            {
                'name': f'{destination} City Walking Tour',
                'rating': 4.3,
                'price_level': 1,
                'description': 'Guided tour of major landmarks and hidden gems',
                'duration': 3
            },
            {
                'name': 'Local Cooking Class',
                'rating': 4.6,
                'price_level': 2,
                'description': 'Learn to cook traditional dishes with local chef',
                'duration': 4
            },
            {
                'name': 'Bike Rental & City Tour',
                'rating': 4.2,
                'price_level': 2,
                'description': 'Explore the city on two wheels',
                'duration': 3
            },
            {
                'name': 'River Cruise',
                'rating': 4.4,
                'price_level': 2,
                'description': 'Scenic boat ride with city skyline views',
                'duration': 2
            },
            {
                'name': 'Adventure Sports Package',
                'rating': 4.5,
                'price_level': 3,
                'description': 'Thrilling outdoor activities and adventures',
                'duration': 4
            }
        ]
        
        # Add interest-specific activities
        if 'museums' in [i.lower() for i in interests]:
            mock_activities.append({
                'name': f'{destination} Museum Pass',
                'rating': 4.4,
                'price_level': 2,
                'description': 'Access to multiple museums and galleries',
                'duration': 4
            })
        
        if 'food' in [i.lower() for i in interests]:
            mock_activities.append({
                'name': 'Food & Wine Tasting Tour',
                'rating': 4.7,
                'price_level': 3,
                'description': 'Sample local wines and gourmet food',
                'duration': 3
            })
        
        if 'nightlife' in [i.lower() for i in interests]:
            mock_activities.append({
                'name': 'Evening Entertainment Package',
                'rating': 4.2,
                'price_level': 3,
                'description': 'Experience local nightlife and entertainment',
                'duration': 4
            })
        
        activities = []
        for mock in mock_activities:
            cost = self._estimate_cost('activity', budget_range, mock['price_level'])
            
            activity = Attraction(
                name=mock['name'],
                type='activity',
                rating=mock['rating'],
                price_level=mock['price_level'],
                address=f"{destination} Activity Center",
                description=mock['description'],
                estimated_cost=cost,
                duration=mock.get('duration', 3)
            )
            activities.append(activity)
        
        return activities
    
    def get_recommendations_by_interests(self, attractions: List[Attraction], interests: List[str]) -> List[Attraction]:
        """Filter and rank attractions based on user interests"""
        if not interests:
            return attractions
        
        scored_attractions = []
        interest_keywords = [interest.lower() for interest in interests]
        
        for attraction in attractions:
            score = 0
            attraction_text = f"{attraction.name} {attraction.description}".lower()
            
            # Score based on keyword matches
            for keyword in interest_keywords:
                if keyword in attraction_text:
                    score += 2
                
                # Bonus for exact matches in name
                if keyword in attraction.name.lower():
                    score += 1
            
            # Bonus for high ratings
            if attraction.rating >= 4.5:
                score += 1
            elif attraction.rating >= 4.0:
                score += 0.5
            
            scored_attractions.append((attraction, score))
        
        # Sort by score (descending) and return attractions
        scored_attractions.sort(key=lambda x: x[1], reverse=True)
        return [attraction for attraction, score in scored_attractions]