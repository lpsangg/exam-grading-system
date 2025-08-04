import os
import shutil
import glob

def cleanup_project():
    """Dọn dẹp toàn bộ dự án exam-grading-system"""
    
    project_root = r"C:\Users\Sang\Desktop\Project\exam-grading-system"
    
    # Files/folders cần xóa theo pattern
    patterns_to_remove = [
        # Test files
        "**/quick_test*.py",
        "**/test_*.py",
        "**/download_*.py",
        
        # Cache và temp
        "**/__pycache__",
        "**/.pytest_cache", 
        "**/node_modules",
        "**/build",
        "**/dist",
        "**/.next",
        
        # Log files
        "**/*.log",
        "**/*.tmp",
        "**/temp",
        "**/text",
        
        # Old venv
        "**/venv",
    ]
    
    # Specific files cần xóa
    specific_files = [
        "backend/utils/test.py",
        "backend/utils/phase1.py", 
        "backend/utils/main.py",
        "backend/utils/read_file_result.py",
        "backend/utils/read_list_of_student.py",
        "backend/text",
        ".coverage"
    ]
    
    print("🧹 BẮT ĐẦU DỌN DẸP DỰ ÁN...")
    print(f"📁 Project root: {project_root}")
    
    removed_count = 0
    
    # Xóa theo patterns
    for pattern in patterns_to_remove:
        full_pattern = os.path.join(project_root, pattern)
        matches = glob.glob(full_pattern, recursive=True)
        
        for match in matches:
            try:
                if os.path.isfile(match):
                    os.remove(match)
                    print(f"✅ Đã xóa file: {os.path.relpath(match, project_root)}")
                    removed_count += 1
                elif os.path.isdir(match):
                    shutil.rmtree(match)
                    print(f"✅ Đã xóa thư mục: {os.path.relpath(match, project_root)}")
                    removed_count += 1
            except Exception as e:
                print(f"❌ Lỗi xóa {match}: {e}")
    
    # Xóa specific files
    for file_path in specific_files:
        full_path = os.path.join(project_root, file_path)
        if os.path.exists(full_path):
            try:
                if os.path.isfile(full_path):
                    os.remove(full_path)
                    print(f"✅ Đã xóa file: {file_path}")
                    removed_count += 1
                elif os.path.isdir(full_path):
                    shutil.rmtree(full_path)
                    print(f"✅ Đã xóa thư mục: {file_path}")
                    removed_count += 1
            except Exception as e:
                print(f"❌ Lỗi xóa {file_path}: {e}")
    
    print(f"\n📊 KẾT QUẢ: Đã xóa {removed_count} files/folders")
    
    # Hiển thị cấu trúc sau khi dọn dẹp
    print("\n📁 CẤU TRÚC DỰ ÁN SAU KHI DỌN DẸP:")
    print_directory_tree(project_root, max_depth=3)

def print_directory_tree(path, prefix="", max_depth=3, current_depth=0):
    """In cấu trúc thư mục dạng tree"""
    if current_depth > max_depth:
        return
    
    try:
        items = sorted([item for item in os.listdir(path) 
                       if not item.startswith('.') or item in ['.venv', '.gitignore']])
    except PermissionError:
        return
    
    for i, item in enumerate(items):
        item_path = os.path.join(path, item)
        is_last = i == len(items) - 1
        
        current_prefix = "└── " if is_last else "├── "
        print(f"{prefix}{current_prefix}{item}")
        
        if os.path.isdir(item_path) and current_depth < max_depth:
            extension = "    " if is_last else "│   "
            print_directory_tree(item_path, prefix + extension, max_depth, current_depth + 1)

def check_file_usage():
    """Kiểm tra file nào đang được import/sử dụng"""
    
    project_root = r"C:\Users\Sang\Desktop\Project\exam-grading-system"
    backend_dir = os.path.join(project_root, "backend")
    
    print("\n🔍 KIỂM TRA FILE ĐANG SỬ DỤNG:")
    
    # Tìm tất cả Python files
    python_files = []
    for root, dirs, files in os.walk(backend_dir):
        for file in files:
            if file.endswith('.py') and not file.startswith('test_') and not file.startswith('quick_'):
                python_files.append(os.path.join(root, file))
    
    # Kiểm tra imports
    used_modules = set()
    for py_file in python_files:
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Tìm import statements
                import re
                imports = re.findall(r'from\s+(\S+)\s+import|import\s+(\S+)', content)
                for imp in imports:
                    module = imp[0] or imp[1]
                    if module.startswith('utils.'):
                        used_modules.add(module.replace('utils.', ''))
                    elif module in ['detectInfo', 'qwen_detector', 'detectCodeBox', 'detectGrade']:
                        used_modules.add(module)
        except Exception as e:
            print(f"❌ Lỗi đọc {py_file}: {e}")
    
    print("✅ Modules đang được sử dụng:")
    for module in sorted(used_modules):
        print(f"   - {module}")

if __name__ == "__main__":
    cleanup_project()
    check_file_usage()