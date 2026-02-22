import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime
import os

# 從查詢結果建立資料
monthly_data = [
    {"month": "2024-01", "monthly_revenue": 604586.0, "order_count": 5},
    {"month": "2024-02", "monthly_revenue": 656767.0, "order_count": 6},
    {"month": "2024-03", "monthly_revenue": 1009724.0, "order_count": 9},
    {"month": "2024-04", "monthly_revenue": 900727.0, "order_count": 7},
    {"month": "2024-05", "monthly_revenue": 1470517.0, "order_count": 9},
    {"month": "2024-06", "monthly_revenue": 1048949.0, "order_count": 8},
    {"month": "2024-07", "monthly_revenue": 870084.0, "order_count": 5},
    {"month": "2024-08", "monthly_revenue": 1073268.0, "order_count": 10},
    {"month": "2024-09", "monthly_revenue": 693661.0, "order_count": 9},
    {"month": "2024-10", "monthly_revenue": 1849539.0, "order_count": 10},
    {"month": "2024-11", "monthly_revenue": 953410.0, "order_count": 12},
    {"month": "2024-12", "monthly_revenue": 1029130.0, "order_count": 7}
]

# 提取月份和營收數據
months = [data["month"] for data in monthly_data]
revenues = [data["monthly_revenue"] for data in monthly_data]
order_counts = [data["order_count"] for data in monthly_data]

# 建立折線圖
fig = go.Figure()

# 添加營收折線
fig.add_trace(go.Scatter(
    x=months,
    y=revenues,
    mode='lines+markers+text',
    name='月營收',
    line=dict(color='royalblue', width=3),
    marker=dict(size=8),
    text=[f'${rev:,.0f}' for rev in revenues],
    textposition='top center',
    hovertemplate='<b>%{x}</b><br>營收: $%{y:,.0f}<br>訂單數: %{customdata}<extra></extra>',
    customdata=order_counts
))

# 添加訂單數柱狀圖（次座標軸）
fig.add_trace(go.Bar(
    x=months,
    y=order_counts,
    name='訂單數',
    yaxis='y2',
    marker_color='rgba(255, 99, 71, 0.6)',
    opacity=0.7,
    hovertemplate='<b>%{x}</b><br>訂單數: %{y}<extra></extra>'
))

# 更新佈局
fig.update_layout(
    title={
        'text': '2024年每月營收趨勢（完成訂單）',
        'font': {'size': 24, 'family': 'Arial Black'},
        'x': 0.5,
        'xanchor': 'center'
    },
    xaxis=dict(
        title='月份',
        tickangle=45,
        gridcolor='lightgray'
    ),
    yaxis=dict(
        title=dict(
            text='營收（美元）',
            font=dict(color='royalblue')
        ),
        tickformat='$,.0f',
        gridcolor='lightgray'
    ),
    yaxis2=dict(
        title=dict(
            text='訂單數',
            font=dict(color='tomato')
        ),
        overlaying='y',
        side='right'
    ),
    hovermode='x unified',
    template='plotly_white',
    height=600,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    plot_bgcolor='rgba(240, 240, 240, 0.5)'
)

# 添加平均線
avg_revenue = sum(revenues) / len(revenues)
fig.add_hline(
    y=avg_revenue,
    line_dash="dash",
    line_color="gray",
    annotation_text=f"平均營收: ${avg_revenue:,.0f}",
    annotation_position="bottom right"
)

# 確保 charts 目錄存在
os.makedirs('charts', exist_ok=True)

# 儲存為 HTML 檔案
output_file = 'charts/monthly_revenue_2024.html'
fig.write_html(output_file)

print(f"圖表已儲存至: {output_file}")
print(f"瀏覽器查看連結: http://localhost:7777/charts/monthly_revenue_2024.html")

# 顯示統計摘要
print("\n📊 2024年營收統計摘要:")
print(f"總營收: ${sum(revenues):,.2f}")
print(f"平均月營收: ${avg_revenue:,.2f}")
print(f"最高月營收: ${max(revenues):,.2f} ({months[revenues.index(max(revenues))]})")
print(f"最低月營收: ${min(revenues):,.2f} ({months[revenues.index(min(revenues))]})")
print(f"總訂單數: {sum(order_counts)}")
print(f"平均訂單金額: ${sum(revenues)/sum(order_counts):,.2f}")