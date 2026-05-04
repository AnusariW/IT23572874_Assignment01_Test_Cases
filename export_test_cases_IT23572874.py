#!/usr/bin/env python3
"""
Extract test cases for Excel import.

This script extracts all test cases from the test suite and outputs them
in a format that can be easily imported into Excel.
"""

import json
from singlish_transliteration import TEST_CASES

def export_test_cases_for_excel():
    """Export test cases in Excel-friendly format."""

    print("Test Case ID,Input Length,Input,Expected Output,Actual Output,Status,Types,Rationale")
    print("-" * 100)

    for tc in TEST_CASES:
        # Escape commas and quotes for CSV
        input_text = tc['input'].replace('"', '""')
        expected = tc['expectedOutput'].replace('"', '""')
        types = tc['types'].replace('"', '""')
        rationale = tc['rationale'].replace('"', '""')

        # Format as CSV row
        row = f'"{tc["id"]}","{input_text}","{expected}","[PENDING]","{types}","{rationale}"'
        print(row)

    print("\n" + "="*100)
    print("Instructions:")
    print("1. Copy the output above")
    print("2. Paste into Excel or Google Sheets")
    print("3. Replace '[PENDING]' in the 'Actual Output' column with real results")
    print("4. Run the full test suite to get actual outputs:")
    print("   python singlish_transliteration.py")
    print("="*100)

if __name__ == '__main__':
    export_test_cases_for_excel()
