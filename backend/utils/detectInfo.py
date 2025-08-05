
import ollama
from PIL import Image
import matplotlib.pyplot as plt
from fuzzywuzzy import process
import re
import numpy as np
import cv2
import os
import uuid
import base64
import io
import json

def image_to_base64(image):
    """Chuyển đổi ảnh PIL hoặc numpy array thành base64"""
    if isinstance(image, np.ndarray):
        # Nếu là numpy array, chuyển sang PIL Image
        image = Image.fromarray(image)
    
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

def query_ollama_vision(image_base64, prompt):
    """Gửi query đến Ollama với vision model"""
    try:
        response = ollama.chat(
            model='qwen2.5vl:3b',
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': [image_base64]
            }]
        )
        return response['message']['content']
    except Exception as e:
        print(f"Lỗi khi gọi Ollama: {e}")
        return ""
def detect_name_student(image_path, student_names):
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

        # # Hiển thị phần ảnh được cắt (tuỳ chọn)
        # plt.imshow(cropped_image)
        # plt.axis('off')
        # plt.title('Phần ảnh được cắt')
        # plt.show()

        # Chuyển đổi sang base64 để gửi cho Ollama
        image_base64 = image_to_base64(cropped_image)
        
        # Prompt cho nhận diện tên sinh viên tiếng Việt
        prompt = """Hãy đọc và trích xuất tên sinh viên từ ảnh này. Ảnh này là phần của một tờ bài thi có chứa thông tin sinh viên.
Chỉ trả về tên sinh viên, không thêm bất kỳ thông tin nào khác. Nếu có dấu tiếng Việt, hãy giữ nguyên."""
        
        # OCR bằng Ollama/Qwen
        text = query_ollama_vision(image_base64, prompt)
        print(f"Văn bản OCR nhận diện được:\n{text}")


        # So khớp fuzzy
        if text.strip():
            matched = process.extractOne(text.strip(), student_names)
            if matched:
                print(f"Khớp với: {matched[0]} (Điểm tương đồng: {matched[1]})")
                return matched[0]
            else:
                print("Không tìm thấy tên phù hợp.")
                return None
        else:
            print("Không nhận diện được văn bản.")
            return None

    except Exception as e:
        print("Lỗi:", e)
        return None


def detect_id_student(image_path, student_ids, show_image=False):
    try:
        # Mở ảnh và chuyển sang RGB
        image = Image.open(image_path).convert("RGB")

        # Hiển thị ảnh nếu cần
        if show_image:
            plt.imshow(image)
            plt.axis('off')
            plt.title('Input Image: ' + image_path)
            plt.show()

        # Chuyển đổi sang base64 để gửi cho Ollama
        image_base64 = image_to_base64(image)
        
        # Prompt cho nhận diện mã số sinh viên (chữ viết tay)
        prompt = """Hãy đọc và trích xuất mã số sinh viên từ ảnh này. Mã số sinh viên thường là dãy số có 7-10 chữ số.
Chỉ trả về mã số sinh viên, không thêm bất kỳ thông tin nào khác. Ví dụ: 2100738"""
        
        # OCR bằng Ollama/Qwen
        generated_text = query_ollama_vision(image_base64, prompt)

        print("Initial text detected for image", image_path, ":", generated_text)


        # So khớp với danh sách MSSV
        if generated_text.strip():
            matched_text = process.extractOne(generated_text, student_ids)
            if matched_text:
                print("Matched student ID:", matched_text[0], "with similarity score:", matched_text[1])
                return matched_text[0]
            else:
                print("No good match found.")
                return None
        else:
            print("No valid text found.")
            return None

    except Exception as e:
        print("Error in detect_id_student:", str(e))
        return None

def detect_index_student(image):
    try:
        # Đọc ảnh (nếu là đường dẫn) hoặc sử dụng trực tiếp (nếu là numpy array)
        if isinstance(image, str):
            # Nếu là đường dẫn file
            img = cv2.imread(image)
            if img is None:
                print(f"Không thể mở ảnh: {image}")
                return []
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        else:
            # Nếu là numpy array
            img_rgb = image

        # Chuyển đổi sang base64 để gửi cho Ollama
        image_base64 = image_to_base64(img_rgb)
        
        # Prompt cho nhận diện số thứ tự/index
        prompt = """Hãy đọc và trích xuất các số thứ tự từ ảnh này. Tìm các số có 1 hoặc 2 chữ số.
Chỉ trả về các số được tìm thấy, cách nhau bằng dấu cách. Ví dụ: 1 23 4"""
        
        # OCR bằng Ollama/Qwen
        result_text = query_ollama_vision(image_base64, prompt)
        
        # Tìm các số có 1 hoặc 2 chữ số từ kết quả
        numbers = re.findall(r'\b\d{1,2}\b', result_text)

        image_name = os.path.basename(image) if isinstance(image, str) else "image_array"
        if numbers:
            print(f"[{image_name}] ➜ {' '.join(numbers)}")
        else:
            print(f"[{image_name}] ➜ Không tìm thấy số")

        return numbers
        
    except Exception as e:
        print(f"Lỗi trong detect_index_student: {e}")
        return []
