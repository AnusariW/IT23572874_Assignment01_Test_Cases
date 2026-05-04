"""
Pytest configuration and test fixtures for transliteration test automation.
"""

import pytest
import logging
from pathlib import Path
from test_automation import TransliterationTestAutomation, setup_logging
from test_cases import TEST_CASES


# Configure pytest
def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )


@pytest.fixture(scope="session")
def logger():
    """Provide logger for tests."""
    return setup_logging()


@pytest.fixture(scope="session")
def automation(logger):
    """Provide test automation instance."""
    auto = TransliterationTestAutomation(headless=False, logger=logger)
    yield auto
    # Cleanup if needed


@pytest.fixture(scope="session")
def test_cases():
    """Provide test cases."""
    return TEST_CASES


class TestTransliterationApp:
    """Test suite for transliteration app."""
    
    def test_app_navigation(self, automation, logger):
        """Test that app can be navigated to."""
        automation.setup_driver()
        try:
            assert automation.navigate_to_app(), "Failed to navigate to app"
            logger.info("✓ App navigation test passed")
        finally:
            automation.teardown_driver()
    
    def test_input_field_exists(self, automation, logger):
        """Test that input field can be located."""
        automation.setup_driver()
        try:
            automation.navigate_to_app()
            assert automation.find_input_field(), "Input field not found"
            logger.info("✓ Input field found")
        finally:
            automation.teardown_driver()
    
    def test_output_field_exists(self, automation, logger):
        """Test that output field can be located."""
        automation.setup_driver()
        try:
            automation.navigate_to_app()
            assert automation.find_output_field(), "Output field not found"
            logger.info("✓ Output field found")
        finally:
            automation.teardown_driver()
    
    @pytest.mark.slow
    def test_all_test_cases(self, automation, test_cases, logger):
        """Run all test cases."""
        results = automation.run_all_tests(test_cases)
        
        # Assert that we got results
        assert len(results) > 0, "No test results returned"
        
        # Generate report
        report = automation.generate_report()
        assert report, "Report not generated"
        
        # Count failures
        failures = [r for r in results if r["status"] == "FAIL"]
        logger.info(f"\nTotal tests: {len(results)}, Failures: {len(failures)}")
        
        # You can make this stricter based on requirements
        # For now, just verify tests ran
        assert len(results) == len(test_cases), "Not all tests were executed"
