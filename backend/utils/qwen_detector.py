"""
Qwen2.5-VL-3B-Instruct detector for text extraction from images
Uses local model from backend/models/Qwen2.5-VL-3B-Instruct
"""

import logging
import re
import os
from typing import List, Optional
from PIL import Image
import torch

# Qwen imports with fallback
try:
    from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
    QWEN_AVAILABLE = True
except ImportError:
    QWEN_AVAILABLE = False
    Qwen2VLForConditionalGeneration = None
    AutoProcessor = None

# Import qwen_vl_utils with fallback
try:
    from qwen_vl_utils import process_vision_info
except ImportError:
    try:
        import sys
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from qwen_vl_utils import process_vision_info
    except ImportError:
        def process_vision_info(messages):
            """Fallback implementation"""
            image_inputs = []
            video_inputs = []
            
            for message in messages:
                if "content" in message:
                    for content_item in message["content"]:
                        if content_item.get("type") == "image":
                            image_path = content_item.get("image")
                            if image_path and os.path.exists(image_path):
                                try:
                                    image = Image.open(image_path).convert('RGB')
                                    image_inputs.append(image)
                                except Exception as e:
                                    logging.warning(f"Failed to load image {image_path}: {e}")
            
            return image_inputs, video_inputs

from fuzzywuzzy import process

logger = logging.getLogger(__name__)

class QwenDetector:
    """Qwen2.5-VL-3B-Instruct model wrapper for text detection"""
    
    def __init__(self):
        self.model = None
        self.processor = None
        self.device = "cpu"  # Force CPU to avoid accelerate requirement
        self._load_model()
    
    def _load_model(self):
        """Load Qwen model and processor from local directory"""
        if not QWEN_AVAILABLE:
            logger.error("❌ Qwen transformers not available")
            return
        
        # Determine model path
        model_path = r"C:\Users\Sang\Desktop\Project\exam-grading-system\backend\models\Qwen2.5-VL-3B-Instruct"
        
        # Verify model path exists
        if not os.path.exists(model_path):
            logger.error(f"❌ Model directory not found: {model_path}")
            return
        
        logger.info(f"🔄 Loading Qwen model from: {model_path}")
        
        # Simple loading strategy without accelerate
        try:
            logger.info("🔄 Loading with CPU-only configuration...")
            
            # Load model without device_map to avoid accelerate requirement
            self.model = Qwen2VLForConditionalGeneration.from_pretrained(
                model_path,
                torch_dtype=torch.float32,  # Use float32 for CPU
                trust_remote_code=True,
                local_files_only=True
                # Remove device_map to avoid accelerate requirement
            )
            
            # Move model to CPU explicitly
            self.model = self.model.to("cpu")
            
            # Load processor
            self.processor = AutoProcessor.from_pretrained(
                model_path,
                trust_remote_code=True,
                local_files_only=True
            )
            
            self.device = "cpu"
            
            logger.info("✅ Qwen model loaded successfully on CPU!")
            logger.info(f"📱 Device: {self.device}")
            
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            
            # Fallback: try loading from HuggingFace (if local fails)
            try:
                logger.info("🔄 Fallback: trying HuggingFace download...")
                
                self.model = Qwen2VLForConditionalGeneration.from_pretrained(
                    "Qwen/Qwen2.5-VL-3B-Instruct",
                    torch_dtype=torch.float32,
                    trust_remote_code=True
                ).to("cpu")
                
                self.processor = AutoProcessor.from_pretrained(
                    "Qwen/Qwen2.5-VL-3B-Instruct",
                    trust_remote_code=True
                )
                
                logger.info("✅ Qwen model loaded from HuggingFace!")
                
            except Exception as e2:
                logger.error(f"❌ Complete failure: {e2}")
                self.model = None
                self.processor = None
    
    def is_available(self) -> bool:
        """Check if model is loaded and available"""
        return self.model is not None and self.processor is not None
    
    def extract_text_from_image(self, image_path: str, prompt: str) -> Optional[str]:
        """Extract text from image using Qwen model"""
        if not self.is_available():
            logger.warning("❌ Qwen model not available")
            return None
        
        if not os.path.exists(image_path):
            logger.warning(f"❌ Image file not found: {image_path}")
            return None
        
        try:
            logger.info(f"🔍 Processing image: {os.path.basename(image_path)}")
            
            # Prepare messages
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "image": image_path,
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ]
            
            # Preparation for inference
            text = self.processor.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
            
            image_inputs, video_inputs = process_vision_info(messages)
            inputs = self.processor(
                text=[text],
                images=image_inputs,
                videos=video_inputs,
                padding=True,
                return_tensors="pt",
            )
            
            # Ensure everything is on CPU
            inputs = inputs.to("cpu")
            
            # Inference with error handling
            with torch.no_grad():
                try:
                    generated_ids = self.model.generate(
                        **inputs, 
                        max_new_tokens=128,
                        do_sample=False,
                        temperature=0.1
                    )
                except Exception as e:
                    logger.error(f"Generation failed: {e}")
                    return None
            
            generated_ids_trimmed = [
                out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
            ]
            
            output_text = self.processor.batch_decode(
                generated_ids_trimmed, 
                skip_special_tokens=True, 
                clean_up_tokenization_spaces=False
            )
            
            if output_text and len(output_text) > 0:
                result = output_text[0].strip()
                logger.info(f"✅ Qwen extracted: '{result}'")
                return result
            else:
                logger.warning("⚠️ Qwen returned empty result")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error extracting text with Qwen: {e}")
            return None

# Global detector instance
_detector_instance = None

def get_qwen_detector() -> QwenDetector:
    """Get singleton Qwen detector instance"""
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = QwenDetector()
    return _detector_instance

def clean_and_normalize(text: str) -> str:
    """Clean and normalize extracted text"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove special characters but keep Vietnamese characters and alphanumeric
    text = re.sub(r'[^\w\sÀ-ỹ]', ' ', text)
    
    # Convert to uppercase for consistency
    text = text.upper()
    
    return text.strip()

def detect_name_student_qwen(image_path: str, student_names: List[str]) -> Optional[str]:
    """Detect student name using Qwen2.5-VL model"""
    try:
        detector = get_qwen_detector()
        
        if not detector.is_available():
            logger.warning("❌ Qwen detector not available")
            return None
        
        # Optimized prompt for Vietnamese names
        name_prompt = """You are a text extraction expert. Extract the student name from this exam paper image.

Look for Vietnamese names with these patterns:
- Family name: NGUYEN, TRAN, LE, PHAM, HOANG, etc.
- Middle name: VAN, THI, QUOC, MINH, etc. 
- Given name: AN, BINH, HUNG, LAN, etc.

Return ONLY the complete full name in uppercase letters.
Example output: NGUYEN VAN AN

Do not include any explanation or additional text."""
        
        # Extract text using Qwen
        extracted_text = detector.extract_text_from_image(image_path, name_prompt)
        
        if not extracted_text:
            logger.warning(f"⚠️ No text extracted from {image_path}")
            return None
        
        logger.info(f"📝 Extracted name text: '{extracted_text}'")
        
        # Clean the extracted text
        cleaned_text = clean_and_normalize(extracted_text)
        
        if not cleaned_text:
            logger.warning("⚠️ No valid text after cleaning")
            return None
        
        # Convert student names to string list for comparison
        student_names_str = [str(name).upper() for name in student_names]
        
        # Try exact match first
        if cleaned_text in student_names_str:
            logger.info(f"✅ Exact name match found: {cleaned_text}")
            return cleaned_text
        
        # Fuzzy matching
        if student_names_str:
            best_match, score = process.extractOne(cleaned_text, student_names_str)
            if score >= 70:  # Threshold for name matching
                logger.info(f"✅ Name matched: '{cleaned_text}' → '{best_match}' (score: {score})")
                return best_match
            else:
                logger.warning(f"⚠️ Name match score too low: {score} for '{cleaned_text}'")
        
        logger.warning(f"❌ No good name match found for: '{cleaned_text}'")
        return None
        
    except Exception as e:
        logger.error(f"❌ Error in Qwen name detection: {e}")
        return None

def detect_id_student_qwen(image_path: str, student_ids: List[str]) -> Optional[str]:
    """Detect student ID using Qwen2.5-VL model"""
    try:
        detector = get_qwen_detector()
        
        if not detector.is_available():
            logger.warning("❌ Qwen detector not available")
            return None
        
        # Optimized prompt for student IDs
        id_prompt = """You are a text extraction expert. Extract the student ID from this exam paper image.

Look for these ID patterns:
1. Numbers only: 8-10 digits (e.g., 20181234, 20200456)
2. Letters + numbers: 2-6 uppercase letters followed by 6-10 digits (e.g., KHMT2101395, NNA2101302)

Return ONLY the complete ID without any explanation.
Examples: 20181234 or KHMT2101395

Do not include any additional text."""
        
        # Extract text using Qwen
        extracted_text = detector.extract_text_from_image(image_path, id_prompt)
        
        if not extracted_text:
            logger.warning(f"⚠️ No text extracted from {image_path}")
            return None
        
        logger.info(f"📝 Extracted ID text: '{extracted_text}'")
        
        # Extract patterns from the text
        # Pattern 1: Only digits (8-10 digits)
        digit_only = re.findall(r'\b\d{8,10}\b', extracted_text)
        
        # Pattern 2: Letters followed by digits
        alphanumeric = re.findall(r'\b[A-Z]{2,6}\d{6,10}\b', extracted_text)
        
        # Pattern 3: Flexible (handle spacing)
        flexible = re.findall(r'[A-Z]{2,6}\s*\d{6,10}', extracted_text)
        flexible_cleaned = [re.sub(r'\s+', '', match) for match in flexible]
        
        # Combine candidates, prioritize alphanumeric
        candidate_ids = alphanumeric + flexible_cleaned + digit_only
        
        if not candidate_ids:
            logger.warning(f"⚠️ No valid ID patterns found in: '{extracted_text}'")
            return None
        
        logger.info(f"🔍 ID candidates: {candidate_ids}")
        
        # Convert student_ids to strings
        student_ids_str = [str(sid) for sid in student_ids]
        
        # Try exact match first
        for candidate in candidate_ids:
            if candidate in student_ids_str:
                logger.info(f"✅ Exact ID match: {candidate}")
                return candidate
        
        # Fuzzy matching with different thresholds
        threshold = 60 if any(re.match(r'[A-Z]+\d+', cid) for cid in candidate_ids) else 70
        
        for candidate in candidate_ids:
            if student_ids_str:
                best_match, score = process.extractOne(candidate, student_ids_str)
                if score >= threshold:
                    logger.info(f"✅ ID matched: '{candidate}' → '{best_match}' (score: {score})")
                    return best_match
        
        logger.warning(f"❌ No good ID match for: {candidate_ids}")
        return None
        
    except Exception as e:
        logger.error(f"❌ Error in Qwen ID detection: {e}")
        return None