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
    GA_file = get_file(txt)
    return shutil.move(f'/content/{GA_file}', f'/content/gdrive/MyDrive/GenerativeArt/Images/{GA_file}.png')
