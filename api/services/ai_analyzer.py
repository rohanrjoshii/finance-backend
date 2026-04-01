from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

def analyze_document(file_bytes: bytes, mime_type: str) -> str:
    """
    Leverages Gemini Flash to quickly process a financial PDF or CSV using direct byte injection.
    Requires GEMINI_API_KEY environment variable.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return (
            "### ⚠️ AI Engine Offline\n\n"
            "The system is missing the `GEMINI_API_KEY` environment variable. "
            "Please configure the backend environment to enable deep financial analysis."
        )

    client = genai.Client(api_key=api_key)
    
    prompt = (
        "You are an expert Financial Analyst. Analyze the following uploaded financial report. "
        "1. Provide a concise 'Overall Summary' at the top.\n"
        "2. Extract exactly every financial piece of information that is important for a person to know.\n"
        "3. Look for anomalies, spending trends, or distinct risks.\n"
        "Please format the entire response in clean, beautiful Markdown with headers, bullet points, and bold text for numbers."
    )

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part.from_bytes(data=file_bytes, mime_type=mime_type),
                prompt
            ]
        )
        return response.text
    except Exception as e:
        return f"### Analysis Error\nFailed to process the requested document: {str(e)}"
