import gdown
import os

def download():
    # Called from main.py
    api_dir = os.path.join(os.path.dirname(__file__), "..", "..")

    # Path to the model
    model_dir = os.path.join(api_dir, "model")
    model_path = os.path.join(model_dir, "model_no_augm.h5")

    # Download the model from Google Drive (1.1Gb)
    if not os.path.exists(model_path):
        print("[INSTALL] Model not found, downloading it ...")
        if not os.path.exists(model_dir):
            os.mkdir(model_dir)
        url = str(os.getenv("MODEL_URL"))
        output = model_path
        gdown.download(url, output, quiet=False)
        print("[INSTALL] Model downloaded")
    else:
        print("[INSTALL] Model already downloaded")

if __name__ == "__main__":
    download()