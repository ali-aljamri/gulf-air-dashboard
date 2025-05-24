from flask import Flask, render_template_string
import requests

app = Flask(__name__)

API_KEY = '0651284ee8a86396948252c9c3b9aae5'  # Replace this with your real API key

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Gulf Air Flights (Live)</title>
    <meta http-equiv="refresh" content="60">
    <style>
        body { font-family: Arial, sans-serif; background: #f9f9f9; padding: 20px; }
        h1 { color: #005587; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: center; }
        th { background-color: #005587; color: white; }
    </style>
</head>
<body>
    <h1>Live Gulf Air Flights</h1>
    <table>
        <thead>
            <tr>
                <th>Flight</th>
                <th>From</th>
                <th>To</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
        {% for flight in flights %}
            <tr>
                <td>{{ flight['flight']['iata'] or 'N/A' }}</td>
                <td>{{ flight['departure']['airport'] or 'N/A' }} ({{ flight['departure']['iata'] or '' }})</td>
                <td>{{ flight['arrival']['airport'] or 'N/A' }} ({{ flight['arrival']['iata'] or '' }})</td>
                <td>{{ flight['flight_status'] or 'N/A' }}</td>
            </tr>
        {% endfor %}
        </tbody>
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
        flights = response.json().get('data', [])
        return render_template_string(TEMPLATE, flights=flights)
    except Exception as e:
        return f"<p>Error: {e}</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
