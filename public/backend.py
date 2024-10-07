from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulated data - you will use your backend search script to replace this
car_reviews = [
    {"name": "Tesla Model 3", "review": "Excellent electric vehicle with top-notch features."},
    {"name": "Ford Mustang", "review": "Powerful engine with a classic design."},
    {"name": "Honda Accord", "review": "Reliable sedan with great fuel economy."}
]

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    keywords = data.get('keywords', '').lower()

    # Filter cars based on the input keywords (you'll likely have your own search logic)
    results = [car for car in car_reviews if keywords in car['name'].lower() or keywords in car['review'].lower()]

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
