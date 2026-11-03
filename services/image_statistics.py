
from PIL import Image, ImageStat


def calculate_image_statistics(image, file_size, file_format):
    """Calculate measurable properties of an image."""

    rgb_image = image.convert("RGB")
    grayscale = rgb_image.convert("L")
    hsv_image = rgb_image.convert("HSV")

    gray_stats = ImageStat.Stat(grayscale)
    color_stats = ImageStat.Stat(hsv_image)

    width, height = image.size

    return {
        "width": width,
        "height": height,
        "megapixels": round((width * height) / 1_000_000, 2),
        "file_size_kb": round(file_size / 1024, 2),
        "format": file_format,
        "aspect_ratio": round(width / height, 2) if height else 0,
        "brightness": round(gray_stats.mean[0], 2),
        "contrast": round(gray_stats.stddev[0], 2),
        "saturation": round(color_stats.mean[1], 2)
    }
