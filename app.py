from flask import Flask, request, jsonify
from httpx import get
from selectolax.parser import HTMLParser
import time

app = Flask(__name__)

def fetch_unsplash_image_url(search_term):
    """
    Scrapes Unsplash for image URLs based on the search term.
    Returns the first high-resolution image URL.
    """
    if not search_term:
        raise ValueError("Search term is required")

    # Construct the Unsplash search URL
    url = f"https://unsplash.com/s/photos/{search_term.replace(' ', '-')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/",
    }

    # Send a GET request to Unsplash
    try:
        response = get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data from Unsplash. Status code: {response.status_code}")

        # Parse the HTML response
        tree = HTMLParser(response.text)

        # Find all image tags
        image_nodes = tree.css("figure a img")
        if not image_nodes:
            raise Exception("No images found on the page")

        # Extract image URLs
        image_urls = [img.attrs.get("src") for img in image_nodes if img.attrs.get("src")]

        # Filter out low-quality or irrelevant images
        filtered_urls = [url for url in image_urls if not any(kw in url for kw in ["premium", "profile", "plus", "data:image"])]

        if not filtered_urls:
            raise Exception("No valid image URLs found")

        # Return the first high-resolution image URL
        return filtered_urls[0].split("?")[0]

    except Exception as e:
        raise Exception(f"Error fetching image: {str(e)}")

@app.route("/get-image", methods=["GET"])
def get_image():
    """
    API endpoint to fetch an image URL based on a search term (place).
    """
    place = request.args.get("place")
    if not place:
        return jsonify({"error": "Place parameter is required"}), 400

    try:
        # Fetch the image URL from Unsplash
        image_url = fetch_unsplash_image_url(place)
        return jsonify({"place": place, "image_url": image_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
