
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import matplotlib.pyplot as plt
from fuzzywuzzdef detect_id_student(image_path, student_ids, use_ollama=True, show_image=False):
    """
    Detect student ID from image
    Args:
        image_path: Path to image containing student ID
        student_ids: List of known student IDs
        use_ollama: Whether to use Ollama model (default True) or fallback to traditional OCR
        show_image: Whether to display the processed image
    Returns:
        Detected student ID or None
    """
    try:
        # First try with Ollama model
        if use_ollama:
            logger.info(f"Using Ollama model for ID detection: {image_path}")
            result = detect_id_student_ollama(image_path, student_ids)
            if result:
                return result
            else:
                logger.warning("Ollama failed, falling back to traditional OCR")port pytesseract
import re
import numpy as np
import cv2
import re
import easyocr
import os
import uuid
import logging

import logging

# Import Ollama detector functions
from .ollama_detector import detect_name_student_ollama, detect_id_student_ollama

logger = logging.getLogger(__name__)

# Try to import tesseract, but make it optional
try:
    import pytesseract
    # Nếu dùng Windows, cần chỉ rõ đường dẫn tesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    logger.warning("Tesseract not available, will use EasyOCR and Ollama only")

# Khởi tạo easyocr reader một lần
try:
    reader = easyocr.Reader(['vi', 'en'])
    EASYOCR_AVAILABLE = True
except Exception as e:
    logger.warning(f"EasyOCR not available: {e}")
    EASYOCR_AVAILABLE = False

logger = logging.getLogger(__name__)
def detect_name_student(image_path, student_names, use_ollama=True):
    """
    Detect student name from image
    Args:
        image_path: Path to image containing student name
        student_names: List of known student names
        use_ollama: Whether to use Ollama model (default True) or fallback to traditional OCR
    Returns:
        Detected student name or None
    """
    try:
        # First try with Ollama model
        if use_ollama:
            logger.info(f"Using Ollama model for name detection: {image_path}")
            result = detect_name_student_ollama(image_path, student_names)
            if result:
                return result
            else:
                logger.warning("Ollama failed, falling back to traditional OCR")
        
        # Fallback to EasyOCR and other methods (no Tesseract)
        logger.info(f"Using EasyOCR for name detection: {image_path}")
        
        # Try EasyOCR first
        if EASYOCR_AVAILABLE:
            try:
                # Đọc ảnh
                image = cv2.imread(image_path)
                if image is None:
                    print(f"Không thể mở ảnh: {image_path}")
                    return None

                # Cắt phần 2/3 dưới ảnh để focus vào tên
                h = image.shape[0]
                cropped_image = image[h // 3:, :, :]

                # EasyOCR
                results = reader.readtext(cropped_image)
                text = ' '.join([result[1] for result in results])
                
                print(f"EasyOCR extracted text: {text}")
                
                # So khớp fuzzy
                if text.strip():
                    matched = process.extractOne(text.strip(), student_names)
                    if matched and matched[1] >= 60:
                        print(f"Khớp với: {matched[0]} (Điểm tương đồng: {matched[1]})")
                        return matched[0]
                
            except Exception as e:
                logger.error(f"EasyOCR failed: {e}")
        
        # Fallback to Tesseract if available
        if TESSERACT_AVAILABLE:
            try:
                # Đọc ảnh và chuyển sang RGB
                image = cv2.imread(image_path)
                if image is None:
                    print(f"Không thể mở ảnh: {image_path}")
                    return None

                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # Cắt phần 2/3 dưới ảnh
                h = image.shape[0]
                cropped_image = image_rgb[h // 3:, :, :]

                # OCR tiếng Việt
                text = pytesseract.image_to_string(cropped_image, lang='vie')
                print(f"Tesseract extracted text: {text}")

                # So khớp fuzzy
                if text.strip():
                    matched = process.extractOne(text.strip(), student_names)
                    if matched and matched[1] >= 60:
                        print(f"Khớp với: {matched[0]} (Điểm tương đồng: {matched[1]})")
                        return matched[0]
                        
            except Exception as e:
                logger.error(f"Tesseract failed: {e}")
        
        logger.warning("All OCR methods failed for name detection")
        return None
        
    except Exception as e:
        logger.error(f"Error in detect_name_student: {e}")
        return None


# Load model và processor 1 lần khi import (only if TrOCR is needed)
try:
    processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten', use_fast=True)
    model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')
    TROCR_AVAILABLE = True
except Exception as e:
    logger.warning(f"TrOCR not available: {e}")
    TROCR_AVAILABLE = False

model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')
def detect_id_student(image_path, student_ids, use_qwen=True, show_image=False):
    """
    Detect student ID from image
    Args:
        image_path: Path to image containing student ID
        student_ids: List of known student IDs
        use_qwen: Whether to use Qwen model (default True) or fallback to traditional OCR
        show_image: Whether to show the image for debugging
    Returns:
        Detected student ID or None
    """
    try:
        # First try with Qwen model
        if use_qwen:
            logger.info(f"Using Qwen model for ID detection: {image_path}")
            result = detect_id_student_qwen(image_path, student_ids)
            if result:
                return result
            else:
                logger.warning("Qwen failed, falling back to traditional OCR")
        
        # Fallback to TrOCR method if available
        if TROCR_AVAILABLE:
            try:
                logger.info(f"Using TrOCR for ID detection: {image_path}")
                # Mở ảnh và chuyển sang RGB
                image = Image.open(image_path).convert("RGB")

                # Tiền xử lý ảnh
                pixel_values = processor(images=image, return_tensors="pt").pixel_values

                # Sinh text từ model
                generated_ids = model.generate(pixel_values)
                generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

                print("TrOCR detected text:", generated_text)

                # Lọc ra chỉ chữ in hoa và số
                filtered_text = ''.join(re.findall(r'[A-Z0-9]', generated_text))
                print("Filtered text (uppercase letters and numbers only):", filtered_text)

                # So khớp với danh sách MSSV
                if filtered_text.strip():
                    matched_text = process.extractOne(filtered_text, student_ids)
                    if matched_text and matched_text[1] >= 60:
                        print("Matched student ID:", matched_text[0], "with similarity score:", matched_text[1])
                        return matched_text[0]
                        
            except Exception as e:
                logger.error(f"TrOCR failed: {e}")
        
        # Try EasyOCR fallback for ID
        if EASYOCR_AVAILABLE:
            try:
                image = cv2.imread(image_path)
                if image is not None:
                    results = reader.readtext(image)
                    text = ' '.join([result[1] for result in results])
                    
                    # Extract potential IDs
                    import re
                    numbers = re.findall(r'\d+', text)
                    candidate_ids = [num for num in numbers if 6 <= len(num) <= 12]
                    
                    if candidate_ids:
                        student_ids_str = [str(sid) for sid in student_ids]
                        for candidate in candidate_ids:
                            matched = process.extractOne(candidate, student_ids_str)
                            if matched and matched[1] >= 60:
                                return matched[0]
            except Exception as e:
                logger.error(f"EasyOCR fallback failed: {e}")
                
        logger.warning("All ID detection methods failed")
        return None
        
    except Exception as e:
        logger.error(f"Error in detect_id_student: {e}")
        return None

def detect_index_student(image_path):
    """
    Detect student index/STT from image
    Args:
        image_path: Path to image containing student index
    Returns:
        Detected index string or None
    """
    try:
        if EASYOCR_AVAILABLE:
            results = reader.readtext(image_path, detail=0)
            if results:
                # Join all detected text
                text = ' '.join(results)
                # Extract numbers (STT is usually numeric)
                import re
                numbers = re.findall(r'\d+', text)
                if numbers:
                    # Return the first reasonable number (usually 1-3 digits for STT)
                    for num in numbers:
                        if 1 <= len(num) <= 3:
                            return num
        
        logger.warning(f"Could not detect index from {image_path}")
        return None
        
    except Exception as e:
        logger.error(f"Error detecting index: {e}")
        return None
    combined = ' '.join(result)

    # Tìm các số có 1 hoặc 2 chữ số
    numbers = re.findall(r'\b\d{1,2}\b', combined)

    if numbers:
        print(f"[{os.path.basename(image)}] ➜ {' '.join(numbers)}")
    else:
        print(f"[{os.path.basename(image)}] ➜ Không tìm thấy số")

    return numbers
# path = 'IMG_001.png'
# print(detect_index_student(path))
    # model = load_model('models/mnist_model.keras')
    # # Chuyển đổi hình ảnh sang màu xám
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # # Ngưỡng hóa hình ảnh
    # _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    # # Tìm các contours
    # contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # digits = []
    # for cnt in contours:
    #     # Tính bounding box cho mỗi contour
    #     x, y, w, h = cv2.boundingRect(cnt)
    #     # Lọc các bounding box nhỏ
    #     if w > 5 and h > 5:
    #         digit = thresh[y:y + h, x:x + w]
    #         # Resize về kích thước 28x28
    #         digit = cv2.resize(digit, (28, 28))
    #         digits.append(digit)
    # predictions = []
    # for digit in digits:
    #     digit = digit.reshape((1, 28, 28, 1)).astype('float32') / 255  # Tiền xử lý
    #     pred = model.predict(digit)
    #     predictions.append(np.argmax(pred))
    # return predictions



# image_path = 'temp/test/id_bounding_box.jpg'
# combined_part_3_5, combined_part_6_8 = divide_image(image_path)
#
# detect_name_student(image_path)
# detect_id_student(combined_part_3_5)
# detect_index_student(combined_part_6_8)