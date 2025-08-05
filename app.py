from flask import Flask, request, jsonify, render_template
import json
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_PATH = "market_data.db"

# Función para guardar o actualizar el precio en la base de datos
def save_price_to_db(symbol, bid, ask):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT 1 FROM prices WHERE symbol = ?", (symbol,))
    exists = c.fetchone()

    if exists:
        c.execute("""
            UPDATE prices 
            SET bid = ?, ask = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE symbol = ?
        """, (bid, ask, symbol))
    else:
        c.execute("""
            INSERT INTO prices (symbol, bid, ask, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (symbol, bid, ask))

    conn.commit()
    conn.close()

# Ruta para recibir datos desde Metatrader
@app.route('/receive', methods=['POST'])
def receive_data():
    try:
        raw_data = request.data.decode('utf-16')
        print("📄 Decoded body:", raw_data)
        data = json.loads(raw_data)

        symbol = data.get("symbol")
        bid = float(data.get("bid", 0.0))
        ask = float(data.get("ask", 0.0))

        if not symbol:
            raise ValueError("Missing 'symbol' in JSON")

        save_price_to_db(symbol, bid, ask)
        print(f"✅ Guardado en DB: {symbol} BID: {bid} ASK: {ask}")
        return jsonify({"status": "saved", "symbol": symbol}), 200

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": str(e)}), 400

# Ruta para mostrar HTML
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para enviar precios como JSON al HTML
@app.route('/prices')
def get_prices():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT symbol, bid, ask, updated_at FROM prices")
    rows = c.fetchall()
    conn.close()

    data = [
        {
            "symbol": row[0],
            "bid": row[1],
            "ask": row[2],
            "updated_at": row[3]
        }
        for row in rows
    ]
    return jsonify(data)

# Ejecutar el servidor Flask
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
