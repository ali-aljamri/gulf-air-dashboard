from flask import Flask, render_template_string
import requests

app = Flask(__name__)

API_KEY = '0651284ee8a86396948252c9c3b9aae5'

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Live Gulf Air Flights</title>
    <meta http-equiv="refresh" content="60">
    <style>
        body { font-family: Arial, sans-serif; background-color: #f0f4f7; padding: 20px; }
        h1 { color: #005587; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: center; }
        th { background-color: #005587; color: white; }
    </style>
</head>
<body>
    <h1>Live Gulf Air Flights (GF)</h1>
    <table>
        <thead>
            <tr>
                <th>Flight Number</th>
                <th>Departure</th>
                <th>Arrival</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            {% for flight in flights %}
            <tr>
                <td>{{ flight['flight']['iata'] }}</td>
                <td>{{ flight['departure']['airport'] }} ({{ flight['departure']['iata'] }})</td>
                <td>{{ flight['arrival']['airport'] }} ({{ flight['arrival']['iata'] }})</td>
                <td>{{ flight['flight_status'] }}</td>
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
        'airline_iata': 'GF'  # Gulf Air
    }

    try:
        response = requests.get(url, params=params)
        flights = response.json().get('data', [])
        return render_template_string(TEMPLATE, flights=flights)
    except Exception as e:
        return f"<p>Error fetching flight data: {e}</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
