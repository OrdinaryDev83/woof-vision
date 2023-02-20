import os
# Disable TensorFlow warnings and errors
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # or any {'0', '1', '2'}

from flask import Flask, request
import tensorflow as tf
import tensorflow_datasets as tfds
import numpy as np
from .utils import base64_to_tensor, prepro
from flask import jsonify
from .install.install_model import download as download_model

# Create the Flask app
app = Flask(__name__)

print("[WOOFVISION] App created")

api_dir = os.path.join(os.path.dirname(__file__), "..")

# Fetch the dataset from the TensorFlow Datasets Catalog
print("[WOOFVISION] Fetching the dataset ...")
ds_both, ds_info = tfds.load("stanford_dogs", as_supervised=False, with_info=True)
print("[WOOFVISION] Dataset fetched")

# Get the class names from the dataset info
classes = ds_info.features["label"].names

# Remove the "n*" prefix from the class names
classes = ["-".join(c.split("-")[1:]) for c in classes]

# Number of classes
n_classes = len(classes)

# Path to the model
model_dir = os.path.join(api_dir, "model")
model_path = os.path.join(model_dir, "model_no_augm.h5")

# Download the model from Google Drive (1.1Gb)
download_model()

# Load the TensorFlow model and compile it for performance
print("[WOOFVISION] Loading model ...")
model = tf.keras.models.load_model(model_path)
print("[WOOFVISION] Model loaded")
print("[WOOFVISION] Listening ...")

# Define the route for the prediction
@app.route("/predict", methods=["POST"])
def predict():
    """Make a prediction with the model"""
    print("[WOOFVISION] [REQUEST]", str(request.json)[:100], "...")

    # Get the image in base64 from the JSON of the POST request
    if request.json is None or "image" not in request.json:
        return "No image in the request", 400
    split = request.json["image"].split(",")
    data = split[min(1, len(split) - 1)]
    print("[WOOFVISION] [IMAGE]", data[:100], "...")

    try:
        # Convert the base64 string to a TensorFlow tensor (image)
        image = base64_to_tensor(data)
        
        # Preprocess the image
        image = prepro(image)

        # Add a batch dimension
        image = np.reshape(image, [1, *image.shape])
    except Exception as error:
        print("[WOOFVISION]", error)
        return "Invalid image", 400

    try:
        # Make a prediction with the model
        prediction = model.predict(image)[0]

        # Get the 3 best matches my matching the prediction with the classes
        hashmap = {}
        for i, key in enumerate(classes):
            hashmap[key] = prediction[i]
        matches = dict(sorted(hashmap.items(), key=lambda x: -x[1])[:3])

        # convert float32 to float
        for k, v in matches.items():
            matches[k] = float(v)
            
        body = { "prediction" : matches }

        print("[WOOFVISION] [RESPONSE]", str(body))

        return jsonify(body)
    except Exception as error:
        print("[WOOFVISION]", error)
        return "Error while making the prediction", 500


# Run the app
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)