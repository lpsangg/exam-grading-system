"""
Quick usage guide and setup for exam detection test
"""

def setup_instructions():
    print("""
🔧 SETUP INSTRUCTIONS FOR EXAM DETECTION TEST
============================================

1. Install Ollama (if not already installed):
   - Download: https://ollama.ai/download/windows
   - Run installer
   - Restart terminal

2. Start Ollama service:
   ollama serve

3. Install Qwen2.5-VL model:
   ollama pull qwen2-vl:3b

4. Install Python dependencies:
   pip install ollama

5. Run the test:
   python test_exam_detection.py

📋 WHAT THE TEST DOES:
===================
- Connects to Ollama service
- Uses Qwen2.5-VL model to analyze exam form images
- Extracts 4 key pieces of information:
  * MÃ ĐỀ (Exam code)
  * HỌ VÀ TÊN (Student name) 
  * MÃ SỐ SINH VIÊN (Student ID)
  * STT (Serial number)
- Returns results in JSON format

📸 SUPPORTED IMAGE FORMATS:
=========================
- JPG, JPEG, PNG
- Should contain Vietnamese exam forms
- Clear, readable text preferred

🎯 USAGE EXAMPLES:
===============
1. Test with sample images:
   python test_exam_detection.py

2. Test with your own image:
   python test_exam_detection.py path/to/your/exam_form.jpg

3. Test with specific image:
   python test_exam_detection.py uploads/images/IMG_017.jpg

⚠️ TROUBLESHOOTING:
=================
- If "Ollama not available": Make sure ollama serve is running
- If "Model not found": Run ollama pull qwen2-vl:3b
- If "Connection refused": Check if Ollama service is running on port 11434
- If JSON parsing fails: Check the raw_response for manual inspection

""")

if __name__ == "__main__":
    setup_instructions()
