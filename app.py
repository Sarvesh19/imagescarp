from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def get_google_hd_image(search_query):
    api_key = "5fa6a7232952b984c0b1775a35bfcde9e4758741	"
    cx = "c5134144fd2164e06"
    url = f"https://www.googleapis.com/customsearch/v1?q={search_query}&searchType=image&key={api_key}&cx={cx}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            return data["items"][0]["link"]  # Return the first HD image URL
    return None

@app.route("/get-image", methods=["GET"])
def get_image():
    place = request.args.get("place")
    if not place:
        return jsonify({"error": "Place is required"}), 400

    image_url = get_google_hd_image(place)

    if image_url:
        return jsonify({"place": place, "image_url": image_url})
    else:
        return jsonify({"error": "No image found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
