![](https://github.com/abh2050/langgraph_multi_agent_ai_travel_agent/blob/main/Gemini_Generated_Image_mk2gn4mk2gn4mk2g.png)
# 🚀 AI旅行助手与费用规划师 - LangGraph多智能体系统

## 项目概述

这是一个使用**LangGraph**、**Google Gemini Flash-2.0**和**DuckDuckGo搜索**构建的最先进的多智能体旅行规划系统。该系统提供三种不同的规划方法，从传统的单智能体到使用现代工业框架的前沿多智能体协作。

## 🤖 规划选项

从三种不同的规划体验中选择：

### 1. 🔧 单智能体规划（经典版）
- 传统的单AI智能体方法
- 直接规划方法论
- 经过验证的可靠性和效率

### 2. 🚀 传统多智能体（自定义框架）
- 6个专业AI智能体协同工作
- 自定义多智能体框架
- 通过协作增强推荐效果

### 3. 🌟 LangGraph多智能体（高级版）⭐ **推荐使用**
- **Google Gemini Flash-2.0**驱动的智能体
- **DuckDuckGo实时搜索**集成
- **LangGraph工作流**编排
- 最先进的多智能体协作

## 🏗️ LangGraph系统架构
![](https://github.com/abh2050/langraph_multi_agent_ai_travel_agent/blob/main/Editor%20_%20Mermaid%20Chart-2025-06-20-183945.png)

### 框架组件
- **LangGraph StateGraph**: 工作流编排和状态管理
- **Google Gemini Flash-2.0**: 高级AI推理和自然语言处理
- **DuckDuckGo搜索**: 实时信息检索（无需API密钥）
- **Pydantic**: 类型安全和数据验证
- **自定义智能体协议**: 智能体间的专业化通信

### 🤖 AI智能体网络

| 智能体 | 角色 | 能力 |
|-------|------|-------------|
| **协调员** | 工作流编排与决策综合 | 总体规划、任务委派、共识构建 |
| **旅行顾问** | 目的地专业知识与实时搜索 | 景点研究、目的地洞察、文化指导 |
| **天气分析师** | 天气情报与当前数据 | 天气预报、气候分析、打包建议 |
| **预算优化师** | 成本分析与实时定价 | 预算规划、成本优化、省钱策略 |
| **当地专家** | 内部知识与本地信息 | 当地贴士、小众景点、文化礼仪 |
| **行程规划师** | 日程优化与物流 | 逐日规划、路线优化、时间安排 |

## 🎯 核心功能

### 高级能力
- ✅ **实时搜索集成**: 来自DuckDuckGo的实时数据
- ✅ **状态管理**: 跨智能体的持久对话状态
- ✅ **工具增强智能体**: 每个智能体都有专门的搜索工具
- ✅ **协作决策制定**: 智能体协同工作创建最优计划
- ✅ **工作流编排**: LangGraph管理复杂的智能体交互
- ✅ **错误处理**: 强大的错误恢复和回退机制

### 搜索工具
1. **目的地信息**: 通用目的地研究
2. **天气情报**: 当前和预测的天气数据
3. **景点发现**: 顶级景点和活动
4. **酒店研究**: 住宿选择和定价
5. **餐厅查找**: 用餐推荐和评价
6. **当地洞察**: 文化贴士和内部知识
7. **预算分析**: 成本估算和预算规划
## 🚀 快速开始

### 前置要求
```bash
# Python 3.10+
pip install -r requirements.txt
```

### 安装配置
1. **获取Gemini API密钥**: 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **配置环境**: 将您的API密钥添加到 `.env` 文件
   ```bash
   GEMINI_API_KEY=your_actual_api_key_here
   ```
3. **验证安装**: 运行测试脚本
   ```bash
   python test_langgraph_system.py
   ```

### 运行系统

#### 选项1: 主菜单（全部3个系统）
```bash
python main.py
# 选择选项3使用LangGraph（推荐）
# 选择选项2使用传统多智能体
# 选择选项1使用单智能体
```

#### 选项2: 直接运行LangGraph系统
```bash
python langgraph_main.py
```

#### 选项3: 无API密钥测试
```bash
python test_langgraph_system.py
```

## 📊 使用示例

### 演示模式
```bash
python langgraph_main.py
# 选择选项1进行北京演示
```

### 交互式规划
```bash
python langgraph_main.py
# 选择选项2进行自定义旅行规划
```

### 系统验证
```bash
python test_langgraph_system.py
# 测试所有组件，无需API调用
```

## 🛠️ 配置说明

### 环境变量
```bash
# LangGraph系统必需
GEMINI_API_KEY=your_gemini_api_key

# 可选（用于传统系统）
OPENWEATHER_API_KEY=your_weather_api_key
GOOGLE_PLACES_API_KEY=your_places_api_key
EXCHANGERATE_API_KEY=your_exchange_rate_api_key
```

### 模型配置
```python
class LangGraphConfig:
    GEMINI_MODEL = "gemini-2.0-flash"
    TEMPERATURE = 0.7
    MAX_TOKENS = 4000
    TOP_P = 0.9
```

### API配置（可选）
为了增强传统功能，可获取免费API密钥：

1. **Google Gemini API**（LangGraph系统必需）
   - 获取密钥: https://makersuite.google.com/app/apikey
   - 添加到.env: `GEMINI_API_KEY=your_key`

2. **OpenWeather API**（传统天气数据）
   - 获取密钥: https://openweathermap.org/api
   - 添加到.env: `OPENWEATHER_API_KEY=your_key`

3. **Google Places API**（传统景点/酒店）
   - 获取密钥: Google Cloud Console
   - 添加到.env: `GOOGLE_PLACES_API_KEY=your_key`

4. **Exchange Rate API**（传统货币转换）
   - 获取密钥: https://exchangerate-api.com/
   - 添加到.env: `EXCHANGERATE_API_KEY=your_key`

**注意**: LangGraph系统使用DuckDuckGo搜索（无需API密钥），独立于传统API工作。

## 使用示例

```
🌍 AI旅行助手与费用规划师
====================================

输入目的地: 北京
开始日期: 2025-12-25
结束日期: 2025-12-30
预算范围: 中等预算
货币: CNY
团队人数: 2
兴趣爱好: 博物馆, 美食, 文化

→ 生成完整的5天北京行程，包含:
   • 天气预报
   • 博物馆和餐厅推荐
   • 酒店选择
   • 每日费用明细
   • 货币转换费用
```
## 示例报告
```
================================================================================
LANGGRAPH多智能体AI旅行规划报告
================================================================================
生成时间: 2025-06-20 12:58:25
系统: LangGraph框架 + Google Gemini & DuckDuckGo

行程概览:
----------------------------------------
目的地: 上海
行程时长: 3天
团队人数: 3人
预算范围: 中等预算
兴趣爱好:

系统性能:
----------------------------------------
规划方法: LangGraph多智能体协作
总迭代次数: 7
参与智能体: 5个

智能体贡献:
----------------------------------------

旅行顾问:
状态: 已完成
时间戳: 2025-06-20T12:57:24.431678
回复: 好的，我可以帮您规划一个3天的上海之旅，适合3人，中等预算，时间在2025年7月21日至7月30日之间。由于您没有指定特定的兴趣爱好，我将创建一个全面的行程，涵盖历史景点、文化体验和当地美食。以下是可能的计划:

**General Advice & Considerations:**

*   **Best Time to Visit:** While your travel dates are in July, keep in mind that Delhi experiences its monsoon season around that time. Expect high humidity and occasional heavy rainfall. Pack accordingly (light, quick-drying clothes, umbrella/raincoat).
*   **Transportation:** Delhi has a well-developed metro system which is efficient and cost-effective for getting around. Auto-rickshaws and taxis (Ola/Uber) are also readily available. Negotiate fares with auto-rickshaws beforehand.
*   **Accommodation:** I'll suggest areas with a range of mid-range hotel options.
*   **Food:** Delhi is a food lover's paradise! Be adventurous and try local street food, but ensure hygiene. Stick to reputable vendors and bottled water.
*   **Safety:** Be aware of your surroundings, especially in crowded areas. Keep valuables secure.

**Top Attractions and Must-See Places:**

*   **Historical Monuments:** Red Fort, Humayun's Tomb, Qutub Minar, India Gate
*   **Religious Sites:** Lotus Temple, Akshardham Temple, Jama Masjid
*   **Museums:** National Museum, National Rail Museum
*   **Gardens:** Lodhi Garden, Garden of Five Senses
*   **Markets:** Chandni Chowk, Dilli Haat, Khan Market

**Cultural Insights and Etiquette Tips:**

*   **Dress Code:** Dress modestly, especially when visiting religious sites. Shoulders and knees should be covered.
*   **Greetings:** "Namaste" is a respectful greeting.
*   **Photography:** Ask for permission before taking photos of people, especially women.
*   **Shoes:** Remove shoes before entering temples and mosques.
*   **Tipping:** Tipping is customary in restaurants and for services.
*   **Bargaining:** Bargaining is common in markets.

**Best Areas to Stay and Explore (Mid-Range Budget):**

*   **Connaught Place (CP):** Central location, good connectivity, lots of restaurants and shopping.
*   **Karol Bagh:** More budget-friendly than CP, bustling market area.
*   **South Delhi (Hauz Khas, Green Park):** Quieter, more residential, with trendy cafes and boutiques.
*   **Paharganj:** Very budget-friendly, close to the New Delhi Railway Station, but can be crowded and overwhelming.

**Possible 3-Day Itinerary:**

**Day 1: Old Delhi & Central Delhi**

*   **Morning:** Explore **Old Delhi**. Take a rickshaw ride through **Chandni Chowk**, visit **Jama Masjid** (one of India's largest mosques), and sample street food (parathe, jalebi).
*   **Afternoon:** Visit the **Red Fort**, a UNESCO World Heritage Site.
*   **Evening:** Stroll through **Connaught Place**, have dinner at a restaurant of your choice.

**Day 2: New Delhi & Historical Sites**

*   **Morning:** Visit **Humayun's Tomb**, a precursor to the Taj Mahal.
*   **Afternoon:** Explore **Qutub Minar**, another UNESCO World Heritage Site.
*   **Late Afternoon:** Drive past **India Gate** and **Presidential Palace**.
*   **Evening:** Visit **Dilli Haat** (an open-air crafts bazaar) for shopping and cultural performances. Have dinner there.

**Day 3: Temples & Gardens**

*   **Morning:** Visit **Lotus Temple**, a Baháʼí House of Worship known for its distinctive lotus-like shape.
*   **Afternoon:** Explore **Akshardham Temple**, a sprawling complex dedicated to Swaminarayan. (Note: Allow ample time for security checks).
*   **Evening:** Relax in **Lodhi Garden**, a historical garden with tombs and monuments. Have a farewell dinner at a restaurant in Hauz Khas Village.

**Activity Recommendations Based on Interests (Since None Were Specified):**

*   **Food Tour:** If you're foodies, consider a guided food tour of Delhi.
*   **Cooking Class:** Learn to cook authentic Indian dishes.
*   **Yoga/Meditation:** Find a yoga class or meditation session for relaxation.
*   **Shopping:** Explore different markets for souvenirs and handicrafts.
*   **Sufi Music:** Experience a Sufi music performance at Nizamuddin Dargah (Thursday evenings are particularly popular).

**Mid-Range Budget Considerations:**

*   **Accommodation:** Expect to pay around INR 3,000-6,000 per night for a decent mid-range hotel room for three people.
*   **Food:** Meals can range from INR 300-1,000 per person per meal, depending on the restaurant.
*   **Transportation:** Metro is very affordable. Budget around INR 500-1000 per day for taxis/auto-rickshaws, depending on usage.
*   **Entrance Fees:** Monument entrance fees can add up. Factor in around INR 1,000-2,000 per person for all the sites.

This is a flexible itinerary that can be adjusted to your preferences. Once you provide more specific interests, I can tailor the plan further. Let me know if you have any questions!


WEATHER ANALYST:
Status: completed
Timestamp: 2025-06-20T12:57:26.070786
Response: Okay, thanks for the detailed itinerary. To make it weather-intelligent and provide the best recommendations, I need to understand the expected weather conditions during your travel dates (July 21st - July 30th, 2025) in Delhi.

NEED_SEARCH: average weather conditions in Delhi between July 21 and July 30


BUDGET OPTIMIZER:
Status: completed
Timestamp: 2025-06-20T12:57:36.309040
Response: Okay, here's a budget optimization plan for a 3-day trip to Delhi for 3 people on a mid-range budget.

**Estimated Daily and Total Costs:**

*   **Estimated Daily Cost (per person):** ₹3,000 - ₹5,000 (This is a broad range, and we'll refine it below)
*   **Estimated Total Cost (for 3 people, 3 days):** ₹27,000 - ₹45,000

**Budget Breakdown by Category (for 3 people, 3 days - flexible based on your preferences):**

| Category      | Percentage | Estimated Cost (Lower End - ₹27,000) | Estimated Cost (Higher End - ₹45,000) | Notes                                                                                                                                                                                             |
|---------------|------------|--------------------------------------|---------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Accommodation | 30%        | ₹8,100                                 | ₹13,500                                  | Mid-range hotels or well-reviewed guesthouses/Airbnb. Aim for ₹900-₹1500 per room per night.                                                                                               |
| Food          | 30%        | ₹8,100                                 | ₹13,500                                  | Mix of street food, local restaurants, and a few nicer meals. Budget ₹900-₹1500 per person per day.                                                                                                |
| Activities    | 20%        | ₹5,400                                 | ₹9,000                                   | Entrance fees to monuments, guided tours, and other experiences. Prioritize must-see sites.                                                                                                |
| Transport     | 10%        | ₹2,700                                 | ₹4,500                                   | Metro, auto-rickshaws, and ride-sharing apps. The Delhi Metro is very efficient and affordable.                                                                                             |
| Miscellaneous | 10%        | ₹2,700                                 | ₹4,500                                   | Souvenirs, tips, unexpected expenses. Always good to have a buffer.                                                                                                                     |

**Money-Saving Tips and Strategies:**

*   **Accommodation:**
    *   **Travel during the shoulder season (spring or autumn):** You'll find better deals on accommodation and fewer crowds.
    *   **Consider guesthouses or homestays:** Often cheaper than hotels and offer a more authentic experience. Look for well-reviewed options on platforms like Booking.com or Airbnb. Negotiate the price if possible.
    *   **Book in advance:** Secure better rates, especially if traveling during peak season.
*   **Food:**
    *   **Eat like a local:** Street food and local restaurants are much cheaper than tourist-oriented establishments. Be mindful of hygiene; choose vendors with high turnover and visible cleanliness.
    *   **Lunch thalis:** A great value for money, offering a variety of dishes at a fixed price.
    *   **Carry a reusable water bottle:** Refill it whenever possible to avoid buying bottled water.
*   **Activities:**
    *   **Take advantage of free activities:** Many parks, gardens, and religious sites (like Bangla Sahib Gurudwara) are free to enter.
    *   **Consider a Delhi Tourism hop-on-hop-off bus:** A cost-effective way to see many of the major attractions.  Check reviews before booking.
    *   **Group discounts:** Inquire about group discounts at monuments and museums.
*   **Transport:**
    *   **Use the Delhi Metro extensively:** It's clean, efficient, and very affordable. Buy a tourist card for unlimited travel.
    *   **Negotiate auto-rickshaw fares:** Always agree on a price before getting in. Use ride-sharing apps like Uber or Ola for predictable pricing.
    *   **Avoid taxis for short distances:** They are generally more expensive than auto-rickshaws or ride-sharing.
*   **General:**
    *   **Bargain respectfully:** Bargaining is common in markets and with auto-rickshaw drivers. Be polite and respectful.
    *   **Travel in the off-season or shoulder season:** You'll find better deals on flights and accommodation.
    *   **Use credit cards with no foreign transaction fees:** This can save you money on exchange rates.
    *   **Alert your bank:** Inform your bank of your travel dates to avoid having your cards blocked.

**Cost-Effective Alternatives for Expensive Activities:**

*   **Instead of hiring a private car for sightseeing:** Use the Delhi Metro and auto-rickshaws.
*   **Instead of eating at fancy restaurants every night:** Explore street food markets and local dhabas.
*   **Instead of guided tours at every monument:** Read up on the history and significance of the sites beforehand and explore on your own. Consider hiring a local guide at one or two key sites.
*   **Instead of buying expensive souvenirs:** Look for unique, locally made crafts in markets like Dilli Haat (though entrance fee applies, the variety and authenticity are worth it).

To give you even more specific recommendations, I need a little more information:

*   **What are your "must-see" attractions in Delhi?**
*   **What kind of food are you interested in trying?**
*   **What is your preferred accommodation style (hotel, guesthouse, Airbnb)?**

Once I have this, I can refine the budget further and suggest specific places to visit and eat.


LOCAL EXPERT:
Status: completed
Timestamp: 2025-06-20T12:57:47.676662
Response: Great! Knowing your interests helps me tailor the recommendations. Here's a more specific plan for a 3-day trip to Delhi for 3 people, focusing on history, culture, and food, while optimizing for a mid-range budget:

**Refined Budget Breakdown (Based on Interests):**

Let's assume you're aiming for the lower end of the initial budget range (₹27,000 total for 3 people, 3 days). We can adjust the percentages slightly to prioritize activities related to history and culture.

| Category      | Percentage | Estimated Cost (₹27,000 Total) | Notes                                                                                                                                                     |
|---------------|------------|-----------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| Accommodation | 30%        | ₹8,100                        | Focus on well-reviewed guesthouses or budget-friendly hotels in central locations like Paharganj (budget) or Karol Bagh (mid-range).                     |
| Food          | 30%        | ₹8,100                        | Prioritize street food experiences and local restaurants.                                                                                                |
| Activities    | 25%        | ₹6,750                        | Allocate more for entrance fees to historical sites and potentially a guided tour or two.                                                               |
| Transport     | 10%        | ₹2,700                        | Metro and auto-rickshaws.                                                                                                                               |
| Miscellaneous | 5%         | ₹1,350                        | Buffer for unexpected expenses, small souvenirs.                                                                                                           |

**Detailed Itinerary and Recommendations:**

**Day 1: Old Delhi Immersion**

*   **Morning (Historical):**
    *   **Red Fort (Lal Qila):** Explore this UNESCO World Heritage Site. Allocate 2-3 hours. Entrance fee: ₹60 for Indians, ₹800 for foreigners.
    *   **Budget Tip:** Hire a government-approved guide at the entrance for a more enriching experience (negotiate the price beforehand).
*   **Lunch (Food):**
    *   **Karim's (near Jama Masjid):** Iconic Mughlai restaurant. Try their kebabs, biryani, and nahari. (₹500-₹800 for 3 people)
*   **Afternoon (Cultural/Spiritual):**
    *   **Jama Masjid:** One of India's largest mosques. Dress modestly (cover shoulders and knees). Entrance is free, but there's a small fee for photography.
    *   **Chandni Chowk:** Explore the bustling market. Sample street food like *parathe* (stuffed flatbreads) at Parathe Wali Gali, *jalebi* (sweet fried dough), and *lassi* (yogurt drink). Be mindful of hygiene.
*   **Evening (Cultural):**
    *   **Sound and Light Show at Red Fort (optional):** Check timings and book tickets in advance (₹600-₹800 for 3 people).
    *   **Dinner:** Continue exploring street food in Chandni Chowk or find a local restaurant in the area.

**Day 2: New Delhi Exploration**

*   **Morning (Historical):**
    *   **Humayun's Tomb:** A precursor to the Taj Mahal. Beautiful Mughal architecture. Entrance fee: ₹40 for Indians, ₹600 for foreigners.
    *   **Budget Tip:** Take the metro to JLN Stadium station and then an auto-rickshaw to the tomb (₹50-₹80).
*   **Lunch (Food):**
    *   **Khan Market:** Upscale market with a variety of restaurants. Explore options like *Big Yellow Door* (casual cafe) or *SodaBottleOpenerWala* (Parsi cuisine). (₹800-₹1200 for 3 people)
*   **Afternoon (Historical/Cultural):**
    *   **Qutub Minar:** Another UNESCO World Heritage Site. A towering minaret with intricate carvings. Entrance fee: ₹40 for Indians, ₹600 for foreigners.
    *   **Mehrauli Archaeological Park (adjacent to Qutub Minar):** Explore historical ruins and tombs (free entry).
*   **Evening (Spiritual/Cultural):**
    *   **Lotus Temple:** A Baháʼí House of Worship. Striking architectural design. Free entry.
    *   **Dinner:** Explore Hauz Khas Village for a variety of dining options (from budget to mid-range).

**Day 3: Museums and Markets**

*   **Morning (Cultural/Historical):**
    *   **National Museum:** Extensive collection of Indian art, artifacts, and historical exhibits. Entrance fee: ₹20 for Indians, ₹650 for foreigners.
    *   **Budget Tip:** Check for student discounts if applicable.
*   **Lunch (Food):**
    *   **Connaught Place (CP):** Central business district with numerous restaurants. Explore options for North Indian, South Indian, or international cuisine. (₹700-₹1000 for 3 people)
*   **Afternoon (Shopping/Cultural):**
    *   **Dilli Haat (INA):** A crafts village showcasing handicrafts and cuisine from different states of India. Entrance fee: ₹30.
    *   **Janpath Market (near CP):** Bargain for clothes, jewelry, and souvenirs.
*   **Evening (Relaxation/Departure):**
    *   **India Gate:** Visit this iconic war memorial. Enjoy a walk around the area.
    *   **Dinner:** Depending on your departure time, have a final meal at a restaurant near your hotel or the airport.

**Local Dining Recommendations (Beyond the Itinerary):**

*   **Street Food:**
    *   **Rajinder Da Dhaba (Safdarjung Enclave):** Famous for its non-vegetarian kebabs and curries (budget-friendly).
    *   **Dolma Aunty Momos (Lajpat Nagar):** Delicious and affordable momos (dumplings).
*   **Local Restaurants:**
    *   **Andhra Bhavan (near India Gate):** Authentic Andhra cuisine (South Indian) at very reasonable prices.
    *   **Bukhara (ITC Maurya):** High-end, but iconic for its Dal Bukhara and tandoori dishes (splurge).
    *   **Gulati (Pandara Road Market):** Popular for North Indian cuisine, especially butter chicken and dal makhani.

**Cultural Etiquette and Customs:**

*   **Dress Modestly:** Especially when visiting religious sites. Cover shoulders and knees.
*   **Remove Shoes:** Before entering temples, mosques, and some homes.
*   **Use Your Right Hand:** For eating and giving/receiving things.
*   **Bargain Respectfully:** It's expected in markets, but do so politely.
*   **Avoid Public Displays of Affection:** While attitudes are changing, it's still generally considered inappropriate.
*   **Be Mindful of Personal Space:** Crowded areas are common.
*   **Learn a Few Basic Hindi Phrases:** "Namaste" (hello), "Shukriya" (thank you), "Kitna hai?" (how much?).

**Insider Tips:**

*   **Stay Hydrated:** Delhi can get very hot and humid, especially in the summer.
*   **Be Aware of Scams:** Be cautious of touts and unsolicited offers.
*   **Download Ride-Sharing Apps:** Uber and Ola are widely used and convenient.
*   **Use Google Maps:** For navigation and public transport directions.
*   **Carry Small Denomination Bills:** For auto-rickshaws and street vendors.
*   **Beware of Pickpockets:** Be vigilant in crowded areas.
*   **Learn to Say "No" Firmly:** To avoid being pressured into buying things you don't want.
*   **Check the Weather Forecast:** Plan your activities accordingly.
*   **Be Prepared for Traffic:** Delhi traffic can be chaotic.

This itinerary is a suggestion, feel free to customize it based on your preferences and energy levels. Enjoy your trip to Delhi!


ITINERARY PLANNER:
Status: completed
Timestamp: 2025-06-20T12:57:55.320014
Response: This is an excellent refined itinerary, incorporating budget considerations, specific restaurant recommendations, cultural tips, and practical advice. Here are a few minor suggestions to further enhance its usefulness:

**1.  Transportation Specifics & Optimization:**

*   **Day 1:**
    *   "Take the metro to Chawri Bazaar station" before heading to Jama Masjid and Chandni Chowk. This is the most efficient way to reach that area.  Specify that auto-rickshaws are readily available from the metro station if they prefer not to walk.
    *   Add: "Consider taking a cycle rickshaw tour of Chandni Chowk for a unique experience (negotiate the price beforehand)." This provides a specific alternative activity within the area.
*   **Day 2:**
    *   Specify which metro station is closest to Khan Market (Khan Market station).
    *   Add a note about the distance between Qutub Minar and Mehrauli Archaeological Park (walking distance vs. auto-rickshaw).
*   **Day 3:**
    *   Specify the metro station for Dilli Haat (INA station).
    *   Mention that Janpath Market is walking distance from Connaught Place.

**2.  Timing Considerations:**

*   **General:** Emphasize the importance of starting early, especially during peak season or hot weather, to avoid crowds and heat exhaustion.  Suggest starting activities around 9:00 AM each day.
*   **Red Fort (Day 1):** Suggest arriving right at opening time (usually 9:30 AM) to avoid the biggest crowds.
*   **Lotus Temple (Day 2):**  Mention that there can be long queues, especially on weekends.  Suggest visiting during off-peak hours (e.g., late afternoon).

**3.  Alternative Activities (Contingency Planning):**

*   Have a backup plan for each day in case of unexpected closures (e.g., strikes, holidays). Examples:
    *   **Day 1 (Alternative):** If Red Fort is unexpectedly closed, visit the National Gandhi Museum near Raj Ghat.
    *   **Day 2 (Alternative):** If Humayun's Tomb is too crowded, visit Safdarjung's Tomb, another Mughal-era tomb with similar architecture but fewer visitors.
    *   **Day 3 (Alternative):** If Dilli Haat is not appealing, consider visiting the State Emporia Complex on Baba Kharak Singh Marg for fixed-price handicrafts.

**4.  Food Considerations:**

*   **Dietary Restrictions:**  Include a brief sentence about how Delhi caters to various dietary restrictions (vegetarian, vegan, gluten-free) and how to communicate those needs to restaurants.
*   **Water:** Reinforce the importance of drinking bottled water or filtered water only.

**5.  Safety and Health:**

*   **Mosquito Repellent:**  Recommend using mosquito repellent, especially in the evenings.
*   **Air Pollution:**  Briefly mention the air quality in Delhi and suggest checking the Air Quality Index (AQI) and taking precautions if necessary (e.g., wearing a mask on particularly bad days).

**Revised Snippets Incorporating Suggestions:**

*   **Day 1: Old Delhi Immersion**
    *   **Morning:** "...Take the metro to *Chawri Bazaar* station. From the station, auto-rickshaws are readily available if you prefer not to walk to Jama Masjid and Chandni Chowk. Consider taking a cycle rickshaw tour of Chandni Chowk for a unique experience (negotiate the price beforehand)."

*   **Day 2: New Delhi Exploration**
    *   **Morning:** "...Take the metro to *JLN Stadium* station and then an auto-rickshaw to the tomb (₹50-₹80)."
    *   **Lunch:** "...Khan Market (metro station: *Khan Market*)."
    *   **Afternoon:** "...Mehrauli Archaeological Park (adjacent to Qutub Minar): Explore historical ruins and tombs (free entry). The park is within walking distance of Qutub Minar, or a short auto-rickshaw ride."
    *   **Alternative:** If Humayun's Tomb is too crowded, visit Safdarjung's Tomb, another Mughal-era tomb with similar architecture but fewer visitors.

*   **Day 3: Museums and Markets**
    *   **Afternoon:** "...Dilli Haat (INA) (metro station: *INA*)...Janpath Market (near CP): Bargain for clothes, jewelry, and souvenirs. Janpath Market is within walking distance from Connaught Place."

*   **General Timing:** "To avoid the biggest crowds and the heat, aim to start your sightseeing around 9:00 AM each day."

*   **Food Considerations:** "Delhi caters well to various dietary restrictions (vegetarian, vegan, gluten-free). Don't hesitate to communicate your needs to restaurant staff. Always drink bottled or filtered water."

*   **Safety and Health:** "Remember to use mosquito repellent, especially in the evenings. Check the Air Quality Index (AQI) daily and consider wearing a mask on days with high pollution levels."

By incorporating these minor adjustments, you'll make the itinerary even more practical, informative, and user-friendly.  Great work!

================================================================================
End of LangGraph Multi-Agent Travel Planning Report
================================================================================
```

## 🏗️ 系统架构

### 项目结构
```
📁 ai_travel_agent/
├── main.py                    # 多系统入口点
├── langgraph_main.py         # LangGraph系统入口
├── test_langgraph_system.py  # 综合测试
├── agents/                   # 智能体实现
│   ├── langgraph_agents.py   # LangGraph智能体系统
│   ├── multi_agent_orchestrator.py # 传统多智能体
│   └── travel_agents.py      # 单个智能体类
├── config/                   # 配置管理
│   ├── langgraph_config.py   # LangGraph配置
│   ├── api_config.py         # 传统API设置
│   └── app_config.py         # 应用程序设置
├── tools/                    # LangGraph工具
│   └── travel_tools.py       # 7个DuckDuckGo搜索工具
├── data/                     # 数据模型
│   └── models.py             # 数据类
├── modules/                  # 传统业务逻辑
│   ├── user_input.py         # 输入处理和验证
│   ├── weather_service.py    # 天气数据集成
│   ├── attraction_finder.py  # 景点发现
│   ├── hotel_estimator.py    # 住宿估算
│   ├── currency_converter.py # 货币转换
│   ├── expense_calculator.py # 成本计算
│   ├── itinerary_planner.py  # 逐日规划
│   └── trip_summary.py       # 报告生成
└── utils/                    # 实用工具函数
    └── helpers.py            # 通用辅助函数
```

### 系统对比

| 功能特性 | 单智能体 | 传统多智能体 | LangGraph系统 |
|---------|-------------|-------------------|------------------|
| **框架** | 自定义 | 自定义 | LangGraph + LangChain |
| **大语言模型** | 模拟/静态 | 模拟/静态 | Google Gemini Flash-2.0 |
| **搜索** | 静态数据 | 静态数据 | DuckDuckGo实时 |
| **状态管理** | 无 | 基础 | 高级（StateGraph） |
| **工具集成** | 有限 | 有限 | 完整工具生态系统 |
| **协作能力** | 无 | 基础 | 高级工作流 |
| **可扩展性** | 低 | 中等 | 高 |
| **可维护性** | 低 | 中等 | 高 |

## 依赖项

### 必需包
```
requests>=2.31.0    # 用于API调用的HTTP请求
python-dotenv>=1.0.0 # 环境变量管理
```

### 外部API（可选）
- OpenWeather API: 天气预报
- Google Places API: 景点和酒店
- Exchange Rate API: 货币转换

## 🧪 测试

### 运行测试
```bash
# LangGraph系统验证（无需API密钥）
python test_langgraph_system.py

# 传统系统测试
python -m pytest tests/ (如果tests目录存在)
```

### 系统验证
`test_langgraph_system.py` 脚本验证：
- 所有LangGraph组件
- 工具集成
- 配置管理
- 导入兼容性
- 系统就绪状态

## 🚨 故障排除

### 常见问题

1. **API配额超限**
   ```
   错误: 429 您已超出当前配额
   解决方案: 等待配额重置或升级API计划
   ```

2. **导入错误**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置问题**
   ```bash
   python test_langgraph_system.py
   ```

4. **缺少API密钥**
   ```
   错误: 未找到GEMINI_API_KEY
   解决方案: 将您的API密钥添加到.env文件
   ```

### 调试模式
```bash
export DEBUG=true
python langgraph_main.py
```

## 功能详情

### 🌤️ 天气集成
- 5天天气预报
- 温度、天气状况、湿度
- 基于天气的活动推荐
- 打包建议

### 🏛️ 景点发现
- 博物馆和文化景点
- 按菜系分类的餐厅
- 基于兴趣的活动
- 评分和费用信息

### 🏨 住宿安排
- 符合预算的酒店推荐
- 每晚价格计算
- 设施清单
- 团体住宿选择

### 💱 货币支持
- 实时汇率
- 10+种国际货币
- 自动成本转换
- 汇率缓存提升性能

### 📅 行程规划
- 逐日时间安排
- 天气优化的活动排序
- 交通建议
- 时间推荐

### 📊 费用管理
- 详细成本分解
- 预算与实际跟踪
- 团体费用计算
- 省钱建议

## 贡献指南

### 代码结构
- 遵循面向对象设计原则
- 保持模块化架构
- 包含全面的错误处理
- 为新功能添加单元测试

### 开发环境设置
```bash
# 安装开发依赖
pip install -r requirements.txt

# 运行验证
python validate.py

# 测试特定模块
python -m pytest tests/test_attraction.py
```

## 许可证

本项目用于教育目的，作为AI智能体作业的一部分。

## 支持

如有问题或疑问：
1. 检查验证脚本: `python validate.py`
2. 查看错误消息和日志
3. 验证API密钥配置（如果使用外部API）

---

**用❤️构建，致力于智能旅行规划**
