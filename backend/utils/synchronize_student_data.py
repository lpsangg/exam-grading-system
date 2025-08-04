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



