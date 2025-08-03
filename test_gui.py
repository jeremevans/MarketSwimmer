#!/usr/bin/env python3
"""
Test script to verify MarketSwimmer GUI functionality
"""

def test_gui_imports():
    """Test if all GUI components can be imported"""
    try:
        from market_swimmer_gui import MarketSwimmerGUI, WorkerThread
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import QThread
        from PyQt6.QtGui import QTextCursor
        print("✅ All GUI imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_gui_creation():
    """Test if GUI window can be created"""
    try:
        from market_swimmer_gui import MarketSwimmerGUI
        from PyQt6.QtWidgets import QApplication
        import sys
        
        app = QApplication([])
        window = MarketSwimmerGUI()
        
        # Test basic functionality
        window.current_ticker = "TEST"
        window.add_output("Test message")
        
        print("✅ GUI window creation successful")
        app.quit()
        return True
    except Exception as e:
        print(f"❌ GUI creation error: {e}")
        return False

def main():
    """Run all tests"""
    print("MarketSwimmer GUI Test Suite")
    print("=" * 30)
    
    tests = [
        ("Import Test", test_gui_imports),
        ("GUI Creation Test", test_gui_creation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nRunning {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print(f"\n{'='*30}")
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! GUI is ready to use.")
        print("\nTo start the GUI, run:")
        print("  .\\start_gui.bat        (PowerShell)")
        print("  .\\launch_gui.bat       (PowerShell)")
        print("  or double-click start_gui.bat in File Explorer")
    else:
        print("⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
