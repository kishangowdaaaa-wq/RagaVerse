
"""Structured learning paths for the RagaVerse Carnatic music academy."""

LEARNING_MODULES = [
    {
        "id": "swara_fundamentals",
        "title": "Swara Fundamentals",
        "level": "Beginner",
        "description": (
            "Learn the seven basic swaras, their names, symbols, "
            "and the different swara positions used in Carnatic music."
        ),
        "prerequisites": [],
        "lessons": [
            {
                "id": "seven_swaras",
                "title": "The Seven Basic Swaras",
                "summary": (
                    "Introduction to Shadja, Rishabha, Gandhara, "
                    "Madhyama, Panchama, Dhaivata and Nishada."
                ),
                "duration_minutes": 10,
            },
            {
                "id": "swara_symbols",
                "title": "Swara Names and Symbols",
                "summary": (
                    "Understand the notation S, R, G, M, P, D and N."
                ),
                "duration_minutes": 10,
            },
            {
                "id": "swara_positions",
                "title": "Swara Positions",
                "summary": (
                    "Explore the variants of Rishabha, Gandhara, "
                    "Madhyama, Dhaivata and Nishada."
                ),
                "duration_minutes": 15,
            },
            {
                "id": "fixed_swaras",
                "title": "Fixed Swara Positions",
                "summary": (
                    "Understand the roles of Shadja and Panchama "
                    "as fixed swara positions."
                ),
                "duration_minutes": 10,
            },
        ],
    },
    {
        "id": "sarali_varisai",
        "title": "Sarali Varisai",
        "level": "Beginner",
        "description": (
            "Begin systematic vocal practice through introductory "
            "swara sequences and ascending and descending patterns."
        ),
        "prerequisites": ["swara_fundamentals"],
        "lessons": [
            {
                "id": "sarali_introduction",
                "title": "Introduction to Sarali Varisai",
                "summary": (
                    "Learn the purpose of Sarali Varisai and its "
                    "place in foundational Carnatic music training."
                ),
                "duration_minutes": 10,
            },
            {
                "id": "sarali_ascending",
                "title": "Ascending Swara Practice",
                "summary": (
                    "Practise orderly ascending swara sequences."
                ),
                "duration_minutes": 15,
            },
            {
                "id": "sarali_descending",
                "title": "Descending Swara Practice",
                "summary": (
                    "Practise orderly descending swara sequences."
                ),
                "duration_minutes": 15,
            },
            {
                "id": "sarali_rhythm",
                "title": "Sarali Varisai with Tala",
                "summary": (
                    "Develop steady rhythm while practising "
                    "Sarali Varisai patterns."
                ),
                "duration_minutes": 15,
            },
        ],
    },
    {
        "id": "janta_varisai",
        "title": "Janta Varisai",
        "level": "Beginner",
        "description": (
            "Develop swara clarity and control through paired-note "
            "exercises and repeated swara patterns."
        ),
        "prerequisites": ["sarali_varisai"],
        "lessons": [
            {
                "id": "janta_introduction",
                "title": "Introduction to Janta Varisai",
                "summary": (
                    "Understand paired swara patterns and their "
                    "role in voice training."
                ),
                "duration_minutes": 10,
            },
            {
                "id": "janta_patterns",
                "title": "Practising Janta Patterns",
                "summary": (
                    "Learn repeated-note patterns with clear "
                    "swara articulation."
                ),
                "duration_minutes": 15,
            },
            {
                "id": "janta_rhythm",
                "title": "Janta Varisai with Rhythm",
                "summary": (
                    "Practise paired swaras with consistent timing."
                ),
                "duration_minutes": 15,
            },
        ],
    },
    {
        "id": "alankaras",
        "title": "Alankaras",
        "level": "Beginner",
        "description": (
            "Explore structured swara exercises across different "
            "tala patterns."
        ),
        "prerequisites": ["sarali_varisai"],
        "lessons": [
            {
                "id": "alankara_introduction",
                "title": "Introduction to Alankaras",
                "summary": (
                    "Understand the purpose and structure of "
                    "Alankara exercises."
                ),
                "duration_minutes": 10,
            },
            {
                "id": "alankara_tala",
                "title": "Alankaras in Different Talas",
                "summary": (
                    "Explore how swara exercises are organised "
                    "within tala structures."
                ),
                "duration_minutes": 20,
            },
            {
                "id": "alankara_practice",
                "title": "Alankara Practice",
                "summary": (
                    "Develop rhythmic consistency through "
                    "structured swara patterns."
                ),
                "duration_minutes": 20,
            },
        ],
    },
    {
        "id": "raga_fundamentals",
        "title": "Raga Fundamentals",
        "level": "Beginner",
        "description": (
            "Understand the foundations of Carnatic ragas, "
            "their swara structures and classifications."
        ),
        "prerequisites": ["swara_fundamentals"],
        "lessons": [
            {
                "id": "what_is_raga",
                "title": "What Is a Raga?",
                "summary": (
                    "Learn the concept of raga and its melodic identity."
                ),
                "duration_minutes": 10,
            },
            {
                "id": "arohanam_avarohanam",
                "title": "Arohanam and Avarohanam",
                "summary": (
                    "Understand ascending and descending melodic "
                    "swara sequences."
                ),
                "duration_minutes": 15,
            },
            {
                "id": "melakarta_janya",
                "title": "Melakarta and Janya Ragas",
                "summary": (
                    "Explore the relationship between parent "
                    "Melakarta ragas and Janya ragas."
                ),
                "duration_minutes": 15,
            },
            {
                "id": "raga_exploration",
                "title": "Exploring Common Ragas",
                "summary": (
                    "Study selected ragas using their swara "
                    "structures and reference information."
                ),
                "duration_minutes": 20,
            },
        ],
    },
    {
        "id": "tala_fundamentals",
        "title": "Tala Fundamentals",
        "level": "Beginner",
        "description": (
            "Learn the basics of Carnatic rhythm, tala structures, "
            "angas and akshara counts."
        ),
        "prerequisites": [],
        "lessons": [
            {
                "id": "what_is_tala",
                "title": "Introduction to Tala",
                "summary": (
                    "Understand tala as the rhythmic framework "
                    "of Carnatic music."
                ),
                "duration_minutes": 10,
            },
            {
                "id": "tala_angas",
                "title": "Tala Angas",
                "summary": (
                    "Learn Laghu, Drutam and Anudrutam."
                ),
                "duration_minutes": 15,
            },
            {
                "id": "adi_tala",
                "title": "Understanding Adi Tala",
                "summary": (
                    "Explore the Chatusra-jati Triputa structure "
                    "and its eight aksharas."
                ),
                "duration_minutes": 15,
            },
            {
                "id": "other_talas",
                "title": "Exploring Other Talas",
                "summary": (
                    "Introduction to Rupaka, Misra Chapu, "
                    "Khanda Chapu and Tisra Chapu."
                ),
                "duration_minutes": 20,
            },
        ],
    },
    {
        "id": "composition_fundamentals",
        "title": "Carnatic Compositions",
        "level": "Beginner",
        "description": (
            "Discover the structure, composers, ragas and talas "
            "of selected Carnatic compositions."
        ),
        "prerequisites": ["swara_fundamentals", "raga_fundamentals"],
        "lessons": [
            {
                "id": "composition_introduction",
                "title": "Introduction to Compositions",
                "summary": (
                    "Understand the role of compositions in "
                    "Carnatic music learning."
                ),
                "duration_minutes": 10,
            },
            {
                "id": "composition_structure",
                "title": "Composition Structure",
                "summary": (
                    "Explore common sections such as Pallavi, "
                    "Anupallavi and Charanam."
                ),
                "duration_minutes": 15,
            },
            {
                "id": "famous_compositions",
                "title": "Exploring Selected Compositions",
                "summary": (
                    "Study selected compositions, their composers, "
                    "ragas and talas."
                ),
                "duration_minutes": 20,
            },
        ],
    },
]
