from flask import Flask, request, jsonify
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_google_hd_image(place):
    """ Scrapes high-quality images from Google Images using Selenium. """

    # ✅ Set up Selenium with headless Chrome
    options = Options()
    options.add_argument("--headless")  # Run in the background
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-dev-shm-usage")

    # ✅ Set up WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # ✅ Open Google Images search
    search_url = f"https://www.google.com/search?tbm=isch&q={place.replace(' ', '+')}"
    driver.get(search_url)

    # ✅ Wait for images to load
    time.sleep(2)

    # ✅ Extract all HD images
    image_elements = driver.find_elements(By.CSS_SELECTOR, "img")

    hd_images = []
    for img in image_elements:
        src = img.get_attribute("src")
        if src and src.startswith("http") and ("encrypted-tbn0.gstatic.com" not in src):  # Remove low-quality images
            hd_images.append(src)

    driver.quit()

    return hd_images[0] if hd_images else None  # Return first HD image

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
