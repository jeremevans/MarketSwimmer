#!/usr/bin/env python3
"""
Test Alternative Owner Earnings Methods
Demonstrates the multiple approaches to calculating Owner Earnings
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from marketswimmer.core.owner_earnings import OwnerEarningsCalculator
from marketswimmer.core.fair_value import FairValueCalculator
from pathlib import Path

def test_alternative_methods():
    """Test the alternative Owner Earnings calculation methods"""
    
    print("🧪 TESTING ALTERNATIVE OWNER EARNINGS METHODS")
    print("=" * 60)
    
    # Find NWN data file (we know this exists from your recent analysis)
    nwn_files = list(Path("downloaded_files").glob("*nwn*.xlsx"))
    if not nwn_files:
        print("❌ No NWN files found. Run analysis first.")
        return
    
    # Use most recent NWN file
    latest_file = sorted(nwn_files, key=lambda x: x.stat().st_mtime)[-1]
    print(f"📁 Using file: {latest_file.name}")
    
    # Test 1: Traditional Owner Earnings (current method)
    print(f"\n1️⃣ TRADITIONAL METHOD TEST")
    print("-" * 40)
    
    calc = OwnerEarningsCalculator(str(latest_file))
    calc.preferred_data_type = 'Annual'
    if calc.load_financial_statements_by_type('Annual'):
        owner_earnings = calc.calculate_owner_earnings()
        if owner_earnings:
            # Show just recent years for brevity
            recent_years = sorted(owner_earnings.keys(), reverse=True)[:3]
            for year in recent_years:
                data = owner_earnings[year]
                print(f"   {year}: ${data['owner_earnings']:,.0f}")
        else:
            print("   ❌ No traditional data calculated")
    
    # Test 2: Alternative Methods
    print(f"\n2️⃣ ALTERNATIVE METHODS TEST") 
    print("-" * 40)
    
    try:
        alternative_methods = calc.calculate_alternative_owner_earnings_methods()
        if alternative_methods:
            # Show comparison for recent years
            recent_years = sorted(alternative_methods.keys(), reverse=True)[:3]
            
            for year in recent_years:
                print(f"\n   📅 {year}:")
                year_data = alternative_methods[year]
                
                for method_name, method_info in year_data.items():
                    method_display = method_name.replace('_', ' ').title()
                    value = method_info['value']
                    print(f"      {method_display:20s}: ${value:>12,.0f}")
        else:
            print("   ❌ No alternative data calculated")
            
    except Exception as e:
        print(f"   ❌ Error calculating alternatives: {e}")
    
    # Test 3: Enhanced Fair Value with Multiple Methods
    print(f"\n3️⃣ ENHANCED FAIR VALUE TEST")
    print("-" * 40)
    
    try:
        fair_calc = FairValueCalculator()
        results = fair_calc.enhanced_fair_value_analysis("NWN", save_detailed_report=True)
        
        if 'alternative_methods' in results and results['alternative_methods']:
            print("   ✅ Alternative methods integrated into fair value analysis")
            
            if 'alternative_valuations' in results and results['alternative_valuations']:
                print("   ✅ Alternative valuations calculated")
                for method, valuation in results['alternative_valuations'].items():
                    if valuation.get('fair_value_per_share'):
                        print(f"      {method.title()} Fair Value: ${valuation['fair_value_per_share']:.2f}")
            else:
                print("   ℹ️ Alternative valuations not available")
        else:
            print("   ℹ️ Alternative methods not available in enhanced analysis")
            
    except Exception as e:
        print(f"   ❌ Enhanced fair value test failed: {e}")
    
    print(f"\n✅ TESTING COMPLETE!")
    print(f"📝 Check enhanced fair value report for detailed alternative methods analysis")

if __name__ == "__main__":
    test_alternative_methods()
