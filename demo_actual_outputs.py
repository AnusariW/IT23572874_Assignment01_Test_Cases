#!/usr/bin/env python3
"""
Demo script to get actual outputs for a few test cases.

This script runs a subset of test cases against the live website
to demonstrate how to capture actual outputs.
"""

import asyncio
import json
from playwright.async_api import async_playwright

# Sample test cases to demonstrate
SAMPLE_TEST_CASES = [
    {
        'id': 'Neg_0001',
        'input': 'mokakda oya karanne?',
        'expectedOutput': 'මොකක්ද ඔයා කරන්නේ?',
        'types': 'Question forms',
    },
    {
        'id': 'Neg_0002',
        'input': 'oya koheda inna hithan inne ada?',
        'expectedOutput': 'ඔයා කොහේද ඉන්න හිතන් ඉන්නේ අද?',
        'types': 'Question forms',
    },
    {
        'id': 'Neg_0003',
        'input': 'apita heta eliyatama yanna one.',
        'expectedOutput': 'අපිට හෙට එළියටම යන්න ඕනේ.',
        'types': 'Command forms',
    }
]

async def open_chat_translator(page):
    """Navigate to the Chat Translator and ensure Chat Sinhala mode is active."""
    try:
        await page.goto('https://www.pixelssuite.com/chat-translator', wait_until='domcontentloaded', timeout=30000)

        # Make sure the "Chat Sinhala" tab / toggle is active
        chat_tab = page.locator('text=Chat Sinhala').first
        if await chat_tab.is_visible():
            await chat_tab.click()

        await page.wait_for_timeout(1000)
        return True
    except Exception as e:
        print(f"❌ Failed to open translator: {e}")
        return False

async def transliterate(page, input_text):
    """Type input into the text box and retrieve the transliterated output."""
    try:
        # Clear existing text
        input_box = page.locator('textarea, [contenteditable="true"]').first
        await input_box.fill('')
        await input_box.type(input_text, delay=30)
        await page.wait_for_timeout(1500)

        # Grab the output — try common selectors used by the site
        output_selectors = [
            '.output-text',
            '.result-text',
            '[class*="output"]',
            '[class*="result"]',
            'textarea >> nth=1',
            '[contenteditable="true"] >> nth=1',
        ]

        actual_output = ''
        for selector in output_selectors:
            try:
                el = page.locator(selector).first
                if await el.is_visible():
                    actual_output = await el.text_content() or ''
                    if actual_output.strip():
                        break
            except Exception:
                continue

        return actual_output.strip()
    except Exception as e:
        return f"ERROR: {e}"

async def run_sample_tests():
    """Run sample tests to demonstrate actual output capture."""
    print("🚀 Running sample tests to capture actual outputs...")
    print("=" * 80)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # Try to open the translator
            if not await open_chat_translator(page):
                print("❌ Could not access the translator website.")
                print("💡 Make sure you have internet connection and the website is accessible.")
                return

            results = []

            for i, tc in enumerate(SAMPLE_TEST_CASES, 1):
                print(f"Testing {i}/3: {tc['id']}...", end=" ")

                try:
                    actual_output = await transliterate(page, tc['input'])

                    # Determine status
                    passed = actual_output == tc['expectedOutput']
                    status = 'Pass' if passed else 'Fail'

                    results.append({
                        'tcId': tc['id'],
                        'input': tc['input'],
                        'expectedOutput': tc['expectedOutput'],
                        'actualOutput': actual_output,
                        'status': status,
                        'types': tc['types'],
                    })

                    print(f"✓ Got output: '{actual_output[:50]}...'")

                except Exception as e:
                    print(f"❌ Error: {e}")
                    results.append({
                        'tcId': tc['id'],
                        'input': tc['input'],
                        'expectedOutput': tc['expectedOutput'],
                        'actualOutput': f"ERROR: {e}",
                        'status': 'Error',
                        'types': tc['types'],
                    })

            await browser.close()

            # Display results
            print("\n" + "=" * 80)
            print("📊 SAMPLE RESULTS:")
            print("=" * 80)

            for result in results:
                print(f"\nTest Case: {result['tcId']}")
                print(f"Input: {result['input']}")
                print(f"Expected: {result['expectedOutput']}")
                print(f"Actual: {result['actualOutput']}")
                print(f"Status: {result['status']}")
                print("-" * 40)

            # Save to JSON
            with open('sample_results.json', 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

            print("\n💾 Results saved to: sample_results.json")
            print("\n📋 Copy the 'Actual' values above to fill your Excel file!")
            print("\n🔄 Run the full test suite with: python singlish_transliteration.py")

    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        print("💡 Make sure Playwright browsers are installed:")
        print("   python -m playwright install chromium")

if __name__ == '__main__':
    asyncio.run(run_sample_tests())
