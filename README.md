# Exam Grading System

Hệ thống chấm điểm bài thi tự động sử dụng AI và xử lý ảnh.

## Tính năng

- 📋 Upload và xử lý file đáp án Excel
- 👥 Quản lý danh sách sinh viên theo phòng thi
- 📸 Upload và xử lý ảnh bài thi
- 🤖 Nhận dạng tự động thông tin sinh viên và mã đề
- ✅ Chấm điểm tự động dựa trên đáp án
- 📊 Xem lại và chỉnh sửa kết quả
- 📄 Xuất kết quả ra file Excel

## Công nghệ sử dụng

### Frontend
- Next.js 15.2.4
- TypeScript
- Tailwind CSS
- shadcn/ui
- Zustand (State management)

### Backend
- FastAPI
- Python 3.13
- OpenCV (Xử lý ảnh)
- Pandas (Xử lý Excel)
- Ollama (AI/OCR)

## Cài đặt

### Yêu cầu hệ thống
- Node.js 18+
- Python 3.13
- Ollama

### Frontend
```bash
npm install
# hoặc
pnpm install

npm run dev
```

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Ollama
```bash
# Cài đặt Ollama
# Tải model
ollama pull qwen2.5vl:3b
```

## Cách sử dụng

1. **Bước 1 - Đáp Án**: Upload file Excel chứa đáp án các mã đề
2. **Bước 2 - Danh Sách**: Upload file Excel danh sách sinh viên
3. **Bước 3 - Bài Làm**: Upload ảnh bài thi và xử lý
4. **Bước 4 - Kết Quả**: Xem lại và chỉnh sửa kết quả nhận dạng
5. **Bước 5 - Xuất File**: Tải xuống file kết quả Excel

## Cấu trúc thư mục

```
exam-grading-system/
├── app/                 # Next.js pages
├── backend/             # FastAPI backend
├── components/          # React components
├── lib/                 # Utilities và store
└── public/              # Static files
```

## Đóng góp

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## License

MIT License

## Liên hệ

- GitHub: [@lpsangg](https://github.com/lpsangg)
- Email: [your-email@example.com]
