from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_google_image(place):
    search_url = f"https://www.google.com/search?tbm=isch&q={place.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    img_tags = soup.find_all("img")
    image_urls = [img["src"] for img in img_tags if "http" in img["src"]]

    return image_urls[0] if image_urls else None  # Returns first valid image URL

@app.route("/get-image", methods=["GET"])
def get_image():
    place = request.args.get("place")
    if not place:
        return jsonify({"error": "Place is required"}), 400

    image_url = get_google_image(place)
    if image_url:
        return jsonify({"place": place, "image_url": image_url})
    else:
        return jsonify({"error": "No image found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
