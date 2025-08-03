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

# Import our logging system
from logger_config import get_logger, log_subprocess_call, log_gui_event, log_function_entry, log_function_exit

# Initialize logger
logger = get_logger()

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
        log_function_entry(logger, "WorkerThread.run", args=[self.command])
        logger.info(f"Starting subprocess: {self.command}")
        log_subprocess_call(logger, self.command, "market_swimmer_gui.py")
        
        try:
            # Change to the working directory
            logger.debug(f"Changing directory to: {self.working_dir}")
            os.chdir(self.working_dir)
            
            # Run the command with proper encoding
            logger.debug(f"Creating subprocess: {self.command}")
            process = subprocess.Popen(
                self.command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                universal_newlines=True,
                encoding='utf-8',
                errors='replace'  # Replace problematic characters instead of failing
            )
            
            logger.info(f"Subprocess PID: {process.pid}")
            
            # Read output in real-time
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.output.emit(output.strip())
            
            # Get any remaining output
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                self.finished.emit("Command completed successfully!")
            else:
                error_msg = stderr if stderr else "Command failed with unknown error"
                self.error.emit(f"Command failed: {error_msg}")
                
        except Exception as e:
            self.error.emit(f"Error running command: {str(e)}")

class MarketSwimmerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        log_function_entry(logger, "MarketSwimmerGUI.__init__")
        log_gui_event(logger, "GUI_INIT_START", f"PID: {os.getpid()}")
        
        self.setWindowTitle("MarketSwimmer - Financial Analysis Tool")
        self.setGeometry(100, 100, 800, 600)
        
        logger.info("GUI window created successfully")
        
        # Set up the main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Set up styling
        self.setup_styling()
        
        # Create header
        self.create_header(layout)
        
        # Create ticker input section
        self.create_ticker_section(layout)
        
        # Create action buttons
        self.create_action_buttons(layout)
        
        # Create output display
        self.create_output_section(layout)
        
        # Create status bar
        self.create_status_section(layout)
        
        # Initialize variables
        self.current_ticker = ""
        self.worker_thread = None
        
    def setup_styling(self):
        """Set up the application styling"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QGroupBox {
                font-weight: bold;
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
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 14px;
                border-radius: 6px;
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
            QTextEdit {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #cccccc;
                border-radius: 4px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
            }
            QLabel {
                color: #333333;
            }
            QProgressBar {
                border: 2px solid #cccccc;
                border-radius: 8px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 6px;
            }
        """)
    
    def create_header(self, layout):
        """Create the header section"""
        header_frame = QFrame()
        header_layout = QVBoxLayout(header_frame)
        
        # Title
        title_label = QLabel("🏊‍♂️ MarketSwimmer Financial Analysis")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2E7D32; margin: 10px;")
        
        # Subtitle
        subtitle_label = QLabel("Analyze stock financials with Warren Buffett's Owner Earnings methodology")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #666666; font-style: italic; margin-bottom: 20px;")
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        layout.addWidget(header_frame)
    
    def create_ticker_section(self, layout):
        """Create the ticker input section"""
        ticker_group = QGroupBox("Stock Ticker")
        ticker_layout = QHBoxLayout(ticker_group)
        
        self.ticker_label = QLabel("No ticker selected")
        self.ticker_label.setStyleSheet("font-size: 14px; color: #666666;")
        
        select_ticker_btn = QPushButton("📊 Select Ticker")
        select_ticker_btn.clicked.connect(self.select_ticker)
        select_ticker_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        
        ticker_layout.addWidget(self.ticker_label)
        ticker_layout.addStretch()
        ticker_layout.addWidget(select_ticker_btn)
        
        layout.addWidget(ticker_group)
    
    def create_action_buttons(self, layout):
        """Create the main action buttons"""
        actions_group = QGroupBox("Analysis Actions")
        actions_layout = QGridLayout(actions_group)
        
        # Button 1: Full Analysis (analyze_ticker.py)
        self.full_analysis_btn = QPushButton("🚀 Complete Analysis\n(One-Click Solution)")
        self.full_analysis_btn.clicked.connect(self.run_full_analysis)
        self.full_analysis_btn.setEnabled(False)
        self.full_analysis_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                min-height: 60px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        
        # Button 2: Download & Monitor
        self.download_btn = QPushButton("📥 Download & Monitor\n(Step 1: Get XLSX Data)")
        self.download_btn.clicked.connect(self.run_download_monitor)
        self.download_btn.setEnabled(False)
        self.download_btn.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                min-height: 60px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
        """)
        
        # Button 3: Process & Visualize
        self.process_btn = QPushButton("📈 Process & Visualize\n(Steps 2-3: Calculate & Chart)")
        self.process_btn.clicked.connect(self.run_process_visualize)
        self.process_btn.setEnabled(False)
        self.process_btn.setStyleSheet("""
            QPushButton {
                background-color: #E91E63;
                min-height: 60px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #C2185B;
            }
        """)
        
        # Add buttons to grid
        actions_layout.addWidget(self.full_analysis_btn, 0, 0, 1, 2)
        actions_layout.addWidget(self.download_btn, 1, 0)
        actions_layout.addWidget(self.process_btn, 1, 1)
        
        # Add helpful descriptions
        desc_label = QLabel("""
        🚀 Complete Analysis: Automated process - opens browser, processes data, creates charts
        📥 Download & Monitor: Opens StockRow manually, monitors for XLSX downloads  
        📈 Process & Visualize: Processes existing XLSX files and creates waterfall charts
        
        Note: Complete Analysis opens StockRow in your browser - download the XLSX file manually when prompted.
        """)
        desc_label.setStyleSheet("color: #666666; font-size: 10px; padding: 10px;")
        desc_label.setWordWrap(True)
        actions_layout.addWidget(desc_label, 2, 0, 1, 2)
        
        layout.addWidget(actions_group)
    
    def create_output_section(self, layout):
        """Create the output display section"""
        output_group = QGroupBox("Output Console")
        output_layout = QVBoxLayout(output_group)
        
        self.output_text = QTextEdit()
        self.output_text.setMaximumHeight(200)
        self.output_text.setPlainText("Ready to analyze financial data...\n")
        
        # Clear button
        clear_btn = QPushButton("🗑️ Clear Output")
        clear_btn.clicked.connect(self.clear_output)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                max-width: 120px;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """)
        
        output_layout.addWidget(self.output_text)
        output_layout.addWidget(clear_btn, alignment=Qt.AlignmentFlag.AlignRight)
        
        layout.addWidget(output_group)
    
    def create_status_section(self, layout):
        """Create the status bar section"""
        status_group = QGroupBox("Status")
        status_layout = QVBoxLayout(status_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.progress_bar)
        
        layout.addWidget(status_group)
    
    def select_ticker(self):
        """Open dialog to select ticker symbol"""
        ticker, ok = QInputDialog.getText(
            self, 
            'Stock Ticker Selection', 
            'Enter ticker symbol (e.g., AAPL, TSLA, BRK.B):',
            text=self.current_ticker
        )
        
        if ok and ticker.strip():
            self.current_ticker = ticker.strip().upper()
            self.ticker_label.setText(f"Selected: {self.current_ticker}")
            self.ticker_label.setStyleSheet("font-size: 14px; color: #2E7D32; font-weight: bold;")
            
            # Enable action buttons
            self.full_analysis_btn.setEnabled(True)
            self.download_btn.setEnabled(True)
            self.process_btn.setEnabled(True)
            
            self.add_output(f"Ticker selected: {self.current_ticker}")
    
    def run_full_analysis(self):
        """Run the complete analysis using analyze_ticker_gui.py (non-interactive version)"""
        log_function_entry(logger, "run_full_analysis", args=[self.current_ticker])
        log_gui_event(logger, "BUTTON_CLICK", "Complete Analysis button clicked")
        
        if not self.current_ticker:
            logger.warning("No ticker selected for full analysis")
            self.show_error("Please select a ticker symbol first!")
            return
        
        logger.info(f"Starting complete analysis for ticker: {self.current_ticker}")
        self.add_output(f"Starting complete analysis for {self.current_ticker}...")
        python_exe = r"C:\Users\jerem\AppData\Local\Programs\Python\Python312\python.exe"
        command = f'"{python_exe}" analyze_ticker_gui.py {self.current_ticker}'
        logger.info(f"Full analysis command: {command}")
        self.run_command(command, "Complete Analysis")
    
    def run_download_monitor(self):
        """Run the download and monitor process"""
        if not self.current_ticker:
            self.show_error("Please select a ticker symbol first!")
            return
        
        self.add_output(f"Starting download process for {self.current_ticker}...")
        python_exe = r"C:\Users\jerem\AppData\Local\Programs\Python\Python312\python.exe"
        # First run get_xlsx.py, then monitor_downloads.py
        command = f'"{python_exe}" get_xlsx.py {self.current_ticker} && "{python_exe}" monitor_downloads.py --check'
        self.run_command(command, "Download & Monitor")
    
    def run_process_visualize(self):
        """Run the processing and visualization"""
        self.add_output("Starting data processing and visualization...")
        python_exe = r"C:\Users\jerem\AppData\Local\Programs\Python\Python312\python.exe"
        # Run owner_earnings.py then visualize_owner_earnings.py
        command = f'"{python_exe}" owner_earnings.py && "{python_exe}" visualize_owner_earnings.py'
        self.run_command(command, "Process & Visualize")
    
    def run_command(self, command, operation_name):
        """Run a command in a separate thread"""
        if self.worker_thread and self.worker_thread.isRunning():
            self.show_error("Another operation is already running. Please wait...")
            return
        
        # Set up UI for running state
        self.set_running_state(True, operation_name)
        
        # Create and start worker thread
        working_dir = os.path.dirname(os.path.abspath(__file__))
        self.worker_thread = WorkerThread(command, working_dir)
        self.worker_thread.finished.connect(self.on_command_finished)
        self.worker_thread.error.connect(self.on_command_error)
        self.worker_thread.output.connect(self.add_output)
        self.worker_thread.start()
    
    def set_running_state(self, running, operation=None):
        """Update UI to show running/idle state"""
        self.full_analysis_btn.setEnabled(not running and bool(self.current_ticker))
        self.download_btn.setEnabled(not running and bool(self.current_ticker))
        self.process_btn.setEnabled(not running and bool(self.current_ticker))
        
        if running:
            self.status_label.setText(f"Running: {operation}...")
            self.status_label.setStyleSheet("color: #FF9800; font-weight: bold;")
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # Indeterminate progress
        else:
            self.status_label.setText("Ready")
            self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
            self.progress_bar.setVisible(False)
    
    def on_command_finished(self, message):
        """Handle successful command completion"""
        self.set_running_state(False)
        self.add_output(f"✅ {message}")
        
        # Show completion dialog
        QMessageBox.information(self, "Success", f"Operation completed successfully!\n\n{message}")
    
    def on_command_error(self, error_message):
        """Handle command errors"""
        self.set_running_state(False)
        self.add_output(f"❌ {error_message}")
        self.show_error(f"Operation failed:\n\n{error_message}")
    
    def add_output(self, text):
        """Add text to the output console"""
        self.output_text.append(text)
        # Auto-scroll to bottom
        cursor = self.output_text.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.output_text.setTextCursor(cursor)
    
    def clear_output(self):
        """Clear the output console"""
        self.output_text.clear()
        self.add_output("Output cleared. Ready for new operations...")
    
    def show_error(self, message):
        """Show error dialog"""
        QMessageBox.critical(self, "Error", message)
    
    def closeEvent(self, event):
        """Handle application close"""
        if self.worker_thread and self.worker_thread.isRunning():
            reply = QMessageBox.question(
                self, 
                'Close Application', 
                'An operation is still running. Are you sure you want to close?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.worker_thread.terminate()
                self.worker_thread.wait()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

def main():
    """Main function to run the application"""
    app = QApplication(sys.argv)
    app.setApplicationName("MarketSwimmer")
    app.setApplicationVersion("1.0")
    
    # Set application icon (if available)
    try:
        app.setWindowIcon(QIcon("icon.png"))
    except:
        pass  # Icon file not found, continue without it
    
    # Create and show the main window
    window = MarketSwimmerGUI()
    window.show()
    
    # Start the event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
