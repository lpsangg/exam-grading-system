import pandas as pd
import numpy as np
import os
import json
import logging

logger = logging.getLogger(__name__)

def process_df_key(file_path):
    """
    Xử lý file đáp án Excel
    """
    try:
        df = pd.read_excel(file_path)
        logger.info(f"Processed answer key: shape={df.shape}, columns={list(df.columns)}")
        return df
    except Exception as e:
        logger.error(f"Error processing answer key: {e}")
        return None

def process_df_student(file):
    """
    Xử lý file danh sách sinh viên Excel theo cấu trúc đặc biệt
    """
    try:
        df_student = pd.read_excel(file, skiprows=6, header=[0, 1, 2])

        df_student = df_student[pd.to_numeric(df_student.iloc[:, 0], errors='coerce').notnull()]
        df_student.reset_index(drop=True, inplace=True)

        logger.info("=== Dữ liệu sau lọc ===")
        logger.info(df_student.head())

        df_student.columns = [
            'STT', 'MSSV', 'HoDem', 'Ten', 'GioiTinh', 'NgaySinh', 'LopHoc', 'HeSo1', 'DuocDuThi', '', 'VangThi',
            'VPQuyChe', 'ThangDiem4', 'DiemChu', 'XepLoai', 'GhiChu', 'GhiChuCuoiKy'
        ]
        df_student.reset_index(drop=True, inplace=True)
        logger.info(df_student.head())

        select_columns = ['STT', 'MSSV', 'HoDem', 'Ten', 'HeSo1', 'ThangDiem4']
        df_select_columns = df_student[select_columns]
        df_select_columns['MSSV'] = df_select_columns['MSSV'].astype(int)
        # Lấy danh sách MSSV
        student_ids = df_select_columns['MSSV'].tolist()

        # Lấy tên Sinh viên
        df_student['HoTen'] = df_student['HoDem'].astype(str).str.strip().str.upper() + ' ' + df_student['Ten'].astype(
            str).str.strip().str.upper()
        student_names = df_student['HoTen'].tolist()

        # logger.info(df_select_columns.head())

        num_parts = 1
        nums_row = len(df_select_columns)
        if nums_row <= 45:
            num_parts = 1
        elif 45 < nums_row <= 90:
            num_parts = 2
        else:
            num_parts = 3

        parts = np.array_split(df_select_columns, num_parts)
        df_parts = {}
        for i, part in enumerate(parts):
            part = part.reset_index(drop=True)
            part.index = part.index + 1
            var_name = f"df_part{i + 1}"
            df_parts[var_name] = part
            logger.info(f"\n=== {var_name} ({len(part)} dòng) ===")
            logger.info(part)

        return {
            'student_ids': student_ids,
            'student_names': student_names,
            'df_parts': df_parts
        }

    except Exception as e:
        logger.error(f"Error processing student list: {e}")
        return {'error': str(e)}


# file = '../uploads/student/20250425114931_MauGhiDiem.xlsx'
# print(process_df_student(file))
