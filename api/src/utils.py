from vit_keras import vit
import base64
import tensorflow as tf

def prepro(img):
    """Preprocess the image to be compatible with the model"""
    img = tf.cast(img, dtype=tf.float32)
    img = vit.preprocess_inputs(img)
    img = tf.image.resize(img, [256, 256])

    return img


def base64_to_tensor(base64_string):
    """Convert a base64 string to a TensorFlow tensor image"""
    # Decode the base64 string to binary data
    image_binary = base64.b64decode(base64_string)

    # Convert the binary data to a TensorFlow tensor
    image_tensor = tf.image.decode_image(image_binary)

    return image_tensor
