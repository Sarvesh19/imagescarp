from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def get_image_url(search_query):
    """Scrapes the first image URL from Unsplash search results."""
    search_url = f"https://unsplash.com/s/photos/{search_query.replace(' ', '-')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        return None  # Request failed

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first image in the grid
    img_tag = soup.find('img', {'class': 'YVj9w'})  # Class name for images on Unsplash
    if img_tag:
        # Extract the image URL from the srcset attribute
        srcset = img_tag.get('srcset')
        if srcset:
            # Get the highest resolution image from the srcset
            image_url = srcset.split(',')[-1].strip().split(' ')[0]
            return image_url

    return None  # No image found

@app.route("/get-image", methods=["GET"])
def get_image():
    place = request.args.get("place")
    if not place:
        return jsonify({"error": "Place is required"}), 400

    image_url = get_image_url(place)

    if image_url:
        return jsonify({"place": place, "image_url": image_url})
    else:
        return jsonify({"error": "No image found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
