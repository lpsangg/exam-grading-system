"""
Test script for the updated detectInfo.py with image preprocessing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.detectInfo import detect_name_student, detect_id_student, detect_index_student
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_detection_functions():
    """Test the detection functions with sample data"""
    
    # Sample data
    student_names = [
        "Bùi Nguyễn Khôi Nguyên",
        "Thái Bảo Nguyên", 
        "Nguyễn Lê Nguyên",
        "Nguyễn Trọng Nhân",
        "Dương Tấn Phát",
        "Đặng Tấn Phát",
        "Phạm Tấn Phát",
        "Đặng Hào Phú",
        "Nguyễn Anh Thư",
        "Huỳnh Nguyễn Thanh Trúc",
        "Trần Nhật Trường",
        "Đinh Hồng Yến"
    ]
    
    student_ids = [
        "20181234",
        "20200456", 
        "KHMT2101395",
        "NNA2101302",
        "20191234",
        "CNTT2020123"
    ]
    
    # Check if test images exist
    test_images = [
        "uploads/images/IMG_017.jpg",
        "uploads/images/IMG_018.jpg", 
        "test_image.jpg"
    ]
    
    available_images = [img for img in test_images if os.path.exists(img)]
    
    if not available_images:
        logger.warning("No test images found. Please make sure you have test images in:")
        for img in test_images:
            logger.warning(f"  - {img}")
        return
    
    logger.info("🧪 TESTING DETECTION FUNCTIONS")
    logger.info("=" * 50)
    
    for image_path in available_images:
        logger.info(f"\n📷 Testing with image: {image_path}")
        
        # Test name detection
        logger.info("🔍 Testing name detection...")
        detected_name = detect_name_student(image_path, student_names, use_ollama=True)
        logger.info(f"   Result: {detected_name}")
        
        # Test ID detection  
        logger.info("🔍 Testing ID detection...")
        detected_id = detect_id_student(image_path, student_ids, use_ollama=True, show_image=False)
        logger.info(f"   Result: {detected_id}")
        
        # Test index detection
        logger.info("🔍 Testing index detection...")
        detected_index = detect_index_student(image_path)
        logger.info(f"   Result: {detected_index}")
        
        logger.info("-" * 30)

def test_fallback_mechanism():
    """Test fallback to traditional OCR when Ollama fails"""
    
    logger.info("\n🔄 TESTING FALLBACK MECHANISM")
    logger.info("=" * 50)
    
    # Test with Ollama disabled
    test_images = [img for img in ["uploads/images/IMG_017.jpg", "test_image.jpg"] if os.path.exists(img)]
    
    if test_images:
        image_path = test_images[0]
        logger.info(f"📷 Testing fallback with: {image_path}")
        
        student_names = ["Nguyễn Văn A", "Trần Thị B"]
        student_ids = ["20181234", "KHMT2101395"]
        
        # Test with Ollama disabled
        logger.info("🔍 Testing with Ollama disabled...")
        detected_name = detect_name_student(image_path, student_names, use_ollama=False)
        detected_id = detect_id_student(image_path, student_ids, use_ollama=False)
        
        logger.info(f"   Name (no Ollama): {detected_name}")
        logger.info(f"   ID (no Ollama): {detected_id}")

def test_image_preprocessing():
    """Test image preprocessing functions"""
    
    logger.info("\n🖼️  TESTING IMAGE PREPROCESSING")
    logger.info("=" * 50)
    
    test_images = [img for img in ["uploads/images/IMG_017.jpg", "test_image.jpg"] if os.path.exists(img)]
    
    if test_images:
        import cv2
        image_path = test_images[0]
        
        try:
            # Test image reading and cropping (name detection preprocessing)
            image = cv2.imread(image_path)
            if image is not None:
                h = image.shape[0]
                cropped_image = image[h // 3:, :, :]
                logger.info(f"✅ Image preprocessing successful")
                logger.info(f"   Original size: {image.shape}")
                logger.info(f"   Cropped size: {cropped_image.shape}")
            else:
                logger.error(f"❌ Failed to read image: {image_path}")
                
        except Exception as e:
            logger.error(f"❌ Image preprocessing failed: {e}")

if __name__ == "__main__":
    logger.info("🚀 STARTING DETECTION TESTS")
    logger.info("=" * 60)
    
    try:
        # Test basic functions
        test_detection_functions()
        
        # Test fallback mechanism  
        test_fallback_mechanism()
        
        # Test image preprocessing
        test_image_preprocessing()
        
        logger.info("\n🎉 ALL TESTS COMPLETED!")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
