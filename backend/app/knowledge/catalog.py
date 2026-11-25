"""Starter reference catalogue for common Carnatic ragas.

Scale notation:
S = Shadja, R = Rishabha, G = Gandhara,
M = Madhyama, P = Panchama, D = Dhaivata,
N = Nishada.

The number after a swara indicates its variety.
These scale descriptions are introductory references;
they do not capture every prayoga or gamaka.
"""

RAGA_CATALOG = [
    {
        "name": "Shankarabharanam",
        "aliases": ["sankarabharanam", "shankara bharanam"],
        "category": "Melakarta",
        "melakarta_number": 29,
        "arohanam": "S R2 G3 M1 P D2 N3 S",
        "avarohanam": "S N3 D2 P M1 G3 R2 S",
        "notes": (
            "A major melakarta raga with a sampurna scale. "
            "Its identity in performance involves characteristic "
            "phrases and gamakas, not only the ascending and "
            "descending scale."
        ),
    },
    {
        "name": "Mayamalavagowla",
        "aliases": ["mayamalavagoula", "maya malava gowla"],
        "category": "Melakarta",
        "melakarta_number": 15,
        "arohanam": "S R1 G3 M1 P D1 N3 S",
        "avarohanam": "S N3 D1 P M1 G3 R1 S",
        "notes": (
            "A sampurna melakarta raga widely used in foundational "
            "Carnatic music lessons. It is commonly used for "
            "beginner swara exercises."
        ),
    },
    {
        "name": "Kalyani",
        "aliases": ["mechakalyani", "mecha kalyani"],
        "category": "Melakarta",
        "melakarta_number": 65,
        "arohanam": "S R2 G3 M2 P D2 N3 S",
        "avarohanam": "S N3 D2 P M2 G3 R2 S",
        "notes": (
            "A sampurna melakarta raga featuring prati madhyama "
            "(M2). Its characteristic phrases and gamakas are "
            "important to its presentation."
        ),
    },
    {
        "name": "Mohanam",
        "aliases": ["mohana"],
        "category": "Audava raga",
        "melakarta_number": None,
        "arohanam": "S R2 G3 P D2 S",
        "avarohanam": "S D2 P G3 R2 S",
        "notes": (
            "An audava-audava raga, using five swara positions "
            "in both ascent and descent. Madhyama and Nishada "
            "are absent from this basic scale."
        ),
    },
    {
        "name": "Hamsadhwani",
        "aliases": ["hamsadhvani", "hamsa dhwani"],
        "category": "Janya raga",
        "melakarta_number": None,
        "commonly_associated_melakarta": 29,
        "arohanam": "S R2 G3 P N3 S",
        "avarohanam": "S N3 P G3 R2 S",
        "notes": (
            "An audava-audava janya raga commonly associated "
            "with the 29th melakarta, Dheera Shankarabharanam. "
            "Madhyama and Dhaivata are absent from this basic scale."
        ),
    },
]

GENERAL_REFERENCE = (
    "Carnatic raga scales are introductory descriptions. "
    "A raga's identity also depends on characteristic phrases "
    "(prayogas), gamakas, emphasis, and performance tradition. "
    "Do not infer the complete grammar of a raga from its scale alone."
)

# Complete 72 Melakarta reference catalogue.
# Swara combinations follow the standard Melakarta structure.

MELAKARTA_NAMES = [
    "Kanakangi", "Ratnangi", "Ganamurti", "Vanaspati", "Manavati", "Tanarupi",
    "Senavati", "Hanumatodi", "Dhenuka", "Natakapriya", "Kokilapriya", "Rupavati",
    "Gayakapriya", "Vakulabharanam", "Mayamalavagowla", "Chakravakam",
    "Suryakantam", "Hatakambari", "Jhankaradhvani", "Natabhairavi",
    "Keeravani", "Kharaharapriya", "Gourimanohari", "Varunapriya",
    "Mararanjani", "Charukesi", "Sarasangi", "Harikambhoji",
    "Dheera Shankarabharanam", "Naganandini", "Yagapriya", "Ragavardhini",
    "Gangeyabhushani", "Vagadheeswari", "Shulini", "Chalanata",
    "Salagam", "Jalarnavam", "Jhalavarali", "Navaneetam", "Pavani",
    "Raghupriya", "Gavambodhi", "Bhavapriya", "Shubhapantuvarali",
    "Shadvidhamargini", "Suvarnangi", "Divyamani", "Dhavalambari",
    "Namanarayani", "Kamavardhini", "Ramapriya", "Gamanashrama",
    "Vishwambari", "Shamalangi", "Shanmukhapriya",
    "Simhendramadhyamam", "Hemavati", "Dharmavati", "Neetimati",
    "Kantamani", "Rishabhapriya", "Latangi", "Vachaspati",
    "Mechakalyani", "Chitrambari", "Sucharitra", "Jyotisvarupini",
    "Dhatuvardhani", "Nasikabhushani", "Kosalam", "Rasikapriya",
]

_RG_PAIRS = [
    ("R1", "G1"), ("R1", "G2"), ("R1", "G3"),
    ("R2", "G2"), ("R2", "G3"), ("R3", "G3"),
]

_DN_PAIRS = [
    ("D1", "N1"), ("D1", "N2"), ("D1", "N3"),
    ("D2", "N2"), ("D2", "N3"), ("D3", "N3"),
]

_CHAKRAS = [
    "Indu", "Netra", "Agni", "Veda", "Bana", "Rutu",
    "Rishi", "Vasu", "Brahma", "Disi", "Rudra", "Aditya",
]


def _build_melakarta_catalog():
    existing_numbers = {
        raga.get("melakarta_number")
        for raga in RAGA_CATALOG
        if raga.get("melakarta_number") is not None
    }

    records = []

    for number, name in enumerate(MELAKARTA_NAMES, start=1):
        if number in existing_numbers:
            continue

        base_number = number if number <= 36 else number - 36
        rg_index = (base_number - 1) // 6
        dn_index = (base_number - 1) % 6

        rishabha, gandhara = _RG_PAIRS[rg_index]
        dhaivata, nishada = _DN_PAIRS[dn_index]
        madhyama = "M1" if number <= 36 else "M2"

        arohanam = (
            f"S {rishabha} {gandhara} {madhyama} "
            f"P {dhaivata} {nishada} S"
        )
        avarohanam = " ".join(reversed(arohanam.split()))

        records.append({
            "name": name,
            "aliases": [],
            "category": "Melakarta",
            "melakarta_number": number,
            "chakra": _CHAKRAS[(number - 1) // 6],
            "arohanam": arohanam,
            "avarohanam": avarohanam,
            "notes": (
                f"{name} is Melakarta {number}, belonging to the "
                f"{_CHAKRAS[(number - 1) // 6]} chakra. "
                f"This sampurna parent scale uses {madhyama}. "
                "Raga identity in performance also involves "
                "characteristic phrases and gamakas."
            ),
            "source": "72 Melakarta scheme; see project reference documentation.",
        })

    return records


ALL_RAGAS = RAGA_CATALOG + _build_melakarta_catalog()
