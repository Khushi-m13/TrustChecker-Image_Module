import os
import json
import streamlit as st

from google import genai
from google.genai import types


LANGUAGES = {
    "English": "English",
    "Hindi": "Hindi",
    "Marathi": "Marathi"
}

AI_ASSESSMENTS = {
    "likely_ai_generated",
    "likely_authentic_photograph",
    "digital_graphic_or_illustration",
    "inconclusive"
}

SCAM_ASSESSMENTS = {
    "likely_scam",
    "suspicious_needs_verification",
    "no_obvious_scam_indicators",
    "insufficient_information"
}


def get_setting(name, default=None):
    value = os.getenv(name)

    if value:
        return value

    try:
        return st.secrets.get(name, default)
    except Exception:
        return default


def get_api_key():
    key = get_setting("GEMINI_API_KEY")

    if not key:
        raise ValueError("Gemini API key is missing.")

    return key


def clean_list(value):
    """Ensure the model returns a list of readable strings."""
    if isinstance(value, list):
        return [str(item) for item in value if item]

    if isinstance(value, str) and value.strip():
        return [value]

    return []


def analyze_image_with_gemini(image, language="English"):

    language = LANGUAGES.get(language, "English")

    prompt = f"""
You are an image analysis assistant for TrustChecker,
a platform that helps users identify potentially misleading
and fraudulent images.

Analyze the uploaded image in {language}.

You MUST perform TWO SEPARATE assessments.

==================================================
PART 1: IMAGE ORIGIN ASSESSMENT
==================================================

Choose exactly one:

- likely_ai_generated
- likely_authentic_photograph
- digital_graphic_or_illustration
- inconclusive

Look for:
- Unnatural textures or repeated patterns.
- Inconsistent lighting and shadows.
- Distorted objects, faces or anatomy.
- Unusual edges and blending.
- Reflections and perspective.
- Digital graphic and illustration characteristics.
- Characteristics commonly found in photographs.

Rules:
- A digital graphic is not automatically AI-generated.
- A photograph is not automatically authentic.
- Artistic style alone is not proof of AI generation.
- Do not invent visual evidence.
- If evidence is insufficient, choose inconclusive.
- Never invent an AI probability percentage.

==================================================
PART 2: POTENTIAL SCAM SCREENING
==================================================

Choose exactly one:

- likely_scam
- suspicious_needs_verification
- no_obvious_scam_indicators
- insufficient_information

Examine the visible image content for:

1. Fake job or internship offers:
   unrealistic salaries, guaranteed jobs, registration fees,
   interview fees or requests for payment.

2. Financial fraud:
   guaranteed returns, investment promises, urgent money
   requests, suspicious loan offers or prize claims.

3. Impersonation:
   misleading use of company names, logos, government
   identities, bank branding or official-looking designs.

4. Suspicious instructions:
   requests to share OTPs, passwords, PINs, bank details
   or personal information.

5. Suspicious contact and payment information:
   visible phone numbers, UPI IDs, payment requests,
   website addresses and QR codes.

6. Manipulative language:
   urgent deadlines, threats, unrealistic rewards,
   pressure to act immediately or claims that sound too good
   to be true.

IMPORTANT SCAM RULES:

- A professional-looking poster is not proof of legitimacy.
- A logo alone cannot verify an organization.
- A payment request is a warning sign, not automatic proof
  of fraud.
- Do not claim a phone number, website, UPI ID or QR code
  is fraudulent unless it has actually been verified.
- Do not invent text, contact details, URLs or QR contents.
- If a QR code is visible but its destination cannot be read,
  explicitly say that it requires separate checking.
- If no suspicious indicators are visible, do not call the
  image safe. Use no_obvious_scam_indicators.
- If the image does not contain enough information, choose
  insufficient_information.
- Explain exactly which visible details caused concern.
- Give practical verification steps to the user.

==================================================
OUTPUT REQUIREMENTS
==================================================

Return ONLY valid JSON in the following structure:

{{
    "assessment": "inconclusive",
    "confidence": "low",
    "summary": "Simple explanation of image origin in {language}",
    "visual_evidence": [],
    "counter_indicators": [],
    "limitations": [],
    "recommendation": "Practical advice",

    "scam_assessment": "insufficient_information",
    "scam_confidence": "low",
    "scam_summary": "Simple explanation of potential scam risk",
    "scam_evidence": [],
    "extracted_text": [],
    "suspicious_elements": [],
    "verification_steps": [],
    "scam_recommendation": "Practical safety advice"
}}

Allowed image-origin assessments:
{sorted(AI_ASSESSMENTS)}

Allowed scam assessments:
{sorted(SCAM_ASSESSMENTS)}

Both confidence fields must be one of:
low, medium, high.

All descriptive text and list items must be in {language}.
Only assessment and confidence values remain in English.

Keep explanations clear, specific and understandable
to an ordinary person.

Do not produce numerical risk percentages.
Do not confuse AI-generated content with scam content.
"""


    primary_model = get_setting(
        "GEMINI_MODEL", "gemini-3.8-flash"
    )

    fallback_model = get_setting(
        "GEMINI_FALLBACK_MODEL", "gemini-3.5-flash-lite"
    )

    models = list(dict.fromkeys([
        primary_model,
        fallback_model
    ]))

    client = genai.Client(api_key=get_api_key())

    errors = []

    try:
        for model in models:
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=[prompt, image],
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.2,
                        max_output_tokens=2500
                    )
                )

                if not response.text:
                    raise ValueError("Empty Gemini response.")

                result = json.loads(response.text)

                # Validate image-origin assessment
                if result.get("assessment") not in AI_ASSESSMENTS:
                    result["assessment"] = "inconclusive"

                # Validate scam assessment
                if result.get("scam_assessment") not in SCAM_ASSESSMENTS:
                    result["scam_assessment"] = "insufficient_information"

                # Validate confidence values
                if result.get("confidence") not in {
                    "low", "medium", "high"
                }:
                    result["confidence"] = "low"

                if result.get("scam_confidence") not in {
                    "low", "medium", "high"
                }:
                    result["scam_confidence"] = "low"

                # Ensure all expected text fields exist
                text_fields = [
                    "summary",
                    "recommendation",
                    "scam_summary",
                    "scam_recommendation"
                ]

                for field in text_fields:
                    if not isinstance(result.get(field), str):
                        result[field] = ""

                # Ensure all expected list fields are lists
                list_fields = [
                    "visual_evidence",
                    "counter_indicators",
                    "limitations",
                    "scam_evidence",
                    "extracted_text",
                    "suspicious_elements",
                    "verification_steps"
                ]

                for field in list_fields:
                    result[field] = clean_list(result.get(field))

                result["language"] = language
                result["model_used"] = model

                return result

            except Exception as error:
                errors.append(f"{model}: {error}")

        raise RuntimeError(
            "Image analysis could not be completed. "
            + " | ".join(errors)
        )

    finally:
        client.close()