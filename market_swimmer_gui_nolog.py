import sys
import os
import subprocess
import threading
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QPushButton, QLabel, QInputDialog, QTextEdit, 
                             QMessageBox, QProgressBar, QFrame, QGroupBox, QGridLayout)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor, QTextCursor

# Dummy logging functions to replace logging
def log_function_entry(*args, **kwargs):
    pass

def log_gui_event(*args, **kwargs):
    pass

def log_subprocess_call(*args, **kwargs):
    pass

def log_function_exit(*args, **kwargs):
    pass

class DummyLogger:
    def info(self, msg): print(f"[INFO] {msg}")
    def debug(self, msg): pass
    def warning(self, msg): print(f"[WARNING] {msg}")
    def error(self, msg): print(f"[ERROR] {msg}")

logger = DummyLogger()

class WorkerThread(QThread):
    """Thread for running long-running tasks without blocking the GUI"""
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    output = pyqtSignal(str)
    
    def __init__(self, command, working_dir):
        super().__init__()
        self.command = command
        self.working_dir = working_dir

    def run(self):
        try:
            os.chdir(self.working_dir)
            
            process = subprocess.Popen(
                self.command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                universal_newlines=True,
                encoding='utf-8',
                errors='replace'
            )
            
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.output.emit(output.strip())
            
            stdout, stderr = process.communicate()
            
            if stdout:
                for line in stdout.split('\n'):
                    if line.strip():
                        self.output.emit(line.strip())
            
            if process.returncode == 0:
                self.finished.emit("Process completed successfully!")
            else:
                error_msg = f"Process failed with return code {process.returncode}"
                if stderr:
                    error_msg += f"\nError: {stderr}"
                self.error.emit(error_msg)
                
        except Exception as e:
            self.error.emit(f"Error running command: {str(e)}")

class MarketSwimmerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MarketSwimmer - Financial Analysis Tool")
        self.setGeometry(100, 100, 800, 600)
        
        print("GUI window created successfully")
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        self.setup_styling()
        self.create_header(layout)
        self.create_ticker_section(layout)
        self.create_action_buttons(layout)
        self.create_output_section(layout)
        self.create_status_section(layout)
        
        self.current_ticker = ""
        self.worker_thread = None
        
        print("GUI initialization completed")

    def setup_styling(self):
        """Set up the application styling"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QGroupBox {
                font-weight: bold;
                font-size: 12px;
                border: 2px solid #cccccc;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 12px 24px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 14px;
                margin: 4px 2px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)

    def create_header(self, layout):
        """Create the header section"""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Shape.Box)
        header_frame.setStyleSheet("background-color: white; padding: 10px; border-radius: 8px;")
        header_layout = QVBoxLayout(header_frame)
        
        title_label = QLabel("🏊 MarketSwimmer Financial Analysis")
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2E7D32; margin: 10px;")
        
        subtitle_label = QLabel("Analyze stock financials with Warren Buffett's Owner Earnings methodology")
        subtitle_label.setFont(QFont("Arial", 10))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #666666; font-style: italic; margin-bottom: 10px;")
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        layout.addWidget(header_frame)

    def create_ticker_section(self, layout):
        """Create the ticker selection section"""
        ticker_group = QGroupBox("Stock Ticker")
        ticker_layout = QHBoxLayout(ticker_group)
        
        self.ticker_label = QLabel("No ticker selected")
        self.ticker_label.setFont(QFont("Arial", 12))
        self.ticker_label.setStyleSheet("color: #666666; padding: 5px;")
        
        self.select_ticker_btn = QPushButton("🎯 Select Ticker")
        self.select_ticker_btn.setStyleSheet("background-color: #2196F3;")
        self.select_ticker_btn.clicked.connect(self.select_ticker)
        
        ticker_layout.addWidget(self.ticker_label)
        ticker_layout.addStretch()
        ticker_layout.addWidget(self.select_ticker_btn)
        
        layout.addWidget(ticker_group)

    def create_action_buttons(self, layout):
        """Create the action buttons section"""
        actions_group = QGroupBox("Analysis Actions")
        actions_layout = QVBoxLayout(actions_group)
        
        # Complete Analysis Button (Full Width)
        self.complete_btn = QPushButton("🚀 Complete Analysis\n(One-Click Solution)")
        self.complete_btn.setStyleSheet("background-color: #FF9800; min-height: 60px; font-size: 16px;")
        self.complete_btn.clicked.connect(self.run_full_analysis)
        self.complete_btn.setEnabled(False)
        actions_layout.addWidget(self.complete_btn)
        
        # Two smaller buttons side by side
        button_row_layout = QHBoxLayout()
        
        self.download_btn = QPushButton("📥 Download & Monitor\nStep 1 & 2 Only")
        self.download_btn.setStyleSheet("background-color: #9C27B0; min-height: 60px;")
        self.download_btn.clicked.connect(self.run_download_monitor)
        self.download_btn.setEnabled(False)
        
        self.process_btn = QPushButton("📊 Process & Visualize\nStep 3 & 4 Only")
        self.process_btn.setStyleSheet("background-color: #E91E63; min-height: 60px;")
        self.process_btn.clicked.connect(self.run_process_visualize)
        self.process_btn.setEnabled(False)
        
        button_row_layout.addWidget(self.download_btn)
        button_row_layout.addWidget(self.process_btn)
        actions_layout.addLayout(button_row_layout)
        
        # Help text
        help_label = QLabel("""
📋 Complete Analysis: Automated process - opens browser, processes data, creates charts
📥 Download & Monitor: Opens StockRow manually, monitors for XLSX downloads
📊 Process & Visualize: Processes existing XLSX files and creates waterfall charts

Note: Complete Analysis opens StockRow in your browser - download the XLSX file manually when prompted.
        """)
        help_label.setFont(QFont("Arial", 9))
        help_label.setStyleSheet("color: #666666; background-color: #f9f9f9; padding: 10px; border-radius: 5px;")
        help_label.setWordWrap(True)
        actions_layout.addWidget(help_label)
        
        layout.addWidget(actions_group)

    def create_output_section(self, layout):
        """Create the output console section"""
        output_group = QGroupBox("Output Console")
        output_layout = QVBoxLayout(output_group)
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Consolas", 9))
        self.output_text.setStyleSheet("""
            background-color: #2b2b2b;
            color: #ffffff;
            border: 1px solid #555555;
            border-radius: 4px;
            padding: 8px;
        """)
        self.output_text.setMaximumHeight(200)
        
        # Clear button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.clear_btn = QPushButton("🗑️ Clear Output")
        self.clear_btn.setStyleSheet("background-color: #757575; min-height: 30px;")
        self.clear_btn.clicked.connect(self.clear_output)
        button_layout.addWidget(self.clear_btn)
        
        output_layout.addWidget(self.output_text)
        output_layout.addLayout(button_layout)
        layout.addWidget(output_group)

    def create_status_section(self, layout):
        """Create the status section"""
        status_group = QGroupBox("Status")
        status_layout = QVBoxLayout(status_group)
        
        self.status_label = QLabel("Ready")
        self.status_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.status_label.setStyleSheet("color: #4CAF50; padding: 5px;")
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.progress_bar)
        layout.addWidget(status_group)
        
        self.add_output("Ready to analyze financial data...")

    def select_ticker(self):
        """Open dialog to select ticker symbol"""
        ticker, ok = QInputDialog.getText(self, 'Select Ticker', 'Enter ticker symbol (e.g., AAPL, TSLA, BRK.B):')
        
        if ok and ticker:
            self.current_ticker = ticker.upper().strip()
            self.ticker_label.setText(f"Selected: {self.current_ticker}")
            self.ticker_label.setStyleSheet("color: #4CAF50; font-weight: bold; padding: 5px;")
            
            # Enable action buttons
            self.complete_btn.setEnabled(True)
            self.download_btn.setEnabled(True)
            self.process_btn.setEnabled(True)
            
            self.add_output(f"Ticker selected: {self.current_ticker}")

    def run_full_analysis(self):
        """Run the complete analysis"""
        if not self.current_ticker:
            self.show_error("Please select a ticker symbol first!")
            return
        
        self.add_output(f"Starting complete analysis for {self.current_ticker}...")
        python_exe = r"C:\Users\jerem\AppData\Local\Programs\Python\Python312\python.exe"
        command = f'"{python_exe}" analyze_ticker_gui.py {self.current_ticker}'
        self.run_command(command, "Complete Analysis")

    def run_download_monitor(self):
        """Run the download and monitor process"""
        if not self.current_ticker:
            self.show_error("Please select a ticker symbol first!")
            return
        
        self.add_output(f"Starting download process for {self.current_ticker}...")
        # Open StockRow download page
        import webbrowser
        url = f"https://stockrow.com/vector/exports/financials/{self.current_ticker}?direction=desc"
        webbrowser.open(url)
        self.add_output(f"Opened: {url}")
        self.add_output("Please download the XLSX file manually from the browser")

    def run_process_visualize(self):
        """Process existing data and create visualizations"""
        self.add_output("Starting data processing and visualization...")
        python_exe = r"C:\Users\jerem\AppData\Local\Programs\Python\Python312\python.exe"
        command = f'"{python_exe}" owner_earnings.py && "{python_exe}" visualize_owner_earnings.py'
        self.run_command(command, "Process & Visualize")

    def run_command(self, command, task_name):
        """Run a command in a worker thread"""
        if self.worker_thread and self.worker_thread.isRunning():
            self.show_error("Another task is already running!")
            return
        
        self.add_output(f"Running: {task_name}...")
        self.set_status(f"Running: {task_name}...", True)
        
        self.worker_thread = WorkerThread(command, os.getcwd())
        self.worker_thread.output.connect(self.add_output)
        self.worker_thread.finished.connect(lambda msg: self.task_finished(msg, task_name))
        self.worker_thread.error.connect(lambda msg: self.task_error(msg, task_name))
        self.worker_thread.start()

    def task_finished(self, message, task_name):
        """Handle task completion"""
        self.add_output(f"✅ {task_name} completed successfully!")
        self.set_status("Ready", False)

    def task_error(self, message, task_name):
        """Handle task error"""
        self.add_output(f"❌ {task_name} failed: {message}")
        self.set_status("Ready", False)

    def add_output(self, text):
        """Add text to the output console"""
        self.output_text.append(text)
        cursor = self.output_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.output_text.setTextCursor(cursor)

    def clear_output(self):
        """Clear the output console"""
        self.output_text.clear()
        self.add_output("Output cleared. Ready to analyze financial data...")

    def set_status(self, text, show_progress=False):
        """Update the status label and progress bar"""
        self.status_label.setText(text)
        self.progress_bar.setVisible(show_progress)
        if show_progress:
            self.progress_bar.setRange(0, 0)  # Indeterminate progress

    def show_error(self, message):
        """Show an error message dialog"""
        QMessageBox.critical(self, "Error", message)

def main():
    """Main function to run the application"""
    print("Starting MarketSwimmer GUI...")
    
    try:
        app = QApplication(sys.argv)
        app.setApplicationName("MarketSwimmer")
        app.setApplicationVersion("1.0")
        
        print("Creating GUI window...")
        window = MarketSwimmerGUI()
        
        print("Showing window...")
        window.show()
        
        print("Starting event loop...")
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"Error starting GUI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
