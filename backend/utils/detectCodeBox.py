import cv2
import pytesseract
import numpy as np
import matplotlib.pyplot as plt
import re  # Thêm thư viện re để sử dụng biểu thức chính quy

# Cấu hình đường dẫn tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def detect_code_box(image_path):
    # Đọc ảnh từ đường dẫn
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Dùng OCR nhận diện nội dung
    text = pytesseract.image_to_string(gray, config="--psm 6 digits")

    # Sử dụng biểu thức chính quy để tìm tất cả các số trong văn bản
    numbers = re.findall(r'\d+', text)  # Tìm tất cả các chuỗi số

    # Nếu có số, in ra và trả về số đầu tiên
    if numbers:
        detected_number = numbers[0]  # Lấy số đầu tiên
        # print("Detected number:", detected_number)
        return detected_number  # Trả về số đầu tiên
    else:
        print("No numbers detected.")
        return None  # Trả về None nếu không tìm thấy số

    # # Hiển thị kết quả
    # plt.figure(figsize=(10, 6))
    # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # plt.title("Detected Exam Code Box")
    # plt.axis("off")
    # plt.show()

# Ví dụ gọi hàm
# final_number = detect_code_box('path_to_your_image.jpg')
