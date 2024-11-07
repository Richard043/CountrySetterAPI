from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS
import random
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Fetch the data once and reuse it for performance
url_api = 'https://restcountries.com/v3.1/all'
response = requests.get(url_api)
data = response.json()

# Endpoint to search for a country by name
@app.route('/search', methods=['GET'])
def search_country():
    country_name = request.args.get('country')
    if not country_name:
        return jsonify({"error": "No country name provided"}), 400  # Handle empty input

    country_name = country_name.capitalize()  # Capitalize for consistent matching

    for country in data:
        if country["name"]["common"].lower() == country_name.lower():  # Case-insensitive match
            return jsonify(extract_country_data(country))
    
    return jsonify({"error": f"Country '{country_name}' not found"}), 404

# Endpoint to get a random country
@app.route('/random', methods=['GET'])
def random_country():
    country = random.choice(data)
    return jsonify(extract_country_data(country))

# Helper function to extract country data
def extract_country_data(country):
    currencies = country['currencies']
    currency_code = list(currencies.keys())[0]
    currency_info = currencies[currency_code]

    return {
        "country": country["name"]["common"],
        "country_code": country['cca2'],
        "continent": country['continents'][0],
        "capital": country['capital'][0] if 'capital' in country and country['capital'] else "N/A",
        "population": country['population'],
        "timezones": country['timezones'],
        "currency": {
            "code": currency_code,
            "name": currency_info['name'],
            "symbol": currency_info.get('symbol', '')
        },
        "flag_url": country['flags']['png']
    }

if __name__ == '__main__':
    app.run(debug=True, host= "0.0.0.0", port=5000)
