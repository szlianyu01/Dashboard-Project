# 📊 E-Commerce KPI Dashboard Project

This project demonstrates how to analyze, validate, and visualize key business performance metrics for an e-commerce platform using Python, MySQL, and ECharts.

## 🚀 Project Overview

The system includes two core implementations:
- ✅ **Static HTML Dashboard**: KPI data is pulled from MySQL and injected into a standalone HTML page.
- ✅ **Flask API Dashboard**: Real-time KPI data is served through a Flask backend and visualized in a dynamic ECharts dashboard.

## 📁 Project Structure

```
ecommerce-kpi-dashboard/
├── README.md
├── requirements.txt
├── scripts/
│   ├── generate_static_kpi_html.py
│   ├── week2_full_excel_report.py
│   └── flask_kpi_dashboard.py
├── dashboards/
│   └── static_kpi_dashboard.html
├── data/
│   └── week2_report.xlsx
└── .gitignore
```

## 📊 KPI Metrics Included

- **Fulfillment Rate** — Percentage of orders delivered/shipped
- **Average Order Value** — Mean total_amount per order
- **Repeat Customer Rate** — Customers who placed 2+ orders
- **Revenue by Country** — Aggregated payment amounts by region

## 🧪 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate Excel Report
```bash
python scripts/week2_full_excel_report.py
```

### 3. Create Static Dashboard
```bash
python scripts/generate_static_kpi_html.py
```
Open the file `dashboards/static_kpi_dashboard.html` in a browser.

### 4. Launch Flask Real-Time Dashboard
```bash
python scripts/flask_kpi_dashboard.py
```
Then visit `http://localhost:5000` to see the dynamic dashboard.

## 🧠 Technologies Used

- Python 3, pandas, SQLAlchemy
- MySQL (local)
- Flask (API backend)
- ECharts (frontend visualization)

## 📂 Data Source

The database is created locally under `ecommerce_db`, with tables:
- `customers`, `orders`, `order_items`, `payments`, `products`

Test data was generated to simulate realistic order and payment behavior.

## 📜 License

MIT License. Educational use encouraged.
