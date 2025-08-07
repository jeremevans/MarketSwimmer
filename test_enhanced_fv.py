#!/usr/bin/env python3
"""
Test script to check enhanced fair value analysis.
"""

from marketswimmer.core.fair_value import FairValueCalculator

def main():
    print("Testing FairValueCalculator methods...")
    
    calc = FairValueCalculator()
    
    # Check available methods
    methods = [m for m in dir(calc) if not m.startswith('_')]
    print(f"Available methods ({len(methods)}):")
    for method in sorted(methods):
        print(f"  - {method}")
    
    # Test specific methods
    if hasattr(calc, 'test_method'):
        print(f"\n✓ test_method exists: {calc.test_method()}")
    else:
        print("\n✗ test_method NOT found")
    
    if hasattr(calc, 'enhanced_fair_value_analysis'):
        print("✓ enhanced_fair_value_analysis exists")
        # Try to call it
        try:
            result = calc.enhanced_fair_value_analysis('AAPL', save_detailed_report=False)
            print("✓ enhanced_fair_value_analysis call successful")
            print(f"  Fair value: ${result['valuation_results'].get('fair_value_per_share', 'N/A')}")
        except Exception as e:
            print(f"✗ enhanced_fair_value_analysis call failed: {e}")
    else:
        print("✗ enhanced_fair_value_analysis NOT found")

if __name__ == "__main__":
    main()
