import pandas as pd

def grading_result(df_answer_student, df_key):

    # Số lượng câu hỏi
    num_questions = len(df_key.columns)

    # Tính điểm cho mỗi câu
    points_per_question = 10 / num_questions
    # Tính điểm cho từng học sinh
    results = []
    ma_de = 212

    # Kiểm tra kiểu dữ liệu của ma_de
    print("ma_de:", ma_de, "type:", type(ma_de))
    print("df_key.index:", df_key.index.tolist())
    print("df_key.index types:", [type(x) for x in df_key.index])

    # Đảm bảo kiểu dữ liệu khớp nếu cần
    if isinstance(ma_de, int):  # Nếu ma_de là số nguyên, đảm bảo df_key.index cũng là số nguyên
        df_key.index = df_key.index.astype(int)

    # Kiểm tra mã đề
    if ma_de not in df_key.index:
        raise ValueError(f"Mã đề {ma_de} không tồn tại trong df_key!")

    # Kiểm tra tên cột
    if set(df_key.columns) != set(df_answer_student.columns):
        raise ValueError("Tên cột của df_key và df_answers không khớp!")

    # Lấy đáp án đúng cho mã đề
    correct_answers = df_key.loc[ma_de].reset_index(drop=True)

    # Kiểm tra chỉ mục của df_answer_first_40
    print(df_answer_student.index)

    # Nếu chỉ mục không phải là số nguyên, reset lại chỉ mục
    df_answer_first_40 = df_answer_student.reset_index(drop=True)
    print(df_answer_first_40)
    # Lấy câu trả lời của sinh viên
    student_answers = df_answer_first_40.iloc[0].reset_index(drop=True)

    # So sánh và tính điểm
    score = (student_answers == correct_answers).astype(int).sum() * points_per_question
    # Làm tròn điểm đến 2 chữ số thập phân
    score = round(score, 2)
    # Tạo kết quả
    result = {'Index': ma_de, 'Score': score}

    # In kết quả
    print(pd.DataFrame([result]))
    return 0