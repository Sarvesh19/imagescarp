from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def get_google_hd_image(place):
    """Scrapes the first HD image URL from Google Images search results."""
    search_url = f"https://www.google.com/search?tbm=isch&q={place.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        return None  # Google blocked the request

    soup = BeautifulSoup(response.text, "html.parser")

    # Google stores HD images inside JavaScript `data` attributes
    scripts = soup.find_all("script")

    for script in scripts:
        script_text = script.text
        if "AF_initDataCallback" in script_text:
            # Use regex to extract HD image URLs
            urls = re.findall(r'\[\"(https:\/\/[^"]+\.(jpg|jpeg|png|gif))\",\d+,\d+\]', script_text)
            hd_images = [url[0] for url in urls if url]
            
            if hd_images:
                return hd_images[0]  # Return the first HD image URL

    return None  # No HD images found

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
