from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_google_hd_image(place):
    search_url = f"https://www.google.com/search?tbm=isch&q={place.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract HD images from Google's JavaScript-rendered elements
    scripts = soup.find_all("script")
    
    for script in scripts:
        if "var s='data:image" in script.text:
            urls = script.text.split('","')[1::2]  # Extract HD URLs
            hd_images = [url for url in urls if url.startswith("http")]
            if hd_images:
                return hd_images[0]  # Return first HD image

    return None  # No HD image found

def get_unsplash_image(place):
    return f"https://source.unsplash.com/1600x900/?{place.replace(' ', '+')}"

@app.route("/get-image", methods=["GET"])
def get_image():
    place = request.args.get("place")
    if not place:
        return jsonify({"error": "Place is required"}), 400

    # Try Google first, fallback to Unsplash
    image_url = get_google_hd_image(place) or get_unsplash_image(place)
    
    return jsonify({"place": place, "image_url": image_url})

if __name__ == "__main__":
    app.run(debug=True)
