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

    for match_div in soup.select('.game__team-names'):
        match_text = match_div.get_text(separator=' ', strip=True)
        if match_text:
            matcher.append(match_text)

    return jsonify({
        "datum": datetime.now().strftime("%Y-%m-%d"),
        "matcher": matcher
    })

if __name__ == '__main__':
    app.run(debug=True)
