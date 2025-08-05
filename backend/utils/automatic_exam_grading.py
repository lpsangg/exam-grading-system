# --------------------Image Processing--------------------
import cv2
import numpy as np
import os
import pandas as pd
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import matplotlib.pyplot as plt
from fuzzywuzzy import process
import pytesseract
import re
import easyocr
import uuid
from collections import Counter
from ultralytics import YOLO

def divide_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Không thể đọc ảnh:", image_path)
        return None, None

    height, width = image.shape[:2]
    part_height = height // 8

    # Gộp các phần thứ 3, 4, 5
    part_3 = image[2 * part_height:3 * part_height, :]
    part_4 = image[3 * part_height:4 * part_height, :]
    part_5 = image[4 * part_height:5 * part_height, :]
    id_student = np.vstack((part_3, part_4, part_5))

    # Gộp các phần thứ 6, 7, 8
    part_6 = image[5 * part_height:6 * part_height, :]
    part_7 = image[6 * part_height:7 * part_height, :]
    part_8 = image[7 * part_height:8 * part_height, :]
    index_student = np.vstack((part_6, part_7, part_8))

    return id_student, index_student


def image_processing(path):
    """
    Xử lý ảnh bài thi để cắt các vùng: mã đề, tên, phiếu thi, mã SV, STT.
    Trả về đường dẫn các vùng cắt và tọa độ vùng phiếu thi.

    Args:
        path (str): Đường dẫn đến ảnh gốc.

    Returns:
        dict:
            - paths: Dictionary chứa đường dẫn các vùng cắt.
            - grading_box: Tuple (x, y, w, h) của vùng phiếu thi.
    """
    # Kiểm tra xem tệp có tồn tại không
    if not os.path.exists(path):
        print(f"Tệp không tồn tại: {path}")
        return {'paths': {}, 'grading_box': None}

    # Đọc hình ảnh
    image = cv2.imread(path)
    if image is None:
        print("Không thể đọc hình ảnh. Kiểm tra lại đường dẫn hoặc định dạng tệp.")
        return {'paths': {}, 'grading_box': None}

    # Tạo thư mục mới trong thư mục temp
    base_temp_dir = './uploads/images/temp'
    if not os.path.exists(base_temp_dir):
        os.makedirs(base_temp_dir)

    # Tạo tên thư mục dựa trên tên tệp ảnh
    image_name = os.path.basename(path).split('.')[0]
    temp_dir = os.path.join(base_temp_dir, image_name)
    os.makedirs(temp_dir, exist_ok=True)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect edges
    edges = cv2.Canny(gray, 50, 150)

    # Detect lines
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=10, minLineLength=500, maxLineGap=50)

    # Variable to store the longest line
    longest_line = None
    max_length = 0

    # Find the longest line
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)  # Calculate the length of the line
            if length > max_length:
                max_length = length
                longest_line = (x1, y1, x2, y2)

    # Rotate the image if the longest line is found
    if longest_line is not None:
        x1, y1, x2, y2 = longest_line
        angle = np.arctan2(y2 - y1, x2 - x1) * 180.0 / np.pi  # Calculate the angle of inclination

        # Rotate the image
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1)
        rotated = cv2.warpAffine(image, M, (w, h))
        white_background = np.ones((h, w, 3), dtype=np.uint8) * 127
        result = np.where(rotated == 0, white_background, rotated)
        # Use the rotated image for further processing
        image = result
    else:
        print("No lines found.")

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Enhance contrast
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    # Blur to reduce noise
    blurred = cv2.GaussianBlur(enhanced, (5, 5), 0)
    # Binarization
    binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get the dimensions of the image
    height, width = image.shape[:2]

    # Calculate the size of each cell
    cell_height = height // 3
    cell_width = width // 3

    # Create a copy of the original image to draw rectangles
    image_with_rectangles = image.copy()

    # Define the top-left cell boundaries
    x_start = 0
    y_start = 0
    x_end = cell_width
    y_end = cell_height

    # List to store bounding boxes in the top-left cell
    bounding_boxes = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if x < x_end and y < y_end:  # Check if the contour is in the top-left cell
            bounding_boxes.append((x, y, w, h))

    # Calculate the diagonal lengths and store them with their bounding boxes
    diagonal_boxes = []
    for (x, y, w, h) in bounding_boxes:
        diagonal = np.sqrt(w ** 2 + h ** 2)  # Calculate the diagonal length
        diagonal_boxes.append((diagonal, (x, y, w, h)))

    # Sort the boxes by diagonal length in descending order
    diagonal_boxes.sort(key=lambda box: box[0], reverse=True)

    # Keep only the largest and second largest bounding boxes
    largest_box = diagonal_boxes[0] if diagonal_boxes else None  # Largest box
    second_largest_box = None

    # Check for the second largest box that is approximately square
    for diagonal, (x, y, w, h) in diagonal_boxes[1:]:
        aspect_ratio = float(w) / h
        if 0.8 < aspect_ratio < 1.2:  # Adjust the aspect ratio range for square-like boxes
            second_largest_box = (diagonal, (x, y, w, h))
            break

    paths = {}

    # Draw the largest bounding box in green if found (Name + id student)
    if largest_box:
        # Unpack the largest bounding box coordinates and dimensions
        _, (x, y, w, h) = largest_box

        # Extract the region of interest (ROI) from the image using the bounding box coordinates
        infor_student = image[y:y + h, x:x + w]

        # Save the extracted region of interest as an image
        infor_path = os.path.join(temp_dir, "infor_student_bounding_box.jpg")
        cv2.imwrite(infor_path, infor_student)
        paths['infor_student'] = infor_path

        # Draw the largest rectangle on the image with green color
        cv2.rectangle(image_with_rectangles, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Get the dimensions of the extracted region of interest
        height, width, _ = infor_student.shape

        # Calculate the size of each part in a 2x2 grid
        grid_height = height // 2
        grid_width = int(width // 3.5)

        # Extract the top-left region of the grid from infor_student
        name_student = infor_student[0:grid_height, 0:grid_width]

        name_path = os.path.join(temp_dir, "name_bounding_box.jpg")
        cv2.imwrite(name_path, name_student)
        paths['name'] = name_path

        # Extract the bottom-left region of the grid from infor_student
        id_student = infor_student[grid_height:height, 0:grid_width]

        id_path = os.path.join(temp_dir, "id_bounding_box.jpg")
        cv2.imwrite(id_path, id_student)
        paths['id_bounding_box'] = id_path

        id_student_part, index_student_part = divide_image(id_path)

        if id_student_part is not None and index_student_part is not None:
            id_student_path = os.path.join(temp_dir, "id_student.jpg")
            index_student_path = os.path.join(temp_dir, "index_student.jpg")
            cv2.imwrite(id_student_path, id_student_part)
            cv2.imwrite(index_student_path, index_student_part)
            paths['id_student'] = id_student_path
            paths['index_student'] = index_student_path
        else:
            print("Không thể chia ảnh id_bounding_box.jpg")

    # Draw the second largest bounding box in blue if found (code box)
    if second_largest_box:
        _, (x, y, w, h) = second_largest_box
        code_box = image[y:y + h, x:x + w]
        code_path = os.path.join(temp_dir, "code_box_bounding_box.jpg")
        cv2.imwrite(code_path, code_box)
        paths['code_box'] = code_path
        cv2.rectangle(image_with_rectangles, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Select the largest contour (assuming it's the main table)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    largest_contour = contours[0] if contours else None

    grading_box = None
    if largest_contour is not None:
        # Find the bounding box around the largest contour
        x, y, w, h = cv2.boundingRect(largest_contour)

        # Extract and save the bounding box around the largest contour
        table_grading = image[y:y + h, x:x + w]
        grading_path = os.path.join(temp_dir, "table_grading_bounding_box.jpg")
        cv2.imwrite(grading_path, table_grading)
        paths['table_grading'] = grading_path
        cv2.rectangle(image_with_rectangles, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Lưu tọa độ vùng phiếu thi
        grading_box = (x, y, w, h)

    return {'paths': paths, 'grading_box': grading_box}


# Detection CodeBox


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

# --------------------Detect Information Student--------------------
# Nếu dùng Windows, cần chỉ rõ đường dẫn tesseract
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Khởi tạo easyocr reader một lần
reader = easyocr.Reader(['vi'])
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

        # OCR tiếng Việt
        text = pytesseract.image_to_string(cropped_image, lang='vie')
        print(f"Văn bản OCR nhận diện được:\n{text}")

        # Lọc ký tự để debug (chỉ lấy A-Z và số)
        filtered_text = ''.join(re.findall(r'[A-Z0-9]', text.upper()))
        print(f"Văn bản đã lọc (chỉ A-Z0-9): {filtered_text}")

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


# Load model và processor 1 lần khi import
processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten', use_fast=True)

model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')
def detect_id_student(image_path, student_ids, show_image=False):
    try:
        # Mở ảnh và chuyển sang RGB
        image = Image.open(image_path).convert("RGB")

        # Tiền xử lý ảnh
        pixel_values = processor(images=image, return_tensors="pt").pixel_values

        # Sinh text từ model
        generated_ids = model.generate(pixel_values)
        generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        # Hiển thị ảnh nếu cần
        if show_image:
            plt.imshow(image)
            plt.axis('off')
            plt.title('Input Image: ' + image_path)
            plt.show()

        print("Initial text detected for image", image_path, ":", generated_text)

        # Lọc ra chỉ chữ in hoa và số
        filtered_text = ''.join(re.findall(r'[A-Z0-9]', generated_text))
        print("Filtered text (uppercase letters and numbers only):", filtered_text)

        # So khớp với danh sách MSSV
        if filtered_text.strip():
            matched_text = process.extractOne(filtered_text, student_ids)
            if matched_text:
                print("Matched student ID:", matched_text[0], "with similarity score:", matched_text[1])
                return matched_text[0]
            else:
                print("No good match found.")
                return None, 0
        else:
            print("No valid text found.")
            return None, 0

    except Exception as e:
        print("Error in detect_id_student:", str(e))
        return None, 0

def detect_index_student(image):
    result = reader.readtext(image, detail=0)
    combined = ' '.join(result)

    # Tìm các số có 1 hoặc 2 chữ số
    numbers = re.findall(r'\b\d{1,2}\b', combined)

    if numbers:
        print(f"[{os.path.basename(image)}] ➜ {' '.join(numbers)}")
    else:
        print(f"[{os.path.basename(image)}] ➜ Không tìm thấy số")

    return numbers

# --------------------Detect Grade--------------------


def predict_grade(path_image, model_path = r"F:\KHMT0121\Do_An_4\Resource\AuGrad\models\final_model.pt"):
    """
    Xử lý ảnh bảng chấm điểm, lưu kết quả đè lên ảnh đầu vào và trả về mảng kết quả ký tự.

    Args:
        path_image (str): Đường dẫn tới ảnh đầu vào, cũng là nơi lưu ảnh kết quả.
        model_path (str): Đường dẫn tới mô hình YOLO (mặc định: /content/final_model.pt).

    Returns:
        tuple: (path_image, student_result)
            - path_image (str): Đường dẫn tới ảnh kết quả đã lưu (đè lên ảnh đầu vào).
            - student_result (dict): Mảng chứa các ký tự từ 1 đến 60.
    """
    # Load mô hình
    model = YOLO(model_path)

    # Đọc ảnh và chuyển màu
    img = cv2.imread(path_image)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Dự đoán bằng YOLO
    results = model.predict(source=img, save=False, conf=0.25)
    boxes = results[0].boxes.xyxy.cpu().numpy()
    cls_ids = results[0].boxes.cls.cpu().numpy().astype(int)
    confidences = results[0].boxes.conf.cpu().numpy()
    names = results[0].names
    labels = [names[i] for i in cls_ids]

    # Tính center cho mỗi bounding box
    centers = []
    for box in boxes:
        x1, y1, x2, y2 = box
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        centers.append([center_x, center_y])
    centers = np.array(centers)

    # Hàm tính khoảng cách
    def is_near(center1, center2, threshold=20):
        return np.linalg.norm(np.array(center1) - np.array(center2)) <= threshold

    # Gom nhóm các box gần nhau
    def group_nearby_boxes(boxes, labels, centers, confidences, threshold=20):
        groups = []
        used = set()
        for i in range(len(centers)):
            if i in used:
                continue
            group = [(boxes[i], labels[i], centers[i], confidences[i])]
            used.add(i)
            for j in range(i + 1, len(centers)):
                if j in used:
                    continue
                if is_near(centers[i], centers[j], threshold):
                    group.append((boxes[j], labels[j], centers[j], confidences[j]))
                    used.add(j)
            groups.append(group)
        return groups

    # Chọn nhãn đại diện trong cụm
    def select_final_label_and_box(group):
        label_suffixes = [label[-1] for _, label, _, _ in group]
        most_common = Counter(label_suffixes).most_common(1)[0][0]
        filtered = [item for item in group if item[1].endswith(most_common)]
        best_item = max(filtered, key=lambda x: x[3])  # theo confidence
        return most_common, best_item

    # Gom cụm
    all_groups = group_nearby_boxes(boxes, labels, centers, confidences, threshold=20)

    # Tạo mảng lưu kết quả
    cluster_results = {}

    # In kết quả
    # print("\nCác cụm bounding box gần nhau:")
    for idx, group in enumerate(all_groups):
        final_char, best_box = select_final_label_and_box(group)
        x1, y1, x2, y2 = best_box[0]
        label = best_box[1]
        center = best_box[2]
        cluster_results[idx + 1] = final_char


    # Tạo danh sách các box và final_char từ các cụm
    cluster_boxes = []
    for idx, group in enumerate(all_groups):
        final_char, best_box = select_final_label_and_box(group)
        box = best_box[0]  # Box coordinates [x1, y1, x2, y2]
        cluster_boxes.append((box, final_char))

    # Sắp xếp theo x1 coordinate để chia thành 3 cụm
    cluster_boxes.sort(key=lambda x: x[0][0])  # Sắp xếp theo x1

    # Chia thành 3 cụm dựa trên x1 coordinate
    n = len(cluster_boxes)
    if n < 3:
        # print("Không đủ cụm để chia thành 3 nhóm!")
        return None, None
    else:
        third = n // 3
        x1_clusters = [
            cluster_boxes[:third],
            cluster_boxes[third:2 * third],
            cluster_boxes[2 * third:]
        ]

        # Sắp xếp từng cụm theo y1 coordinate
        for i in range(3):
            x1_clusters[i].sort(key=lambda x: x[0][1])  # Sắp xếp theo y1

        # In kết quả 3 cụm
        # print("\nBa cụm được chia theo x1 coordinate và sắp xếp theo y1 coordinate:")
        for i, cluster in enumerate(x1_clusters, 1):
            # print(f"\nCụm X1 {i} (số lượng {len(cluster)}):")
            for box, final_char in cluster:
                x1, y1, x2, y2 = box
                # print(f"  Ký tự: {final_char} | Coordinates: (x1={x1:.1f}, y1={y1:.1f}) | Box: ({int(x1)}, {int(y1)}) - ({int(x2)}, {int(y2)})")

    # Tạo mảng student_result từ 1 đến 60
    student_result = {}
    index = 1
    for cluster in x1_clusters:
        for _, final_char in cluster:
            student_result[index] = final_char
            index += 1

    # In mảng student_result
    # print("\nMảng student_result:")
    # for idx in range(1, 61):
    # print(f"{idx}:{student_result[idx]}")

    # Copy ảnh để vẽ lên
    img_result = img.copy()

    # Vẽ các box đại diện
    for idx, group in enumerate(all_groups):
        final_char, best_box = select_final_label_and_box(group)
        x1, y1, x2, y2 = map(int, best_box[0])

        # Vẽ khung chữ nhật
        cv2.rectangle(img_result, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Vẽ ký tự cuối (final_char) vào trong box
        label = final_char
        font_scale = 0.9
        font = cv2.FONT_HERSHEY_SIMPLEX
        label_size = cv2.getTextSize(label, font, font_scale, 2)[0]
        label_x = x1 + 5
        label_y = y1 + label_size[1] + 5

        cv2.rectangle(img_result, (x1, y1), (x1 + label_size[0] + 10, y1 + label_size[1] + 10), (0, 255, 0), -1)
        cv2.putText(img_result, label, (label_x, label_y), font, font_scale, (0, 0, 0), 2)

    # Lưu ảnh vào đường dẫn (đè lên ảnh đầu vào)
    cv2.imwrite(path_image, img_result)
    # print(f"Ảnh đã được lưu tại: {path_image}")

    return path_image, student_result

# Grading

def calculate_score(answers, df_key, exam_code):
    try:
        exam_code = str(exam_code).strip()
        
        # Lấy mã đề từ cột đầu tiên (không phải index)
        first_column = df_key.iloc[:, 0]  # Cột đầu tiên
        exam_codes_available = [str(val).strip().replace('.0', '') for val in first_column.dropna() if pd.notna(val)]
        
        print(f"Available exam codes in df_key (from first column): {exam_codes_available}")
        print(f"Checking exam_code: '{exam_code}' (type: {type(exam_code)})")

        if exam_code not in exam_codes_available:
            print(f"Exam code '{exam_code}' not found in answer key: {exam_codes_available}")
            return 0

        # Tìm index của row có mã đề khớp
        matching_row_index = None
        for idx in df_key.index:
            val = df_key.iloc[df_key.index.get_loc(idx), 0]  # Lấy giá trị cột đầu tiên
            if pd.notna(val) and str(val).strip().replace('.0', '') == exam_code:
                matching_row_index = df_key.index.get_loc(idx)  # Lấy vị trí iloc
                break
        
        if matching_row_index is None:
            print(f"Could not find matching row for exam code '{exam_code}'")
            return 0
            
        print(f"Found exam code '{exam_code}' at row index: {matching_row_index}")

        # Lấy đáp án đúng từ hàng đó (bỏ qua cột đầu tiên là mã đề)
        correct_answers = df_key.iloc[matching_row_index, 1:].values  # Bỏ cột đầu tiên
        num_questions = len(correct_answers)
        print(f"Correct answers (length: {num_questions}): {correct_answers}")

        answers = answers or [''] * num_questions
        if len(answers) != num_questions:
            print(f"Cảnh báo: Số câu trả lời ({len(answers)}) không khớp với số câu hỏi ({num_questions})")
            answers = answers + [''] * (num_questions - len(answers)) if len(answers) < num_questions else answers[
                                                                                                           :num_questions]
        print(f"Student answers (length: {len(answers)}): {answers}")

        score = sum(1 for student_answer, correct_answer in zip(answers, correct_answers)
                    if student_answer and correct_answer and student_answer.upper() == correct_answer.upper())

        print(f"Calculated score for exam_code {exam_code}: {score}/{num_questions}")
        return score
    except Exception as e:
        print(f"Error calculating score for exam_code {exam_code}: {e}")
        return 0

# --------------------Synchronize student--------------------
def synchronize_student_data(student, df_part):
    """
    Đồng bộ dữ liệu student dựa trên df_part.
    - Nếu 2/3 thuộc tính (id, name, index_student) khớp với một hàng trong df_part, đồng bộ thuộc tính còn lại.
    - Nếu cả 3 thuộc tính không khớp, lấy id làm chính, đồng bộ name và index_student theo hàng có MSSV khớp id.
    """
    try:
        id_student = student.get('id', 'N/A')
        name_student = student.get('name', 'N/A')
        index_student = student.get('index_student', 'N/A')

        # Tạo cột tên đầy đủ trong df_part
        if 'HoDem' in df_part and 'Ten' in df_part:
            df_part['full_name'] = (df_part['HoDem'].astype(str) + ' ' + df_part['Ten'].astype(str)).str.strip()
        elif 'Ten' in df_part:
            df_part['full_name'] = df_part['Ten'].astype(str).str.strip()
        else:
            df_part['full_name'] = ''

        # Chuyển đổi dữ liệu để so sánh
        df_part['MSSV'] = df_part['MSSV'].astype(str).str.strip()
        df_part['STT'] = df_part['STT'].astype(str).str.strip()
        df_part['full_name'] = df_part['full_name'].str.strip()

        # Kiểm tra từng hàng trong df_part
        matches = []
        for _, row in df_part.iterrows():
            match_count = 0
            if id_student != 'N/A' and id_student == row['MSSV']:
                match_count += 1
            if name_student != 'N/A' and name_student == row['full_name']:
                match_count += 1
            if index_student != 'N/A' and index_student == row['STT']:
                match_count += 1
            matches.append((match_count, row))

        # Sắp xếp theo số lượng khớp, ưu tiên hàng có >= 2 thuộc tính khớp
        matches.sort(key=lambda x: x[0], reverse=True)
        top_match = matches[0] if matches else (0, None)

        if top_match[0] >= 2:
            # Trường hợp 1: Có ít nhất 2 thuộc tính khớp, đồng bộ thuộc tính còn lại
            row = top_match[1]
            student['id'] = row['MSSV']
            student['name'] = row['full_name']
            student['index_student'] = row['STT']
            student['has_issue'] = False
            print(
                f"Synchronized student (2+ matches): id={student['id']}, name={student['name']}, index_student={student['index_student']}")
        else:
            # Trường hợp 2: Không có hàng nào khớp 2 thuộc tính, lấy id làm chính
            if id_student != 'N/A':
                matching_row = df_part[df_part['MSSV'] == id_student]
                if not matching_row.empty:
                    row = matching_row.iloc[0]
                    student['id'] = row['MSSV']
                    student['name'] = row['full_name']
                    student['index_student'] = row['STT']
                    student['has_issue'] = False
                    print(
                        f"Synchronized student (by id): id={student['id']}, name={student['name']}, index_student={student['index_student']}")
                else:
                    # Không tìm thấy id, giữ nguyên và đánh dấu has_issue
                    student['has_issue'] = True
                    print(f"No matching row for id={id_student}, keeping original values")
            else:
                # Không có id hợp lệ, giữ nguyên và đánh dấu has_issue
                student['has_issue'] = True
                print(f"No valid id for student, keeping original values")

        # Xóa cột tạm
        if 'full_name' in df_part:
            df_part.drop(columns=['full_name'], inplace=True)

        return student
    except Exception as e:
        print(f"Error synchronizing student data: {e}")
        student['has_issue'] = True
        return student