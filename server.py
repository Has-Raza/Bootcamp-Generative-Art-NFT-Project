import os
import json
from dotenv import load_dotenv
import requests
from PIL import Image
from io import BytesIO
from flask import Flask, render_template, request, send_from_directory, url_for
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired

## UNCOMMENT THIS CODE WHEN RUNNING ON GOOGLE COLAB ##
# from big_sleep import Imagine
# import shutil

# def run_dreams(txt, Learning_rate, Number_of_iterations, Number_of_epochs, Seed):
#     dream = Imagine(
#         text = txt,
#         save_every = 5,
#         save_progress = True,
#         lr = Learning_rate,
#         iterations = Number_of_iterations,
#         epochs = Number_of_epochs,
#         seed = Seed
#     )
#     return dream()

# def get_file(txt):
#     spl = txt.split()
#     GA_file = '_'.join(spl)
#     return f"{GA_file}.png"

# def save_files(txt):
#     GA_file = get_file(txt)
#     return shutil.move(f'/content/{GA_file}', f'/content/gdrive/MyDrive/GenerativeArt/static/Images/{GA_file}')


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['UPLOADED_PHOTOS_DEST'] = 'static/Images/'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Only images are allowed'),
            FileRequired('File field should not be empty')
        ]
    )
    name = StringField('What is your token called?', validators=[DataRequired()])
    submit = SubmitField('Upload')


json_headers = {
    "Content-Type": "application/json",
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_API_KEY"),
}

file_headers = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_API_KEY"),
}

def convert_data_to_json(content):
    data = {"pinataOptions": {"cidVersion": 1}, "pinataContent": content}
    return json.dumps(data)

def pin_file_to_ipfs(data):
    r = requests.post(
        "https://api.pinata.cloud/pinning/pinFileToIPFS",
        files={'file': data},
        headers=file_headers
    )
    print(r.json())
    ipfs_hash = r.json()["IpfsHash"]
    return ipfs_hash

def pin_json_to_ipfs(json):
    r = requests.post(
        "https://api.pinata.cloud/pinning/pinJSONToIPFS",
        data=json,
        headers=json_headers
    )
    print(r.json())
    ipfs_hash = r.json()["IpfsHash"]
    return ipfs_hash

def pin_artwork(artwork_name, artwork_file):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(artwork_file)

    # Build a token metadata file for the artwork
    token_json = {
        "name": artwork_name,
        "image": ipfs_file_hash
    }
    json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash, token_json

nft_url = ''

@app.route("/")
@app.route("/home/")
def home():
    return render_template("home.html")

@app.route("/generate-art/")
def generate_art():
    return render_template("generate-art.html")

## UNCOMMENT THIS CODE WHEN RUNNING ON GOOGLE COLAB ##
# @app.route('/run', methods = ['POST','GET'])
# def execute_dreams():
#   if text_records['text']:
#       run_dreams(text_records['text'], 0.10, 10, 1, 300)
#       save_files(text_records['text'])
#       g_a = get_file(text_records['text'])
#       return render_template("generate-art.html", generated_image = IMAGE_FOLDER + f"/{g_a}", response = "Successfully Generated")
#   else:
#       return render_template("generate-art.html", response = "No Text was given")

@app.route('/images/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'],
                               filename)

@app.route('/mint-nft/')
def mint_nft_page():
    form = UploadForm()
    return render_template("nft.html", form=form)

@app.route("/mint-nft/ipfs-file", methods=['POST'])
def nft():
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file', filename=filename)

        with open(photos.path(filename), "rb") as image:
            f = image.read()
            file = bytearray(f)
        
        nft_name = form.name.data
        nft_ipfs_hash,token_json = pin_artwork(
            nft_name,
            file)
        
        nft_uri = f"ipfs.io/ipfs/{nft_ipfs_hash}"

    else:
        file_url = None
    return render_template("nft.html", form=form, nft_uri=nft_uri, token_json=token_json, file_url=file_url)

@app.route("/images/")
def images():
    return render_template("images.html")

if __name__ == "__main__":
    app.run(debug=True)