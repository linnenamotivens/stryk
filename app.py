from flask import Flask, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/api/topptips', methods=['GET'])
def get_topptips():
    url = "https://tipsrader.se/api/tips/24/matches"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return jsonify({"error": "Kunde inte hämta data från API"}), 500

    data = response.json()
    matcher = []

    for match in data:
        home = match.get("homeTeam")
        away = match.get("awayTeam")
        if home and away:
            matcher.append(f"{home} - {away}")

    return jsonify({
        "datum": datetime.now().strftime("%Y-%m-%d"),
        "matcher": matcher
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
