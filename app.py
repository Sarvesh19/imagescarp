from flask import Flask, request, jsonify
from httpx import get
from selectolax.parser import HTMLParser
import os

app = Flask(__name__)

class ImageScraper:
    def __init__(self, search_term):
        self.search_term = search_term
        self.image_nodes = []
        self.img_urls = []

    def fetch_image_tags(self):
        """Fetch image tags from Unsplash based on the provided search term."""
        if not self.search_term:
            raise Exception("No search term provided")

        url = f"https://unsplash.com/s/photos/{self.search_term}"
        response = get(url)

        if response.status_code != 200:
            raise Exception(f"Error getting response. Status code: {response.status_code}")

        tree = HTMLParser(response.text)
        self.image_nodes = tree.css("figure a img")
        self.img_urls = [i.attrs['src'] for i in self.image_nodes]

    def filter_images(self, keywords):
        """Filter out images based on specified keywords."""
        return [url for url in self.img_urls if not self.img_filter_out(url, keywords)]

    @staticmethod
    def img_filter_out(url, keywords):
        """Check if any keyword is present in the image URL."""
        return any(x in url for x in keywords)

    @staticmethod
    def get_high_res_img_url(img_urls):
        """Extract high-resolution image URLs from the original URLs."""
        return [url.split("?")[0] for url in img_urls]

@app.route("/get-image", methods=["GET"])
def get_image():
    place = request.args.get("place")
    if not place:
        return jsonify({"error": "Place is required"}), 400

    try:
        # Fetch image URLs from Unsplash
        scraper = ImageScraper(place)
        scraper.fetch_image_tags()

        # Filter out irrelevant images
        relevant_urls = scraper.filter_images(['premium', 'profile', 'plus', 'data:image/bmp'])

        # Get high-resolution image URLs
        high_res_img_urls = ImageScraper.get_high_res_img_url(relevant_urls)

        if high_res_img_urls:
            # Return the first high-resolution image URL
            return jsonify({"place": place, "image_url": high_res_img_urls[0]})
        else:
            return jsonify({"error": "No image found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
