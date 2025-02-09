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
    
    # Find the first image in the grid
    grid_div = soup.find('div', {'data-testid': 'masonry-grid-count-three'})
    if grid_div:
        # Find all figure tags with photo-grid-masonry-figure data-testid
        figures = grid_div.find_all('figure', {'data-testid': 'photo-grid-masonry-figure'})
        if figures:
            for figure in figures:
                image = figure.find('img', {'srcset': True})
                if image:
                    image_url = image['srcset'].split(' ')[0]
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
