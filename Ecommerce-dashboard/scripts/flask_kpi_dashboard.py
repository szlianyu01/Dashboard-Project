from flask import Flask, jsonify, render_template_string
from sqlalchemy import create_engine
import pandas as pd

app = Flask(__name__)
engine = create_engine("mysql+pymysql://root:Ly731111%40@localhost/ecommerce_db")

# Predefined queries
queries = {
    "fulfillmentRate": """
        SELECT ROUND(SUM(CASE WHEN status IN ('shipped', 'delivered') THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS value
        FROM orders;
    """,
    "avgOrderValue": "SELECT ROUND(AVG(total_amount), 2) AS value FROM orders;",
    "repeatRate": """
        SELECT ROUND(COUNT(*) / (SELECT COUNT(*) FROM customers) * 100, 2) AS value
        FROM (
            SELECT customer_id FROM orders GROUP BY customer_id HAVING COUNT(order_id) >= 2
        ) sub;
    """,
    "countryRevenue": """
        SELECT c.country, ROUND(SUM(p.amount_paid), 2) AS value
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN payments p ON o.order_id = p.order_id
        WHERE p.is_successful = TRUE
        GROUP BY c.country;
    """
}

@app.route("/api/kpis")
def get_kpis():
    result = {}
    with engine.connect() as conn:
        for key, sql in queries.items():
            df = pd.read_sql(sql, conn)
            if key == "countryRevenue":
                result[key] = df.to_dict(orient="records")
            else:
                result[key] = df['value'].iloc[0] if not df.empty else 0
    return jsonify(result)

@app.route("/")
def dashboard():
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset='UTF-8'>
        <title>KPI Dashboard</title>
        <script src='https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js'></script>
        <style>
            body { font-family: Arial; padding: 20px; background: #f0f2f5; }
            .chart-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; }
            .chart-box { background: #fff; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
            .chart { width: 100%; height: 300px; }
        </style>
    </head>
    <body>
        <h1>KPI Dashboard</h1>
        <div class='chart-container'>
            <div class='chart-box'><h3>Fulfillment Rate</h3><div id='fulfillmentChart' class='chart'></div></div>
            <div class='chart-box'><h3>Average Order Value</h3><div id='aovChart' class='chart'></div></div>
            <div class='chart-box'><h3>Repeat Customer Rate</h3><div id='repeatChart' class='chart'></div></div>
            <div class='chart-box'><h3>Revenue by Country</h3><div id='countryChart' class='chart'></div></div>
        </div>
        <script>
            fetch('/api/kpis').then(res => res.json()).then(data => {
                echarts.init(document.getElementById('fulfillmentChart')).setOption({
                    series: [{ type: 'gauge', progress: { show: true }, detail: { formatter: '{value}%' }, data: [{ value: data.fulfillmentRate }] }]
                });
                echarts.init(document.getElementById('aovChart')).setOption({
                    xAxis: { type: 'category', data: ['Avg Order'] },
                    yAxis: { type: 'value' },
                    series: [{ type: 'bar', data: [data.avgOrderValue] }]
                });
                echarts.init(document.getElementById('repeatChart')).setOption({
                    series: [{
                        type: 'pie',
                        radius: '70%',
                        data: [
                            { value: data.repeatRate, name: 'Repeat' },
                            { value: 100 - data.repeatRate, name: 'New' }
                        ]
                    }]
                });
                echarts.init(document.getElementById('countryChart')).setOption({
                    xAxis: { type: 'category', data: data.countryRevenue.map(r => r.country) },
                    yAxis: { type: 'value' },
                    series: [{ type: 'bar', data: data.countryRevenue.map(r => r.value) }]
                });
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)

if __name__ == "__main__":
    app.run(debug=True)
