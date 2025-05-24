from flask import Flask, render_template_string
import requests
from datetime import datetime
import pytz

app = Flask(__name__)

API_KEY = '0651284ee8a86396948252c9c3b9aae5'  # Replace with your AviationStack API key
BAHRAIN_TZ = pytz.timezone('Asia/Bahrain')

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Gulf Air Flights - Bahrain International Airport</title>
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
    <h1>Live Gulf Air Flights at Bahrain (BAH)</h1>
    <table>
        <tr>
            <th>Flight</th>
            <th>From</th>
            <th>Departure</th>
            <th>To</th>
            <th>Arrival</th>
            <th>Status</th>
        </tr>
        {% for flight in flights %}
        <tr>
            <td>{{ flight['flight']['iata'] or '-' }}</td>
            <td>{{ flight['departure']['airport'] or '-' }}</td>
            <td>{{ flight['departure_local'] or '-' }}</td>
            <td>{{ flight['arrival']['airport'] or '-' }}</td>
            <td>{{ flight['arrival_local'] or '-' }}</td>
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
        res = requests.get(url, params=params)
        flights = res.json().get('data', [])

        filtered = []
        for flight in flights:
            dep = flight.get('departure', {})
            arr = flight.get('arrival', {})

            # Only show flights where BAH is departure or arrival
            if dep.get('iata') == 'BAH' or arr.get('iata') == 'BAH':
                # Convert UTC times to local
                flight['departure_local'] = format_time(dep.get('scheduled'))
                flight['arrival_local'] = format_time(arr.get('scheduled'))
                filtered.append(flight)

        return render_template_string(TEMPLATE, flights=filtered)

    except Exception as e:
        return f"<p>Error: {e}</p>"

def format_time(utc_time):
    try:
        dt = datetime.strptime(utc_time, '%Y-%m-%dT%H:%M:%S+00:00')
        dt = pytz.utc.localize(dt).astimezone(BAHRAIN_TZ)
        return dt.strftime('%Y-%m-%d %H:%M')
    except:
        return '-'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
