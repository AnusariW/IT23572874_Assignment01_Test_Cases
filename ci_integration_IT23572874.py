"""
CI/CD Integration utilities for test automation results.
Use this to parse and process test results in CI/CD pipelines.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class TestResultsProcessor:
    """Process and analyze test automation results."""
    
    def __init__(self, results_file: str):
        """Initialize processor with results JSON file."""
        self.results_file = Path(results_file)
        self.results = []
        self.load_results()
    
    def load_results(self) -> None:
        """Load results from JSON file."""
        if not self.results_file.exists():
            raise FileNotFoundError(f"Results file not found: {self.results_file}")
        
        with open(self.results_file, 'r', encoding='utf-8') as f:
            self.results = json.load(f)
    
    def get_summary(self) -> Dict:
        """Get test execution summary."""
        total = len(self.results)
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        failed = sum(1 for r in self.results if r["status"] == "FAIL")
        errors = sum(1 for r in self.results if r["status"] == "ERROR")
        
        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "pass_rate": (passed / total * 100) if total > 0 else 0,
        }
    
    def get_failed_tests(self) -> List[Dict]:
        """Get list of failed tests."""
        return [r for r in self.results if r["status"] == "FAIL"]
    
    def get_error_tests(self) -> List[Dict]:
        """Get list of tests with errors."""
        return [r for r in self.results if r["status"] == "ERROR"]
    
    def generate_github_summary(self) -> str:
        """Generate summary for GitHub Actions."""
        summary = self.get_summary()
        
        output = f"""# Test Automation Results

## Summary
- **Total Tests**: {summary['total']}
- **Passed**: {summary['passed']} ✓
- **Failed**: {summary['failed']} ✗
- **Errors**: {summary['errors']} ⚠
- **Pass Rate**: {summary['pass_rate']:.1f}%

"""
        
        failed_tests = self.get_failed_tests()
        if failed_tests:
            output += "## Failed Tests\n"
            for test in failed_tests:
                output += f"- {test['tc_id']}: {test['name']}\n"
            output += "\n"
        
        error_tests = self.get_error_tests()
        if error_tests:
            output += "## Tests with Errors\n"
            for test in error_tests:
                output += f"- {test['tc_id']}: {test['error']}\n"
            output += "\n"
        
        return output
    
    def should_pass_ci(self, min_pass_rate: float = 100.0) -> bool:
        """Determine if CI should pass."""
        summary = self.get_summary()
        return summary["pass_rate"] >= min_pass_rate and summary["errors"] == 0
    
    def print_report(self) -> None:
        """Print formatted report."""
        summary = self.get_summary()
        
        print("\n" + "=" * 70)
        print("TEST AUTOMATION RESULTS")
        print("=" * 70)
        print(f"Total Tests:    {summary['total']}")
        print(f"Passed:         {summary['passed']} ({summary['pass_rate']:.1f}%)")
        print(f"Failed:         {summary['failed']}")
        print(f"Errors:         {summary['errors']}")
        print("=" * 70)
        
        failed = self.get_failed_tests()
        if failed:
            print("\n❌ FAILED TESTS:")
            for test in failed:
                print(f"  - {test['tc_id']}: {test['name']}")
        
        errors = self.get_error_tests()
        if errors:
            print("\n⚠️  ERROR TESTS:")
            for test in errors:
                print(f"  - {test['tc_id']}: {test['error']}")
        
        if not failed and not errors:
            print("\n✅ ALL TESTS PASSED!")
        
        print()


# GitHub Actions Integration
def github_actions_integration(results_file: str, min_pass_rate: float = 100.0):
    """Integrate with GitHub Actions."""
    processor = TestResultsProcessor(results_file)
    
    # Print summary for GitHub Actions
    summary_output = processor.generate_github_summary()
    print(summary_output)
    
    # Set output for GitHub Actions
    summary = processor.get_summary()
    print(f"::set-output name=total::{summary['total']}")
    print(f"::set-output name=passed::{summary['passed']}")
    print(f"::set-output name=failed::{summary['failed']}")
    print(f"::set-output name=pass_rate::{summary['pass_rate']:.1f}")
    
    # Exit with appropriate code
    if not processor.should_pass_ci(min_pass_rate):
        sys.exit(1)


# GitLab CI Integration
def gitlab_ci_integration(results_file: str, min_pass_rate: float = 100.0):
    """Integrate with GitLab CI."""
    processor = TestResultsProcessor(results_file)
    processor.print_report()
    
    if not processor.should_pass_ci(min_pass_rate):
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="CI/CD Integration for test results")
    parser.add_argument("results_file", help="Path to results JSON file")
    parser.add_argument("--min-pass-rate", type=float, default=100.0,
                       help="Minimum pass rate to pass CI (default: 100.0)")
    parser.add_argument("--ci", choices=["github", "gitlab"], default="gitlab",
                       help="CI platform to integrate with")
    
    args = parser.parse_args()
    
    if args.ci == "github":
        github_actions_integration(args.results_file, args.min_pass_rate)
    else:
        gitlab_ci_integration(args.results_file, args.min_pass_rate)
