import plotly.graph_objects as go
import os
from db_helper import query

def plot_monthly_revenue_trend(year=2024, output_filename=None):
    """
    Plot monthly revenue trend for completed orders in specified year.
    
    Parameters:
    - year: int, year to analyze (default: 2024)
    - output_filename: str, output HTML filename (default: f'monthly_revenue_{year}.html')
    
    Returns:
    - dict: Contains file_path, total_revenue, avg_monthly_revenue, max_month, min_month
    """
    
    # Query monthly revenue data
    sql_query = f"""
    SELECT 
        strftime('%Y-%m', order_date) as month,
        SUM(total_amount) as monthly_revenue,
        COUNT(*) as order_count
    FROM orders 
    WHERE status = 'completed' 
        AND strftime('%Y', order_date) = '{year}'
    GROUP BY strftime('%Y-%m', order_date)
    ORDER BY month
    """
    
    monthly_data = query(sql_query)
    
    if not monthly_data:
        return {"error": f"No completed orders found for year {year}"}
    
    # Extract data
    months = [data["month"] for data in monthly_data]
    revenues = [data["monthly_revenue"] for data in monthly_data]
    order_counts = [data["order_count"] for data in monthly_data]
    
    # Create figure
    fig = go.Figure()
    
    # Add revenue line
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
    
    # Add order count bar chart (secondary axis)
    fig.add_trace(go.Bar(
        x=months,
        y=order_counts,
        name='訂單數',
        yaxis='y2',
        marker_color='rgba(255, 99, 71, 0.6)',
        opacity=0.7,
        hovertemplate='<b>%{x}</b><br>訂單數: %{y}<extra></extra>'
    ))
    
    # Update layout
    fig.update_layout(
        title={
            'text': f'{year}年每月營收趨勢（完成訂單）',
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
    
    # Add average line
    avg_revenue = sum(revenues) / len(revenues)
    fig.add_hline(
        y=avg_revenue,
        line_dash="dash",
        line_color="gray",
        annotation_text=f"平均營收: ${avg_revenue:,.0f}",
        annotation_position="bottom right"
    )
    
    # Ensure charts directory exists
    os.makedirs('charts', exist_ok=True)
    
    # Set output filename
    if output_filename is None:
        output_filename = f'monthly_revenue_{year}.html'
    
    output_file = f'charts/{output_filename}'
    
    # Save as HTML file
    fig.write_html(output_file)
    
    # Calculate statistics
    total_revenue = sum(revenues)
    max_revenue = max(revenues)
    min_revenue = min(revenues)
    max_month = months[revenues.index(max_revenue)]
    min_month = months[revenues.index(min_revenue)]
    total_orders = sum(order_counts)
    avg_order_amount = total_revenue / total_orders if total_orders > 0 else 0
    
    result = {
        "file_path": output_file,
        "web_url": f"http://localhost:7777/charts/{output_filename}",
        "year": year,
        "total_revenue": total_revenue,
        "avg_monthly_revenue": avg_revenue,
        "max_month": max_month,
        "max_revenue": max_revenue,
        "min_month": min_month,
        "min_revenue": min_revenue,
        "total_orders": total_orders,
        "avg_order_amount": avg_order_amount,
        "month_count": len(months)
    }
    
    return result