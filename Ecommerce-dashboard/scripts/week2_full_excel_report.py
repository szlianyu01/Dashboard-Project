from sqlalchemy import create_engine
import pandas as pd

# Connect to MySQL using SQLAlchemy
engine = create_engine("mysql+pymysql://root:Ly731111%40@localhost/ecommerce_db")

# Dictionary to store results
results = {}

def run_query(query, desc):
    print(f"\n📌 {desc}")
    df = pd.read_sql(query, con=engine)
    print(df.head())
    results[desc] = df

# 1. Data Profiling
run_query("SELECT COUNT(*) AS customer_count FROM customers;", "Customer count")
run_query("SELECT COUNT(*) AS orders_count FROM orders;", "Orders count")
run_query("SELECT COUNT(*) AS payments_count FROM payments;", "Payments count")

run_query("SELECT COUNT(*) AS null_emails FROM customers WHERE email IS NULL;", "Customers with NULL email")
run_query("SELECT email, COUNT(*) AS dup_count FROM customers GROUP BY email HAVING dup_count > 1;", "Duplicate emails")

# 2. Anomaly Detection
run_query("SELECT * FROM products WHERE price <= 0;", "Products with non-positive price")
run_query("SELECT * FROM payments WHERE amount_paid IS NULL;", "Payments with missing amount")
run_query("SELECT product_id, COUNT(*) AS count FROM products GROUP BY product_id HAVING count > 1;", "Duplicate product IDs")

# 3. Data Reconciliation
run_query("""
SELECT o.order_id, o.total_amount, 
       ROUND(SUM(oi.quantity * oi.unit_price), 2) AS item_total,
       ROUND(o.total_amount - SUM(oi.quantity * oi.unit_price), 2) AS diff
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id
HAVING diff != 0;
""", "Order vs Order Items mismatch")

run_query("""
SELECT o.order_id, o.total_amount, p.amount_paid,
       ROUND(p.amount_paid - o.total_amount, 2) AS payment_diff
FROM orders o
JOIN payments p ON o.order_id = p.order_id
WHERE ROUND(p.amount_paid - o.total_amount, 2) != 0;
""", "Order vs Payment mismatch")

run_query("""
SELECT o.order_id FROM orders o
LEFT JOIN payments p ON o.order_id = p.order_id
WHERE p.order_id IS NULL;
""", "Orders with no payment record")

# 4. KPI Calculation
run_query("""
SELECT 
  ROUND(SUM(CASE WHEN status IN ('shipped', 'delivered') THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS fulfillment_rate
FROM orders;
""", "Fulfillment Rate")

run_query("SELECT ROUND(AVG(total_amount), 2) AS avg_order_value FROM orders;", "Average Order Value")

run_query("""
SELECT 
  ROUND(COUNT(*) / (SELECT COUNT(*) FROM customers) * 100, 2) AS repeat_customer_rate
FROM (
  SELECT customer_id FROM orders
  GROUP BY customer_id
  HAVING COUNT(order_id) >= 2
) sub;
""", "Repeat Customer Rate")

run_query("""
SELECT c.country, ROUND(SUM(p.amount_paid), 2) AS revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN payments p ON o.order_id = p.order_id
WHERE p.is_successful = TRUE
GROUP BY c.country;
""", "Revenue by Country")

# Save to Excel
output_path = "D:/Myproject/python/week2_report.xlsx"
with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    for sheet_name, df in results.items():
        safe_sheet = sheet_name[:31].replace(":", "-")  # Excel sheet name max 31 chars
        df.to_excel(writer, sheet_name=safe_sheet, index=False)

print(f"✅ Full report saved to {output_path}")
