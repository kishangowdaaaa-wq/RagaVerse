from app.knowledge.catalog import ALL_RAGAS

MELAKARTA_RAGAS = [
    r for r in ALL_RAGAS
    if r["category"] == "Melakarta"
]

def test_exactly_72_melakarta_ragas():
    assert len(MELAKARTA_RAGAS) == 72

def test_all_melakarta_numbers_are_unique():
    numbers = [r["melakarta_number"] for r in MELAKARTA_RAGAS]
    assert sorted(numbers) == list(range(1, 73))

def test_all_melakarta_ragas_have_names():
    assert all(r["name"].strip() for r in MELAKARTA_RAGAS)

def test_all_melakarta_ragas_have_scales():
    for raga in MELAKARTA_RAGAS:
        assert raga["arohanam"].startswith("S ")
        assert raga["arohanam"].endswith(" S")
        assert raga["avarohanam"].startswith("S ")
        assert raga["avarohanam"].endswith(" S")

def test_first_and_last_melakarta():
    first = next(r for r in MELAKARTA_RAGAS if r["melakarta_number"] == 1)
    last = next(r for r in MELAKARTA_RAGAS if r["melakarta_number"] == 72)

    assert first["name"] == "Kanakangi"
    assert last["name"] == "Rasikapriya"

def test_madhyama_division():
    for raga in MELAKARTA_RAGAS:
        expected = "M1" if raga["melakarta_number"] <= 36 else "M2"
        assert expected in raga["arohanam"]
