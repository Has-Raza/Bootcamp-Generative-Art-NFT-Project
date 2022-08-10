import os
from flask import Flask, render_template, request, send_from_directory
# from generative_art import *

app = Flask(__name__)

IMAGE_FOLDER = "static/Images"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['IMAGE_FOLDER'] = IMAGE_FOLDER

@app.route("/")
@app.route("/home/")
def home():
    return render_template("home.html")

@app.route("/generate-art/")
def generate_art():
    return render_template("generate-art.html")

@app.route("/mint-nft/")
def nft():
    return render_template("nft.html")

@app.route("/images/")
def images():
    return render_template("images.html")

@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['IMAGE_FOLDER'],
                               filename)



if __name__ == "__main__":
    app.run(debug=True)