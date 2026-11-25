
"""Structured reference catalogue of Carnatic talas."""

TALA_CATALOG = [
    {
        "name": "Adi",
        "aliases": ["Chatusra-jati Triputa"],
        "jati": "Chatusra",
        "anga_structure": ["Laghu", "Drutam", "Drutam"],
        "anga_counts": [4, 2, 2],
        "akshara_count": 8,
        "description": (
            "One of the most widely used Carnatic talas. "
            "It is a Chatusra-jati Triputa tala."
        ),
    },
    {
        "name": "Rupaka",
        "aliases": ["Rupaka Tala"],
        "jati": None,
        "anga_structure": ["Drutam", "Laghu"],
        "anga_counts": [2, 4],
        "akshara_count": 6,
        "description": (
            "A commonly taught Rupaka tala structure. "
            "Performance conventions can vary."
        ),
    },
    {
        "name": "Misra Chapu",
        "aliases": ["Mishra Chapu"],
        "jati": None,
        "anga_structure": ["Subdivision"],
        "anga_counts": [3, 2, 2],
        "akshara_count": 7,
        "description": (
            "A commonly used chapu tala with a 3+2+2 "
            "subdivision pattern."
        ),
    },
    {
        "name": "Khanda Chapu",
        "aliases": ["Kanda Chapu"],
        "jati": None,
        "anga_structure": ["Subdivision"],
        "anga_counts": [2, 3],
        "akshara_count": 5,
        "description": (
            "A chapu tala commonly described using "
            "a 2+3 subdivision pattern."
        ),
    },
    {
        "name": "Tisra Chapu",
        "aliases": [],
        "jati": None,
        "anga_structure": ["Subdivision"],
        "anga_counts": [3],
        "akshara_count": 3,
        "description": (
            "A three-unit chapu rhythm reference."
        ),
    },
]


ALL_TALAS = TALA_CATALOG
