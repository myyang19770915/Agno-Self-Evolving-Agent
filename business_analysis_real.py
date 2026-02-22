import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import os
from datetime import datetime

# 創建圖表目錄
os.makedirs('charts', exist_ok=True)

print("開始商業資料庫分析 (使用真實資料)...")

# ============================================================================
# 1. 產品分析 - 使用真實數據
# ============================================================================
print("\n1. 正在分析產品資料...")

product_data = [
    {"category": "電腦", "product_count": 4, "avg_price": 49425.0, "total_stock": 787, "min_price": 39900.0, "max_price": 59900.0},
    {"category": "配件", "product_count": 4, "avg_price": 8670.0, "total_stock": 1162, "min_price": 3490.0, "max_price": 12800.0},
    {"category": "手機", "product_count": 3, "avg_price": 31900.0, "total_stock": 245, "min_price": 26900.0, "max_price": 36900.0},
    {"category": "遊戲", "product_count": 2, "avg_price": 15390.0, "total_stock": 449, "min_price": 12800.0, "max_price": 17980.0},
    {"category": "相機", "product_count": 2, "avg_price": 19850.0, "total_stock": 82, "min_price": 13800.0, "max_price": 25900.0},
    {"category": "家電", "product_count": 2, "avg_price": 43900.0, "total_stock": 745, "min_price": 24900.0, "max_price": 62900.0},
    {"category": "閱讀", "product_count": 1, "avg_price": 4490.0, "total_stock": 312, "min_price": 4490.0, "max_price": 4490.0},
    {"category": "穿戴", "product_count": 1, "avg_price": 27900.0, "total_stock": 150, "min_price": 27900.0, "max_price": 27900.0},
    {"category": "平板", "product_count": 1, "avg_price": 22900.0, "total_stock": 22, "min_price": 22900.0, "max_price": 22900.0}
]

df_products = pd.DataFrame(product_data)

# 產品分析圖表 - 產品數量與平均價格
fig1 = make_subplots(
    rows=1, cols=2,
    subplot_titles=('各類別產品數量', '各類別平均價格'),
    specs=[[{'type': 'bar'}, {'type': 'bar'}]]
)

fig1.add_trace(
    go.Bar(x=df_products['category'], y=df_products['product_count'],
           name='產品數量', marker_color='skyblue'),
    row=1, col=1
)

fig1.add_trace(
    go.Bar(x=df_products['category'], y=df_products['avg_price'],
           name='平均價格', marker_color='salmon'),
    row=1, col=2
)

fig1.update_layout(
    title_text="產品類別分析",
    showlegend=False,
    height=500
)

fig1.write_html('charts/product_category_analysis_real.html')
print("  產品分析圖表已保存: charts/product_category_analysis_real.html")

# 庫存分析圖表
fig2 = go.Figure(data=[
    go.Bar(name='庫存總量', x=df_products['category'], y=df_products['total_stock'], marker_color='lightgreen'),
    go.Bar(name='產品數量', x=df_products['category'], y=df_products['product_count']*50, marker_color='orange')
])

fig2.update_layout(
    title='產品庫存分析',
    xaxis_title='產品類別',
    yaxis_title='數量',
    barmode='group',
    height=500
)

fig2.write_html('charts/product_inventory_analysis_real.html')
print("  庫存分析圖表已保存: charts/product_inventory_analysis_real.html")

# ============================================================================
# 2. 銷售分析 - 使用真實數據
# ============================================================================
print("\n2. 正在分析銷售資料...")

# 真實的銷售數據
sales_data = [
    {"month": "2024-01", "order_count": 5, "customer_count": 5, "total_sales": 604586.0, "avg_order_value": 120917.2},
    {"month": "2024-02", "order_count": 6, "customer_count": 6, "total_sales": 656767.0, "avg_order_value": 109461.16666666667},
    {"month": "2024-03", "order_count": 9, "customer_count": 8, "total_sales": 1009724.0, "avg_order_value": 112191.55555555556},
    {"month": "2024-04", "order_count": 7, "customer_count": 7, "total_sales": 900727.0, "avg_order_value": 128675.28571428571},
    {"month": "2024-05", "order_count": 9, "customer_count": 7, "total_sales": 1470517.0, "avg_order_value": 163390.77777777778},
    {"month": "2024-06", "order_count": 8, "customer_count": 7, "total_sales": 1048949.0, "avg_order_value": 131118.625},
    {"month": "2024-07", "order_count": 5, "customer_count": 4, "total_sales": 870084.0, "avg_order_value": 174016.8},
    {"month": "2024-08", "order_count": 10, "customer_count": 10, "total_sales": 1073268.0, "avg_order_value": 107326.8},
    {"month": "2024-09", "order_count": 9, "customer_count": 9, "total_sales": 693661.0, "avg_order_value": 77073.44444444444},
    {"month": "2024-10", "order_count": 10, "customer_count": 10, "total_sales": 1849539.0, "avg_order_value": 184953.9},
    {"month": "2024-11", "order_count": 12, "customer_count": 8, "total_sales": 953410.0, "avg_order_value": 79450.83333333333},
    {"month": "2024-12", "order_count": 7, "customer_count": 7, "total_sales": 1029130.0, "avg_order_value": 147018.57142857142},
    {"month": "2025-01", "order_count": 11, "customer_count": 11, "total_sales": 1437021.0, "avg_order_value": 130638.27272727272},
    {"month": "2025-02", "order_count": 10, "customer_count": 10, "total_sales": 1615222.0, "avg_order_value": 161522.2},
    {"month": "2025-03", "order_count": 5, "customer_count": 5, "total_sales": 652766.0, "avg_order_value": 130553.2},
    {"month": "2025-04", "order_count": 11, "customer_count": 10, "total_sales": 1048316.0, "avg_order_value": 95301.45454545454},
    {"month": "2025-05", "order_count": 6, "customer_count": 6, "total_sales": 740974.0, "avg_order_value": 123495.66666666667},
    {"month": "2025-06", "order_count": 6, "customer_count": 5, "total_sales": 989738.0, "avg_order_value": 164956.33333333334},
    {"month": "2025-07", "order_count": 8, "customer_count": 8, "total_sales": 1009172.0, "avg_order_value": 126146.5},
    {"month": "2025-08", "order_count": 10, "customer_count": 9, "total_sales": 1680531.0, "avg_order_value": 168053.1},
    {"month": "2025-09", "order_count": 8, "customer_count": 7, "total_sales": 999585.0, "avg_order_value": 124948.125},
    {"month": "2025-10", "order_count": 9, "customer_count": 9, "total_sales": 977745.0, "avg_order_value": 108638.33333333333},
    {"month": "2025-11", "order_count": 12, "customer_count": 11, "total_sales": 1788576.0, "avg_order_value": 149048.0},
    {"month": "2025-12", "order_count": 9, "customer_count": 9, "total_sales": 1007849.0, "avg_order_value": 111983.22222222222}
]

df_sales = pd.DataFrame(sales_data)

# 銷售趨勢圖表
fig3 = make_subplots(
    rows=2, cols=1,
    subplot_titles=('月度銷售額趨勢', '月度訂單數量與客戶數'),
    vertical_spacing=0.15
)

fig3.add_trace(
    go.Scatter(x=df_sales['month'], y=df_sales['total_sales'],
               mode='lines+markers', name='銷售額', line=dict(color='royalblue', width=3)),
    row=1, col=1
)

fig3.add_trace(
    go.Bar(x=df_sales['month'], y=df_sales['order_count'],
           name='訂單數', marker_color='lightcoral'),
    row=2, col=1
)

fig3.add_trace(
    go.Scatter(x=df_sales['month'], y=df_sales['customer_count'],
               mode='lines+markers', name='客戶數', line=dict(color='green', width=2)),
    row=2, col=1
)

fig3.update_layout(
    title_text="銷售趨勢分析",
    height=700,
    showlegend=True
)

fig3.update_yaxes(title_text="銷售額 (元)", row=1, col=1)
fig3.update_yaxes(title_text="數量", row=2, col=1)

fig3.write_html('charts/sales_trend_analysis_real.html')
print("  銷售趨勢圖表已保存: charts/sales_trend_analysis_real.html")

# 月度平均訂單價值趨勢
fig3b = go.Figure()
fig3b.add_trace(go.Scatter(
    x=df_sales['month'], 
    y=df_sales['avg_order_value'],
    mode='lines+markers',
    name='平均訂單價值',
    line=dict(color='purple', width=3)
))
fig3b.update_layout(
    title='月度平均訂單價值趨勢',
    xaxis_title='月份',
    yaxis_title='平均訂單價值 (元)',
    height=500
)
fig3b.write_html('charts/avg_order_value_trend_real.html')
print("  平均訂單價值圖表已保存: charts/avg_order_value_trend_real.html")

# ============================================================================
# 3. 客戶分析 - 使用真實數據
# ============================================================================
print("\n3. 正在分析客戶資料...")

# 真實的客戶會員等級數據
customer_data = [
    {"membership_level": "Gold", "customer_count": 14, "order_count": 56, "total_spent": 8396131.0, "avg_order_value": 149930.9107142857},
    {"membership_level": "Bronze", "customer_count": 17, "order_count": 68, "total_spent": 6882518.0, "avg_order_value": 101213.5},
    {"membership_level": "Silver", "customer_count": 13, "order_count": 50, "total_spent": 6355406.0, "avg_order_value": 127108.12},
    {"membership_level": "Platinum", "customer_count": 6, "order_count": 28, "total_spent": 4473802.0, "avg_order_value": 159778.64285714287}
]

df_customers = pd.DataFrame(customer_data)

# 真實的城市客戶分佈數據
city_data = [
    {"city": "新竹", "customer_count": 10, "platinum_count": 3, "gold_count": 1, "silver_count": 1, "bronze_count": 5},
    {"city": "台中", "customer_count": 8, "platinum_count": 0, "gold_count": 3, "silver_count": 2, "bronze_count": 3},
    {"city": "新北", "customer_count": 7, "platinum_count": 2, "gold_count": 2, "silver_count": 1, "bronze_count": 2},
    {"city": "高雄", "customer_count": 6, "platinum_count": 0, "gold_count": 2, "silver_count": 1, "bronze_count": 3},
    {"city": "嘉義", "customer_count": 6, "platinum_count": 1, "gold_count": 1, "silver_count": 2, "bronze_count": 2},
    {"city": "台北", "customer_count": 5, "platinum_count": 0, "gold_count": 1, "silver_count": 3, "bronze_count": 1},
    {"city": "桃園", "customer_count": 4, "platinum_count": 0, "gold_count": 1, "silver_count": 2, "bronze_count": 1},
    {"city": "台南", "customer_count": 4, "platinum_count": 0, "gold_count": 3, "silver_count": 1, "bronze_count": 0}
]

df_cities = pd.DataFrame(city_data)

# 會員等級貢獻分析圖表
fig4 = make_subplots(
    rows=1, cols=2,
    subplot_titles=('會員等級客戶分佈', '會員等級銷售貢獻'),
    specs=[[{'type': 'pie'}, {'type': 'bar'}]]
)

fig4.add_trace(
    go.Pie(labels=df_customers['membership_level'], values=df_customers['customer_count'],
           name='客戶數', hole=0.3, marker_colors=['#FFD700', '#C0C0C0', '#CD7F32', '#8B4513']),
    row=1, col=1
)

fig4.add_trace(
    go.Bar(x=df_customers['membership_level'], y=df_customers['total_spent'],
           name='總消費額', marker_color='mediumseagreen'),
    row=1, col=2
)

fig4.update_layout(
    title_text="客戶會員等級分析",
    height=500
)

fig4.write_html('charts/customer_membership_analysis_real.html')
print("  客戶會員等級圖表已保存: charts/customer_membership_analysis_real.html")

# 城市客戶分佈圖表
fig5 = go.Figure()

fig5.add_trace(go.Bar(
    x=df_cities['city'],
    y=df_cities['customer_count'],
    name='總客戶數',
    marker_color='steelblue'
))

fig5.add_trace(go.Bar(
    x=df_cities['city'],
    y=df_cities['platinum_count'],
    name='Platinum會員',
    marker_color='gold'
))

fig5.add_trace(go.Bar(
    x=df_cities['city'],
    y=df_cities['gold_count'],
    name='Gold會員',
    marker_color='silver'
))

fig5.update_layout(
    title='各城市客戶分佈',
    xaxis_title='城市',
    yaxis_title='客戶數量',
    barmode='group',
    height=500
)

fig5.write_html('charts/city_customer_distribution_real.html')
print("  城市客戶分佈圖表已保存: charts/city_customer_distribution_real.html")

# ============================================================================
# 4. 員工分析 - 使用真實數據
# ============================================================================
print("\n4. 正在分析員工資料...")

# 真實的員工部門數據
employee_data = [
    {"department": "人資部", "employee_count": 2, "avg_salary": 105566.5, "min_salary": 98273.0, "max_salary": 112860.0, "total_salary": 211133.0},
    {"department": "財務部", "employee_count": 3, "avg_salary": 62533.0, "min_salary": 39062.0, "max_salary": 91911.0, "total_salary": 187599.0},
    {"department": "業務部", "employee_count": 3, "avg_salary": 57053.666666666664, "min_salary": 37631.0, "max_salary": 94151.0, "total_salary": 171161.0},
    {"department": "工程部", "employee_count": 4, "avg_salary": 56834.25, "min_salary": 44725.0, "max_salary": 69226.0, "total_salary": 227337.0},
    {"department": "行銷部", "employee_count": 2, "avg_salary": 46016.5, "min_salary": 44830.0, "max_salary": 47203.0, "total_salary": 92033.0}
]

df_employees = pd.DataFrame(employee_data)

# 員工部門薪資分析圖表
fig6 = make_subplots(
    rows=1, cols=2,
    subplot_titles=('各部門平均薪資', '各部門員工數量與薪資總額'),
    specs=[[{'type': 'bar'}, {'type': 'bar'}]]
)

fig6.add_trace(
    go.Bar(x=df_employees['department'], y=df_employees['avg_salary'],
           name='平均薪資', marker_color='coral'),
    row=1, col=1
)

fig6.add_trace(
    go.Bar(x=df_employees['department'], y=df_employees['employee_count'],
           name='員工數量', marker_color='lightblue'),
    row=1, col=2
)

fig6.add_trace(
    go.Scatter(x=df_employees['department'], y=df_employees['total_salary']/1000,
               mode='lines+markers', name='薪資總額(千元)', line=dict(color='green', width=2)),
    row=1, col=2
)

fig6.update_layout(
    title_text="員工部門分析",
    height=500,
    showlegend=True
)

fig6.write_html('charts/employee_department_analysis_real.html')
print("  員工部門分析圖表已保存: charts/employee_department_analysis_real.html")

# ============================================================================
# 5. 產品銷售排名 - 使用真實數據
# ============================================================================
print("\n5. 正在分析產品銷售排名...")

# 真實的產品銷售排名數據
product_sales_data = [
    {"name": "LG OLED 65吋電視", "category": "家電", "total_quantity": 70, "total_revenue": 4031115.0, "order_count": 35},
    {"name": "MacBook Pro 14吋", "category": "電腦", "total_quantity": 62, "total_revenue": 3410977.0, "order_count": 32},
    {"name": "Dell XPS 15", "category": "電腦", "total_quantity": 51, "total_revenue": 2421733.0, "order_count": 25},
    {"name": "ASUS ROG 電競筆電", "category": "電腦", "total_quantity": 49, "total_revenue": 2102618.0, "order_count": 25},
    {"name": "Samsung 49吋曲面螢幕", "category": "電腦", "total_quantity": 55, "total_revenue": 2026785.0, "order_count": 29},
    {"name": "Google Pixel 9", "category": "手機", "total_quantity": 70, "total_revenue": 1773631.0, "order_count": 33},
    {"name": "iPhone 16 Pro", "category": "手機", "total_quantity": 39, "total_revenue": 1341960.0, "order_count": 23},
    {"name": "Apple Watch Ultra", "category": "穿戴", "total_quantity": 47, "total_revenue": 1207535.0, "order_count": 22},
    {"name": "DJI Mini 4 Pro", "category": "相機", "total_quantity": 49, "total_revenue": 1166426.0, "order_count": 21},
    {"name": "Samsung Galaxy S25", "category": "手機", "total_quantity": 35, "total_revenue": 1040438.0, "order_count": 18}
]

df_product_sales = pd.DataFrame(product_sales_data)

# 產品銷售排名圖表
fig7 = make_subplots(
    rows=1, cols=2,
    subplot_titles=('產品銷售額排名', '產品銷售量排名'),
    specs=[[{'type': 'bar'}, {'type': 'bar'}]]
)

# 按銷售額排序
df_sorted_by_revenue = df_product_sales.sort_values('total_revenue', ascending=True)
fig7.add_trace(
    go.Bar(y=df_sorted_by_revenue['name'], x=df_sorted_by_revenue['total_revenue'],
           name='銷售額', orientation='h', marker_color='royalblue'),
    row=1, col=1
)

# 按銷售量排序
df_sorted_by_quantity = df_product_sales.sort_values('total_quantity', ascending=True)
fig7.add_trace(
    go.Bar(y=df_sorted_by_quantity['name'], x=df_sorted_by_quantity['total_quantity'],
           name='銷售量', orientation='h', marker_color='lightcoral'),
    row=1, col=2
)

fig7.update_layout(
    title_text="熱銷產品排名分析",
    height=600,
    showlegend=False
)

fig7.update_xaxes(title_text="銷售額 (元)", row=1, col=1)
fig7.update_xaxes(title_text="銷售數量", row=1, col=2)

fig7.write_html('charts/top_products_analysis_real.html')
print("  產品銷售排名圖表已保存: charts/top_products_analysis_real.html")

# ============================================================================
# 6. 生成分析報告
# ============================================================================
print("\n6. 生成分析報告...")

# 計算關鍵指標
total_products = df_products['product_count'].sum()
total_stock = df_products['total_stock'].sum()
avg_product_price = (df_products['avg_price'] * df_products['product_count']).sum() / total_products

total_customers = df_customers['customer_count'].sum()
total_sales_all = df_sales['total_sales'].sum()
total_sales_latest = df_sales['total_sales'].iloc[-1]
sales_growth = ((df_sales['total_sales'].iloc[-1] - df_sales['total_sales'].iloc[0]) / df_sales['total_sales'].iloc[0]) * 100

total_employees = df_employees['employee_count'].sum()
total_salary = df_employees['total_salary'].sum()

# 客戶平均消費
avg_customer_spent = df_customers['total_spent'].sum() / total_customers

# 產品銷售集中度
top3_product_revenue = df_product_sales['total_revenue'].head(3).sum()
product_concentration = (top3_product_revenue / df_product_sales['total_revenue'].sum()) * 100

# 生成報告
report = f"""
# 商業資料庫分析報告 (使用真實資料)
生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 關鍵指標摘要

### 產品相關指標
- 產品總數: {total_products} 個
- 庫存總量: {total_stock} 件
- 平均產品價格: NT${avg_product_price:,.0f}
- 產品類別數: {len(df_products)} 個

### 銷售相關指標
- 總客戶數: {total_customers} 人
- 總銷售額: NT${total_sales_all:,.0f}
- 最新月度銷售額: NT${total_sales_latest:,.0f}
- 銷售成長率: {sales_growth:.1f}% (從分析期初至今)
- 平均訂單價值: NT${df_sales['avg_order_value'].mean():,.0f}
- 總訂單數: {df_sales['order_count'].sum()} 筆

### 客戶相關指標
- 客戶平均消費: NT${avg_customer_spent:,.0f}
- 最密集客戶城市: {df_cities.iloc[0]['city']} ({df_cities.iloc[0]['customer_count']}人)
- 最高價值會員等級: {df_customers.iloc[0]['membership_level']}

### 人力資源指標
- 員工總數: {total_employees} 人
- 月度薪資總額: NT${total_salary:,.0f}
- 平均薪資: NT${total_salary/total_employees:,.0f}

### 產品銷售指標
- 熱銷產品數: {len(df_product_sales)} 個
- 前3大產品銷售集中度: {product_concentration:.1f}%
- 最佳銷售產品: {df_product_sales.iloc[0]['name']} (NT${df_product_sales.iloc[0]['total_revenue']:,.0f})

## 📈 圖表分析

已生成以下互動式圖表:
1. 產品類別分析 - http://localhost:7777/charts/product_category_analysis_real.html
2. 產品庫存分析 - http://localhost:7777/charts/product_inventory_analysis_real.html
3. 銷售趨勢分析 - http://localhost:7777/charts/sales_trend_analysis_real.html
4. 平均訂單價值趨勢 - http://localhost:7777/charts/avg_order_value_trend_real.html
5. 客戶會員等級分析 - http://localhost:7777/charts/customer_membership_analysis_real.html
6. 城市客戶分佈 - http://localhost:7777/charts/city_customer_distribution_real.html
7. 員工部門分析 - http://localhost:7777/charts/employee_department_analysis_real.html
8. 熱銷產品排名 - http://localhost:7777/charts/top_products_analysis_real.html

## 💡 專業建議

### 產品管理建議
1. **庫存優化**: 
   - 平板類產品庫存僅22件，建議增加庫存或促銷
   - 配件類產品庫存充足(1,162件)，可考慮捆綁銷售

2. **定價策略**:
   - 電腦類產品平均價格最高(NT$49,425)，可考慮推出中階產品線
   - 閱讀類產品價格最低(NT$4,490)，可作為引流產品

### 銷售與客戶建議
1. **會員經營**:
   - Gold會員(14人)貢獻最多銷售額(NT$8,396,131)，應加強高價值客戶維護
   - Platinum會員僅6人但平均訂單價值最高(NT$159,779)，應增加Platinum會員數量

2. **區域拓展**:
   - 新竹市客戶最多(10人)，但Gold會員僅1人，有升級潛力
   - 台中市有8名客戶但無Platinum會員，可針對高端客戶進行行銷

3. **銷售策略**:
   - 平均訂單價值波動大(NT$77,073-NT$184,954)，應穩定訂單價值
   - 2024年10月銷售額最高(NT$1,849,539)，可分析成功因素複製

### 人力資源建議
1. **薪資結構**:
   - 人資部平均薪資最高(NT$105,567)，反映對人才管理的重視
   - 行銷部平均薪資最低(NT$46,017)，可考慮績效獎金激勵

2. **部門配置**:
   - 工程部員工最多(4人)，反映對技術開發的重視
   - 行銷部僅2人，可考慮擴充以支持業務成長

### 產品銷售建議
1. **熱銷產品聚焦**:
   - LG OLED 65吋電視銷售額最高(NT$4,031,115)，可加大推廣力度
   - 前3大產品佔總銷售額{product_concentration:.1f}%，應分散風險開發新熱銷品

2. **類別平衡**:
   - 電腦類產品有4項進入熱銷榜，顯示強勢地位
   - 手機類有3項產品熱銷，應維持此類別競爭力

## 🚀 行動方案

### 短期行動 (1-3個月)
1. 增加平板產品庫存至合理水平(建議50-100件)
2. 設計Bronze會員升級Gold會員的獎勵計畫
3. 在台中市開展高端客戶行銷活動
4. 優化行銷部門績效考核制度

### 中期行動 (3-6個月)
1. 開發中階電腦產品線(價格帶NT$25,000-35,000)
2. 建立客戶分層經營體系，提升Platinum會員比例至10%
3. 擴充行銷團隊至4-5人
4. 分析2024年10月成功因素，複製銷售高峰策略

### 長期策略 (6-12個月)
1. 建立數據驅動的庫存管理系統
2. 發展全渠道銷售策略，降低對單一產品的依賴
3. 實施智能定價系統，穩定平均訂單價值
4. 建立客戶忠誠度生態系統，提升客戶終身價值
"""

# 保存報告
with open('business_analysis_report_real.md', 'w', encoding='utf-8') as f:
    f.write(report)

print("  分析報告已保存: business_analysis_report_real.md")

# 保存關鍵數據為CSV文件
df_products.to_csv('products_analysis_real.csv', index=False, encoding='utf-8-sig')
df_sales.to_csv('sales_analysis_real.csv', index=False, encoding='utf-8-sig')
df_customers.to_csv('customer_analysis_real.csv', index=False, encoding='utf-8-sig')
df_cities.to_csv('city_analysis_real.csv', index=False, encoding='utf-8-sig')
df_employees.to_csv('employee_analysis_real.csv', index=False, encoding='utf-8-sig')
df_product_sales.to_csv('product_sales_ranking_real.csv', index=False, encoding='utf-8-sig')

print("  數據文件已保存為CSV格式")
print("\n✅ 分析完成！")