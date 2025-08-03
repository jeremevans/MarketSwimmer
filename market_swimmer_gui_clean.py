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

class WorkerThread(QThread):
    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        print(f"[DEBUG] Starting subprocess: {self.command}")
        
        try:
            # Change to the correct directory
            os.chdir(Path(__file__).parent)
            print(f"[DEBUG] Working directory: {Path(__file__).parent}")
            
            # Create the subprocess
            process = subprocess.Popen(
                self.command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            print(f"[DEBUG] Subprocess PID: {process.pid}")
            
            # Read output in real-time
            for line in iter(process.stdout.readline, ''):
                if line:
                    self.output_signal.emit(line.rstrip())
            
            # Wait for process to complete
            process.wait()
            
            if process.returncode == 0:
                print(f"[DEBUG] Process completed successfully with return code: {process.returncode}")
                self.finished_signal.emit()
            else:
                error_msg = f"Process failed with return code: {process.returncode}"
                print(f"[ERROR] {error_msg}")
                self.error_signal.emit(error_msg)
                
        except Exception as e:
            error_msg = f"Error running subprocess: {str(e)}"
            print(f"[ERROR] {error_msg}")
            self.error_signal.emit(error_msg)

class MarketSwimmerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("MarketSwimmer - Financial Analysis Tool (No Logging)")
        self.setGeometry(100, 100, 1000, 700)
        
        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
                background-color: white;
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
                padding: 8px 16px;
                text-align: center;
                font-size: 14px;
                border-radius: 4px;
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
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
                background-color: #fafafa;
            }
            QLabel {
                font-size: 12px;
                color: #333;
            }
        """)

        # Initialize UI
        self.init_ui()
        
        # Current ticker
        self.current_ticker = ""
        
        print("[INFO] GUI window created successfully")

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Title
        title_label = QLabel("MarketSwimmer Financial Analysis")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; margin: 10px;")
        main_layout.addWidget(title_label)
        
        # Ticker input section
        ticker_group = QGroupBox("Stock Ticker Selection")
        ticker_layout = QHBoxLayout(ticker_group)
        
        self.ticker_label = QLabel("Selected Ticker: None")
        self.ticker_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2980b9;")
        
        self.select_ticker_button = QPushButton("Select Ticker")
        self.select_ticker_button.clicked.connect(self.select_ticker)
        
        ticker_layout.addWidget(self.ticker_label)
        ticker_layout.addStretch()
        ticker_layout.addWidget(self.select_ticker_button)
        
        main_layout.addWidget(ticker_group)
        
        # Analysis buttons section
        analysis_group = QGroupBox("Analysis Options")
        analysis_layout = QGridLayout(analysis_group)
        
        # Individual analysis buttons
        self.download_button = QPushButton("Download Financial Data")
        self.download_button.clicked.connect(self.download_data)
        self.download_button.setEnabled(False)
        
        self.earnings_button = QPushButton("Calculate Owner Earnings")
        self.earnings_button.clicked.connect(self.calculate_earnings)
        self.earnings_button.setEnabled(False)
        
        self.visualize_button = QPushButton("Create Visualizations")
        self.visualize_button.clicked.connect(self.create_visualizations)
        self.visualize_button.setEnabled(False)
        
        self.complete_button = QPushButton("Complete Analysis")
        self.complete_button.clicked.connect(self.run_full_analysis)
        self.complete_button.setEnabled(False)
        self.complete_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                font-size: 16px;
                padding: 12px 24px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)
        
        # Arrange buttons in grid
        analysis_layout.addWidget(self.download_button, 0, 0)
        analysis_layout.addWidget(self.earnings_button, 0, 1)
        analysis_layout.addWidget(self.visualize_button, 1, 0)
        analysis_layout.addWidget(self.complete_button, 1, 1)
        
        main_layout.addWidget(analysis_group)
        
        # Console output section
        console_group = QGroupBox("Console Output")
        console_layout = QVBoxLayout(console_group)
        
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        self.console_output.setMinimumHeight(300)
        console_layout.addWidget(self.console_output)
        
        # Clear console button
        clear_button = QPushButton("Clear Console")
        clear_button.clicked.connect(self.clear_console)
        clear_button.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                max-width: 150px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        console_layout.addWidget(clear_button)
        
        main_layout.addWidget(console_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Status bar
        self.statusBar().showMessage("Ready - Select a ticker to begin analysis")

    def select_ticker(self):
        print("[DEBUG] Select Ticker button clicked")
        
        ticker, ok = QInputDialog.getText(self, 'Select Ticker', 'Enter stock ticker symbol:')
        
        if ok and ticker:
            ticker = ticker.upper().strip()
            self.current_ticker = ticker
            self.ticker_label.setText(f"Selected Ticker: {ticker}")
            
            # Enable analysis buttons
            self.download_button.setEnabled(True)
            self.earnings_button.setEnabled(True)
            self.visualize_button.setEnabled(True)
            self.complete_button.setEnabled(True)
            
            self.console_output.append(f"✓ Ticker selected: {ticker}")
            self.statusBar().showMessage(f"Ticker selected: {ticker} - Ready for analysis")
            
            print(f"[INFO] Ticker selected: {ticker}")

    def download_data(self):
        if not self.current_ticker:
            QMessageBox.warning(self, "Warning", "Please select a ticker first.")
            return
            
        print(f"[INFO] Starting data download for ticker: {self.current_ticker}")
        
        self.console_output.append(f"\n🔄 Starting data download for {self.current_ticker}...")
        self.disable_buttons()
        self.show_progress()
        
        # Download command with monitoring
        command = f'"{sys.executable}" get_xlsx.py {self.current_ticker} && "{sys.executable}" monitor_downloads.py --check'
        self.run_command(command)

    def calculate_earnings(self):
        if not self.current_ticker:
            QMessageBox.warning(self, "Warning", "Please select a ticker first.")
            return
            
        print(f"[INFO] Starting earnings calculation for ticker: {self.current_ticker}")
        
        self.console_output.append(f"\n📊 Calculating owner earnings for {self.current_ticker}...")
        self.disable_buttons()
        self.show_progress()
        
        command = f'"{sys.executable}" owner_earnings_fixed.py'
        self.run_command(command)

    def create_visualizations(self):
        if not self.current_ticker:
            QMessageBox.warning(self, "Warning", "Please select a ticker first.")
            return
            
        print(f"[INFO] Starting visualization creation for ticker: {self.current_ticker}")
        
        self.console_output.append(f"\n📈 Creating visualizations for {self.current_ticker}...")
        self.disable_buttons()
        self.show_progress()
        
        command = f'"{sys.executable}" visualize_owner_earnings.py'
        self.run_command(command)

    def run_full_analysis(self):
        if not self.current_ticker:
            QMessageBox.warning(self, "Warning", "Please select a ticker first.")
            return
            
        print(f"[INFO] Starting complete analysis for ticker: {self.current_ticker}")
        
        self.console_output.append(f"\n🚀 Starting complete analysis for {self.current_ticker}...")
        self.console_output.append("This will run the full analysis pipeline:")
        self.console_output.append("  1. Download financial data")
        self.console_output.append("  2. Calculate owner earnings")  
        self.console_output.append("  3. Create visualizations")
        self.console_output.append("Please wait...\n")
        
        self.disable_buttons()
        self.show_progress()
        
        # Full analysis command
        command = f'"{sys.executable}" analyze_ticker_gui.py {self.current_ticker}'
        print(f"[INFO] Full analysis command: {command}")
        
        self.run_command(command)

    def run_command(self, command):
        """Run a command in a separate thread"""
        self.worker_thread = WorkerThread(command)
        self.worker_thread.output_signal.connect(self.update_console)
        self.worker_thread.finished_signal.connect(self.on_process_finished)
        self.worker_thread.error_signal.connect(self.on_process_error)
        self.worker_thread.start()

    def update_console(self, text):
        """Update console output with new text"""
        self.console_output.append(text)
        
        # Auto-scroll to bottom
        cursor = self.console_output.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.console_output.setTextCursor(cursor)

    def on_process_finished(self):
        """Handle process completion"""
        self.console_output.append("\n✅ Process completed successfully!")
        self.hide_progress()
        self.enable_buttons()
        self.statusBar().showMessage(f"Analysis completed for {self.current_ticker}")
        
        print("[INFO] Process completed successfully")

    def on_process_error(self, error_msg):
        """Handle process error"""
        self.console_output.append(f"\n❌ Error: {error_msg}")
        self.hide_progress()
        self.enable_buttons()
        self.statusBar().showMessage("Error occurred during analysis")
        
        print(f"[ERROR] Process error: {error_msg}")

    def disable_buttons(self):
        """Disable all analysis buttons during processing"""
        self.download_button.setEnabled(False)
        self.earnings_button.setEnabled(False)
        self.visualize_button.setEnabled(False)
        self.complete_button.setEnabled(False)

    def enable_buttons(self):
        """Enable all analysis buttons after processing"""
        if self.current_ticker:
            self.download_button.setEnabled(True)
            self.earnings_button.setEnabled(True)
            self.visualize_button.setEnabled(True)
            self.complete_button.setEnabled(True)

    def show_progress(self):
        """Show indeterminate progress bar"""
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress

    def hide_progress(self):
        """Hide progress bar"""
        self.progress_bar.setVisible(False)

    def clear_console(self):
        """Clear the console output"""
        self.console_output.clear()
        self.console_output.append("Console cleared.")
        
        print("[INFO] Console cleared by user")

def main():
    print("[INFO] Starting MarketSwimmer GUI...")
    
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("MarketSwimmer")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("MarketSwimmer Analytics")
    
    # Create and show the main window
    window = MarketSwimmerGUI()
    window.show()
    
    print("[INFO] MarketSwimmer GUI started successfully")
    
    # Start the event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
