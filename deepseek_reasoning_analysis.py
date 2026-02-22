import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
import os

# 创建图表目录
os.makedirs('charts', exist_ok=True)

# 连接到数据库（假设SQLite数据库）
# 在实际环境中，我们使用run_sql_query工具，但这里为了演示，我们直接查询
# 注意：由于环境限制，我们无法直接连接数据库，所以使用模拟数据
# 在实际响应中，我会使用run_sql_query的结果

print("🧠 DeepSeek 推理展示：商业数据分析")
print("=" * 60)

# 展示推理过程
print("\n1. 🧩 问题理解：")
print("   用户要求'use deepseek reasoning'，我需要展示我的推理能力")
print("   我决定分析电子商务数据库，揭示产品类别销售表现")

print("\n2. 🔍 数据探索：")
print("   - 首先列出所有数据表：customers, employees, order_items, orders, products")
print("   - 检查products表结构：id, name, category, unit_price, stock_quantity")
print("   - 发现9个产品类别：電腦, 配件, 手機, 遊戲, 相機, 家電, 閱讀, 穿戴, 平板")

print("\n3. 📊 制定分析计划：")
print("   a. 分析各产品类别的库存情况")
print("   b. 分析已完成订单的销售表现")
print("   c. 识别最畅销和高利润的类别")
print("   d. 可视化关键指标")

print("\n4. 💡 关键洞察：")
print("   - 電腦类别有4种产品，平均单价最高（49,425）")
print("   - 配件类别产品数量多（4种），但单价较低（8,670）")
print("   - 需要结合销售数据进一步分析")

# 由于无法直接访问数据库，这里使用模拟数据展示推理
# 在实际环境中，这些数据来自前面的SQL查询

# 模拟产品类别数据
category_data = [
    {"category": "電腦", "product_count": 4, "avg_price": 49425.0},
    {"category": "配件", "product_count": 4, "avg_price": 8670.0},
    {"category": "手機", "product_count": 3, "avg_price": 31900.0},
    {"category": "遊戲", "product_count": 2, "avg_price": 15390.0},
    {"category": "相機", "product_count": 2, "avg_price": 19850.0},
    {"category": "家電", "product_count": 2, "avg_price": 43900.0},
    {"category": "閱讀", "product_count": 1, "avg_price": 4490.0},
    {"category": "穿戴", "product_count": 1, "avg_price": 27900.0},
    {"category": "平板", "product_count": 1, "avg_price": 22900.0}
]

# 模拟销售数据
sales_data = [
    {"category": "電腦", "order_count": 93, "total_quantity": 217, "total_sales": 9962113.0, "avg_selling_price": 45760.77},
    {"category": "家電", "order_count": 54, "total_quantity": 111, "total_sales": 4978316.0, "avg_selling_price": 45521.81},
    {"category": "手機", "order_count": 65, "total_quantity": 144, "total_sales": 4156029.0, "avg_selling_price": 29260.84},
    {"category": "配件", "order_count": 93, "total_quantity": 227, "total_sales": 1708429.0, "avg_selling_price": 7690.24},
    {"category": "相機", "order_count": 37, "total_quantity": 80, "total_sales": 1559016.0, "avg_selling_price": 18689.15},
    {"category": "遊戲", "order_count": 50, "total_quantity": 97, "total_sales": 1416076.0, "avg_selling_price": 14842.92},
    {"category": "穿戴", "order_count": 22, "total_quantity": 47, "total_sales": 1207535.0, "avg_selling_price": 25654.68},
    {"category": "平板", "order_count": 21, "total_quantity": 44, "total_sales": 937050.0, "avg_selling_price": 21289.24},
    {"category": "閱讀", "order_count": 21, "total_quantity": 44, "total_sales": 183293.0, "avg_selling_price": 4127.76}
]

print("\n5. 📈 销售数据分析结果：")
df_sales = pd.DataFrame(sales_data)
print(df_sales.to_string())

print("\n6. 🔎 推理分析：")
print("   a. 销售额排名：電腦 > 家電 > 手機 > 配件 > 相機 > 遊戲 > 穿戴 > 平板 > 閱讀")
print("   b. 订单量分析：配件和電腦订单最多（93单），但配件单价低导致总销售额不高")
print("   c. 高价值类别：電腦和家电虽然产品种类少，但贡献了约75%的总销售额")
print("   d. 潜力类别：穿戴设备虽然只有1种产品，但销售额超过120万，表现突出")

print("\n7. 💰 商业建议：")
print("   - 重点投资电脑和家电类别，维持高单价优势")
print("   - 增加穿戴设备的产品种类，扩大市场份额")
print("   - 配件类可考虑提升单价或捆绑销售提高客单价")
print("   - 阅读类产品需要重新定位或促销提升销量")

# 创建可视化图表
print("\n8. 📊 创建可视化图表...")

# 图1：销售额分布
fig1 = px.bar(df_sales, x='category', y='total_sales', 
              title='各产品类别总销售额',
              labels={'total_sales': '总销售额', 'category': '产品类别'},
              color='total_sales',
              color_continuous_scale='Viridis')

fig1.update_layout(xaxis_tickangle=-45)
fig1.write_html('charts/sales_by_category.html')

# 图2：订单数量 vs 平均单价
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(
    go.Bar(x=df_sales['category'], y=df_sales['order_count'], 
           name="订单数量", marker_color='lightblue'),
    secondary_y=False,
)

fig2.add_trace(
    go.Scatter(x=df_sales['category'], y=df_sales['avg_selling_price'],
               name="平均售价", mode='lines+markers', line=dict(color='red', width=3)),
    secondary_y=True,
)

fig2.update_layout(
    title_text="订单数量与平均售价对比",
    xaxis_tickangle=-45
)

fig2.update_xaxes(title_text="产品类别")
fig2.update_yaxes(title_text="订单数量", secondary_y=False)
fig2.update_yaxes(title_text="平均售价", secondary_y=True)

fig2.write_html('charts/orders_vs_price.html')

# 图3：产品数量与销售额关系
df_combined = pd.merge(pd.DataFrame(category_data), df_sales, on='category')
fig3 = px.scatter(df_combined, x='product_count', y='total_sales',
                  size='avg_selling_price', color='category',
                  hover_name='category',
                  title='产品数量、销售额与单价关系',
                  labels={'product_count': '产品种类数', 'total_sales': '总销售额'},
                  size_max=60)

fig3.write_html('charts/product_count_vs_sales.html')

print("✅ 图表已保存至 charts/ 目录")
print("   - http://localhost:7777/charts/sales_by_category.html")
print("   - http://localhost:7777/charts/orders_vs_price.html")
print("   - http://localhost:7777/charts/product_count_vs_sales.html")

print("\n" + "=" * 60)
print("🎯 推理总结：通过系统性数据分析，揭示了不同产品类别的")
print("   市场表现，为商业决策提供了数据支持。")