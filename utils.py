from PIL import Image
import numpy as np
import base64
import string
import random
import io


def random_image(width=100, height=50, format='base64'):
    """
    Generate an image from random noise as a placeholder
    """
    image = Image.fromarray(
        np.random.randint(0, 255, size=(height, width, 3)).astype(np.uint8))
    if format == 'image':
        return image
    elif format == 'base64':
        buf = io.BytesIO()
        image.save(buf, format='png')
        return base64.b64encode(buf.getvalue())

def random_string(length=10):
    """
    Generate a random string as a placeholder
    """
    return ''.join(random.choices(string.ascii_lowercase + string.digits,
                                  k=length))
