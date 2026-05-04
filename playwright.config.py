"""
Playwright configuration for Singlish transliteration testing.

This module defines the test environment setup and browser configuration
for running the test suite against the Chat Sinhala translator.
"""

# Test configuration
config = {
    'testDir': './tests',
    'timeout': 30000,
    'retries': 0,
    'reporter': [
        ['list'],
        ['json', {'outputFile': 'results/test-results.json'}]
    ],
    'use': {
        'baseURL': 'https://www.pixelssuite.com',
        'headless': True,
        'viewport': {'width': 1280, 'height': 720},
        'actionTimeout': 15000,
        'navigationTimeout': 30000,
    },
    'projects': [
        {
            'name': 'chromium',
            'use': {'browserName': 'chromium'},
        },
    ],
    'outputDir': 'results/artifacts',
}


# Browser launch options
BROWSER_OPTIONS = {
    'headless': config['use']['headless'],
}

# Viewport configuration
VIEWPORT = config['use']['viewport']

# Base URL for all tests
BASE_URL = config['use']['baseURL']

# Timeouts (in milliseconds)
ACTION_TIMEOUT = config['use']['actionTimeout']
NAVIGATION_TIMEOUT = config['use']['navigationTimeout']
TEST_TIMEOUT = config['timeout']

# Output configuration
OUTPUT_DIR = config['outputDir']
RESULTS_FILE = 'results/test-results.json'
