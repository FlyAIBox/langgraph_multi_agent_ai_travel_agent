"""
行程规划逻辑模块

这个模块负责创建详细的逐日行程安排，包括：
- 景点和活动的时间分配
- 基于天气的活动推荐
- 交通方式和时间估算
- 餐饮安排和时间规划
- 每日费用计算和优化
- 个性化行程定制

适用于大模型技术初级用户：
这个模块展示了如何设计一个智能的行程规划系统，
包含时间管理、天气适应和个性化推荐算法。
"""

import random
from typing import Dict, Any, List
from datetime import datetime, date, timedelta
from ..data.models import DayPlan, Weather, Attraction, Transportation

class ItineraryPlanner:
    """
    行程规划服务类

    这个类负责创建详细的逐日旅行行程，包括：
    1. 景点和活动的智能分配
    2. 基于天气的活动调整
    3. 时间段的合理安排
    4. 交通方式的选择和估算
    5. 餐饮时间的规划
    6. 每日费用的计算

    主要功能：
    - 智能时间分配
    - 天气适应性规划
    - 交通优化
    - 个性化定制

    适用于大模型技术初级用户：
    这个类展示了如何构建一个复杂的规划算法，
    包含多维度的约束条件和优化目标。
    """

    def __init__(self):
        """
        初始化行程规划服务

        设置活动时间偏好、天气活动推荐和交通估算，
        为智能行程规划做准备。
        """
        # 活动时间偏好设置
        self.activity_timings = {
            'morning': {    # 上午时段
                'start': 9, 'end': 12,
                'activities': ['博物馆', '美术馆', '公园', '观光']
            },
            'afternoon': {  # 下午时段
                'start': 13, 'end': 17,
                'activities': ['活动', '购物', '游览', '景点']
            },
            'evening': {    # 晚上时段
                'start': 18, 'end': 21,
                'activities': ['用餐', '娱乐', '夜生活', '文化']
            }
        }

        # 基于天气的活动推荐
        self.weather_activities = {
            'sunny': ['户外游览', '公园', '步行游', '户外活动'],      # 晴天
            'rainy': ['博物馆', '美术馆', '购物', '室内景点'],       # 雨天
            'cloudy': ['观光', '文化景点', '混合活动'],             # 多云
            'cold': ['室内景点', '博物馆', '温暖咖啡厅', '购物'],    # 寒冷
            'hot': ['室内景点', '早晨游览', '晚间活动']              # 炎热
        }

        # 活动间交通估算（人民币和时间）
        self.transport_estimates = {
            'walking': {'cost': 0, 'time': 15},           # 步行
            'public_transport': {'cost': 20, 'time': 20}, # 公共交通
            'taxi': {'cost': 80, 'time': 15},             # 出租车
            'uber': {'cost': 70, 'time': 12}              # 网约车
        }
    
    def create_itinerary(self, trip_details: Dict[str, Any], weather_data: List[Weather],
                        attractions: List[Attraction], restaurants: List[Attraction],
                        activities: List[Attraction]) -> List[DayPlan]:
        """
        创建完整的逐日行程安排

        这个方法是行程规划的核心，它整合所有信息，
        创建优化的每日行程计划。

        参数：
        - trip_details: 旅行详情字典
        - weather_data: 天气预报数据列表
        - attractions: 景点列表
        - restaurants: 餐厅列表
        - activities: 活动列表

        返回：DayPlan对象列表，每个代表一天的行程

        功能说明：
        1. 提取旅行基本信息
        2. 将景点、餐厅、活动分配到各天
        3. 根据天气优化每日安排
        4. 计算每日费用和交通
        5. 生成完整的行程计划
        """

        # 提取基本信息
        total_days = trip_details['total_days']                           # 总天数
        start_date = trip_details['start_date']                          # 开始日期
        budget_range = trip_details.get('budget_range', '中等预算')       # 预算范围
        group_size = trip_details.get('group_size', 1)                   # 团队人数
        interests = trip_details.get('preferences', {}).get('interests', [])  # 兴趣爱好

        itinerary = []  # 行程列表

        # 将景点、餐厅和活动分配到各天
        daily_attractions = self._distribute_items_across_days(attractions, total_days, 2)  # 每天2个景点
        daily_restaurants = self._distribute_items_across_days(restaurants, total_days, 2)  # 每天2个餐厅
        daily_activities = self._distribute_items_across_days(activities, total_days, 1)
        
        for day_num in range(1, total_days + 1):
            current_date = start_date + timedelta(days=day_num - 1)
            date_str = current_date.strftime('%Y-%m-%d')
            
            # Get weather for this day
            day_weather = self._get_weather_for_day(weather_data, day_num - 1)
            
            # Create day plan
            day_plan = DayPlan(
                day=day_num,
                date=date_str,
                weather=day_weather
            )
            
            # Add attractions for the day
            if day_num <= len(daily_attractions):
                day_plan.attractions = daily_attractions[day_num - 1]
            
            # Add restaurants for the day
            if day_num <= len(daily_restaurants):
                day_plan.restaurants = daily_restaurants[day_num - 1]
            
            # Add activities for the day
            if day_num <= len(daily_activities):
                day_plan.activities = daily_activities[day_num - 1]
            
            # Optimize schedule based on weather and interests
            day_plan = self._optimize_day_schedule(day_plan, interests, budget_range)
            
            # Add transportation between activities
            day_plan.transportation = self._plan_transportation(day_plan, budget_range)
            
            # Calculate daily costs
            day_plan.daily_cost = self._calculate_daily_cost(day_plan, group_size)
            
            itinerary.append(day_plan)
        
        # Balance the itinerary across days
        itinerary = self._balance_itinerary(itinerary, total_days)
        
        return itinerary
    
    def _distribute_items_across_days(self, items: List[Attraction], total_days: int, items_per_day: int) -> List[List[Attraction]]:
        """Distribute attractions/restaurants/activities across days"""
        if not items:
            return [[] for _ in range(total_days)]
        
        # Sort items by rating (best first)
        sorted_items = sorted(items, key=lambda x: x.rating, reverse=True)
        
        daily_items = []
        for day in range(total_days):
            start_idx = day * items_per_day
            end_idx = start_idx + items_per_day
            day_items = sorted_items[start_idx:end_idx]
            daily_items.append(day_items)
        
        return daily_items
    
    def _get_weather_for_day(self, weather_data: List[Weather], day_index: int) -> Weather:
        """Get weather data for specific day"""
        if day_index < len(weather_data):
            return weather_data[day_index]
        
        # Fallback weather if not enough data
        return Weather(
            temperature=22.0,
            description="Partly Cloudy",
            humidity=65,
            wind_speed=5.0,
            feels_like=24.0,
            date=(datetime.now() + timedelta(days=day_index)).strftime('%Y-%m-%d')
        )
    
    def _optimize_day_schedule(self, day_plan: DayPlan, interests: List[str], budget_range: str) -> DayPlan:
        """Optimize daily schedule based on weather and preferences"""
        
        # Get weather condition category
        weather_condition = self._categorize_weather(day_plan.weather)
        
        # Reorder activities based on weather
        if weather_condition == 'rainy':
            # Prioritize indoor activities
            day_plan.attractions = self._prioritize_indoor_activities(day_plan.attractions)
            day_plan.activities = self._prioritize_indoor_activities(day_plan.activities)
        elif weather_condition == 'sunny':
            # Prioritize outdoor activities
            day_plan.attractions = self._prioritize_outdoor_activities(day_plan.attractions)
            day_plan.activities = self._prioritize_outdoor_activities(day_plan.activities)
        
        # Add timing recommendations
        day_plan = self._add_timing_recommendations(day_plan)
        
        # Add weather-specific recommendations
        day_plan = self._add_weather_recommendations(day_plan, weather_condition)
        
        return day_plan
    
    def _categorize_weather(self, weather: Weather) -> str:
        """Categorize weather condition"""
        description = weather.description.lower()
        temp = weather.temperature
        
        if 'rain' in description or 'storm' in description:
            return 'rainy'
        elif temp < 10:
            return 'cold'
        elif temp > 30:
            return 'hot'
        elif 'sun' in description or 'clear' in description:
            return 'sunny'
        else:
            return 'cloudy'
    
    def _prioritize_indoor_activities(self, activities: List[Attraction]) -> List[Attraction]:
        """Prioritize indoor activities for bad weather"""
        indoor_keywords = ['museum', 'gallery', 'mall', 'center', 'indoor', 'theater', 'cinema']
        
        indoor_activities = []
        outdoor_activities = []
        
        for activity in activities:
            is_indoor = any(keyword in activity.name.lower() or keyword in activity.description.lower() 
                          for keyword in indoor_keywords)
            
            if is_indoor:
                indoor_activities.append(activity)
            else:
                outdoor_activities.append(activity)
        
        return indoor_activities + outdoor_activities
    
    def _prioritize_outdoor_activities(self, activities: List[Attraction]) -> List[Attraction]:
        """Prioritize outdoor activities for good weather"""
        outdoor_keywords = ['park', 'garden', 'tour', 'walk', 'outdoor', 'beach', 'view', 'nature']
        
        outdoor_activities = []
        indoor_activities = []
        
        for activity in activities:
            is_outdoor = any(keyword in activity.name.lower() or keyword in activity.description.lower() 
                           for keyword in outdoor_keywords)
            
            if is_outdoor:
                outdoor_activities.append(activity)
            else:
                indoor_activities.append(activity)
        
        return outdoor_activities + indoor_activities
    
    def _add_timing_recommendations(self, day_plan: DayPlan) -> DayPlan:
        """Add timing recommendations for activities"""
        
        # Add timing attributes to activities
        for i, attraction in enumerate(day_plan.attractions):
            if i == 0:
                attraction.recommended_time = "9:00 AM - 11:00 AM"
                attraction.time_slot = "morning"
            else:
                attraction.recommended_time = "2:00 PM - 4:00 PM"
                attraction.time_slot = "afternoon"
        
        for activity in day_plan.activities:
            activity.recommended_time = "10:00 AM - 1:00 PM"
            activity.time_slot = "morning-afternoon"
        
        for i, restaurant in enumerate(day_plan.restaurants):
            if i == 0:
                restaurant.recommended_time = "12:00 PM - 1:30 PM"
                restaurant.time_slot = "lunch"
            else:
                restaurant.recommended_time = "7:00 PM - 9:00 PM"
                restaurant.time_slot = "dinner"
        
        return day_plan
    
    def _add_weather_recommendations(self, day_plan: DayPlan, weather_condition: str) -> DayPlan:
        """Add weather-specific recommendations"""
        recommendations = []
        
        if weather_condition == 'rainy':
            recommendations.extend([
                "Carry an umbrella or raincoat",
                "Focus on indoor attractions today",
                "Consider museum hopping",
                "Perfect day for shopping centers"
            ])
        elif weather_condition == 'sunny':
            recommendations.extend([
                "Great day for outdoor activities",
                "Don't forget sunscreen and water",
                "Perfect for walking tours",
                "Consider outdoor dining"
            ])
        elif weather_condition == 'cold':
            recommendations.extend([
                "Dress warmly in layers",
                "Indoor attractions recommended",
                "Hot drinks and warm cafes",
                "Shorter outdoor activities"
            ])
        elif weather_condition == 'hot':
            recommendations.extend([
                "Stay hydrated and seek shade",
                "Plan indoor activities during peak heat",
                "Early morning or evening outdoor activities",
                "Air-conditioned venues recommended"
            ])
        
        # Add recommendations as an attribute to the day plan
        if not hasattr(day_plan, 'recommendations'):
            day_plan.recommendations = []
        day_plan.recommendations.extend(recommendations)
        
        return day_plan
    
    def _plan_transportation(self, day_plan: DayPlan, budget_range: str) -> List[Transportation]:
        """Plan transportation between activities"""
        transportation = []
        
        # Count total activities for the day
        total_activities = len(day_plan.attractions) + len(day_plan.activities) + len(day_plan.restaurants)
        
        if total_activities <= 1:
            return transportation
        
        # Determine transport mode based on budget
        transport_modes = {
            'budget': ['walking', 'public_transport'],
            'mid-range': ['walking', 'public_transport', 'uber'],
            'luxury': ['taxi', 'uber', 'public_transport']
        }
        
        available_modes = transport_modes.get(budget_range, ['public_transport', 'walking'])
        
        # Create transportation entries between activities
        for i in range(total_activities - 1):
            mode = random.choice(available_modes)
            transport_info = self.transport_estimates[mode]
            
            transport = Transportation(
                mode=mode.replace('_', ' ').title(),
                estimated_cost=transport_info['cost'],
                duration=transport_info['time']
            )
            transportation.append(transport)
        
        return transportation
    
    def _calculate_daily_cost(self, day_plan: DayPlan, group_size: int) -> float:
        """Calculate total cost for the day"""
        total_cost = 0.0
        
        # Add attraction costs
        for attraction in day_plan.attractions:
            total_cost += attraction.estimated_cost * group_size
        
        # Add restaurant costs
        for restaurant in day_plan.restaurants:
            total_cost += restaurant.estimated_cost * group_size
        
        # Add activity costs
        for activity in day_plan.activities:
            total_cost += activity.estimated_cost * group_size
        
        # Add transportation costs
        for transport in day_plan.transportation:
            total_cost += transport.estimated_cost * group_size
        
        return round(total_cost, 2)
    
    def _balance_itinerary(self, itinerary: List[DayPlan], total_days: int) -> List[DayPlan]:
        """Balance activities across days to avoid overloading"""
        
        # Calculate average activities per day
        total_attractions = sum(len(day.attractions) for day in itinerary)
        total_activities = sum(len(day.activities) for day in itinerary)
        
        target_attractions_per_day = max(1, total_attractions // total_days)
        target_activities_per_day = max(1, total_activities // total_days)
        
        # Redistribute if any day is heavily overloaded
        for i, day_plan in enumerate(itinerary):
            if len(day_plan.attractions) > target_attractions_per_day + 1:
                # Move excess attractions to less busy days
                excess = day_plan.attractions[target_attractions_per_day:]
                day_plan.attractions = day_plan.attractions[:target_attractions_per_day]
                
                # Find days with fewer attractions
                for j, other_day in enumerate(itinerary):
                    if j != i and len(other_day.attractions) < target_attractions_per_day and excess:
                        other_day.attractions.append(excess.pop(0))
            
            # Recalculate daily cost after rebalancing
            day_plan.daily_cost = self._calculate_daily_cost(day_plan, 1)  # Will be multiplied by group size later
        
        return itinerary
    
    def generate_itinerary_summary(self, itinerary: List[DayPlan]) -> Dict[str, Any]:
        """Generate summary of the complete itinerary"""
        
        total_attractions = sum(len(day.attractions) for day in itinerary)
        total_restaurants = sum(len(day.restaurants) for day in itinerary)
        total_activities = sum(len(day.activities) for day in itinerary)
        total_cost = sum(day.daily_cost for day in itinerary)
        
        # Find best rated activities
        all_items = []
        for day in itinerary:
            all_items.extend(day.attractions + day.restaurants + day.activities)
        
        top_rated = sorted(all_items, key=lambda x: x.rating, reverse=True)[:5]
        
        # Weather overview
        weather_conditions = [day.weather.description for day in itinerary]
        
        summary = {
            'total_days': len(itinerary),
            'total_attractions': total_attractions,
            'total_restaurants': total_restaurants,
            'total_activities': total_activities,
            'estimated_total_cost': round(total_cost, 2),
            'average_daily_cost': round(total_cost / len(itinerary), 2) if itinerary else 0,
            'top_rated_experiences': [
                {
                    'name': item.name,
                    'type': item.type,
                    'rating': item.rating,
                    'cost': item.estimated_cost
                } for item in top_rated
            ],
            'weather_overview': {
                'conditions': weather_conditions,
                'rainy_days': len([w for w in weather_conditions if 'rain' in w.lower()]),
                'sunny_days': len([w for w in weather_conditions if 'sun' in w.lower() or 'clear' in w.lower()])
            },
            'daily_highlights': [
                {
                    'day': day.day,
                    'date': day.date,
                    'weather': day.weather.description,
                    'main_attractions': [a.name for a in day.attractions[:2]],
                    'main_activity': day.activities[0].name if day.activities else None,
                    'cost': day.daily_cost
                } for day in itinerary
            ]
        }
        
        return summary
    
    def export_itinerary_to_text(self, itinerary: List[DayPlan], trip_details: Dict[str, Any]) -> str:
        """Export itinerary to formatted text"""
        
        text_output = []
        text_output.append("=" * 60)
        text_output.append(f"TRAVEL ITINERARY - {trip_details['destination'].upper()}")
        text_output.append("=" * 60)
        text_output.append(f"Duration: {len(itinerary)} days")
        text_output.append(f"Dates: {trip_details['start_date']} to {trip_details['end_date']}")
        text_output.append(f"Budget Range: {trip_details['budget_range'].title()}")
        text_output.append("")
        
        for day_plan in itinerary:
            text_output.append(f"DAY {day_plan.day} - {day_plan.date}")
            text_output.append("-" * 40)
            text_output.append(f"Weather: {day_plan.weather}")
            text_output.append("")
            
            if day_plan.attractions:
                text_output.append("🏛️  ATTRACTIONS:")
                for attraction in day_plan.attractions:
                    time_info = getattr(attraction, 'recommended_time', 'Flexible timing')
                    text_output.append(f"   • {attraction.name} ({time_info})")
                    text_output.append(f"     Rating: {attraction.rating}⭐ | Cost: ${attraction.estimated_cost}")
                text_output.append("")
            
            if day_plan.activities:
                text_output.append("🎯 ACTIVITIES:")
                for activity in day_plan.activities:
                    time_info = getattr(activity, 'recommended_time', 'Flexible timing')
                    text_output.append(f"   • {activity.name} ({time_info})")
                    text_output.append(f"     Duration: {activity.duration}h | Cost: ${activity.estimated_cost}")
                text_output.append("")
            
            if day_plan.restaurants:
                text_output.append("🍽️  DINING:")
                for restaurant in day_plan.restaurants:
                    time_info = getattr(restaurant, 'recommended_time', 'Meal time')
                    text_output.append(f"   • {restaurant.name} ({time_info})")
                    text_output.append(f"     Rating: {restaurant.rating}⭐ | Cost: ${restaurant.estimated_cost}")
                text_output.append("")
            
            if hasattr(day_plan, 'recommendations') and day_plan.recommendations:
                text_output.append("💡 RECOMMENDATIONS:")
                for rec in day_plan.recommendations:
                    text_output.append(f"   • {rec}")
                text_output.append("")
            
            text_output.append(f"💰 Daily Cost Estimate: ${day_plan.daily_cost}")
            text_output.append("")
            text_output.append("=" * 60)
            text_output.append("")
        
        return "\n".join(text_output)