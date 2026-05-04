"""
Singlish → Sinhala Transliteration Test Suite
Target: https://www.pixelssuite.com/chat-translator

This module tests the Chat Sinhala transliteration feature using Playwright.
It validates both positive and negative test cases for the Singlish input/Sinhala output conversion.
"""

import asyncio
import json
import os
from pathlib import Path
from playwright.async_api import async_playwright

# ─────────────────────────────────────────────────────────────────────────────
# Helper: load the page and select "Chat Sinhala" mode
# ─────────────────────────────────────────────────────────────────────────────
async def open_chat_translator(page):
    """Navigate to the Chat Translator and ensure Chat Sinhala mode is active."""
    await page.goto('https://www.pixelssuite.com/chat-translator', wait_until='domcontentloaded')
    
    # Make sure the "Chat Sinhala" tab / toggle is active
    chat_tab = page.locator('text=Chat Sinhala').first
    if await chat_tab.is_visible():
        await chat_tab.click()
    
    await page.wait_for_timeout(1000)


# ─────────────────────────────────────────────────────────────────────────────
# Helper: type input and capture output
# ─────────────────────────────────────────────────────────────────────────────
async def transliterate(page, input_text):
    """Type input into the text box and retrieve the transliterated output."""
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


# ─────────────────────────────────────────────────────────────────────────────
# Result collector
# ─────────────────────────────────────────────────────────────────────────────
results = []


def input_length_type(input_text):
    """Determine input length category: S (short), M (medium), or L (long)."""
    length = len(input_text)
    if length <= 30:
        return 'S'
    elif length <= 299:
        return 'M'
    else:
        return 'L'


# ─────────────────────────────────────────────────────────────────────────────
# 50 Negative Test Cases
# ─────────────────────────────────────────────────────────────────────────────
TEST_CASES = [
    # ── 1) Question forms ──────────────────────────────────────────────────────
    {
        'id': 'Neg_0001',
        'input': 'mokakda oya karanne?',
        'expectedOutput': 'මොකක්ද ඔයා කරන්නේ?',
        'types': 'Question forms',
        'rationale': 'A direct question asking what someone is doing — the system fails to correctly transliterate "mokakda" and "karanne".',
    },
    {
        'id': 'Neg_0002',
        'input': 'oya koheda inna hithan inne ada?',
        'expectedOutput': 'ඔයා කොහේද ඉන්න හිතන් ඉන්නේ අද?',
        'types': 'Question forms',
        'rationale': 'A question about where someone plans to stay today — "koheda" and "hithan inne" are commonly mistransliterated.',
    },

    # ── 2) Command forms ───────────────────────────────────────────────────────
    {
        'id': 'Neg_0003',
        'input': 'apita heta eliyatama yanna one.',
        'expectedOutput': 'අපිට හෙට එළියටම යන්න ඕනේ.',
        'types': 'Command forms',
        'rationale': 'A command stating they must go out tomorrow — "eliyatama" causes incorrect output.',
    },
    {
        'id': 'Neg_0004',
        'input': 'thamuseta giya thaenata phone karanna kiwwa.',
        'expectedOutput': 'තාමුසේට ගිය තැනට phone කරන්න කිව්වා.',
        'types': 'Command forms',
        'rationale': 'Command to call wherever he went — "thamuseta" and "thaenata" fail to transliterate correctly.',
    },

    # ── 3) Greetings ───────────────────────────────────────────────────────────
    {
        'id': 'Neg_0005',
        'input': 'kohomada bro, hodatama innawada?',
        'expectedOutput': 'කොහොමද bro, හොඳටම ඉන්නවද?',
        'types': 'Greetings',
        'rationale': 'Casual greeting asking if someone is doing well — "hodatama" fails to map correctly.',
    },
    {
        'id': 'Neg_0006',
        'input': 'subha aluth awuruddak wewa machan!',
        'expectedOutput': 'සුභ අලුත් අවුරුද්දක් වේවා මචන්!',
        'types': 'Greetings',
        'rationale': 'New Year wish to a friend — "wewa" and "machan" are frequently mis-transliterated.',
    },

    # ── 4) Requests ────────────────────────────────────────────────────────────
    {
        'id': 'Neg_0007',
        'input': 'puluwan nam mage jacket eka gahuwa thaenata yawanna.',
        'expectedOutput': 'පුළුවන් නම් මගේ jacket එක ගාහුව තැනට යවන්න.',
        'types': 'Requests',
        'rationale': 'Request to send something to where the jacket was — "gahuwa thaenata" fails.',
    },
    {
        'id': 'Neg_0008',
        'input': 'please mage number eka save karanna mahapath wenawada.',
        'expectedOutput': 'please මගේ number එක save කරන්න මහාපත් වෙනවද.',
        'types': 'Requests',
        'rationale': 'Polite request to save a number — "mahapath wenawada" is incorrectly handled.',
    },

    # ── 5) Responses ───────────────────────────────────────────────────────────
    {
        'id': 'Neg_0009',
        'input': 'nae bro, mama danna nae.',
        'expectedOutput': 'නෑ bro, මම දන්න නෑ.',
        'types': 'Responses',
        'rationale': 'Response saying "No bro, I don\'t know" — "nae" repeated is often mis-handled.',
    },
    {
        'id': 'Neg_0010',
        'input': 'achchi, mama heta balamu kiyala kiwwa.',
        'expectedOutput': 'අච්චි, මම හෙට බලමු කියලා කිව්වා.',
        'types': 'Responses',
        'rationale': 'Response relaying what someone said about checking tomorrow — "achchi" fails.',
    },

    # ── 6) Repeated Words ─────────────────────────────────────────────────────
    {
        'id': 'Neg_0011',
        'input': 'eka eka katha karanna epa, kollo awoth ammata kiyawi.',
        'expectedOutput': 'ඒක ඒක කතා කරන්න එපා, කොල්ලො ආවොත් අම්මට කියාවි.',
        'types': 'Repeated Words',
        'rationale': 'Repeated phrase "eka eka" meaning one by one — repetition causes transliteration error.',
    },
    {
        'id': 'Neg_0012',
        'input': 'awa awa, mata therenne nae mokakwath.',
        'expectedOutput': 'ආව ආව, මට තේරෙන්නේ නෑ මොකක්වත්.',
        'types': 'Repeated Words',
        'rationale': 'Repeated "awa awa" expressing indifference — system fails to handle word-level repetition.',
    },

    # ── 7) Inputs with Punctuation Marks ──────────────────────────────────────
    {
        'id': 'Neg_0013',
        'input': 'mama... mata therila nae, api eka tharamata thereen nokara neda?',
        'expectedOutput': 'මම... මට තේරිලා නෑ, අපි එකතරමට තේරෙන් නොකරා නේද?',
        'types': 'Inputs with Punctuation Marks',
        'rationale': 'Ellipsis mid-sentence with question mark — punctuation causes the output to break.',
    },
    {
        'id': 'Neg_0014',
        'input': 'api yanawa! oyath enavada, hari?',
        'expectedOutput': 'අපි යනවා! ඔයාත් එනවද, හරි?',
        'types': 'Inputs with Punctuation Marks',
        'rationale': 'Exclamation and comma with question mark — mixed punctuation disrupts transliteration.',
    },

    # ── 8) Romanization / Spelling Variants ───────────────────────────────────
    {
        'id': 'Neg_0015',
        'input': 'mn oyta gyhilla blnwa.',
        'expectedOutput': 'මං ඔයාට ගැහිල්ලා බලනවා.',
        'types': 'Romanization / Spelling Variants',
        'rationale': 'Heavily abbreviated spelling of a common sentence — the system cannot map shortened consonants.',
    },
    {
        'id': 'Neg_0016',
        'input': 'eyaagen passe eyaa enawaa kiyalaa kiwwaa.',
        'expectedOutput': 'එයාගේ පස්සේ එයා එනවා කියලා කිව්වා.',
        'types': 'Romanization / Spelling Variants',
        'rationale': 'Elongated vowels (double "a") for emphasis — the system does not normalise doubled vowels.',
    },

    # ── 9) Isolated English Word Insertions in Singlish ───────────────────────
    {
        'id': 'Neg_0017',
        'input': 'mama ada gym giya hadisi wage feeling karanna.',
        'expectedOutput': 'මම අද gym ගිය හදිසි වගේ feeling කරන්න.',
        'types': 'Isolated English Word Insertions in Singlish',
        'rationale': 'Single English words "gym" and "feeling" inserted into Singlish — system breaks output around them.',
    },
    {
        'id': 'Neg_0018',
        'input': 'oya doctor ekata giyada heta appointment eka ganna.',
        'expectedOutput': 'ඔයා doctor එකට ගියද හෙට appointment එක ගන්න.',
        'types': 'Isolated English Word Insertions in Singlish',
        'rationale': 'English nouns "doctor" and "appointment" cause the surrounding Singlish to be mis-transliterated.',
    },

    # ── 10) Multi-Word English Phrases in Singlish ────────────────────────────
    {
        'id': 'Neg_0019',
        'input': 'mama heta office nae, working from home.',
        'expectedOutput': 'මම හෙට office නෑ, working from home.',
        'types': 'Multi-Word English Phrases in Singlish',
        'rationale': 'Multi-word English phrase "working from home" embedded — system fails to preserve the phrase and corrupts surrounding Singlish.',
    },
    {
        'id': 'Neg_0020',
        'input': 'api traffic ekata hema hari slow and steady move wenawa.',
        'expectedOutput': 'අපි traffic එකට හේම හරි slow and steady move වෙනවා.',
        'types': 'Multi-Word English Phrases in Singlish',
        'rationale': 'English idiom "slow and steady" within Singlish causes incorrect transliteration of the surrounding words.',
    },

    # ── 11) English Digital Terms in Singlish ─────────────────────────────────
    {
        'id': 'Neg_0021',
        'input': 'oya Bluetooth on karadadd, file eka share karamu.',
        'expectedOutput': 'ඔයා Bluetooth on කරදාද්ද, file එක share කරමු.',
        'types': 'English Digital Terms in Singlish',
        'rationale': 'Digital terms "Bluetooth" and "share" — system fails to correctly output Singlish portions adjacent to tech words.',
    },
    {
        'id': 'Neg_0022',
        'input': 'mage laptop eke battery finish wela, charger ekkuth nae.',
        'expectedOutput': 'මගේ laptop එකේ battery finish වෙලා, charger එකුත් නෑ.',
        'types': 'English Digital Terms in Singlish',
        'rationale': 'Multiple digital terms in one sentence cause the system to lose correct mapping of Singlish particles.',
    },

    # ── 12) Platform/App Names in Singlish ────────────────────────────────────
    {
        'id': 'Neg_0023',
        'input': 'YouTube eke comment ekak dala mama giya, balannako.',
        'expectedOutput': 'YouTube එකේ comment එකක් දාලා මම ගියා, බලන්නකො.',
        'types': 'Platform/App Names in Singlish',
        'rationale': 'Platform name "YouTube" next to Singlish breaks transliteration of "balannako".',
    },
    {
        'id': 'Neg_0024',
        'input': 'Instagram story eka dala mama kalin giya.',
        'expectedOutput': 'Instagram story එක දාලා මම කලින් ගියා.',
        'types': 'Platform/App Names in Singlish',
        'rationale': 'App name "Instagram" followed by English "story" and Singlish — mixed context causes failure.',
    },

    # ── 13) English Abbreviations/Acronyms in Singlish ────────────────────────
    {
        'id': 'Neg_0025',
        'input': 'CV eka update karanna ona, HR kiyanawa.',
        'expectedOutput': 'CV එක update කරන්න ඕනේ, HR කියනවා.',
        'types': 'English Abbreviations/Acronyms in Singlish',
        'rationale': 'Acronyms "CV" and "HR" disrupt transliteration of adjacent Singlish words.',
    },
    {
        'id': 'Neg_0026',
        'input': 'OT karala GDP gana presentation ekak hadannada?',
        'expectedOutput': 'OT කරලා GDP ගැන presentation එකක් හදන්නද?',
        'types': 'English Abbreviations/Acronyms in Singlish',
        'rationale': 'Economic acronym "GDP" inside a question — system fails on "hadannada" following the acronym.',
    },

    # ── 14) English Clipped Forms in Singlish ─────────────────────────────────
    {
        'id': 'Neg_0027',
        'input': 'heta uni nae, holiday kiyala kiwwa.',
        'expectedOutput': 'හෙට uni නෑ, holiday කියලා කිව්වා.',
        'types': 'English Clipped Forms in Singlish',
        'rationale': 'Clipped form "uni" for university not recognised correctly by the system.',
    },
    {
        'id': 'Neg_0028',
        'input': 'oya ada gym poddak dhamuwada, bro?',
        'expectedOutput': 'ඔයා අද gym පොඩ්ඩක් දාමුවද, bro?',
        'types': 'English Clipped Forms in Singlish',
        'rationale': 'Clipped "bro" used as address alongside Singlish — creates incorrect output around "dhamuwada".',
    },

    # ── 15) Place Names Embedded in Singlish ──────────────────────────────────
    {
        'id': 'Neg_0029',
        'input': 'api Kandy giya welawata Peradeniya road eke traffic mara.',
        'expectedOutput': 'අපි Kandy ගිය වේලාවට Peradeniya road එකේ traffic මාර.',
        'types': 'Place Names Embedded in Singlish',
        'rationale': 'Place names "Kandy" and "Peradeniya" cause surrounding Singlish to be mis-converted.',
    },
    {
        'id': 'Neg_0030',
        'input': 'Colombo 3 ekata yanna bus deka thenata pita wela.',
        'expectedOutput': 'Colombo 3 එකට යන්න bus දෙකතෙනට පිට වෙලා.',
        'types': 'Place Names Embedded in Singlish',
        'rationale': 'City name with number "Colombo 3" alongside Singlish breaks transliteration.',
    },

    # ── 16) Person Names Embedded in Singlish ─────────────────────────────────
    {
        'id': 'Neg_0031',
        'input': 'Dilshan aiye ada bohoma late awe, boss hariyata kiyawi.',
        'expectedOutput': 'Dilshan අයියේ අද බොහොම late ආවේ, boss හරියට කියාවි.',
        'types': 'Person Names Embedded in Singlish',
        'rationale': 'Person name "Dilshan" causes the word after it to be incorrectly transliterated.',
    },
    {
        'id': 'Neg_0032',
        'input': 'Nishani saha Priyanka dennama ekka giya, mata kiwwanae.',
        'expectedOutput': 'නිශානි සහ Priyanka දෙන්නම එකක ගියා, මට කිව්වනේ.',
        'types': 'Person Names Embedded in Singlish',
        'rationale': 'Two person names connected with "saha" — system fails to handle multiple name entities.',
    },

    # ── 17) Inputs with Numbers and Numeric Suffixes ──────────────────────────
    {
        'id': 'Neg_0033',
        'input': 'mama 3rd floor ekata giya, lift eka nae wunath.',
        'expectedOutput': 'මම 3rd floor එකට ගියා, lift එක නෑ වුනත්.',
        'types': 'Inputs with Numbers and Numeric Suffixes',
        'rationale': 'Ordinal suffix "3rd" not handled — system corrupts surrounding words.',
    },
    {
        'id': 'Neg_0034',
        'input': 'class eka 9.30am ta patan gahuwa, 2nd time late wunama.',
        'expectedOutput': 'class එක 9.30am ට පටන් ගාහුව, 2nd time late වුනාම.',
        'types': 'Inputs with Numbers and Numeric Suffixes',
        'rationale': 'Time with number "9.30am" and ordinal "2nd" both present — combined failure.',
    },

    # ── 18) Inputs with Currency ───────────────────────────────────────────────
    {
        'id': 'Neg_0035',
        'input': 'e jacket eka Rs. 4500 ta gatta, sale price.',
        'expectedOutput': 'ඒ jacket එක Rs. 4500 ට ගත්තා, sale price.',
        'types': 'Inputs with Currency',
        'rationale': 'Currency symbol "Rs." followed by amount disrupts transliteration of surrounding Singlish.',
    },
    {
        'id': 'Neg_0036',
        'input': 'USD 150 kiyanne lankave rupiyal walata mara hari.',
        'expectedOutput': 'USD 150 කියන්නේ ලංකාවේ රුපියල් වලට මාර හරි.',
        'types': 'Inputs with Currency',
        'rationale': 'Currency acronym "USD" with amount inside a Singlish sentence — system corrupts "kiyanne".',
    },

    # ── 19) Inputs with Time Formats ──────────────────────────────────────────
    {
        'id': 'Neg_0037',
        'input': 'meeting eka 3:00PM ta schedule kara thiyanawa.',
        'expectedOutput': 'meeting එක 3:00PM ට schedule කරා තියනවා.',
        'types': 'Inputs with Time Formats',
        'rationale': 'Time format "3:00PM" embedded in Singlish — system fails on "kara thiyanawa" after the time.',
    },
    {
        'id': 'Neg_0038',
        'input': 'bus eka 6.45am ta wenna one api ganna.',
        'expectedOutput': 'bus එක 6.45am ට වෙන්න ඕනේ අපි ගන්න.',
        'types': 'Inputs with Time Formats',
        'rationale': 'AM time with decimal format causes system to lose transliteration of "wenna one".',
    },

    # ── 20) Inputs with Dates ─────────────────────────────────────────────────
    {
        'id': 'Neg_0039',
        'input': 'birthday eka March 22 ta, gift eka ganna ona.',
        'expectedOutput': 'birthday එක March 22 ට, gift එක ගන්න ඕනේ.',
        'types': 'Inputs with Dates',
        'rationale': 'Date with month name "March 22" breaks transliteration of "gift eka ganna ona".',
    },
    {
        'id': 'Neg_0040',
        'input': 'submit karanna one 2026-05-10 ta kalin.',
        'expectedOutput': 'submit කරන්න ඕනේ 2026-05-10 ට කලින්.',
        'types': 'Inputs with Dates',
        'rationale': 'ISO date format "2026-05-10" within Singlish sentence causes incorrect output.',
    },

    # ── 21) Inputs with Unit of Measurements ──────────────────────────────────
    {
        'id': 'Neg_0041',
        'input': 'mama kilograma 2k vitara thava kanna one.',
        'expectedOutput': 'මම කිලෝග්‍රාම 2ක් විතරා තව කන්න ඕනේ.',
        'types': 'Inputs with Unit of Measurements',
        'rationale': 'Mass unit "kilograma 2k" causes system to fail on "vitara thava kanna one".',
    },
    {
        'id': 'Neg_0042',
        'input': 'e board eka centi 50k hari 60k wenna one.',
        'expectedOutput': 'ඒ board එක සෙන්ටි 50ක් හරි 60ක් වෙන්න ඕනේ.',
        'types': 'Inputs with Unit of Measurements',
        'rationale': 'Measurement unit "centi" with numeric suffix causes incorrect Sinhala output.',
    },

    # ── 22) Inputs with Slang and Casual Phrasing ─────────────────────────────
    {
        'id': 'Neg_0043',
        'input': 'meka bohoma gas, uba hithagena inne mokakda?',
        'expectedOutput': 'මේක බොහොම ගාස්, උඹ හිතාගෙන ඉන්නේ මොකක්ද?',
        'types': 'Inputs with Slang and Casual Phrasing',
        'rationale': 'Slang "gas" meaning nonsense alongside "uba" — casual phrasing causes system failure.',
    },
    {
        'id': 'Neg_0044',
        'input': 'machang, e kella bohoma niyarayi, uba dannawada eya.',
        'expectedOutput': 'මචං, ඒ කෙල්ලා බොහොම නියරයි, උඹ දන්නවද එයා.',
        'types': 'Inputs with Slang and Casual Phrasing',
        'rationale': 'Slang "machang" and "niyarayi" (cool/awesome) — informal phrasing is not correctly mapped.',
    },

    # ── 23) Online Identifiers in Singlish ────────────────────────────────────
    {
        'id': 'Neg_0045',
        'input': 'mee profile link eka balanna: https://linkedin.com/in/kasun',
        'expectedOutput': 'මේ profile link එක බලන්න: https://linkedin.com/in/kasun',
        'types': 'Online Identifiers in Singlish',
        'rationale': 'Full URL with path appended — system corrupts the Singlish portion before the URL.',
    },
    {
        'id': 'Neg_0046',
        'input': '@Kasun bro, oyage email eka dannawada, mata mail ekak ewanna.',
        'expectedOutput': '@Kasun bro, ඔයාගේ email එක දන්නවද, මට mail එකක් එවන්න.',
        'types': 'Online Identifiers in Singlish',
        'rationale': '@mention at the start with Singlish causes incorrect output for the following sentence.',
    },

    # ── 24) Inputs Containing Emojis ──────────────────────────────────────────
    {
        'id': 'Neg_0047',
        'input': 'bohoma stressful day ekak 😩, heta poddak rest gamu.',
        'expectedOutput': 'බොහොම stressful day එකක් 😩, හෙට පොඩ්ඩක් rest ගමු.',
        'types': 'Inputs Containing Emojis',
        'rationale': 'Emoji mid-sentence causes the transliteration after it to fail completely.',
    },
    {
        'id': 'Neg_0048',
        'input': 'happy birthday machan 🎂🥳 bohoma pin!',
        'expectedOutput': 'happy birthday මචන් 🎂🥳 බොහොම පිං!',
        'types': 'Inputs Containing Emojis',
        'rationale': 'Multiple consecutive emojis confuse the parser, breaking "bohoma pin" transliteration.',
    },

    # ── Remaining 2 (any type) ─────────────────────────────────────────────────
    {
        'id': 'Neg_0049',
        'input': 'mata heta amma ekka Kandy gihilla doctor ekata yanna one, 8am ta patan.',
        'expectedOutput': 'මට හෙට අම්මා එකක Kandy ගිහිල්ලා doctor එකට යන්න ඕනේ, 8am ට පටන්.',
        'types': 'Place Names Embedded in Singlish; Inputs with Time Formats; Isolated English Word Insertions in Singlish',
        'rationale': 'Combined: place name "Kandy", English word "doctor", and time "8am" all in one sentence — system fails on multiple levels.',
    },
    {
        'id': 'Neg_0050',
        'input': 'sirawata bro 🔥, CV eka update karala HR ekata 2026-04-30 ta kalin ewanna.',
        'expectedOutput': 'සිරාවට bro 🔥, CV එක update කරලා HR එකට 2026-04-30 ට කලින් එවන්න.',
        'types': 'Inputs with Slang and Casual Phrasing; English Abbreviations/Acronyms in Singlish; Inputs with Dates; Inputs Containing Emojis',
        'rationale': 'Complex combined input with slang "sirawata", emoji, acronyms "CV"/"HR", and ISO date — system fails across all these dimensions.',
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# Main test function
# ─────────────────────────────────────────────────────────────────────────────
async def run_tests():
    """Run all test cases against the Chat Sinhala translator."""
    # Create results directory
    results_dir = Path('results')
    results_dir.mkdir(exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        print("\n" + "="*80)
        print("Chat Sinhala Transliteration – 50 Negative Test Cases")
        print("="*80 + "\n")

        try:
            for i, tc in enumerate(TEST_CASES, 1):
                print(f"Testing {i}/50: {tc['id']} | {tc['types'].split(';')[0].strip()}...", end=" ")

                await open_chat_translator(page)
                actual_output = await transliterate(page, tc['input'])

                length_type = input_length_type(tc['input'])
                passed = actual_output == tc['expectedOutput']
                status = 'Pass' if passed else 'Fail'

                results.append({
                    'tcId': tc['id'],
                    'inputLengthType': length_type,
                    'input': tc['input'],
                    'expectedOutput': tc['expectedOutput'],
                    'actualOutput': actual_output,
                    'status': status,
                    'types': tc['types'],
                    'rationale': tc['rationale'],
                })

                # Negative cases should fail (not match expected output)
                if actual_output != tc['expectedOutput']:
                    print("✓ (Failed as expected)")
                else:
                    print("✗ (Unexpectedly passed)")

        finally:
            await browser.close()

        # Write JSON results
        output_path = results_dir / 'test-results-summary.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print("\n" + "="*80)
        print(f"✅ Results saved to {output_path}")
        print(f"   Total tests: {len(results)}")
        print(f"   Failed (as expected): {sum(1 for r in results if r['status'] == 'Fail')}")
        print(f"   Passed (unexpected): {sum(1 for r in results if r['status'] == 'Pass')}")
        print("="*80 + "\n")


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    asyncio.run(run_tests())
