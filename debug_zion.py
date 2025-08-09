#!/usr/bin/env python3

import pandas as pd

# Load ZION data
df = pd.read_csv('data/owner_earnings_annual_zion.csv')

print("ZION Annual Data Issue Analysis")
print("=" * 50)

print("\nRaw Data (first 5 rows):")
print(df.head().to_string())

print("\nOwner Earnings Formula Verification:")
print("Formula: OE = Net Income + Depreciation - CapEx - Working Capital Changes")
print("Note: Banks should exclude WC, but let's check if formula is applied correctly first")
print()

for idx, row in df.head(5).iterrows():
    period = int(row['Period'])
    ni = row['Net Income'] / 1e6  # Convert to millions
    dep = row['Depreciation'] / 1e6
    capex = row['CapEx'] / 1e6  # Already negative in CSV
    wc = row['Working Capital Change'] / 1e6
    stated_oe = row['Owner Earnings'] / 1e6
    
    # Standard formula: NI + Depreciation + CapEx + WC_Change 
    # (where CapEx is negative, WC_Change can be positive or negative)
    calculated_oe = ni + dep + capex + wc
    
    print(f"{period}:")
    print(f"  NI: {ni:8.0f}M")
    print(f"  Dep: {dep:7.0f}M") 
    print(f"  CapEx: {capex:5.0f}M (negative)")
    print(f"  WC Chg: {wc:5.0f}M")
    print(f"  Calculated: {calculated_oe:6.0f}M")
    print(f"  CSV States: {stated_oe:6.0f}M")
    
    error = abs(calculated_oe - stated_oe)
    if error > 1:  # More than 1M difference
        print(f"  ❌ ERROR: {error:.0f}M difference!")
    else:
        print(f"  ✅ Match")
    print()

print("\nData Scale Analysis:")
print("Checking if values make sense for ZION Bancorporation...")

# ZION is a regional bank, typical annual numbers should be:
# Net Income: ~$400-800M per year
# Owner Earnings: Should be similar to Net Income for banks (since WC excluded)

max_oe = df['Owner Earnings'].max() / 1e6
min_oe = df['Owner Earnings'].min() / 1e6
avg_ni = df['Net Income'].mean() / 1e6

print(f"Max Owner Earnings: {max_oe:,.0f}M")
print(f"Min Owner Earnings: {min_oe:,.0f}M") 
print(f"Average Net Income: {avg_ni:,.0f}M")

if max_oe > 5000:  # >$5B seems too high for ZION
    print("❌ WARNING: Owner Earnings values seem too high for ZION")
if abs(min_oe) > 5000:  # Large negative also suspicious
    print("❌ WARNING: Large negative Owner Earnings suspicious")

print(f"\nWorking Capital Analysis:")
print("For banks, WC changes should typically be excluded from OE calculation")
wc_values = df['Working Capital Change'] / 1e6
print(f"WC Change range: {wc_values.min():,.0f}M to {wc_values.max():,.0f}M")
if wc_values.abs().max() > 2000:
    print("❌ WARNING: Working Capital changes are extremely large for a bank")
