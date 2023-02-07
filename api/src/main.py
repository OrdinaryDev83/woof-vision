from flask import Flask, request
import tensorflow as tf
import tensorflow_datasets as tfds
import numpy as np
import json
from utils import base64_to_tensor, prepro
import os

api_dir = os.path.join(os.path.dirname(__file__), "..")

# Fetch the dataset from the TensorFlow Datasets Catalog
ds_both, ds_info = tfds.load("stanford_dogs", as_supervised=False, with_info=True)

# Get the class names from the dataset info
classes = ds_info.features["label"].names

# Remove the "n*" prefix from the class names
classes = ["-".join(c.split("-")[1:]) for c in classes]

# Number of classes
n_classes = len(classes)

# Load the TensorFlow model and compile it for performance
model = tf.keras.models.load_model(
    os.path.join(api_dir, "model/model_no_augm.h5"), compile=True
)

# Create the Flask app
app = Flask("Woof Vision")


# Define the route for the prediction
@app.route("/predict", methods=["POST"])
def predict():
    """Make a prediction with the model"""

    # Get the image in base64 from the JSON of the POST request
    data = request.json["image"]

    # Convert the base64 string to a TensorFlow tensor (image)
    image = base64_to_tensor(data)

    # Preprocess the image
    image = prepro(image)

    # Add a batch dimension
    image = np.reshape(image, [1, *image.shape])

    # Make a prediction with the model
    prediction = model.predict(image)[0]

    # Get the 3 best matches my matching the prediction with the classes
    hashmap = {}
    for i, key in enumerate(classes):
        hashmap[key] = prediction[i]
    matches = dict(sorted(hashmap.items(), key=lambda x: -x[1])[:3])

    body = {"prediction": matches}

    # Return the prediction as a JSON
    response = app.response_class(
        response=json.dumps(str(body)), status=200, mimetype="application/json"
    )

    return response


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
