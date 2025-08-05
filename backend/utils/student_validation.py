import pandas as pd
from fuzzywuzzy import process, fuzz

def combine_name(ho_dem, ten):
    """Kết hợp họ đệm và tên thành tên đầy đủ"""
    if pd.isna(ho_dem) and pd.isna(ten):
        return ""
    if pd.isna(ho_dem):
        return str(ten).strip()
    if pd.isna(ten):
        return str(ho_dem).strip()
    return f"{str(ho_dem).strip()} {str(ten).strip()}".strip()

def validate_and_correct_student_info(detected_name, detected_mssv, detected_stt, df_students):
    """
    Validate và auto-correct thông tin sinh viên dựa trên danh sách gốc
    
    Args:
        detected_name: Tên được nhận diện
        detected_mssv: MSSV được nhận diện  
        detected_stt: STT được nhận diện
        df_students: DataFrame chứa danh sách sinh viên gốc
        
    Returns:
        dict: {
            'name': tên đã correct,
            'mssv': mssv đã correct,
            'stt': stt đã correct,
            'status': 'exact_match' | 'auto_corrected' | 'no_match',
            'correction_reason': lý do sửa
        }
    """
    
    # Đảm bảo DataFrame có index là số nguyên
    df_students = df_students.reset_index(drop=True)
    
    # Tạo danh sách tên đầy đủ từ DataFrame
    if 'HoDem' in df_students.columns and 'Ten' in df_students.columns:
        df_students['FullName'] = df_students.apply(
            lambda row: combine_name(row['HoDem'], row['Ten']), axis=1
        )
    elif 'Ten' in df_students.columns:
        df_students['FullName'] = df_students['Ten'].astype(str)
    else:
        # Nếu không có cột tên, sử dụng MSSV làm tên
        df_students['FullName'] = df_students['MSSV'].astype(str)
    
    # Chuyển đổi tất cả thành string để so sánh
    df_students['MSSV_str'] = df_students['MSSV'].astype(str)
    df_students['STT_str'] = df_students['STT'].astype(str)
    
    detected_name_str = str(detected_name) if detected_name else ""
    detected_mssv_str = str(detected_mssv) if detected_mssv else ""
    detected_stt_str = str(detected_stt) if detected_stt else ""
    
    # Tìm các match với threshold cao
    name_matches = []
    mssv_matches = []
    stt_matches = []
    
    # Tìm match cho từng thuộc tính
    for idx, row in df_students.iterrows():
        # Name matching
        if detected_name_str and row['FullName']:
            name_score = fuzz.ratio(detected_name_str.lower(), row['FullName'].lower())
            if name_score >= 70:  # Threshold cho tên
                name_matches.append((idx, name_score))
        
        # MSSV matching
        if detected_mssv_str and row['MSSV_str']:
            mssv_score = fuzz.ratio(detected_mssv_str, row['MSSV_str'])
            if mssv_score >= 80:  # Threshold cho MSSV
                mssv_matches.append((idx, mssv_score))
        
        # STT matching
        if detected_stt_str and row['STT_str']:
            if detected_stt_str == row['STT_str']:  # STT phải match chính xác
                stt_matches.append((idx, 100))
    
    # Tìm intersection của các matches
    name_indices = set([m[0] for m in name_matches])
    mssv_indices = set([m[0] for m in mssv_matches])
    stt_indices = set([m[0] for m in stt_matches])
    
    # Case 1: Cả 3 thuộc tính đều match cùng 1 row
    all_match = name_indices & mssv_indices & stt_indices
    if all_match:
        row_idx = list(all_match)[0]
        row = df_students.iloc[row_idx]
        return {
            'name': row['FullName'],
            'mssv': row['MSSV_str'],
            'stt': row['STT_str'],
            'status': 'exact_match',
            'correction_reason': 'Cả 3 thuộc tính đều khớp với danh sách'
        }
    
    # Case 2: 2/3 thuộc tính match cùng 1 row
    name_mssv = name_indices & mssv_indices
    name_stt = name_indices & stt_indices
    mssv_stt = mssv_indices & stt_indices
    
    if name_mssv:
        row_idx = list(name_mssv)[0]
        row = df_students.iloc[row_idx]
        return {
            'name': row['FullName'],
            'mssv': row['MSSV_str'],
            'stt': row['STT_str'],
            'status': 'auto_corrected',
            'correction_reason': 'Tên và MSSV khớp, STT được sửa theo danh sách'
        }
    
    if name_stt:
        row_idx = list(name_stt)[0]
        row = df_students.iloc[row_idx]
        return {
            'name': row['FullName'],
            'mssv': row['MSSV_str'],
            'stt': row['STT_str'],
            'status': 'auto_corrected',
            'correction_reason': 'Tên và STT khớp, MSSV được sửa theo danh sách'
        }
    
    if mssv_stt:
        row_idx = list(mssv_stt)[0]
        row = df_students.iloc[row_idx]
        return {
            'name': row['FullName'],
            'mssv': row['MSSV_str'],
            'stt': row['STT_str'],
            'status': 'auto_corrected',
            'correction_reason': 'MSSV và STT khớp, Tên được sửa theo danh sách'
        }
    
    # Case 3: Chỉ có 1 hoặc 0 thuộc tính match → Ưu tiên theo Tên
    if name_matches:
        # Lấy match tốt nhất cho tên
        best_name_match = max(name_matches, key=lambda x: x[1])
        row_idx = best_name_match[0]
        row = df_students.iloc[row_idx]
        return {
            'name': row['FullName'],
            'mssv': row['MSSV_str'],
            'stt': row['STT_str'],
            'status': 'auto_corrected',
            'correction_reason': 'Ưu tiên theo Tên sinh viên, MSSV và STT được sửa theo danh sách'
        }
    
    # Case 4: Không có gì match → Giữ nguyên giá trị đã nhận diện
    return {
        'name': detected_name_str,
        'mssv': detected_mssv_str,
        'stt': detected_stt_str,
        'status': 'no_match',
        'correction_reason': 'Không tìm thấy thông tin khớp trong danh sách'
    }
