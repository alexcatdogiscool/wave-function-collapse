import cv2
from flask import Flask, render_template, jsonify
import base64
from io import BytesIO
from PIL import Image
from flask_cors import CORS



app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/generate_pattern")
def sendImage():
    #print("nkkk")
    img = cv2.imread("image.png")
    img = Image.fromarray(img)
    buffered = BytesIO()
    img.save(buffered, format='PNG')
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return jsonify({"image_data" : img_str})


if __name__ == "__main__":
    app.run(debug=True)