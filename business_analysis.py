import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import sqlite3
from datetime import datetime

# 連接資料庫
conn = sqlite3.connect('database.db')

# 1. 產品分析
print("=== 產品分析 ===")
product_query = """
SELECT 
    category,
    COUNT(*) as product_count,
    AVG(unit_price) as avg_price,
    SUM(stock_quantity) as total_stock,
    MIN(unit_price) as min_price,
    MAX(unit_price) as max_price
FROM products
GROUP BY category
ORDER BY product_count DESC
"""
df_products = pd.read_sql_query(product_query, conn)
print(df_products.to_string())

# 2. 銷售分析
print("\n=== 銷售分析 ===")
sales_query = """
SELECT 
    strftime('%Y-%m', o.order_date) as month,
    COUNT(DISTINCT o.id) as order_count,
    COUNT(DISTINCT o.customer_id) as customer_count,
    SUM(o.total_amount) as total_sales,
    AVG(o.total_amount) as avg_order_value
FROM orders o
WHERE o.status = 'completed'
GROUP BY strftime('%Y-%m', o.order_date)
ORDER BY month
"""
df_sales = pd.read_sql_query(sales_query, conn)
print(df_sales.to_string())

# 3. 產品銷售排名
print("\n=== 產品銷售排名 ===")
product_sales_query = """
SELECT 
    p.name,
    p.category,
    SUM(oi.quantity) as total_quantity,
    SUM(oi.subtotal) as total_revenue,
    COUNT(DISTINCT oi.order_id) as order_count
FROM order_items oi
JOIN products p ON oi.product_id = p.id
JOIN orders o ON oi.order_id = o.id
WHERE o.status = 'completed'
GROUP BY p.id, p.name, p.category
ORDER BY total_revenue DESC
LIMIT 10
"""
df_product_sales = pd.read_sql_query(product_sales_query, conn)
print(df_product_sales.to_string())

# 4. 客戶分析
print("\n=== 客戶分析 ===")
customer_query = """
SELECT 
    c.membership_level,
    COUNT(DISTINCT c.id) as customer_count,
    COUNT(DISTINCT o.id) as order_count,
    SUM(o.total_amount) as total_spent,
    AVG(o.total_amount) as avg_order_value
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id AND o.status = 'completed'
GROUP BY c.membership_level
ORDER BY total_spent DESC
"""
df_customers = pd.read_sql_query(customer_query, conn)
print(df_customers.to_string())

# 5. 城市客戶分佈
print("\n=== 城市客戶分佈 ===")
city_query = """
SELECT 
    city,
    COUNT(*) as customer_count,
    COUNT(DISTINCT CASE WHEN membership_level = 'Platinum' THEN id END) as platinum_count,
    COUNT(DISTINCT CASE WHEN membership_level = 'Gold' THEN id END) as gold_count,
    COUNT(DISTINCT CASE WHEN membership_level = 'Silver' THEN id END) as silver_count,
    COUNT(DISTINCT CASE WHEN membership_level = 'Bronze' THEN id END) as bronze_count
FROM customers
GROUP BY city
ORDER BY customer_count DESC
"""
df_cities = pd.read_sql_query(city_query, conn)
print(df_cities.to_string())

# 6. 員工分析
print("\n=== 員工分析 ===")
employee_query = """
SELECT 
    department,
    COUNT(*) as employee_count,
    AVG(salary) as avg_salary,
    MIN(salary) as min_salary,
    MAX(salary) as max_salary,
    SUM(salary) as total_salary
FROM employees
GROUP BY department
ORDER BY avg_salary DESC
"""
df_employees = pd.read_sql_query(employee_query, conn)
print(df_employees.to_string())

conn.close()

# 保存數據到文件以便後續使用
df_products.to_csv('products_analysis.csv', index=False)
df_sales.to_csv('sales_analysis.csv', index=False)
df_product_sales.to_csv('product_sales_ranking.csv', index=False)
df_customers.to_csv('customer_analysis.csv', index=False)
df_cities.to_csv('city_analysis.csv', index=False)
df_employees.to_csv('employee_analysis.csv', index=False)

print("\n數據已保存為 CSV 文件")