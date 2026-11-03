
from PIL import Image


def process_image(uploaded_file):

    uploaded_file.seek(0)

    image = Image.open(uploaded_file)

    # Convert image into RGB format
    image = image.convert("RGB")

    # Resize large images while preserving proportions
    image.thumbnail((1600, 1600))

    return image
