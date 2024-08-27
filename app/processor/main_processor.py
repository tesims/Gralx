
# main_processor.py
# Main processor to handle different media types for PII masking
from app.processor.text_processor import *


def process_media(media_path: str, media_type: str, api_key: str, data_usage: str, llm_model: str) -> str:
    """
    Process the media file based on its type (text, image, audio, video).
    :param media_path: Path to the media file.
    :param media_type: Type of the media ('text', 'image', 'audio', 'video').
    :return: Path to the processed media file.
    """
    if media_type == 'text': 
        return process_text(media_path, api_key, data_usage, llm_model)
    elif media_type == 'image':
        # Call image processing function
        pass
    elif media_type == 'audio':
        # Call audio processing function
        pass
    elif media_type == 'video':
        # Call video processing function
        pass
    else:
        raise ValueError("Unsupported media type")

