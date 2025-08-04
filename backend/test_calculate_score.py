#!/usr/bin/env python3
"""
Test script để kiểm tra function calculate_score
"""

import sys
import os
import pandas as pd

# Thêm đường dẫn để import
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from automatic_exam_grading import calculate_score

def test_calculate_score():
    """Test function calculate_score với data thực"""
    
    # Đọc file Excel thực
    excel_path = "uploads/key/KHMT0121_MauDapAn.xlsx"
    
    if not os.path.exists(excel_path):
        print(f"❌ File không tồn tại: {excel_path}")
        return
    
    # Đọc DataFrame
    df_key = pd.read_excel(excel_path)
    print(f"📊 df_key shape: {df_key.shape}")
    print(f"📝 df_key first column: {df_key.iloc[:, 0].tolist()}")
    
    # Test với mã đề 103
    print("\n=== Testing calculate_score với mã đề 103 ===")
    
    # Tạo answers giả định
    answers = ['A', 'B', 'C', 'D'] * 15  # 60 câu với pattern lặp
    
    score = calculate_score(answers, df_key, '103')
    print(f"🎯 Kết quả score: {score}")
    
    print("\n=== Testing với mã đề 101 ===")
    score2 = calculate_score(answers, df_key, '101')
    print(f"🎯 Kết quả score: {score2}")
    
    print("\n=== Testing với mã đề không tồn tại ===")
    score3 = calculate_score(answers, df_key, '999')
    print(f"🎯 Kết quả score: {score3}")

if __name__ == "__main__":
    test_calculate_score()
