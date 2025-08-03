import sys
print("Python executable:", sys.executable)
print("Python version:", sys.version)

try:
    from PyQt6.QtWidgets import QApplication
    print("✅ PyQt6.QtWidgets imported successfully")
    
    from PyQt6.QtCore import Qt
    print("✅ PyQt6.QtCore imported successfully")
    
    from PyQt6.QtGui import QFont
    print("✅ PyQt6.QtGui imported successfully")
    
    print("✅ All PyQt6 imports successful - GUI should work!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    
except Exception as e:
    print(f"❌ Unexpected error: {e}")
