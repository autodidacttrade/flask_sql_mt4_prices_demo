# 📊 flask_sql_mt4_prices_demo

This project show you how to connect **MetaTrader 4 (MT4)** with a server **Flask in Python**, to send prices in real time of several financial instruments such as XRPUSD, EURUSD and others and show it in a HTML table using SQLite as local database.

## 📁 Estructura del proyecto

flask_sql_mt4_prices_demo/
├── app.py # Flask server that get and save prices
├── market_data.db # SQLite database with table "prices"
├── templates/
│ └── index.html # Prices Front End
├── mql4/
│ └── SendPricesToFlask.mq4 # Expert Advisor sends prices from MT4

## ⚙️ Used Technologies

- **Python 3.x**
- **Flask**
- **SQLite3**
- **MQL4 (MetaTrader 4)**
- **HTML (Jinja2 template)**
