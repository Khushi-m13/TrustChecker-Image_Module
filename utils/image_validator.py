
from PIL import Image, UnidentifiedImageError

ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def validate_image(uploaded_file):
    """Validate uploaded image format, size and integrity."""

    if uploaded_file is None:
        return False, "Please upload an image."

    try:
        uploaded_file.seek(0)
        image_data = uploaded_file.read()
        uploaded_file.seek(0)

        if len(image_data) == 0:
            return False, "The uploaded file is empty."

        if len(image_data) > MAX_FILE_SIZE:
            return False, "Image size must not exceed 5 MB."

        image = Image.open(uploaded_file)

        if image.format not in ALLOWED_FORMATS:
            return False, "Only JPG, PNG and WEBP images are allowed."

        image.verify()

        return True, "Image is valid."

    except (UnidentifiedImageError, OSError, ValueError):
        return False, "Invalid or corrupted image file."

    finally:
        uploaded_file.seek(0)
