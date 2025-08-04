"""
Test script for Ollama Qwen2.5-VL to detect exam form information
"""

import ollama
import base64
import json
import os
import sys
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ExamFormDetector:
    """
    Detector for exam form information using Ollama Qwen2.5-VL
    """
    
    def __init__(self, model_name="qwen2.5vl:3b"):
        self.model_name = model_name
        self.client = ollama.Client()
        self._check_model_availability()
    
    def _check_model_availability(self):
        """Check if Qwen model is available in Ollama"""
        try:
            models = self.client.list()
            available_models = [model['name'] for model in models['models']]
            
            if self.model_name not in available_models:
                logger.warning(f"⚠️ Model {self.model_name} not found in Ollama")
                logger.info("📥 Available models:")
                for model in available_models:
                    logger.info(f"   - {model}")
                logger.info(f"💡 To install the model, run: ollama pull {self.model_name}")
                return False
            else:
                logger.info(f"✅ Model {self.model_name} is available in Ollama")
                return True
                
        except Exception as e:
            logger.error(f"❌ Failed to connect to Ollama: {e}")
            logger.info("💡 Make sure Ollama is running. Start it with: ollama serve")
            return False
    
    def _encode_image_to_base64(self, image_path):
        """Convert image to base64 string"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            logger.error(f"❌ Failed to encode image: {e}")
            return None
    
    def detect_exam_info(self, image_path):
        """
        Detect exam form information from image
        
        Args:
            image_path: Path to exam form image
            
        Returns:
            Dictionary with detected information or None if failed
        """
        
        if not os.path.exists(image_path):
            logger.error(f"❌ Image file not found: {image_path}")
            return None
        
        # Encode image
        image_base64 = self._encode_image_to_base64(image_path)
        if not image_base64:
            return None
        
        # Detailed prompt for exam form detection
        prompt = """Bạn là một chuyên gia OCR (Optical Character Recognition) chuyên nhận diện các thông tin từ phiếu thi trắc nghiệm. Hãy phân tích hình ảnh phiếu thi này và trích xuất chính xác 4 thông tin sau:

1. MÃ ĐỀ: Số nằm trong ô vuông phía trên bên trái, dưới dòng "Mã đề:"
2. HỌ VÀ TÊN: Tên sinh viên viết tay trong ô chữ nhật dưới "Họ và tên sinh viên"  
3. MÃ SỐ SINH VIÊN: Số sinh viên viết tay trong ô dưới "Mã số sinh viên"
4. STT: Số thứ tự nằm sau chữ "STT:"

Lưu ý quan trọng:
- Mã đề là số in sẵn, còn lại là chữ viết tay
- Đọc kỹ từng ký tự, bao gồm cả chữ viết tay không rõ ràng
- Nếu không chắc chắn về ký tự nào, hãy đưa ra phỏng đoán tốt nhất

Trả lời theo định dạng JSON chính xác như sau:
{
  "ma_de": "số_mã_đề",
  "ho_ten": "họ_và_tên_đầy_đủ",
  "ma_so_sinh_vien": "mã_số_sinh_viên",
  "stt": "số_thứ_tự"
}"""

        try:
            logger.info(f"🔍 Processing exam form: {os.path.basename(image_path)}")
            
            # Send request to Ollama
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                images=[image_base64],
                options={
                    'temperature': 0.1,  # Low temperature for more consistent results
                    'top_p': 0.9,
                    'top_k': 40,
                    'num_predict': 256  # Allow longer response for JSON
                }
            )
            
            if response and 'response' in response:
                result_text = response['response'].strip()
                logger.info(f"📝 Raw response: {result_text}")
                
                # Try to parse JSON from response
                try:
                    # Extract JSON from response (handle cases where there might be extra text)
                    json_start = result_text.find('{')
                    json_end = result_text.rfind('}') + 1
                    
                    if json_start >= 0 and json_end > json_start:
                        json_text = result_text[json_start:json_end]
                        parsed_result = json.loads(json_text)
                        
                        logger.info("✅ Successfully parsed JSON response")
                        return parsed_result
                    else:
                        logger.warning("⚠️ No valid JSON found in response")
                        # Return raw response for manual inspection
                        return {"raw_response": result_text}
                        
                except json.JSONDecodeError as e:
                    logger.warning(f"⚠️ Failed to parse JSON: {e}")
                    logger.info(f"Raw response: {result_text}")
                    # Return raw response for manual inspection
                    return {"raw_response": result_text}
            else:
                logger.warning("⚠️ Empty response from Ollama")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error detecting exam info: {e}")
            return None
    
    def test_with_sample_images(self):
        """Test with available sample images"""
        
        # List of potential test images
        test_images = [
            "uploads/images/IMG_017.jpg",

        ]
        
        available_images = [img for img in test_images if os.path.exists(img)]
        
        if not available_images:
            logger.warning("❌ No test images found")
            logger.info("Available test image paths to try:")
            for img in test_images:
                logger.info(f"   - {img}")
            return
        
        logger.info(f"📸 Found {len(available_images)} test images")
        
        for image_path in available_images:
            logger.info(f"\n{'='*60}")
            logger.info(f"🎯 Testing with: {image_path}")
            logger.info(f"{'='*60}")
            
            result = self.detect_exam_info(image_path)
            
            if result:
                logger.info("📋 DETECTION RESULTS:")
                if "raw_response" in result:
                    logger.info("Raw response (JSON parsing failed):")
                    logger.info(result["raw_response"])
                else:
                    logger.info("Parsed JSON result:")
                    for key, value in result.items():
                        logger.info(f"   {key}: {value}")
            else:
                logger.error("❌ Detection failed")
            
            logger.info(f"{'='*60}\n")

def main():
    """Main function to run the test"""
    
    logger.info("🚀 STARTING EXAM FORM DETECTION TEST")
    logger.info("=" * 80)
    
    # Check if custom image path is provided
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        logger.info(f"📷 Using custom image: {image_path}")
        
        detector = ExamFormDetector()
        result = detector.detect_exam_info(image_path)
        
        if result:
            print("\n" + "="*50)
            print("📋 EXAM FORM DETECTION RESULTS")
            print("="*50)
            
            if "raw_response" in result:
                print("⚠️ Raw response (JSON parsing failed):")
                print(result["raw_response"])
            else:
                print("✅ Parsed information:")
                for key, value in result.items():
                    print(f"   {key.upper()}: {value}")
        else:
            print("❌ Detection failed")
    
    else:
        logger.info("🔍 Testing with available sample images")
        detector = ExamFormDetector()
        detector.test_with_sample_images()
    
    logger.info("\n🎉 TEST COMPLETED!")
    logger.info("=" * 80)

if __name__ == "__main__":
    print("""
🎯 EXAM FORM DETECTOR TEST
========================

This script tests Ollama Qwen2.5-VL for detecting exam form information.

Usage:
1. Test with sample images: python test_exam_detection.py
2. Test with custom image: python test_exam_detection.py path/to/your/image.jpg

Requirements:
- Ollama installed and running (ollama serve)
- qwen2-vl:3b model pulled (ollama pull qwen2-vl:3b)

""")
    
    main()
