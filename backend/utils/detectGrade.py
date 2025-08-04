import cv2
import numpy as np
from collections import Counter
from ultralytics import YOLO
import uuid

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
        # print(f"\nCụm {idx + 1} (số lượng {len(group)}): Chọn ký tự cuối là '{final_char}'")
        # for b in group:
    # print(f"  {b[1]} | Center: ({b[2][0]:.1f}, {b[2][1]:.1f}) | Box: ({int(b[0][0])}, {int(b[0][1])}) - ({int(b[0][2])}, {int(b[0][3])}) | Conf: {b[3]:.2f}")
    # print(f"=> Được chọn: {label} | Center: ({center[0]:.1f}, {center[1]:.1f}) | Box: ({int(x1)}, {int(y1)}) - ({int(x2)}, {int(y2)})")

    # In mảng kết quả
    # print("\nMảng kết quả:")
    # print(cluster_results)

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