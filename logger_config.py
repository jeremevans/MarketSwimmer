#!/usr/bin/env python3
"""
MarketSwimmer Logging System
Provides centralized logging for debugging GUI spawning issues and process flow.
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path

def setup_logger(name="MarketSwimmer", log_level=logging.DEBUG):
    """
    Set up a comprehensive logger for MarketSwimmer.
    
    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Create timestamp for log filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = logs_dir / f"marketswimmer_{timestamp}.log"
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)8s | %(filename)s:%(lineno)d | %(funcName)s() | %(message)s'
    )
    
    console_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)8s | %(message)s'
    )
    
    # File handler (detailed logging)
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)
    
    # Console handler (less verbose)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Log the startup
    logger.info("="*80)
    logger.info("MarketSwimmer Logger Initialized")
    logger.info(f"Log file: {log_filename}")
    logger.info(f"Process ID: {os.getpid()}")
    logger.info(f"Working directory: {os.getcwd()}")
    logger.info(f"Python executable: {sys.executable}")
    logger.info(f"Command line: {' '.join(sys.argv)}")
    logger.info("="*80)
    
    return logger

def log_subprocess_call(logger, command, script_name):
    """Log subprocess calls to track where GUI windows might be spawned."""
    logger.warning(f"SUBPROCESS CALL from {script_name}:")
    logger.warning(f"  Command: {command}")
    logger.warning(f"  PID: {os.getpid()}")
    
    # Check if this might spawn a GUI
    if any(keyword in str(command).lower() for keyword in ['gui', 'start_gui', 'market_swimmer_gui']):
        logger.error(f"POTENTIAL GUI SPAWN DETECTED in {script_name}!")
        logger.error(f"  Command: {command}")

def log_function_entry(logger, func_name, args=None, kwargs=None):
    """Log function entry for debugging."""
    msg = f"ENTER: {func_name}()"
    if args:
        msg += f" args={args}"
    if kwargs:
        msg += f" kwargs={kwargs}"
    logger.debug(msg)

def log_function_exit(logger, func_name, result=None):
    """Log function exit for debugging."""
    msg = f"EXIT:  {func_name}()"
    if result is not None:
        msg += f" -> {result}"
    logger.debug(msg)

def log_gui_event(logger, event_type, details):
    """Log GUI events specifically."""
    logger.info(f"GUI EVENT: {event_type} | {details}")

def get_process_info():
    """Get current process information for logging."""
    return {
        'pid': os.getpid(),
        'cwd': os.getcwd(),
        'argv': sys.argv,
        'python_exe': sys.executable
    }

# Global logger instance
_logger = None

def get_logger():
    """Get the global logger instance."""
    global _logger
    if _logger is None:
        _logger = setup_logger()
    return _logger

if __name__ == "__main__":
    # Test the logging system
    logger = setup_logger()
    logger.info("Testing MarketSwimmer logging system")
    logger.debug("Debug message test")
    logger.warning("Warning message test")
    logger.error("Error message test")
    
    log_subprocess_call(logger, "python market_swimmer_gui.py", "test_script.py")
    log_gui_event(logger, "WINDOW_OPENED", "MarketSwimmer main window")
    
    print(f"Log test completed. Check logs/ directory for output.")
