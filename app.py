from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

@app.route('/api/topptips', methods=['GET'])
def get_topptips():
    url = "https://tipsrader.se/spel/topptips"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return jsonify({"error": "Kunde inte hämta data från sidan"}), 500

    soup = BeautifulSoup(response.text, 'html.parser')
    matcher = []

    for row in soup.select('table tr'):
        cols = row.find_all('td')
        if len(cols) >= 2:
            lagtext = cols[1].get_text(strip=True)
            if ' - ' in lagtext:
                matcher.append(lagtext)

    return jsonify({
        "datum": datetime.now().strftime("%Y-%m-%d"),
        "matcher": matcher
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
