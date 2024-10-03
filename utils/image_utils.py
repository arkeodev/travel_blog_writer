from io import BytesIO

import numpy as np
import requests
from PIL import Image

# Define a custom User-Agent
USER_AGENT = "TravelBlogWriterApp/1.0 (https://github.com/arkeodev/travel_blog_writer; arkeodev@gmail.com) Python/3.9"


def fetch_image(url):
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))


def normalize_image(image_file):
    """
    Resize the image to 224x224 pixels and normalize its pixel values.

    Args:
    image_file: A file-like object containing the image data.

    Returns:
    A numpy array of shape (224, 224, 3) with normalized pixel values.
    """
    # Open the image using PIL
    img = Image.open(image_file)

    # Resize the image to 224x224 pixels
    img_resized = img.resize((224, 224))

    # Convert the image to RGB mode if it's not already
    img_rgb = img_resized.convert("RGB")

    # Convert the image to a numpy array
    img_array = np.array(img_rgb)

    # Normalize the pixel values to the range [0, 1]
    img_normalized = img_array.astype(np.float32) / 255.0

    return img_normalized
