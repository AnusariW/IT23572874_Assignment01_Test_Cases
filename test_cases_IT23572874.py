"""
Test case definitions for the Singlish → Sinhala transliteration app.
Target: https://www.pixelssuite.com/chat-translator

Columns:
  tc_id          : Unique test case ID (Pos_Fun_XXXX / Neg_Fun_XXXX / Pos_UI_XXXX / Neg_UI_XXXX)
  name           : Short descriptive name
  input_length   : S (≤30 chars) | M (31–299 chars) | L (≥300 chars)
  singlish_input : Raw Singlish input text
  expected_output: Expected Sinhala output (empty string = output captured at runtime)
  what_covered   : 4-line coverage tag (Input Type | Grammar Focus | Length | Quality Focus)

NOTE: Expected outputs marked with [VERIFY] must be confirmed against the live app
      before finalising the test suite.
"""

TEST_CASES = [

    # ─────────────────────────────────────────────────────────────────
    # POSITIVE FUNCTIONAL — Simple sentences
    # ─────────────────────────────────────────────────────────────────
    {
        "tc_id": "Pos_Fun_0001",
        "name": "Convert a short daily greeting phrase",
        "input_length": "S",
        "singlish_input": "oyaata kohomadha?",
        "expected_output": "ඔයාට කොහොමද?",
        "what_covered": (
            "· Greeting / request / response\n"
            "· Interrogative (question)\n"
            "· S (≤30 characters)\n"
            "· Accuracy validation"
        ),
    },
    {
        "tc_id": "Pos_Fun_0002",
        "name": "Long mixed-language input with slang + typo causes incorrect conversion",
        "input_length": "M",
        "singlish_input": (
            "machan mata adha meeting ekee Zoom link eka email ekak vidhihata evanna puLuvandha? "
            "Please send it before 3pm. Mama office yanna kalin check karanna oonea. "
            "Email ekak evanna amaarunam WhatsApp msg ekak dhaapan. Thx!"
        ),
        "expected_output": (
            "මචන් මට අද meeting එකේ Zoom link එක email එකක් විදිහට එවන්න පුළුවන්ද? "
            "Please send it before 3pm. මම office යන්න කලින් check කරන්න ඕනේ. "
            "Email එකක් එවන්න අමාරුනම් WhatsApp ම්ස්ග් එකක් දාපන්. ථx!!"
        ),
        "what_covered": (
            "· Mixed Singlish + English\n"
            "· Compound sentence\n"
            "· M (31–299 characters)\n"
            "· Robustness validation"
        ),
    },
    {
        "tc_id": "Pos_Fun_0003",
        "name": "Convert a short request phrase",
        "input_length": "S",
        "singlish_input": "mata help ekak karanna puLuvandha?",
        "expected_output": "මට help එකක් කරන්න පුළුවන්ද?",
        "what_covered": (
            "· Greeting / request / response\n"
            "· Interrogative (question)\n"
            "· S (≤30 characters)\n"
            "· Accuracy validation"
        ),
    },
    {
        "tc_id": "Pos_Fun_0004",
        "name": "Convert a simple present-tense statement",
        "input_length": "S",
        "singlish_input": "mama gedhara yanavaa.",
        "expected_output": "මම ගෙදර යනවා.",
        "what_covered": (
            "· Daily language usage\n"
            "· Simple sentence\n"
            "· S (≤30 characters)\n"
            "· Accuracy validation"
        ),
    },
    {
        "tc_id": "Pos_Fun_0005",
        "name": "Convert a short expression of need",
        "input_length": "S",
        "singlish_input": "mata bath oonee.",
        "expected_output": "මට බත් ඕනේ.",
        "what_covered": (
            "· Daily language usage\n"
            "· Simple sentence\n"
            "· S (≤30 characters)\n"
            "· Accuracy validation"
        ),
    },
    {
        "tc_id": "Pos_Fun_0006",
        "name": "Convert a short plural-subject sentence",
        "input_length": "S",
        "singlish_input": "api paasal yanavaa.",
        "expected_output": "අපි පාසල් යනවා.",
        "what_covered": (
            "· Daily language usage\n"
            "· Simple sentence\n"
            "· S (≤30 characters)\n"
            "· Accuracy validation"
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # POSITIVE FUNCTIONAL — Compound sentences
    # ─────────────────────────────────────────────────────────────────
    {
        "tc_id": "Pos_Fun_0007",
        "name": "Convert a compound sentence with contrast",
        "input_length": "M",
        "singlish_input": "mama gedhara yanavaa, haebaeyi vahina nisaa dhaenma yannee naee.",
        "expected_output": "මම ගෙදර යනවා, හැබැයි වහින නිසා දැන්ම යන්නේ නැහැ.",
        "what_covered": (
            "· Daily language usage\n"
            "· Compound sentence\n"
            "· M (31–299 characters)\n"
            "· Accuracy validation"
        ),
    },
    {
        "tc_id": "Pos_Fun_0008",
        "name": "Convert a compound sentence with two activities",
        "input_length": "M",
        "singlish_input": "api kaeema kanna yanavaa saha passe chithrapatayakuth balanavaa.",
        "expected_output": "අපි කෑම කන්න යනවා සහ පස්සේ චිත්‍රපටයකුත් බලනවා.",
        "what_covered": (
            "· Daily language usage\n"
            "· Compound sentence\n"
            "· M (31–299 characters)\n"
            "· Accuracy validation"
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # POSITIVE FUNCTIONAL — Complex / conditional sentences
    # ─────────────────────────────────────────────────────────────────
    {
        "tc_id": "Pos_Fun_0009",
        "name": "Convert a conditional complex sentence",
        "input_length": "M",
        "singlish_input": "oya enavaanam mama balan innavaa.",
        "expected_output": "ඔය එනවානම් මම බලන් ඉන්නවා.",
        "what_covered": (
            "· Daily language usage\n"
            "· Complex sentence\n"
            "· M (31–299 characters)\n"
            "· Accuracy validation"
        ),
    },
    {
        "tc_id": "Pos_Fun_0010",
        "name": "Convert a concessive complex sentence",
        "input_length": "M",
        "singlish_input": "vaessa unath api yanna epaeyi.",
        "expected_output": "වැස්ස උනත් අපි යන්න එපැයි.",
        "what_covered": (
            "· Daily language usage\n"
            "· Complex sentence\n"
            "· M (31–299 characters)\n"
            "· Accuracy validation"
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # POSITIVE FUNCTIONAL — Interrogative (questions)
    # ─────────────────────────────────────────────────────────────────
    {
        "tc_id": "Pos_Fun_0011",
        "name": "Convert an interrogative sentence about arrival time",
        "input_length": "M",
        "singlish_input": "oyaa kavadhdha enna hithan inne?",
        "expected_output": "ඔයා කවදද එන්න හිතන් ඉන්නේ?",
        "what_covered": (
            "· Daily language usage\n"
            "· Interrogative (question)\n"
            "· M (31–299 characters)\n"
            "· Accuracy validation"
        ),
    },
    {
        "tc_id": "Pos_Fun_0012",
        "name": "Convert a yes/no interrogative sentence",
        "input_length": "M",
        "singlish_input": "meeka hariyata vaeda karanavadha?",
        "expected_output": "මේකා හරියට වැද කරනවාද?",
        "what_covered": (
            "· Daily language usage\n"
            "· Interrogative (question)\n"
            "· M (31–299 characters)\n"
            "· Accuracy validation"
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # POSITIVE FUNCTIONAL — Imperative (commands)
    # ─────────────────────────────────────────────────────────────────
    {
        "tc_id": "Pos_Fun_0013",
        "name": "Convert a short imperative command — come quickly",
        "input_length": "S",
        "singlish_input": "vahaama enna.",
        "expected_output": "වහාම එන්න.",
        "what_covered": (
            "· Daily language usage\n"
            "· Imperative (command)\n"
            "· S (≤30 characters)\n"
            "· Accuracy validation"
        ),
    },
    {
        "tc_id": "Pos_Fun_0014",
        "name": "Convert a short imperative command — go forward",
        "input_length": "S",
        "singlish_input": "issarahata yanna.",
        "expected_output": "ඉස්සරහට යන්න.",
        "what_covered": (
            "· Daily language usage\n"
            "· Imperative (command)\n"
            "· S (≤30 characters)\n"
            "· Accuracy validation"
        ),
    },
    {
        "tc_id": "Pos_Fun_0015",
        "name": "Convert a short imperative command — tell me",
        "input_length": "S",
        "singlish_input": "mata kiyanna.",
        "expected_output": "මට කියන්න.",
        "what_covered": (
            "· Daily language usage\n"
            "· Imperative (command)\n"
            "· S (≤30 characters)\n"
            "· Accuracy validation"
        ),
    },
    {
        "tc_id": "Pos_Fun_0016",
        "name": "Convert a short imperative command — give it",
        "input_length": "S",
        "singlish_input": "eeka dhenna.",
        "expected_output": "ඒකා දෙන්න.",
        "what_covered": (
            "· Daily language usage\n"
            "· Imperative (command)\n"
            "· S (≤30 characters)\n"
            "· Accuracy validation"
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # POSITIVE FUNCTIONAL — Negation patterns
    # ─────────────────────────────────────────────────────────────────
    {
        "tc_id": "Pos_Fun_0017",
        "name": "Convert a simple negation — don't know",
        "input_length": "S",
        "singlish_input": "mama dhannee naee.",
        "expected_output": "මම දන්නේ නැහැ.",
        "what_covered": (
            "· Daily language usage\n"
            "· Negation (negative form)\n"
            "· S (≤30 characters)\n"
            "· Accuracy validation"
        ),
    },
    {
        "tc_id": "Pos_Fun_0018",
        "name": "Convert a short negation — don't want it",
        "input_length": "S",
        "singlish_input": "mata eeka epaa.",
        "expected_output": "මට ඒකා එපා.",
        "what_covered": (
            "· Daily language usage\n"
            "· Negation (negative form)\n"
            "· S (≤30 characters)\n"
            "· Accuracy validation"
        ),
    },
    {
        "tc_id": "Pos_Fun_0019",
        "name": "Convert a negation expressing inability",
        "input_length": "S",
        "singlish_input": "mata eeka karanna baee.",
        "expected_output": "මට ඒකා කරන්න බෑ.",
        "what_covered": (
            "· Daily language usage\n"
            "· Negation (negative form)\n"
            "· S (≤30 characters)\n"
            "· Accuracy validation"
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # POSITIVE FUNCTIONAL — Tenses
    # ─────────────────────────────────────────────────────────────────
    {
        "tc_id": "Pos_Fun_0020",
        "name": "Convert a past-tense sentence",
        "input_length": "S",
        "singlish_input": "mama iiyee gedhara giyaa.",
        "expected_output": "මම ඊයේ ගෙදර ගියා.",
        "what_covered": (
            "· Daily language usage\n"
            "· Past tense\n"
            "· S (≤30 characters)\n"
            "· Accuracy validation"
        ),
    },
    {
        "tc_id": "Pos_Fun_0021",
        "name": "Convert a present continuous sentence",
        "input_length": "S",
        "singlish_input": "mama dhaen vaeda karanavaa.",
        "expected_output": "මම දැන් වැද කරනවා.",
        "what_covered": (
            "· Daily language usage\n"
            "· Present tense / Past tense / Future tense\n"
            "· S (≤30 characters)\n"
            "· Accuracy validation"
        ),
    },
    {
        "tc_id": "Pos_Fun_0022",
        "name": "Convert a future-tense sentence",
        "input_length": "S",
        "singlish_input": "mama heta enavaa.",
        "expected_output": "මම හේත එනවා.",
        "what_covered": (
            "· Daily language usage\n"
            "· Present tense / Past tense / Future tense\n"
            "· S (≤30 characters)\n"
            "· Accuracy validation"
        ),
    },
    {
        "tc_id": "Pos_Fun_0023",
        "name": "Convert a future-tense sentence with next week",
        "input_length": "M",
        "singlish_input": "api iiLaGa sathiyee gedhara yamu.",
        "expected_output": "අපි ඊළඟ සතියේ ගෙදර යමු.",
        "what_covered": (
            "· Daily language usage\n"
            "· Present tense / Past tense / Future tense\n"
            "· M (31–299 characters)\n"
            "· Accuracy validation"
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # POSITIVE FUNCTIONAL — Greetings, requests, responses
    # ─────────────────────────────────────────────────────────────────
    {
        "tc_id": "Pos_Fun_0024",
        "name": "Convert a traditional greeting",
        "input_length": "S",
        "singlish_input": "aayuboovan!",
        "expected_output": "ආයුබෝවන්!",
        "what_covered": (
            "· Greeting / request / response\n"
            "· Simple sentence\n"
            "· S (≤30 characters)\n"
            "· Accuracy validation"
        ),
    },
    {
        "tc_id": "Pos_Fun_0025",
        "name": "Convert a well-wishes greeting",
        "input_length": "S",
        "singlish_input": "suba udhaeesanak!",
        "expected_output": "සුබ උදේසනක්!",
        "what_covered": (
            "· Greeting / request / response\n"
            "· Simple sentence\n"
            "· S (≤30 characters)\n"
            "· Accuracy validation"
        ),
    },
    {
        "tc_id": "Pos_Fun_0026",
        "name": "Convert a polite request for assistance",
        "input_length": "M",
        "singlish_input": "karuNaakaralaa mata podi udhavvak karanna puLuvandha?",
        "expected_output": "කරුණාකරලා මට පොඩි උදව්වක් කරන්න පුළුවන්ද?",
        "what_covered": (
            "· Greeting / request / response\n"
            "· Interrogative (question)\n"
            "· M (31–299 characters)\n"
            "· Accuracy validation"
        ),
    },
    {
        "tc_id": "Pos_Fun_0027",
        "name": "Convert a polite affirmative response",
        "input_length": "S",
        "singlish_input": "hari, mama karannam.",
        "expected_output": "හරි, මම කරන්නම්.",
        "what_covered": (
            "· Greeting / request / response\n"
            "· Simple sentence\n"
            "· S (≤30 characters)\n"
            "· Accuracy validation"
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # POSITIVE FUNCTIONAL — Polite vs informal phrasing
    # ─────────────────────────────────────────────────────────────────
    {
        "tc_id": "Pos_Fun_0028",
        "name": "Convert a polite phrasing — send the document",
        "input_length": "M",
        "singlish_input": "oyaata puLuvannam karuNaakara eyaava yavanna.",
        "expected_output": "ඔයාට පුළුවන්නම් කරුණාකර ඒවාව යවන්න.",
        "what_covered": (
            "· Greeting / request / response\n"
            "· Imperative (command)\n"
            "· M (31–299 characters)\n"
            "· Accuracy validation"
        ),
    },
    {
        "tc_id": "Pos_Fun_0029",
        "name": "Convert an informal phrase — come here",
        "input_length": "S",
        "singlish_input": "oya enne.",
        "expected_output": "ඔය එන්නේ.",
        "what_covered": (
            "· Slang / informal language\n"
            "· Imperative (command)\n"
            "· S (≤30 characters)\n"
            "· Accuracy validation"
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # POSITIVE FUNCTIONAL — Day-to-day expressions
    # ─────────────────────────────────────────────────────────────────
    {
        "tc_id": "Pos_Fun_0030",
        "name": "Convert a day-to-day tiredness expression",
        "input_length": "S",
        "singlish_input": "mata nidhimathayi.",
        "expected_output": "මට නිදිමතයි.",
        "what_covered": (
            "· Daily language usage\n"
            "· Simple sentence\n"
            "· S (≤30 characters)\n"
            "· Accuracy validation"
        ),
    },
    {
        "tc_id": "Pos_Fun_0031",
        "name": "Convert a weather expression",
        "input_length": "S",
        "singlish_input": "dhaen vahinavaa.",
        "expected_output": "දැන් වහිනවා.",
        "what_covered": (
            "· Daily language usage\n"
            "· Simple sentence\n"
            "· S (≤30 characters)\n"
            "· Accuracy validation"
        ),
    },
    {
        "tc_id": "Pos_Fun_0032",
        "name": "Convert a fear expression",
        "input_length": "S",
        "singlish_input": "mata baya hithenavaa.",
        "expected_output": "මට බය හිතෙනවා.",
        "what_covered": (
            "· Daily language usage\n"
            "· Simple sentence\n"
            "· S (≤30 characters)\n"
            "· Accuracy validation"
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # POSITIVE FUNCTIONAL — Repeated words for emphasis
    # ─────────────────────────────────────────────────────────────────
    {
        "tc_id": "Pos_Fun_0033",
        "name": "Convert repeated word used for agreement",
        "input_length": "S",
        "singlish_input": "hari hari",
        "expected_output": "හරි හරි",
        "what_covered": (
            "· Word combination / phrase pattern\n"
            "· Simple sentence\n"
            "· S (≤30 characters)\n"
            "· Accuracy validation"
        ),
    },
    {
        "tc_id": "Pos_Fun_0034",
        "name": "Convert repeated word used for emphasis — little by little",
        "input_length": "S",
        "singlish_input": "tika tika",
        "expected_output": "ටික ටික",
        "what_covered": (
            "· Word combination / phrase pattern\n"
            "· Simple sentence\n"
            "· S (≤30 characters)\n"
            "· Accuracy validation"
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # POSITIVE FUNCTIONAL — Pronoun variations (singular / plural)
    # ─────────────────────────────────────────────────────────────────
    {
        "tc_id": "Pos_Fun_0035",
        "name": "Convert singular pronoun sentence — third person",
        "input_length": "S",
        "singlish_input": "eyaa gedhara giyaa.",
        "expected_output": "ඔහු ගෙදර ගියා.",
        "what_covered": (
            "· Daily language usage\n"
            "· Pronoun variation (I/you/we/they)\n"
            "· S (≤30 characters)\n"
            "· Accuracy validation"
        ),
    },
    {
        "tc_id": "Pos_Fun_0036",
        "name": "Convert plural pronoun sentence — third person plural",
        "input_length": "S",
        "singlish_input": "eyaalaa enavaa.",
        "expected_output": "ඔවුන් එනවා.",
        "what_covered": (
            "· Daily language usage\n"
            "· Plural form\n"
            "· S (≤30 characters)\n"
            "· Accuracy validation"
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # POSITIVE FUNCTIONAL — English technical terms embedded
    # ─────────────────────────────────────────────────────────────────
    {
        "tc_id": "Pos_Fun_0037",
        "name": "Convert sentence with Zoom meeting reference",
        "input_length": "M",
        "singlish_input": "Zoom meeting ekak thiyennee.",
        "expected_output": "Zoom meeting එකක් තියෙන්නේ.",
        "what_covered": (
            "· Mixed Singlish + English\n"
            "· Simple sentence\n"
            "· M (31–299 characters)\n"
            "· Accuracy validation"
        ),
    },
    {
        "tc_id": "Pos_Fun_0038",
        "name": "Convert sentence with place names and English words",
        "input_length": "M",
        "singlish_input": "nimaali office enna late vennee traffic nisaa.",
        "expected_output": "නිමාලි office එන්න late වෙන්නේ traffic නිසා.",
        "what_covered": (
            "· Names / places / common English words\n"
            "· Simple sentence\n"
            "· M (31–299 characters)\n"
            "· Accuracy validation"
        ),
    },
    {
        "tc_id": "Pos_Fun_0039",
        "name": "Convert sentence with WhatsApp sharing request",
        "input_length": "M",
        "singlish_input": "Teams meeting ekee link eka WhatsApp karanna puLuvandha.",
        "expected_output": "Teams meeting එකේ link eka WhatsApp කරන්න පුළුවන්ද.",
        "what_covered": (
            "· Mixed Singlish + English\n"
            "· Interrogative (question)\n"
            "· M (31–299 characters)\n"
            "· Accuracy validation"
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # POSITIVE FUNCTIONAL — Currency, time, dates, units
    # ─────────────────────────────────────────────────────────────────
    {
        "tc_id": "Pos_Fun_0040",
        "name": "Convert sentence containing currency amount",
        "input_length": "M",
        "singlish_input": "meeka Rs. 5343 kalin ganna puluvandha?",
        "expected_output": "මේකා Rs. 5343 කලින් ගන්න පුළුවන්ද?",
        "what_covered": (
            "· Punctuation / numbers\n"
            "· Interrogative (question)\n"
            "· M (31–299 characters)\n"
            "· Accuracy validation"
        ),
    },
    {
        "tc_id": "Pos_Fun_0041",
        "name": "Convert sentence with date in Singlish",
        "input_length": "M",
        "singlish_input": "dhesaembar 25 wena dhin api yamu.",
        "expected_output": "දෙසැම්බර් 25 වෙන දින අපි යමු.",
        "what_covered": (
            "· Punctuation / numbers\n"
            "· Simple sentence\n"
            "· M (31–299 characters)\n"
            "· Accuracy validation"
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # POSITIVE FUNCTIONAL — Punctuation handling
    # ─────────────────────────────────────────────────────────────────
    {
        "tc_id": "Pos_Fun_0042",
        "name": "Convert sentence with exclamation mark",
        "input_length": "S",
        "singlish_input": "sthuthi machan!",
        "expected_output": "ස්තූතී මචන්!",
        "what_covered": (
            "· Punctuation / numbers\n"
            "· Simple sentence\n"
            "· S (≤30 characters)\n"
            "· Accuracy validation"
        ),
    },
    {
        "tc_id": "Pos_Fun_0043",
        "name": "Convert sentence with parentheses preserved",
        "input_length": "M",
        "singlish_input": "api heta (eeta passe) enavaa.",
        "expected_output": "අපි හේත (ඒට පස්සේ) එනවා.",
        "what_covered": (
            "· Punctuation / numbers\n"
            "· Simple sentence\n"
            "· M (31–299 characters)\n"
            "· Accuracy validation"
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # POSITIVE FUNCTIONAL — Slang and colloquial phrasing
    # ─────────────────────────────────────────────────────────────────
    {
        "tc_id": "Pos_Fun_0044",
        "name": "Convert colloquial slang expression — great friend",
        "input_length": "S",
        "singlish_input": "ela machan! supiri!!",
        "expected_output": "ඇල මචන්! සුපිරි!!",
        "what_covered": (
            "· Slang / informal language\n"
            "· Simple sentence\n"
            "· S (≤30 characters)\n"
            "· Robustness validation"
        ),
    },
    {
        "tc_id": "Pos_Fun_0045",
        "name": "Convert slang expression for difficulty",
        "input_length": "S",
        "singlish_input": "eka poddak amaaruyi vagee",
        "expected_output": "ඒකා පොඩ්ඩක් අමාරුයි වගේ",
        "what_covered": (
            "· Slang / informal language\n"
            "· Simple sentence\n"
            "· S (≤30 characters)\n"
            "· Robustness validation"
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # POSITIVE FUNCTIONAL — Long paragraph input
    # ─────────────────────────────────────────────────────────────────
    {
        "tc_id": "Pos_Fun_0046",
        "name": "Convert a long paragraph-style news input",
        "input_length": "L",
        "singlish_input": (
            "dhitvaa suLi kuNaatuva samaGa aethi vuu gQQvathura saha naayayaeem heethuven "
            "maarga sQQvarDhana aDhikaariya sathu maarga kotas 430k vinaashayata pathva aethi "
            "athara, ehi samastha dhiga pramaaNaya kiloomiitar 300k pamaNa vana bava pravaahana, "
            "mahaamaarga saha naagarika sQQvarDhana amaathYA bimal rathnaayaka saDHahan kaLeeya."
        ),
        "expected_output": "",
        "what_covered": (
            "· Daily language usage\n"
            "· Complex sentence\n"
            "· L (≥300 characters)\n"
            "· Robustness validation"
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # POSITIVE FUNCTIONAL — Multiple spaces (formatting)
    # ─────────────────────────────────────────────────────────────────
    {
        "tc_id": "Pos_Fun_0047",
        "name": "Convert sentence with multiple internal spaces",
        "input_length": "M",
        "singlish_input": "mama gedhara   yanavaa.",
        "expected_output": "මම ගෙදර   යනවා.",
        "what_covered": (
            "· Formatting (spaces / line breaks / paragraph)\n"
            "· Simple sentence\n"
            "· M (31–299 characters)\n"
            "· Robustness validation"
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # POSITIVE UI — Functional UI behaviour
    # ─────────────────────────────────────────────────────────────────
    {
        "tc_id": "Pos_UI_0001",
        "name": "Sinhala output updates automatically in real-time",
        "input_length": "S",
        "singlish_input": "man gedhara yanavaa",
        "expected_output": (
            "Sinhala output should update automatically while typing and display: "
            "මන් ගෙදර යනවා"
        ),
        "what_covered": (
            "· Usability flow (real-time conversion)\n"
            "· Simple sentence\n"
            "· S (≤30 characters)\n"
            "· Real-time output update behavior"
        ),
    },
    {
        "tc_id": "Pos_UI_0002",
        "name": "Output area displays Sinhala Unicode correctly",
        "input_length": "S",
        "singlish_input": "api enavaa.",
        "expected_output": "අපි එනවා.",
        "what_covered": (
            "· Daily language usage\n"
            "· Simple sentence\n"
            "· S (≤30 characters)\n"
            "· Real-time output update behavior"
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # NEGATIVE FUNCTIONAL — Joined words (no spaces — stress test)
    # ─────────────────────────────────────────────────────────────────
    {
        "tc_id": "Neg_Fun_0001",
        "name": "Input with all words joined — no spaces",
        "input_length": "S",
        "singlish_input": "mamagedharayanavaa",
        "expected_output": "",
        "what_covered": (
            "· Typographical error handling\n"
            "· Simple sentence\n"
            "· S (≤30 characters)\n"
            "· Robustness validation"
        ),
    },
    {
        "tc_id": "Neg_Fun_0002",
        "name": "Input with partially joined words — missing space",
        "input_length": "M",
        "singlish_input": "matapaankannaoonee",
        "expected_output": "",
        "what_covered": (
            "· Typographical error handling\n"
            "· Simple sentence\n"
            "· M (31–299 characters)\n"
            "· Robustness validation"
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    # NEGATIVE UI — Edge-case UI behaviour
    # ─────────────────────────────────────────────────────────────────
    {
        "tc_id": "Neg_UI_0001",
        "name": "Empty input field — output should be empty or cleared",
        "input_length": "S",
        "singlish_input": "",
        "expected_output": "",
        "what_covered": (
            "· Empty/cleared input handling\n"
            "· Simple sentence\n"
            "· S (≤30 characters)\n"
            "· Error handling / input validation"
        ),
    },
    {
        "tc_id": "Neg_UI_0002",
        "name": "Input with only whitespace — no meaningful output expected",
        "input_length": "S",
        "singlish_input": "   ",
        "expected_output": "",
        "what_covered": (
            "· Empty/cleared input handling\n"
            "· Simple sentence\n"
            "· S (≤30 characters)\n"
            "· Error handling / input validation"
        ),
    },
    {
        "tc_id": "Neg_UI_0003",
        "name": "Input with only punctuation — no Singlish words",
        "input_length": "S",
        "singlish_input": "!?!?",
        "expected_output": "!?!?",
        "what_covered": (
            "· Punctuation / numbers\n"
            "· Simple sentence\n"
            "· S (≤30 characters)\n"
            "· Error handling / input validation"
        ),
    },
]
