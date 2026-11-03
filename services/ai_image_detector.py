
from services.gemini_service import analyze_image_with_gemini


def detect_ai_image(processed_image, language="English"):

    if processed_image is None:
        raise ValueError("No processed image was provided.")

    return analyze_image_with_gemini(
        processed_image,
        language=language
    )
