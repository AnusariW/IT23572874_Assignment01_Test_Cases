# Test Automation Framework - Singlish → Sinhala Transliteration App

Automated testing framework for the Singlish to Sinhala transliteration app at https://www.pixelssuite.com/chat-translator

## 📋 Overview

This test automation framework provides:

- **Selenium-based automation** for browser testing
- **Comprehensive test coverage** with 100+ test cases
- **Parallel test execution** support
- **Detailed logging and reporting** 
- **Screenshot capture** on test failures
- **JSON export** for integration with CI/CD pipelines

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Tests Directly

```bash
# Run all tests with full output
python test_automation.py

# Run in headless mode (faster, no browser UI)
python test_automation.py --headless
```

### 3. Run Tests with Pytest

```bash
# Run all tests
pytest conftest.py

# Run only quick tests (skip slow tests)
pytest conftest.py -m "not slow"

# Run with verbose output
pytest conftest.py -v

# Run with detailed output
pytest conftest.py -vv

# Run tests in parallel (requires pytest-xdist)
pytest conftest.py -n auto
```

## 📁 Project Structure

```
test_cases_py/
├── test_cases.py           # Test case definitions
├── test_automation.py      # Main test automation engine
├── conftest.py             # Pytest configuration & fixtures
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── test_logs/             # Test execution logs (auto-created)
│   ├── test_execution_*.log
│   ├── report_*.txt
│   └── results_*.json
└── test_screenshots/      # Failure screenshots (auto-created)
    └── *.png
```

## 🛠️ Configuration

### Modifying Test Execution

Edit the `main()` function in `test_automation.py`:

```python
# Change to headless mode
automation = TransliterationTestAutomation(headless=True, logger=logger)

# Or with custom settings
automation = TransliterationTestAutomation(
    headless=False,
    logger=logger
)
```

### Adjusting Timeouts

In `test_automation.py`, modify these values:

```python
# Page load timeout (seconds)
self.driver.set_page_load_timeout(15)

# Wait time between tests (seconds)
time.sleep(0.5)  # Change this value
```

### Custom Web Element Selectors

If the app's HTML structure changes, update the selectors in:

- `get_input_field()` - Input text field selectors
- `get_output_field()` - Output text field selectors

## 📊 Test Reports

### Text Report
Located in `test_logs/report_*.txt`

Contains:
- Test execution summary (pass rate, total time)
- Detailed results for each test case
- Failure details with actual vs. expected output

### JSON Report
Located in `test_logs/results_*.json`

Contains:
- All test result data in JSON format
- Suitable for integration with CI/CD tools
- Easy to parse and process programmatically

### Screenshots
Located in `test_screenshots/`

Auto-captured on:
- Test failures
- Test errors
- For debugging purposes

## 🔍 Understanding Test Results

### Status Values

| Status | Meaning |
|--------|---------|
| `PASS` | Test passed, output matches expected |
| `FAIL` | Test failed, output does not match |
| `ERROR` | Error during test execution |
| `PASS_CAPTURED` | Output captured but not verified yet |
| `INCONCLUSIVE` | Unable to determine pass/fail |

### Log Files

Each test run generates:

1. **test_execution_YYYYMMDD_HHMMSS.log** - Detailed execution log
2. **report_YYYYMMDD_HHMMSS.txt** - Human-readable report
3. **results_YYYYMMDD_HHMMSS.json** - Machine-readable results

## 🧪 Test Case Format

Test cases are defined in `test_cases.py`:

```python
{
    "tc_id": "Pos_Fun_0001",           # Unique test ID
    "name": "Short description",        # Test name
    "input_length": "S",                # S (≤30) | M (31-299) | L (≥300)
    "singlish_input": "oyaata kohomadha?",
    "expected_output": "ඔයාට කොහොමද?",
    "what_covered": "Coverage description"
}
```

## 🚨 Troubleshooting

### Chrome Driver Issues

If WebDriver fails to start:

```bash
# Reinstall chromedriver
pip install --upgrade webdriver-manager

# Or specify a specific version
pip install webdriver-manager==4.0.1
```

### Element Not Found

1. Check if app structure has changed
2. Update selectors in `get_input_field()` and `get_output_field()`
3. Run in non-headless mode to visually inspect

### Connection Timeout

1. Increase timeout in `setup_driver()`:
   ```python
   self.driver.set_page_load_timeout(30)  # Increase from 15 to 30
   ```

2. Check internet connection
3. Verify app is accessible at https://www.pixelssuite.com/chat-translator

### Tests Pass Individually but Fail in Batch

1. Increase delay between tests:
   ```python
   time.sleep(2)  # Increase from 0.5 to 2
   ```

2. Reduce parallel execution (if using pytest-xdist)

## 📈 Advanced Usage

### Custom Test Suite

```python
from test_automation import TransliterationTestAutomation
from test_cases import TEST_CASES

# Filter and run only certain tests
positive_tests = [tc for tc in TEST_CASES if "Pos_" in tc["tc_id"]]

automation = TransliterationTestAutomation()
results = automation.run_all_tests(test_cases=positive_tests)

# Generate report
report = automation.generate_report(output_file="custom_report.txt")
```

### Integrating with CI/CD

Export results to JSON and parse in your CI/CD pipeline:

```bash
python test_automation.py
# Generates test_logs/results_YYYYMMDD_HHMMSS.json

# Parse and check in your pipeline
python -c "
import json
with open('test_logs/results_*.json') as f:
    results = json.load(f)
    failures = [r for r in results if r['status'] == 'FAIL']
    exit(0 if not failures else 1)
"
```

## 📝 Logging Levels

The framework uses Python's `logging` module. To adjust verbosity:

```python
# In test_automation.py, modify logger levels:
fh.setLevel(logging.DEBUG)   # File: DEBUG for detailed logs
ch.setLevel(logging.INFO)    # Console: INFO for normal output
```

Log levels:
- `DEBUG` - Detailed diagnostic information
- `INFO` - General informational messages
- `WARNING` - Warning messages
- `ERROR` - Error messages

## 🔐 Best Practices

1. **Run in headless mode** for CI/CD pipelines (faster)
2. **Use pytest** for parallel execution (`pytest -n auto`)
3. **Monitor screenshots** for visual debugging
4. **Review JSON reports** for automated processing
5. **Update selectors** if app structure changes
6. **Increase delays** if tests are flaky

## 📞 Support

For issues or questions:

1. Check logs in `test_logs/test_execution_*.log`
2. Review screenshots in `test_screenshots/`
3. Verify app is accessible at target URL
4. Check selectors match current app HTML structure

## 📄 License

Test automation framework for https://www.pixelssuite.com/chat-translator

---

**Last Updated:** 2024
**Framework Version:** 1.0
**Python Version:** 3.8+
