from datetime import datetime, date, timedelta
import pandas as pd
import plotly.express as px
import os

# Query result reproduced here
data = [
    {"year_week": "2025-48", "total_sales": 162462.0},
    {"year_week": "2025-49", "total_sales": 301589.0},
    {"year_week": "2025-51", "total_sales": 334180.0},
    {"year_week": "2025-52", "total_sales": 209618.0},
]

# Create DataFrame
df = pd.DataFrame(data)

# Parse year_week into a date representing the Monday of that week
def year_week_to_date(yw):
    try:
        return datetime.strptime(yw + '-1', '%Y-%W-%w').date()
    except Exception:
        y, w = yw.split('-')
        y = int(y); w = int(w)
        jan1 = date(y, 1, 1)
        # find the first Monday on or after Jan 1
        days_to_monday = (7 - jan1.weekday()) % 7
        first_monday = jan1 + timedelta(days=days_to_monday)
        return first_monday + timedelta(weeks=w)

if not df.empty:
    df['week_start'] = df['year_week'].apply(year_week_to_date)
else:
    df['week_start'] = pd.to_datetime([])

# Prepare last 12 weeks (week starts on Monday)
_today = date.today()
most_recent_monday = _today - timedelta(days=_today.weekday())
start_monday = most_recent_monday - timedelta(weeks=11)
week_starts = [start_monday + timedelta(weeks=i) for i in range(12)]
labels = [d.strftime('%Y-%W') for d in week_starts]

# Map existing totals to labels, fill missing with 0
totals_map = dict(zip(df['year_week'], df['total_sales']))
y = [totals_map.get(lbl, 0.0) for lbl in labels]

# Build DataFrame for plotting
plot_df = pd.DataFrame({'week_start': week_starts, 'year_week': labels, 'total_sales': y})

# Ensure charts directory exists
os.makedirs('charts', exist_ok=True)

# Create line chart
fig = px.line(plot_df, x='week_start', y='total_sales', markers=True,
              title='過去 12 週銷售趨勢', labels={'week_start': 'Week Start', 'total_sales': 'Total Sales (NT$)'})
fig.update_layout(xaxis=dict(tickformat='%Y-%W'))

outpath = 'charts/sales_trend_12_weeks.html'
fig.write_html(outpath)

result = {'html_path': outpath, 'plot_data': plot_df.to_dict(orient='records')}