#!/usr/bin/env python3
"""
Script để debug cấu trúc file Excel answer key
"""

import pandas as pd
import os

def debug_excel_structure(file_path):
    """Debug cấu trúc file Excel"""
    print(f"=== DEBUG FILE: {file_path} ===\n")
    
    if not os.path.exists(file_path):
        print(f"❌ File không tồn tại: {file_path}")
        return
    
    try:
        # Đọc file Excel
        df = pd.read_excel(file_path)
        print(f"📊 Shape của DataFrame: {df.shape}")
        print(f"📝 Columns: {list(df.columns)}")
        print("\n" + "="*50)
        
        # Hiển thị 5 hàng đầu
        print("🔍 5 hàng đầu tiên:")
        print(df.head())
        print("\n" + "="*50)
        
        # Hiển thị hàng đầu tiên (có thể là mã đề)
        print("📋 Hàng đầu tiên (có thể chứa mã đề):")
        first_row = df.iloc[0]
        print(first_row)
        print("\n" + "="*50)
        
        # Hiển thị cột đầu tiên
        print("📋 Cột đầu tiên:")
        first_col = df.iloc[:, 0]
        print(first_col.head(10))
        print("\n" + "="*50)
        
        # Tìm mã đề trong hàng đầu tiên
        print("🔎 Tìm mã đề trong hàng đầu tiên:")
        exam_codes_row = []
        for col in df.columns:
            value = df.iloc[0][col]
            if pd.notna(value):
                # Chuyển thành string và loại bỏ .0
                str_value = str(value).replace('.0', '')
                # Kiểm tra nếu là số (mã đề thường là số)
                if str_value.isdigit():
                    exam_codes_row.append(str_value)
        
        print(f"Mã đề tìm thấy trong hàng đầu tiên: {exam_codes_row}")
        
        # Tìm mã đề trong cột đầu tiên
        print("\n🔎 Tìm mã đề trong cột đầu tiên:")
        exam_codes_col = []
        for i, value in enumerate(df.iloc[:, 0]):
            if pd.notna(value):
                str_value = str(value).replace('.0', '')
                if str_value.isdigit():
                    exam_codes_col.append(str_value)
        
        print(f"Mã đề tìm thấy trong cột đầu tiên: {exam_codes_col[:10]}...")  # Chỉ hiển thị 10 đầu
        
        # Đọc không có header để xem raw data
        print("\n🔍 Đọc file không có header:")
        df_no_header = pd.read_excel(file_path, header=None)
        print("5 hàng đầu tiên (raw):")
        print(df_no_header.head())
        
    except Exception as e:
        print(f"❌ Lỗi khi đọc file: {e}")

if __name__ == "__main__":
    # Test với file có sẵn
    test_files = [
        "test_answer_key.xlsx",
        "uploads/key/MauDapAn.xlsx",
        "uploads/key/KHMT0121_MauDapAn.xlsx"
    ]
    
    for file_path in test_files:
        if os.path.exists(file_path):
            debug_excel_structure(file_path)
            print("\n" + "="*80 + "\n")
