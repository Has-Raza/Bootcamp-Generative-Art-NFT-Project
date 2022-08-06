from webbrowser import get
import streamlit as st
from big_sleep import Imagine
import shutil

def run_dreams(txt, Learning_rate, Number_of_iterations, Number_of_epochs, Seed):
    dream = Imagine(
        text = txt,
        save_every = 1000,
        save_progress = True,
        lr = Learning_rate,
        iterations = Number_of_iterations,
        epochs = Number_of_epochs,
        seed = Seed
    )
    return dream()

def get_file(txt):
    spl = txt.split()
    GA_file = '_'.join(spl)
    return f"{GA_file}.png"

def save_files(txt):
    spl = txt.split()
    GA_file = '_'.join(spl)
    return shutil.move(f'/content/{GA_file}.png', f'/content/gdrive/MyDrive/GenerativeArt/Images/{GA_file}.png')


st.markdown("# NFT Generator")
st.markdown("## Use Artificial Intelligence to generate your NFT Art collection by describing your image")

tab1, tab2 = st.tabs(["Generate Art", "Mint your NFT"])

with tab1:

    text = st.text_input("Describe your Art here")
    learning_rate = st.text_input("Set to 0.5")
    iterations = st.text_input("For good results, set to 100000")
    epochs = st.text_input("Set to 1")
    seed = st.text_input("Set seed to 5092785 for now")

    if st.button("Generate Art"):
        st.write("This will take a while")
        run_dreams(text, learning_rate, iterations, epochs, seed)
        save_files(text)
        art = get_file(text)
        st.image(art)