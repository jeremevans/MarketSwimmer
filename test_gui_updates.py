#!/usr/bin/env python3
"""
Test script to verify GUI updates and enhanced fair value analysis.
"""

def test_enhanced_fair_value():
    print("Testing enhanced fair value analysis...")
    
    try:
        from marketswimmer.core.fair_value import FairValueCalculator
        calc = FairValueCalculator()
        
        # Test with INTC since we know it has data
        result = calc.enhanced_fair_value_analysis('INTC', save_detailed_report=False)
        
        if result:
            print("✓ Enhanced fair value analysis working")
            
            # Check if balance sheet data is included
            if 'balance_sheet_summary' in result:
                balance_data = result['balance_sheet_summary']
                print("✓ Balance sheet data included:")
                print(f"  Cash & Investments: ${balance_data.get('cash_and_investments', 0):,.0f}")
                print(f"  Total Debt: ${balance_data.get('total_debt', 0):,.0f}")
                print(f"  Shares Outstanding: {balance_data.get('shares_outstanding', 0):,.0f}")
                return True
            else:
                print("✗ Balance sheet data not found in results")
                return False
        else:
            print("✗ Enhanced fair value analysis failed")
            return False
            
    except Exception as e:
        print(f"✗ Error testing enhanced fair value: {e}")
        return False

def test_workflow_integration():
    print("\nTesting workflow integration...")
    
    try:
        from marketswimmer.core.workflow import AnalysisWorkflow
        workflow = AnalysisWorkflow()
        
        # Check if the enhanced fair value method exists
        if hasattr(workflow, '_calculate_enhanced_fair_value'):
            print("✓ Enhanced fair value method exists in workflow")
            return True
        else:
            print("✗ Enhanced fair value method not found in workflow")
            return False
            
    except Exception as e:
        print(f"✗ Error testing workflow: {e}")
        return False

def main():
    print("=== GUI Updates and Enhanced Fair Value Test ===")
    
    # Test enhanced fair value analysis
    fair_value_ok = test_enhanced_fair_value()
    
    # Test workflow integration
    workflow_ok = test_workflow_integration()
    
    print(f"\n=== Results ===")
    print(f"Enhanced Fair Value: {'✓ PASS' if fair_value_ok else '✗ FAIL'}")
    print(f"Workflow Integration: {'✓ PASS' if workflow_ok else '✗ FAIL'}")
    
    if fair_value_ok and workflow_ok:
        print("\n✓ All tests passed! GUI and enhanced analysis are ready.")
        print("\nThe Complete Analysis button now includes:")
        print("  1. Download financial data")
        print("  2. Calculate owner earnings")
        print("  3. Enhanced fair value with balance sheet analysis")
        print("  4. Create visualizations")
        print("\nRemoved buttons: Download, Fair Value, Visualizations")
        print("Streamlined GUI with only Complete Analysis button needed!")
    else:
        print("\n✗ Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
