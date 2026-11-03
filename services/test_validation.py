from PIL import Image
from io import BytesIO

from utils.image_validator import validate_image
from services.image_processor import process_image


# Create a sample image
sample = Image.new("RGB", (500, 500), "white")

buffer = BytesIO()
sample.save(buffer, format="PNG")
buffer.seek(0)

# Simulate an uploaded file
buffer.name = "sample.png"
buffer.size = len(buffer.getvalue())

# Validate
valid, message = validate_image(buffer)

print("Validation:", message)

# Process
if valid:
    processed = process_image(buffer)
    print("Image processed successfully!")
    print("Image dimensions:", processed.size)