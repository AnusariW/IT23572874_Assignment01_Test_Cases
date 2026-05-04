#!/usr/bin/env python3
"""
Generate CSV file with all test cases for Excel import.

This creates a CSV file that can be opened in Excel with all test cases,
ready for you to fill in the actual outputs.
"""

import csv
from singlish_transliteration import TEST_CASES

def generate_excel_csv():
    """Generate CSV file with test cases for Excel import."""

    filename = 'test_cases_for_excel.csv'

    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['Test Case ID', 'Input', 'Expected Output', 'Actual Output', 'Status', 'Types', 'Rationale']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Write test cases
        for tc in TEST_CASES:
            writer.writerow({
                'Test Case ID': tc['id'],
                'Input': tc['input'],
                'Expected Output': tc['expectedOutput'],
                'Actual Output': '[FILL THIS WITH ACTUAL OUTPUT FROM WEBSITE]',
                'Status': '',
                'Types': tc['types'],
                'Rationale': tc['rationale']
            })

    print(f"✅ CSV file generated: {filename}")
    print("\n📋 Instructions:")
    print("1. Open test_cases_for_excel.csv in Excel")
    print("2. For each row, manually test the input on:")
    print("   https://www.pixelssuite.com/chat-translator")
    print("3. Copy the actual Sinhala output from the website")
    print("4. Paste it in the 'Actual Output' column")
    print("5. Save as Excel file (.xlsx)")
    print("\n🔄 Or run the automated tests:")
    print("   python singlish_transliteration.py")
    print("   (then copy from results/test-results-summary.json)")

if __name__ == '__main__':
    generate_excel_csv()
