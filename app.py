from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_unsplash(query):
    url = f"https://unsplash.com/s/photos/{query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return {"error": "Failed to fetch data from Unsplash"}
    
    soup = BeautifulSoup(response.text, "html.parser")
    images = []
    
    # Find image elements (this may change if Unsplash updates their HTML structure)
    for img in soup.find_all("img", {"class": "img.cnmNG"}):
        image_url =  img.get("currentSrc")
        if image_url:
            images.append({"url": image_url})
    
    return images

@app.route("/images", methods=["GET"])
def get_images():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Query parameter 'query' is required"}), 400
    
    images = scrape_unsplash(query)
    return jsonify(images)

if __name__ == "__main__":
    app.run(debug=True)
