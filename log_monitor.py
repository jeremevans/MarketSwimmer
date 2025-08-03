#!/usr/bin/env python3
"""
MarketSwimmer Log Viewer
Real-time log monitoring to debug GUI spawning issues.
"""

import os
import time
import glob
from pathlib import Path

def get_latest_log():
    """Get the most recent log file."""
    logs_dir = Path("logs")
    if not logs_dir.exists():
        return None
    
    log_files = list(logs_dir.glob("marketswimmer_*.log"))
    if not log_files:
        return None
    
    return max(log_files, key=os.path.getmtime)

def tail_log(log_file, lines=50):
    """Display the last N lines of a log file."""
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.readlines()
            return content[-lines:] if len(content) > lines else content
    except Exception as e:
        return [f"Error reading log: {e}\n"]

def monitor_log():
    """Monitor the log file for new entries."""
    print("MarketSwimmer Log Monitor")
    print("="*50)
    
    latest_log = get_latest_log()
    if not latest_log:
        print("No log files found. Start the GUI first.")
        return
    
    print(f"Monitoring: {latest_log}")
    print("Looking for:")
    print("  - GUI spawning events")
    print("  - Subprocess calls")
    print("  - Multiple PID detection")
    print("="*50)
    
    # Show last 20 lines
    lines = tail_log(latest_log, 20)
    for line in lines:
        print(line.rstrip())
    
    print("\n" + "="*50)
    print("Monitoring for new entries (Ctrl+C to stop)...")
    print("="*50)
    
    last_size = os.path.getsize(latest_log)
    
    try:
        while True:
            current_size = os.path.getsize(latest_log)
            if current_size > last_size:
                # New content added
                with open(latest_log, 'r', encoding='utf-8') as f:
                    f.seek(last_size)
                    new_content = f.read()
                    
                for line in new_content.split('\n'):
                    if line.strip():
                        # Highlight important events
                        if any(keyword in line.upper() for keyword in ['GUI', 'SUBPROCESS', 'SPAWN', 'PID']):
                            print(f">>> {line}")
                        else:
                            print(line)
                
                last_size = current_size
            
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

def show_summary():
    """Show a summary of all processes and subprocess calls."""
    latest_log = get_latest_log()
    if not latest_log:
        print("No log files found.")
        return
    
    print("MarketSwimmer Process Summary")
    print("="*50)
    
    pids = set()
    subprocess_calls = []
    gui_events = []
    
    with open(latest_log, 'r', encoding='utf-8') as f:
        for line in f:
            if 'PID:' in line:
                # Extract PID
                try:
                    pid = line.split('PID:')[1].strip().split()[0]
                    pids.add(pid)
                except:
                    pass
            
            if 'SUBPROCESS CALL' in line:
                subprocess_calls.append(line.strip())
            
            if 'GUI EVENT' in line:
                gui_events.append(line.strip())
    
    print(f"Detected PIDs: {len(pids)}")
    for pid in sorted(pids):
        print(f"  - {pid}")
    
    print(f"\nSubprocess calls: {len(subprocess_calls)}")
    for call in subprocess_calls[-5:]:  # Last 5
        print(f"  - {call}")
    
    print(f"\nGUI events: {len(gui_events)}")
    for event in gui_events[-5:]:  # Last 5
        print(f"  - {event}")
    
    if len(pids) > 1:
        print("\n⚠️  WARNING: Multiple PIDs detected!")
        print("   This indicates multiple GUI instances running.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--summary":
        show_summary()
    else:
        monitor_log()
