
import cv2
import numpy as np
import os


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
