"""
Quick Ollama installation guide and troubleshooting
"""

# Step 1: Install Ollama
# Download from: https://ollama.ai/download/windows
# Run the installer

# Step 2: Fix Ollama directory issue
# The error suggests Ollama directory already exists but has permission issues

import os
import subprocess

def fix_ollama_directory():
    """Fix Ollama directory permission issues"""
    ollama_dir = os.path.expanduser("~/.ollama")
    
    try:
        # Remove existing directory if it has issues
        if os.path.exists(ollama_dir):
            import shutil
            shutil.rmtree(ollama_dir)
            print(f"✅ Removed problematic directory: {ollama_dir}")
        
        # Start Ollama service (will recreate directory)
        print("🚀 Starting Ollama service...")
        subprocess.Popen(['ollama', 'serve'], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        
        print("✅ Ollama service started")
        return True
        
    except Exception as e:
        print(f"❌ Failed to fix Ollama: {e}")
        return False

def install_qwen_model():
    """Install Qwen model after Ollama is fixed"""
    try:
        # Wait a moment for service to start
        import time
        time.sleep(3)
        
        # Pull the model
        result = subprocess.run(['ollama', 'pull', 'qwen2-vl:3b'], 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Qwen model installed successfully")
            return True
        else:
            print(f"❌ Failed to install model: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error installing model: {e}")
        return False

if __name__ == "__main__":
    print("🔧 FIXING OLLAMA ISSUES")
    print("=" * 40)
    
    if fix_ollama_directory():
        if install_qwen_model():
            print("\n🎉 OLLAMA SETUP COMPLETED!")
            print("You can now test your application again.")
        else:
            print("\n⚠️ Ollama service started but model installation failed")
            print("Try running: ollama pull qwen2-vl:3b")
    else:
        print("\n❌ Failed to fix Ollama")
        print("Manual steps:")
        print("1. Download Ollama from: https://ollama.ai/download")
        print("2. Run as administrator")
        print("3. Restart terminal")
        print("4. Run: ollama serve")
        print("5. Run: ollama pull qwen2-vl:3b")
