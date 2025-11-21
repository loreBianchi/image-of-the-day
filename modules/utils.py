import os
from datetime import datetime

def generate_unique_filename(base_dir, base_name="news_art", extension=".png"):
    """
    Generates a full, unique file path using date and timestamp.

    Args:
        base_dir (str): Base directory where the file should be saved.
        base_name (str): Base name of the file (e.g., 'news_art').
        extension (str): File extension (e.g., '.png').

    Returns:
        str: The full, unique file path (directory/base_name_YYYYMMDD_HHMMSS.png).
    """
    # Create timestamp: YYYYMMDD_HHMMSS
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{base_name}_{timestamp}{extension}"
    
    # Ensure the directory exists before returning the path
    os.makedirs(base_dir, exist_ok=True)
    
    return os.path.join(base_dir, filename)

def get_text_filepath(image_path):
    """
    Returns the path for the prompt text file, based on the image path.
    Replaces the image extension with '.txt'.
    """
    base, _ = os.path.splitext(image_path)
    return f"{base}.txt"