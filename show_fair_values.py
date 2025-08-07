#!/usr/bin/env python3
"""
Show Fair Value Per Share for Each Owner Earnings Method
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from marketswimmer.core.fair_value import FairValueCalculator
from pathlib import Path

def show_fair_values():
    """Show fair value per share for each Owner Earnings method"""
    
    print("💰 FAIR VALUE PER SHARE - ALL METHODS")
    print("=" * 50)
    
    try:
        fair_calc = FairValueCalculator()
        results = fair_calc.enhanced_fair_value_analysis("NWN", save_detailed_report=True)
        
        print(f"\n📊 TICKER: NWN")
        print("-" * 30)
        
        # Show traditional fair value first
        if 'fair_value_per_share' in results:
            print(f"Traditional Method:     ${results['fair_value_per_share']:>8.2f}")
        
        # Show alternative method fair values
        if 'alternative_valuations' in results and results['alternative_valuations']:
            for method, valuation in results['alternative_valuations'].items():
                if valuation and valuation.get('fair_value_per_share'):
                    method_name = method.replace('_', ' ').title()
                    print(f"{method_name:20s}: ${valuation['fair_value_per_share']:>8.2f}")
        
        # Show percentage differences if available
        if 'alternative_methods' in results and results['alternative_methods']:
            print(f"\n📈 PERCENTAGE DIFFERENCES:")
            print("-" * 30)
            
            traditional_avg = None
            alt_averages = {}
            
            # Extract 10-year averages
            alt_methods = results['alternative_methods']
            if alt_methods:
                # Calculate traditional average
                traditional_values = []
                for year, year_data in alt_methods.items():
                    if 'traditional_method' in year_data:
                        traditional_values.append(year_data['traditional_method']['value'])
                
                if traditional_values:
                    traditional_avg = sum(traditional_values) / len(traditional_values)
                    print(f"Traditional (10yr avg): ${traditional_avg:>12,.0f}")
                
                # Calculate alternative averages
                for method in ['operating_cash_flow_method', 'free_cash_flow_method']:
                    method_values = []
                    for year, year_data in alt_methods.items():
                        if method in year_data:
                            method_values.append(year_data[method]['value'])
                    
                    if method_values:
                        avg = sum(method_values) / len(method_values)
                        alt_averages[method] = avg
                        method_display = method.replace('_', ' ').title()
                        
                        if traditional_avg and traditional_avg != 0:
                            pct_diff = ((avg - traditional_avg) / abs(traditional_avg)) * 100
                            print(f"{method_display:20s}: ${avg:>12,.0f} ({pct_diff:+.1f}%)")
                        else:
                            print(f"{method_display:20s}: ${avg:>12,.0f}")
        
        print(f"\n📝 Detailed report saved to analysis_output/")
        print(f"✅ All methods calculated successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    show_fair_values()
