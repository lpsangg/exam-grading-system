"""
Ollama Qwen2.5-VL detector for text extraction from images
Uses Ollama server running locally
"""

import logging
import re
import os
import base64
from typing import List, Optional
from PIL import Image
import ollama
from fuzzywuzzy import process

logger = logging.getLogger(__name__)

class OllamaDetector:
    """Ollama Qwen2.5-VL model wrapper for text detection"""
    
    def __init__(self, model_name: str = "qwen2-vl:3b"):
        self.model_name = model_name
        self.client = ollama.Client()
        self._check_model_availability()
    
    def _check_model_availability(self):
        """Check if Qwen model is available in Ollama"""
        try:
            # List available models
            models = self.client.list()
            available_models = [model['name'] for model in models['models']]
            
            if self.model_name not in available_models:
                logger.warning(f"⚠️ Model {self.model_name} not found in Ollama")
                logger.info("📥 Available models:")
                for model in available_models:
                    logger.info(f"   - {model}")
                logger.info(f"💡 To install the model, run: ollama pull {self.model_name}")
            else:
                logger.info(f"✅ Model {self.model_name} is available in Ollama")
                
        except Exception as e:
            logger.error(f"❌ Failed to connect to Ollama: {e}")
            logger.info("💡 Make sure Ollama is running. Start it with: ollama serve")
    
    def is_available(self) -> bool:
        """Check if Ollama service and model are available"""
        try:
            # Test connection to Ollama
            models = self.client.list()
            available_models = [model['name'] for model in models['models']]
            return self.model_name in available_models
        except Exception as e:
            logger.error(f"❌ Ollama not available: {e}")
            return False
    
    def _encode_image_to_base64(self, image_path: str) -> Optional[str]:
        """Convert image to base64 string for Ollama"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            logger.error(f"❌ Failed to encode image: {e}")
            return None
    
    def extract_text_from_image(self, image_path: str, prompt: str) -> Optional[str]:
        """Extract text from image using Ollama Qwen model"""
        if not self.is_available():
            logger.warning("❌ Ollama model not available")
            return None
        
        if not os.path.exists(image_path):
            logger.warning(f"❌ Image file not found: {image_path}")
            return None
        
        try:
            logger.info(f"🔍 Processing image with Ollama: {os.path.basename(image_path)}")
            
            # Encode image to base64
            image_base64 = self._encode_image_to_base64(image_path)
            if not image_base64:
                return None
            
            # Prepare the request for Ollama
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                images=[image_base64],
                options={
                    'temperature': 0.1,
                    'top_p': 0.9,
                    'max_tokens': 128
                }
            )
            
            if response and 'response' in response:
                result = response['response'].strip()
                logger.info(f"✅ Ollama extracted: '{result}'")
                return result
            else:
                logger.warning("⚠️ Ollama returned empty result")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error extracting text with Ollama: {e}")
            return None

# Global detector instance
_detector_instance = None

def get_ollama_detector(model_name: str = "qwen2-vl:3b") -> OllamaDetector:
    """Get singleton Ollama detector instance"""
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = OllamaDetector(model_name)
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

def detect_name_student_ollama(image_path: str, student_names: List[str]) -> Optional[str]:
    """Detect student name using Ollama Qwen2.5-VL model"""
    try:
        detector = get_ollama_detector()
        
        if not detector.is_available():
            logger.warning("❌ Ollama detector not available")
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
        
        # Extract text using Ollama
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
        logger.error(f"❌ Error in Ollama name detection: {e}")
        return None

def detect_id_student_ollama(image_path: str, student_ids: List[str]) -> Optional[str]:
    """Detect student ID using Ollama Qwen2.5-VL model"""
    try:
        detector = get_ollama_detector()
        
        if not detector.is_available():
            logger.warning("❌ Ollama detector not available")
            return None
        
        # Optimized prompt for student IDs
        id_prompt = """You are a text extraction expert. Extract the student ID from this exam paper image.

Look for these ID patterns:
1. Numbers only: 8-10 digits (e.g., 20181234, 20200456)
2. Letters + numbers: 2-6 uppercase letters followed by 6-10 digits (e.g., KHMT2101395, NNA2101302)

Return ONLY the complete ID without any explanation.
Examples: 20181234 or KHMT2101395

Do not include any additional text."""
        
        # Extract text using Ollama
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
        logger.error(f"❌ Error in Ollama ID detection: {e}")
        return None
