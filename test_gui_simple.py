#!/usr/bin/env python3
"""
Simplified GUI test to debug startup issues.
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt

class SimpleGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MarketSwimmer Test")
        self.setGeometry(100, 100, 400, 300)
        
        label = QLabel("MarketSwimmer GUI Test - If you see this, PyQt6 is working!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)
        
        print("Simple GUI initialized successfully")

def main():
    print("Starting simple GUI test...")
    
    try:
        app = QApplication(sys.argv)
        print("QApplication created")
        
        window = SimpleGUI()
        print("Window created")
        
        window.show()
        print("Window shown")
        
        print("Starting event loop...")
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
