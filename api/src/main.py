from flask import Flask, request
import tensorflow as tf
import tensorflow_datasets as tfds
import numpy as np
from vit_keras.vit import preprocess_inputs
import base64
import json

ds_both, ds_info = tfds.load("stanford_dogs", as_supervised=False, with_info=True)

classes = ds_info.features['label'].names
classes = ['-'.join(c.split('-')[1:]) for c in classes]

n_classes = len(classes)

ds_train, ds_test = ds_both["train"], ds_both["test"]

def prepro(img):
    img = tf.cast(img, dtype=tf.float32)
    img = preprocess_inputs(img)
    img = tf.image.resize(img, [256, 256])
    
    return img

app = Flask("Dog Vision")

# Load your TensorFlow model
model = tf.keras.models.load_model("model_no_augm.h5", compile=True)

print("Started Web API")

def base64_to_tensor(base64_string):
  # Decode the base64 string to binary data
  image_binary = base64.b64decode(base64_string)

  # Convert the binary data to a TensorFlow tensor
  image_tensor = tf.image.decode_image(image_binary)

  return image_tensor


@app.route("/predict", methods=["POST"])
def predict():
    # Get the image from the GET request
    data = request.json["image"]
    image = base64_to_tensor(data)
    
    # Preprocess the image
    image = prepro(image)
    image = np.reshape(image, [1, *image.shape])
    
    # Make a prediction with the model
    prediction = model.predict(image)[0]

    hashmap = {}
    for i, key in enumerate(classes):
        hashmap[key] = prediction[i]
    matches = dict(sorted(hashmap.items(), key=lambda x:-x[1])[:3]) # 3 best matches
    
    res = { "prediction": matches }
    
    response = app.response_class(
        response=json.dumps(str(res)),
        status=200,
        mimetype='application/json'
    )

    return response

if __name__ == "__main__":
    app.run(debug=True)