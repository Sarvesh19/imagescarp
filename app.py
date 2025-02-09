from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def get_image_url(search_query):
    """Scrapes the first image URL from Unsplash search results."""
    search_url = f"https://unsplash.com/s/photos/{search_query.replace(' ', '-')}"
    
    response = requests.get(search_url)
    if response.status_code != 200:
        return None  # Request failed
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    image = soup.find('img', {'srcset': True})
    if image:
        # Extract URL from srcset and pick the highest resolution image
        srcset = image['srcset'].split(',')
        highest_res_url = srcset[-1].split(' ')[0]
        return highest_res_url
    else:
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
