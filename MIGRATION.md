# Migration from Qwen Local to Ollama

This document describes the migration from using local Qwen2.5-VL model to Ollama for the exam grading system.

## 🎯 Why Migrate to Ollama?

- **Easier Setup**: No need to download large model files manually
- **Better Resource Management**: Ollama handles model loading/unloading automatically
- **Simplified Dependencies**: Fewer Python packages required
- **Model Updates**: Easy to update models through Ollama
- **Multiple Models**: Can easily switch between different models

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Run Setup Script
```bash
python setup_ollama.py
```

This script will:
- Check if Ollama is installed
- Install Python dependencies
- Start Ollama service
- Pull Qwen2-VL model
- Test the connection

### 3. Manual Ollama Installation (if needed)

If the setup script indicates Ollama is not installed:

1. **Download Ollama**: Go to https://ollama.ai/download/windows
2. **Install**: Run the installer
3. **Restart** your terminal
4. **Run setup again**: `python setup_ollama.py`

## 📋 Manual Setup Steps

If you prefer manual setup:

### 1. Install Ollama
```bash
# Download from https://ollama.ai/download
# Then install the downloaded file
```

### 2. Start Ollama Service
```bash
ollama serve
```

### 3. Pull Qwen Model
```bash
# Try these models in order:
ollama pull qwen2-vl:3b
# or
ollama pull qwen2-vl:latest  
# or
ollama pull qwen2-vl
```

### 4. Test Connection
```python
import ollama
client = ollama.Client()
models = client.list()
print(models)
```

## 🔧 Configuration

### Model Configuration

Edit `backend/utils/ollama_detector.py` if you want to use a different model:

```python
# Change this line in OllamaDetector.__init__()
def __init__(self, model_name: str = "qwen2-vl:3b"):  # Change model name here
```

### Available Models

Check available Qwen models:
```bash
ollama list | grep qwen
```

## 🆚 Differences from Previous Implementation

### Before (Local Qwen)
```python
# Old import
from .qwen_detector import detect_name_student_qwen, detect_id_student_qwen

# Old usage
result = detect_name_student_qwen(image_path, student_names)
```

### After (Ollama)
```python
# New import  
from .ollama_detector import detect_name_student_ollama, detect_id_student_ollama

# New usage
result = detect_name_student_ollama(image_path, student_names)
```

### Function Parameters

The function signatures remain the same, so existing code continues to work:

```python
# Both old and new versions support:
detect_name_student(image_path, student_names, use_model=True)
detect_id_student(image_path, student_ids, use_model=True)
```

## 🐛 Troubleshooting

### Ollama Service Not Running
```bash
# Start the service
ollama serve

# Check if it's running
curl http://localhost:11434/api/version
```

### Model Not Found
```bash
# List available models
ollama list

# Pull the model if missing
ollama pull qwen2-vl:3b
```

### Connection Errors
```python
# Test connection in Python
import ollama
try:
    client = ollama.Client()
    models = client.list()
    print("✅ Connection successful")
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

### Performance Issues

If Ollama is slow:

1. **Check system resources**: Ollama needs sufficient RAM
2. **Try smaller model**: Use `qwen2-vl:1.5b` instead of `qwen2-vl:3b`
3. **Adjust Ollama settings**: See Ollama documentation

### Memory Issues

If you get out-of-memory errors:

```bash
# Remove unused models to free space
ollama rm <unused-model-name>

# Check disk space
ollama list
```

## 📊 Performance Comparison

| Aspect | Local Qwen | Ollama |
|--------|------------|--------|
| Setup Time | Long (model download) | Medium (Ollama + model) |
| Disk Space | ~6-8 GB | ~6-8 GB |
| Memory Usage | High (always loaded) | Dynamic (loads on demand) |
| Startup Time | Slow | Fast |
| Model Updates | Manual | Automatic |
| Multi-model Support | Limited | Excellent |

## 🔄 Fallback Mechanism

The system maintains fallback to traditional OCR if Ollama fails:

1. **Ollama** (primary)
2. **EasyOCR** (fallback 1)
3. **Tesseract** (fallback 2)

## 📝 Files Changed

### Modified Files:
- `backend/requirements.txt` - Updated dependencies
- `backend/utils/detectInfo.py` - Updated to use Ollama

### New Files:
- `backend/utils/ollama_detector.py` - Ollama implementation
- `backend/setup_ollama.py` - Setup script
- `MIGRATION.md` - This documentation

### Deprecated Files:
- `backend/utils/qwen_detector.py` - Can be removed after migration
- `backend/models/Qwen2.5-VL-3B-Instruct/` - Can be removed to save space

## 🎉 Post-Migration Cleanup

After confirming Ollama works correctly:

### Remove Old Dependencies
```bash
pip uninstall transformers torch accelerate qwen-vl-utils
```

### Remove Old Model Files
```bash
# This can free up 6-8 GB of disk space
rm -rf backend/models/Qwen2.5-VL-3B-Instruct
```

### Update Documentation
Update any documentation that references the old Qwen setup.

## 📞 Support

If you encounter issues:

1. **Check logs**: Look for error messages in the application logs
2. **Verify Ollama**: Run `ollama list` to check if models are available
3. **Test independently**: Try Ollama commands directly
4. **Fallback**: The system should fallback to traditional OCR if Ollama fails

## 🔗 Useful Links

- [Ollama Documentation](https://ollama.ai/docs)
- [Qwen2-VL Model](https://ollama.ai/library/qwen2-vl)
- [Ollama Python Package](https://pypi.org/project/ollama/)
- [Ollama GitHub](https://github.com/ollama/ollama)
