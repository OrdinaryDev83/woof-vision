import os
# Disable TensorFlow warnings and errors
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}

import tensorflow as tf
import tensorflow_datasets as tfds

def download():
    print("[INSTALL] Fetching the dataset ...")
    tfds.load("stanford_dogs")
    print("[INSTALL] Dataset fetched")

if __name__ == "__main__":
    download()