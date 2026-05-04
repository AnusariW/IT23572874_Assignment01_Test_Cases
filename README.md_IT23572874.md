# Assignment 1 – Chat Sinhala Transliteration Test Automation

**Module:** IT3040 – ITPM | **Option:** 1 (Transliteration Accuracy Testing)

This Playwright project automates **50 negative test cases** that verify where the Chat Sinhala transliteration feature at https://www.pixelssuite.com/chat-translator fails to correctly convert chat-style Singlish into Sinhala.

---

## Prerequisites

| Tool | Version |
|------|---------|
| Python | >= 3.8 |
| pip | >= 21.x |

---

## Installation

```bash
# 1. Clone the repository
git clone <YOUR_GITHUB_REPO_URL>
cd test_automation

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install Playwright browsers
python -m playwright install chromium
```

---

## Running the Tests

```bash
# Run all 50 test cases (headless)
python run_tests.py

# Run with browser visible
python run_tests.py --headed

# View test report
python run_tests.py --report

# Install browsers (first time only)
python run_tests.py --install
```

Results are saved to:
- results/test-results-summary.json — per-test summary (TC ID, input, expected, actual, status)
- results/artifacts/ — screenshots and traces (on failure)

---

## Project Structure

```
test_automation/
├── singlish_transliteration.py   # All 50 test cases
├── run_tests.py                  # Test runner script
├── playwright.config.py          # Playwright configuration
├── requirements.txt              # Python dependencies
├── setup.py                      # Project setup
├── results/                      # Auto-generated results
└── README.md
```

---

## Test Case Summary

All 50 test cases are negative (Neg_) — they expect the system to produce incorrect output.
The cases cover all 24 Singlish input types defined in Appendix 1:

 #  | Input Type                          | Test Cases
----|-------------------------------------|------------------
 1  | Question forms                      | Neg_0001, Neg_0002
 2  | Command forms                       | Neg_0003, Neg_0004
 3  | Greetings                           | Neg_0005, Neg_0006
 4  | Requests                            | Neg_0007, Neg_0008
 5  | Responses                           | Neg_0009, Neg_0010
 6  | Repeated Words                      | Neg_0011, Neg_0012
 7  | Inputs with Punctuation Marks       | Neg_0013, Neg_0014
 8  | Romanization / Spelling Variants    | Neg_0015, Neg_0016
 9  | Isolated English Word Insertions    | Neg_0017, Neg_0018
10  | Multi-Word English Phrases          | Neg_0019, Neg_0020
11  | English Digital Terms               | Neg_0021, Neg_0022
12  | Platform/App Names                  | Neg_0023, Neg_0024
13  | English Abbreviations/Acronyms      | Neg_0025, Neg_0026
14  | English Clipped Forms               | Neg_0027, Neg_0028
15  | Place Names Embedded                | Neg_0029, Neg_0030
16  | Person Names Embedded               | Neg_0031, Neg_0032
17  | Numbers and Numeric Suffixes        | Neg_0033, Neg_0034
18  | Inputs with Currency                | Neg_0035, Neg_0036
19  | Inputs with Time Formats            | Neg_0037, Neg_0038
20  | Inputs with Dates                   | Neg_0039, Neg_0040
21  | Unit of Measurements                | Neg_0041, Neg_0042
22  | Slang and Casual Phrasing           | Neg_0043, Neg_0044
23  | Online Identifiers                  | Neg_0045, Neg_0046
24  | Inputs Containing Emojis            | Neg_0047, Neg_0048
 -  | Combined (any type)                 | Neg_0049, Neg_0050
