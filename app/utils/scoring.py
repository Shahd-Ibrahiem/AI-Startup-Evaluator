import re

def extract_score(text: str) -> int:
    """
    Extracts investment score (0–100) from LLM output
    """

    match = re.search(r"(\d{1,3})\s*/\s*100", text)

    if match:
        return int(match.group(1))

    # fallback if model doesn't format correctly
    return 50