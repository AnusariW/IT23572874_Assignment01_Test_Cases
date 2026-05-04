#!/usr/bin/env python3
"""
Test automation runner for Singlish transliteration tests.

Usage:
    python run_tests.py              # Run all tests
    python run_tests.py --headed     # Run tests with browser UI visible
    python run_tests.py --report     # Show test report
    python run_tests.py --install    # Install Playwright browsers
"""

import sys
import subprocess
from pathlib import Path


def install_browsers():
    """Install Playwright browsers."""
    print("Installing Playwright browsers...")
    try:
        subprocess.run([sys.executable, '-m', 'playwright', 'install'], check=True)
        print("✅ Browsers installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install browsers: {e}")
        sys.exit(1)


def run_tests(headed=False):
    """Run the test suite."""
    print("Running test suite...")
    
    script = Path(__file__).parent / 'singlish_transliteration.py'
    
    if not script.exists():
        print(f"❌ Test script not found: {script}")
        sys.exit(1)
    
    try:
        subprocess.run([sys.executable, str(script)], check=True)
        print("\n✅ Tests completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code {e.returncode}")
        sys.exit(e.returncode)


def show_report():
    """Display the test report."""
    report_file = Path('results/test-results-summary.json')
    
    if not report_file.exists():
        print(f"❌ Report file not found: {report_file}")
        sys.exit(1)
    
    print(f"\n📊 Test Report: {report_file}")
    print(report_file.read_text())


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--headed':
            run_tests(headed=True)
        elif sys.argv[1] == '--report':
            show_report()
        elif sys.argv[1] == '--install':
            install_browsers()
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print("Available options: --headed, --report, --install")
            sys.exit(1)
    else:
        run_tests()
