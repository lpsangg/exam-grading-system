"""
Setup script for migrating from local Qwen to Ollama
This script helps install and configure Ollama for the exam grading system
"""

import subprocess
import sys
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_ollama_installed():
    """Check if Ollama is installed on the system"""
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, text=True, check=True)
        logger.info(f"✅ Ollama is installed: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.warning("❌ Ollama is not installed or not in PATH")
        return False

def install_ollama_windows():
    """Instructions for installing Ollama on Windows"""
    logger.info("📥 To install Ollama on Windows:")
    logger.info("1. Download Ollama from: https://ollama.ai/download/windows")
    logger.info("2. Run the installer")
    logger.info("3. Restart your terminal")
    logger.info("4. Run this script again")

def start_ollama_service():
    """Start Ollama service"""
    try:
        logger.info("🚀 Starting Ollama service...")
        subprocess.Popen(['ollama', 'serve'], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        logger.info("✅ Ollama service started in background")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to start Ollama service: {e}")
        return False

def pull_qwen_model():
    """Pull Qwen2-VL model from Ollama registry"""
    try:
        logger.info("📥 Pulling Qwen2-VL model (this may take a while)...")
        
        # Try different model variants
        models_to_try = [
            "qwen2-vl:3b",
            "qwen2-vl:latest", 
            "qwen2-vl"
        ]
        
        for model in models_to_try:
            try:
                logger.info(f"Trying to pull {model}...")
                result = subprocess.run(['ollama', 'pull', model], 
                                      capture_output=True, text=True, check=True)
                logger.info(f"✅ Successfully pulled {model}")
                return model
            except subprocess.CalledProcessError:
                logger.warning(f"⚠️ Failed to pull {model}, trying next...")
                continue
                
        logger.error("❌ Failed to pull any Qwen2-VL model")
        return None
        
    except Exception as e:
        logger.error(f"❌ Error pulling model: {e}")
        return None

def list_available_models():
    """List models available in Ollama"""
    try:
        result = subprocess.run(['ollama', 'list'], 
                              capture_output=True, text=True, check=True)
        logger.info("📋 Available models in Ollama:")
        logger.info(result.stdout)
        return True
    except Exception as e:
        logger.error(f"❌ Error listing models: {e}")
        return False

def test_ollama_connection():
    """Test connection to Ollama service"""
    try:
        # Import here to avoid issues if ollama package not installed
        import ollama
        
        client = ollama.Client()
        models = client.list()
        
        logger.info("✅ Successfully connected to Ollama service")
        logger.info(f"📊 Available models: {len(models['models'])}")
        
        for model in models['models']:
            logger.info(f"   - {model['name']}")
            
        return True
        
    except ImportError:
        logger.error("❌ ollama package not installed. Install with: pip install ollama")
        return False
    except Exception as e:
        logger.error(f"❌ Failed to connect to Ollama: {e}")
        logger.info("💡 Make sure Ollama service is running: ollama serve")
        return False

def install_python_dependencies():
    """Install required Python packages"""
    try:
        logger.info("📦 Installing Python dependencies...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'ollama'], check=True)
        logger.info("✅ ollama package installed")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to install dependencies: {e}")
        return False

def cleanup_old_model_files():
    """Clean up old Qwen model files to save space"""
    model_dir = r"C:\Users\Sang\Desktop\Project\exam-grading-system\backend\models"
    
    if os.path.exists(model_dir):
        try:
            import shutil
            logger.info(f"🧹 Cleaning up old model files in {model_dir}")
            
            # List files to be removed
            for item in os.listdir(model_dir):
                item_path = os.path.join(model_dir, item)
                if os.path.isdir(item_path) and "Qwen" in item:
                    size = sum(os.path.getsize(os.path.join(dirpath, filename))
                              for dirpath, dirnames, filenames in os.walk(item_path)
                              for filename in filenames) / (1024**3)  # GB
                    logger.info(f"   📁 {item} (~{size:.1f} GB)")
            
            response = input("Do you want to remove old Qwen model files? (y/N): ")
            if response.lower() == 'y':
                for item in os.listdir(model_dir):
                    item_path = os.path.join(model_dir, item)
                    if os.path.isdir(item_path) and "Qwen" in item:
                        shutil.rmtree(item_path)
                        logger.info(f"✅ Removed {item}")
                logger.info("🎉 Cleanup completed!")
            else:
                logger.info("⏭️  Skipped cleanup")
                
        except Exception as e:
            logger.error(f"❌ Error during cleanup: {e}")

def main():
    """Main setup function"""
    logger.info("🔧 OLLAMA SETUP FOR EXAM GRADING SYSTEM")
    logger.info("=" * 50)
    
    # Step 1: Check if Ollama is installed
    if not check_ollama_installed():
        install_ollama_windows()
        return
    
    # Step 2: Install Python dependencies
    if not install_python_dependencies():
        return
    
    # Step 3: Start Ollama service
    start_ollama_service()
    
    # Wait a moment for service to start
    import time
    time.sleep(2)
    
    # Step 4: Test connection
    if not test_ollama_connection():
        return
    
    # Step 5: Pull Qwen model
    model_name = pull_qwen_model()
    if not model_name:
        logger.error("❌ Failed to setup Qwen model")
        return
    
    # Step 6: List available models
    list_available_models()
    
    # Step 7: Optional cleanup
    cleanup_old_model_files()
    
    logger.info("\n🎉 SETUP COMPLETED SUCCESSFULLY!")
    logger.info("=" * 50)
    logger.info("🚀 Your exam grading system is now using Ollama!")
    logger.info(f"📋 Model available: {model_name}")
    logger.info("\n📝 Next steps:")
    logger.info("1. Make sure Ollama service is running: ollama serve")
    logger.info("2. Test your application")
    logger.info("3. If you encounter issues, check the logs")
    
    logger.info("\n💡 Useful commands:")
    logger.info("   - Start Ollama: ollama serve")
    logger.info("   - List models: ollama list")
    logger.info("   - Pull models: ollama pull <model-name>")
    logger.info("   - Remove models: ollama rm <model-name>")

if __name__ == "__main__":
    main()
