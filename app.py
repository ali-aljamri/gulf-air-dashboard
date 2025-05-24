from flask import Flask, render_template_string
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = '0651284ee8a86396948252c9c3b9aae5'  # Replace with your actual AviationStack API key

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Gulf Air Flights</title>
    <meta http-equiv="refresh" content="60">
    <style>
        body { font-family: Arial; background: #f4f4f4; padding: 20px; }
        h1 { color: #004080; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 10px; border: 1px solid #ccc; text-align: center; }
        th { background: #004080; color: #fff; }
    </style>
</head>
<body>
    <h1>Live Gulf Air Flights (GF)</h1>
    <table>
        <tr>
            <th>Flight</th>
            <th>From</th>
            <th>Departure Time</th>
            <th>To</th>
            <th>Arrival Time</th>
            <th>Status</th>
        </tr>
        {% for flight in flights %}
        <tr>
            <td>{{ flight['flight']['iata'] or '-' }}</td>
            <td>{{ flight['departure']['airport'] or '-' }}</td>
            <td>{{ flight['departure']['scheduled'] or '-' }}</td>
            <td>{{ flight['arrival']['airport'] or '-' }}</td>
            <td>{{ flight['arrival']['scheduled'] or '-' }}</td>
            <td>{{ flight['flight_status'] or '-' }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route('/')
def index():
    url = 'http://api.aviationstack.com/v1/flights'
    params = {
        'access_key': API_KEY,
        'airline_iata': 'GF'
    }
    try:
        response = requests.get(url, params=params)
        data = response.json().get('data', [])
        return render_template_string(TEMPLATE, flights=data)
    except Exception as e:
        return f"<p>Error: {e}</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
