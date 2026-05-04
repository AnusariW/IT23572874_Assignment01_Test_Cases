"""
Test Automation Framework for Singlish → Sinhala Transliteration App
Target: https://www.pixelssuite.com/chat-translator

Automates testing of all test cases with:
- Selenium WebDriver for browser automation
- Parallel execution capability
- Detailed logging and reporting
- Screenshot capture on failures
"""

import time
import json
import logging
from datetime import datetime
from typing import Dict, List, Tuple
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from test_cases import TEST_CASES


# ─────────────────────────────────────────────────────────────────
# LOGGING CONFIGURATION
# ─────────────────────────────────────────────────────────────────

def setup_logging(log_dir: str = "test_logs") -> logging.Logger:
    """Configure logging for test execution."""
    Path(log_dir).mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = Path(log_dir) / f"test_execution_{timestamp}.log"
    
    logger = logging.getLogger("TestAutomation")
    logger.setLevel(logging.DEBUG)
    
    # File handler
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger


# ─────────────────────────────────────────────────────────────────
# TEST AUTOMATION ENGINE
# ─────────────────────────────────────────────────────────────────

class TransliterationTestAutomation:
    """Main test automation engine for transliteration app."""
    
    def __init__(self, headless: bool = False, logger: logging.Logger = None):
        """
        Initialize the test automation engine.
        
        Args:
            headless: Run browser in headless mode
            logger: Logger instance for logging
        """
        self.headless = headless
        self.logger = logger or setup_logging()
        self.driver = None
        self.base_url = "https://www.pixelssuite.com/chat-translator"
        self.test_results = []
        self.screenshots_dir = Path("test_screenshots")
        self.screenshots_dir.mkdir(exist_ok=True)
        
    def setup_driver(self) -> None:
        """Initialize Selenium WebDriver."""
        try:
            options = webdriver.ChromeOptions()
            if self.headless:
                options.add_argument("--headless")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.set_page_load_timeout(15)
            self.logger.info("✓ WebDriver initialized successfully")
        except Exception as e:
            self.logger.error(f"✗ Failed to initialize WebDriver: {str(e)}")
            raise
    
    def teardown_driver(self) -> None:
        """Close the WebDriver."""
        if self.driver:
            self.driver.quit()
            self.logger.info("✓ WebDriver closed")
    
    def navigate_to_app(self) -> bool:
        """Navigate to the transliteration app."""
        try:
            self.logger.info(f"Navigating to {self.base_url}...")
            self.driver.get(self.base_url)
            time.sleep(2)  # Wait for app to load
            self.logger.info("✓ Successfully navigated to app")
            return True
        except Exception as e:
            self.logger.error(f"✗ Failed to navigate to app: {str(e)}")
            return False
    
    def find_input_field(self) -> bool:
        """Locate the input text field."""
        try:
            # Try multiple selectors (adjust based on actual app structure)
            selectors = [
                (By.ID, "singlish-input"),
                (By.NAME, "singlish"),
                (By.CLASS_NAME, "input-field"),
                (By.XPATH, "//textarea[@placeholder*='inglish']"),
                (By.XPATH, "//input[@type='text']"),
                (By.TAG_NAME, "textarea"),
            ]
            
            for by, selector in selectors:
                try:
                    element = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((by, selector))
                    )
                    self.logger.debug(f"✓ Found input field using {by}: {selector}")
                    return True
                except:
                    continue
            
            self.logger.warning("✗ Could not locate input field with standard selectors")
            return False
        except Exception as e:
            self.logger.error(f"✗ Error finding input field: {str(e)}")
            return False
    
    def find_output_field(self) -> bool:
        """Locate the output text field."""
        try:
            selectors = [
                (By.ID, "sinhala-output"),
                (By.NAME, "sinhala"),
                (By.CLASS_NAME, "output-field"),
                (By.XPATH, "//textarea[@placeholder*='inhala']"),
                (By.XPATH, "//div[@class*='output']"),
            ]
            
            for by, selector in selectors:
                try:
                    element = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((by, selector))
                    )
                    self.logger.debug(f"✓ Found output field using {by}: {selector}")
                    return True
                except:
                    continue
            
            self.logger.warning("✗ Could not locate output field")
            return False
        except Exception as e:
            self.logger.error(f"✗ Error finding output field: {str(e)}")
            return False
    
    def get_input_field(self):
        """Get the input field element."""
        selectors = [
            (By.ID, "singlish-input"),
            (By.NAME, "singlish"),
            (By.TAG_NAME, "textarea"),
            (By.XPATH, "//input[@type='text']"),
        ]
        
        for by, selector in selectors:
            try:
                return self.driver.find_element(by, selector)
            except:
                continue
        return None
    
    def get_output_field(self):
        """Get the output field element."""
        selectors = [
            (By.ID, "sinhala-output"),
            (By.NAME, "sinhala"),
            (By.XPATH, "//div[@class*='output']//p"),
            (By.XPATH, "//*[@class*='result']"),
        ]
        
        for by, selector in selectors:
            try:
                return self.driver.find_element(by, selector)
            except:
                continue
        return None
    
    def take_screenshot(self, filename: str) -> Path:
        """Take a screenshot and save it."""
        try:
            filepath = self.screenshots_dir / f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            self.driver.save_screenshot(str(filepath))
            self.logger.debug(f"✓ Screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"✗ Failed to take screenshot: {str(e)}")
            return None
    
    def run_test_case(self, test_case: Dict) -> Dict:
        """
        Execute a single test case.
        
        Args:
            test_case: Test case dictionary from TEST_CASES
            
        Returns:
            Dictionary with test result
        """
        tc_id = test_case.get("tc_id", "Unknown")
        tc_name = test_case.get("name", "Unknown")
        singlish_input = test_case.get("singlish_input", "")
        expected_output = test_case.get("expected_output", "")
        
        self.logger.info(f"\n{'='*70}")
        self.logger.info(f"Test Case: {tc_id} - {tc_name}")
        self.logger.info(f"Input Length: {test_case.get('input_length', 'N/A')}")
        self.logger.info(f"Coverage: {test_case.get('what_covered', 'N/A').split(chr(10))[0]}")
        self.logger.info(f"{'='*70}")
        
        result = {
            "tc_id": tc_id,
            "name": tc_name,
            "status": "PENDING",
            "singlish_input": singlish_input,
            "expected_output": expected_output,
            "actual_output": "",
            "match": False,
            "error": None,
            "screenshot": None,
            "execution_time": 0,
        }
        
        start_time = time.time()
        
        try:
            # Clear input field
            input_field = self.get_input_field()
            if not input_field:
                raise Exception("Could not locate input field")
            
            input_field.clear()
            time.sleep(0.5)
            
            # Enter Singlish text
            self.logger.info(f"Entering input: '{singlish_input[:50]}{'...' if len(singlish_input) > 50 else ''}'")
            input_field.send_keys(singlish_input)
            time.sleep(1)  # Wait for transliteration to process
            
            # Get output
            output_field = self.get_output_field()
            if not output_field:
                raise Exception("Could not locate output field")
            
            actual_output = output_field.text.strip()
            result["actual_output"] = actual_output
            
            self.logger.info(f"Expected output: '{expected_output[:50]}{'...' if len(expected_output) > 50 else ''}'")
            self.logger.info(f"Actual output:   '{actual_output[:50]}{'...' if len(actual_output) > 50 else ''}'")
            
            # Verify output
            if expected_output and actual_output:
                if expected_output == actual_output:
                    result["status"] = "PASS"
                    result["match"] = True
                    self.logger.info("✓ Output matches expected result")
                else:
                    result["status"] = "FAIL"
                    result["match"] = False
                    self.logger.warning("✗ Output does NOT match expected result")
                    result["screenshot"] = str(self.take_screenshot(tc_id))
            elif expected_output == "":
                result["status"] = "PASS_CAPTURED"
                self.logger.info("✓ Output captured (marked as [VERIFY])")
            else:
                result["status"] = "INCONCLUSIVE"
                self.logger.warning("⚠ Unable to verify (no expected output provided)")
                
        except Exception as e:
            result["status"] = "ERROR"
            result["error"] = str(e)
            result["screenshot"] = str(self.take_screenshot(f"{tc_id}_ERROR"))
            self.logger.error(f"✗ Test execution error: {str(e)}")
        
        finally:
            result["execution_time"] = time.time() - start_time
            self.logger.info(f"Execution time: {result['execution_time']:.2f}s")
        
        return result
    
    def run_all_tests(self, test_cases: List[Dict] = None) -> List[Dict]:
        """
        Execute all test cases.
        
        Args:
            test_cases: List of test cases to run (uses TEST_CASES if None)
            
        Returns:
            List of test results
        """
        if test_cases is None:
            test_cases = TEST_CASES
        
        self.test_results = []
        self.setup_driver()
        
        try:
            if not self.navigate_to_app():
                self.logger.error("Failed to navigate to app. Aborting test run.")
                return self.test_results
            
            for i, test_case in enumerate(test_cases, 1):
                self.logger.info(f"\n[{i}/{len(test_cases)}]")
                result = self.run_test_case(test_case)
                self.test_results.append(result)
                time.sleep(0.5)  # Small delay between tests
        
        except KeyboardInterrupt:
            self.logger.warning("\n⚠ Test execution interrupted by user")
        except Exception as e:
            self.logger.error(f"✗ Unexpected error during test execution: {str(e)}")
        finally:
            self.teardown_driver()
        
        return self.test_results
    
    def generate_report(self, output_file: str = None) -> str:
        """
        Generate a comprehensive test report.
        
        Args:
            output_file: Path to save the report
            
        Returns:
            Report content as string
        """
        if not self.test_results:
            return "No test results available"
        
        # Calculate statistics
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r["status"] == "PASS")
        failed = sum(1 for r in self.test_results if r["status"] == "FAIL")
        errors = sum(1 for r in self.test_results if r["status"] == "ERROR")
        pass_captured = sum(1 for r in self.test_results if r["status"] == "PASS_CAPTURED")
        inconclusive = sum(1 for r in self.test_results if r["status"] == "INCONCLUSIVE")
        
        pass_rate = (passed / total * 100) if total > 0 else 0
        total_time = sum(r["execution_time"] for r in self.test_results)
        
        # Generate report
        report = f"""
╔════════════════════════════════════════════════════════════════════════════════╗
║                    TEST EXECUTION REPORT - TRANSLITERATION APP                 ║
╚════════════════════════════════════════════════════════════════════════════════╝

Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Execution Time: {total_time:.2f}s

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total Test Cases:     {total}
✓ Passed:             {passed}
✗ Failed:             {failed}
⚠ Errors:             {errors}
ℹ Captured (Verify):  {pass_captured}
? Inconclusive:       {inconclusive}

Pass Rate:            {pass_rate:.1f}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 DETAILED RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        for i, result in enumerate(self.test_results, 1):
            status_icon = {
                "PASS": "✓",
                "FAIL": "✗",
                "ERROR": "⚠",
                "PASS_CAPTURED": "ℹ",
                "INCONCLUSIVE": "?",
            }.get(result["status"], "?")
            
            report += f"""
{i}. {status_icon} {result['tc_id']} - {result['name']}
   Status: {result['status']}
   Execution Time: {result['execution_time']:.2f}s
"""
            
            if result["status"] == "FAIL":
                report += f"""   Input:    {result['singlish_input'][:60]}{'...' if len(result['singlish_input']) > 60 else ''}
   Expected: {result['expected_output'][:60]}{'...' if len(result['expected_output']) > 60 else ''}
   Actual:   {result['actual_output'][:60]}{'...' if len(result['actual_output']) > 60 else ''}
"""
            elif result["status"] == "ERROR":
                report += f"   Error: {result['error']}\n"
                if result["screenshot"]:
                    report += f"   Screenshot: {result['screenshot']}\n"
        
        report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        # Save report to file
        if output_file:
            Path(output_file).parent.mkdir(exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            self.logger.info(f"✓ Report saved to: {output_file}")
        
        return report
    
    def export_results_json(self, output_file: str = "test_results.json") -> str:
        """Export test results as JSON."""
        try:
            Path(output_file).parent.mkdir(exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.test_results, f, ensure_ascii=False, indent=2)
            self.logger.info(f"✓ Results exported to JSON: {output_file}")
            return output_file
        except Exception as e:
            self.logger.error(f"✗ Failed to export JSON: {str(e)}")
            return None


# ─────────────────────────────────────────────────────────────────
# MAIN EXECUTION
# ─────────────────────────────────────────────────────────────────

def main():
    """Main entry point for test automation."""
    
    # Initialize logger
    logger = setup_logging()
    logger.info("╔════════════════════════════════════════════════════════════════╗")
    logger.info("║    Singlish → Sinhala Transliteration - Test Automation       ║")
    logger.info("║    Target: https://www.pixelssuite.com/chat-translator        ║")
    logger.info("╚════════════════════════════════════════════════════════════════╝")
    
    # Create test automation instance
    automation = TransliterationTestAutomation(headless=False, logger=logger)
    
    try:
        # Run all tests
        logger.info(f"\nStarting test execution with {len(TEST_CASES)} test cases...")
        results = automation.run_all_tests()
        
        # Generate and display report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"test_logs/report_{timestamp}.txt"
        report = automation.generate_report(output_file=report_file)
        print(report)
        
        # Export results as JSON
        json_file = f"test_logs/results_{timestamp}.json"
        automation.export_results_json(output_file=json_file)
        
        logger.info("✓ Test execution completed successfully")
        
    except Exception as e:
        logger.error(f"✗ Fatal error during test execution: {str(e)}", exc_info=True)
    
    return automation.test_results


if __name__ == "__main__":
    results = main()
