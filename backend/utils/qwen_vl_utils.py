"""
Local qwen_vl_utils implementation for backend utils
This is a fallback implementation in case the official qwen-vl-utils package is not available
"""

import re
from PIL import Image
import requests
from io import BytesIO
import base64
import os

def process_vision_info(messages):
    """
    Process vision information from messages
    Args:
        messages: List of message dictionaries containing image and text content
    Returns:
        tuple: (image_inputs, video_inputs)
    """
    image_inputs = []
    video_inputs = []
    
    for message in messages:
        if "content" in message:
            for content_item in message["content"]:
                if content_item.get("type") == "image":
                    image_path = content_item.get("image")
                    if image_path:
                        try:
                            # Handle different image input types
                            if isinstance(image_path, str):
                                if image_path.startswith(("http://", "https://")):
                                    # URL image
                                    response = requests.get(image_path)
                                    image = Image.open(BytesIO(response.content))
                                elif image_path.startswith("data:image"):
                                    # Base64 encoded image
                                    header, encoded = image_path.split(",", 1)
                                    image_data = base64.b64decode(encoded)
                                    image = Image.open(BytesIO(image_data))
                                elif os.path.exists(image_path):
                                    # Local file path
                                    image = Image.open(image_path)
                                else:
                                    print(f"Warning: Cannot load image from {image_path}")
                                    continue
                                
                                # Convert to RGB if necessary
                                if image.mode != "RGB":
                                    image = image.convert("RGB")
                                
                                image_inputs.append(image)
                            
                        except Exception as e:
                            print(f"Error processing image {image_path}: {e}")
                            continue
                
                elif content_item.get("type") == "video":
                    # Video processing (not implemented in this basic version)
                    video_path = content_item.get("video")
                    if video_path:
                        print(f"Video input detected but not implemented: {video_path}")
    
    return image_inputs, video_inputs

def load_image(image_path):
    """
    Load image from various sources
    Args:
        image_path: Path to image (local file, URL, or base64)
    Returns:
        PIL Image object
    """
    try:
        if isinstance(image_path, str):
            if image_path.startswith(("http://", "https://")):
                # URL image
                response = requests.get(image_path)
                image = Image.open(BytesIO(response.content))
            elif image_path.startswith("data:image"):
                # Base64 encoded image
                header, encoded = image_path.split(",", 1)
                image_data = base64.b64decode(encoded)
                image = Image.open(BytesIO(image_data))
            elif os.path.exists(image_path):
                # Local file path
                image = Image.open(image_path)
            else:
                raise FileNotFoundError(f"Image not found: {image_path}")
            
            # Convert to RGB if necessary
            if image.mode != "RGB":
                image = image.convert("RGB")
            
            return image
    
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None
