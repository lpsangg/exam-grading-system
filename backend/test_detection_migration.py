#!/usr/bin/env python3
"""
Test script cho các hàm detection đã migrate sang Ollama
"""

import sys
import os

# Thêm đường dẫn để import các module utils
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from detectInfo import detect_name_student, detect_id_student, detect_index_student

def test_detection_functions():
    """Test cả 3 hàm detection với Ollama"""
    
    # Đường dẫn ảnh test (thay đổi theo ảnh có sẵn)
    test_image = "utils/IMG_031.jpg"
    
    if not os.path.exists(test_image):
        print(f"Không tìm thấy ảnh test: {test_image}")
        print("Vui lòng cung cấp đường dẫn ảnh test hợp lệ")
        return
    
    print("=== TEST OLLAMA DETECTION FUNCTIONS ===\n")
    
    # Test data mẫu
    sample_student_names = [
        "Nguyễn Văn An", 
        "Trần Thị Bình", 
        "Phạm Hoàng Quốc Anh",
        "Lê Minh Cường"
    ]
    
    sample_student_ids = [
        "2100738", 
        "2100739", 
        "2100740", 
        "2100741"
    ]
    
    # Test 1: detect_name_student
    print("1. Testing detect_name_student với Ollama...")
    try:
        name_result = detect_name_student(test_image, sample_student_names)
        print(f"Kết quả nhận diện tên: {name_result}")
    except Exception as e:
        print(f"Lỗi trong detect_name_student: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 2: detect_id_student
    print("2. Testing detect_id_student với Ollama...")
    try:
        id_result = detect_id_student(test_image, sample_student_ids, show_image=False)
        print(f"Kết quả nhận diện MSSV: {id_result}")
    except Exception as e:
        print(f"Lỗi trong detect_id_student: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 3: detect_index_student
    print("3. Testing detect_index_student với Ollama...")
    try:
        index_result = detect_index_student(test_image)
        print(f"Kết quả nhận diện index: {index_result}")
    except Exception as e:
        print(f"Lỗi trong detect_index_student: {e}")
    
    print("\n=== HOÀN THÀNH TEST ===")

if __name__ == "__main__":
    test_detection_functions()
