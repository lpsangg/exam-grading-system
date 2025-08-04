from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from api_mobile import router as api_mobile_router

app = FastAPI(title="Exam Grading System API", version="1.0.0")

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cấu hình thư mục upload
UPLOAD_FOLDER_KEY = os.path.join('uploads', 'key')
UPLOAD_FOLDER_STUDENT = os.path.join('uploads', 'student')
UPLOAD_FOLDER_IMAGES = os.path.join('uploads', 'images')

for folder in [UPLOAD_FOLDER_KEY, UPLOAD_FOLDER_STUDENT, UPLOAD_FOLDER_IMAGES]:
    os.makedirs(folder, exist_ok=True)

# Đăng ký router
app.include_router(api_mobile_router)

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.post("/login")
async def login(request: Request):
    data = await request.json()
    return {"status": "success", "user": data.get("username")}

# Thêm đoạn này để có thể chạy trực tiếp file
if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Exam Grading System API Server...")
    print("📍 Server will run on: http://localhost:5000")
    print("📚 API Documentation: http://localhost:5000/docs")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")