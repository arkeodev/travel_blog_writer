import base64
import io
from io import BytesIO

import numpy as np
import requests
from PIL import Image

from constants import IMAGE_SIZE

# Define a custom User-Agent
USER_AGENT = "TravelBlogWriterApp/1.0 (https://github.com/arkeodev/travel_blog_writer; arkeodev@gmail.com) Python/3.9"


def fetch_image(url):
    """
    Fetch an image from a URL and return a PIL Image object.

    Args:
    url: The URL of the image to fetch.

    Returns:
    A PIL Image object.
    """
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))


def resize_image(image_file):
    """
    Resize the image to IMAGE_SIZE x IMAGE_SIZE pixels and normalize its pixel values.

    Args:
    image_file: A file-like object containing the image data.

    Returns:
    A numpy array of shape (IMAGE_SIZE, IMAGE_SIZE, 3) with normalized pixel values.
    """
    # Open the image using PIL
    img = Image.open(image_file)
    # Resize the image to IMAGE_SIZE x IMAGE_SIZE pixels
    img_resized = img.resize((IMAGE_SIZE, IMAGE_SIZE))
    # Convert the image to RGB mode if it's not already
    img_rgb = img_resized.convert("RGB")
    # Convert the image to a numpy array
    img_array = np.array(img_rgb)

    return img_array.astype(np.float32)


def numpy_to_base64(image_data):
    """
    Convert a numpy array to a base64 encoded image.

    Args:
    image_data: A numpy array of shape (IMAGE_SIZE, IMAGE_SIZE, 3) with normalized pixel values.

    Returns:
    A base64 encoded image string.
    """
    img = Image.fromarray((image_data).astype(np.uint8))
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return img_str
