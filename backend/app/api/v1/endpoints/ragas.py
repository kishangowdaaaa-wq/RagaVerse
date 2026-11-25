from fastapi import APIRouter, HTTPException, Query

from app.knowledge.catalog import ALL_RAGAS

router = APIRouter()


@router.get("/")
def search_ragas(
    q: str | None = Query(default=None, description="Search by raga name"),
    melakarta_number: int | None = Query(
        default=None, ge=1, le=72
    ),
):
    results = ALL_RAGAS

    if q:
        term = q.casefold().strip()
        results = [
            raga for raga in results
            if term in raga["name"].casefold()
            or any(term in alias.casefold() for alias in raga.get("aliases", []))
        ]

    if melakarta_number is not None:
        results = [
            raga for raga in results
            if raga.get("melakarta_number") == melakarta_number
        ]

    return {
        "count": len(results),
        "results": results,
    }


@router.get("/{raga_name}")
def get_raga(raga_name: str):
    term = raga_name.casefold().strip()

    for raga in ALL_RAGAS:
        names = [raga["name"], *raga.get("aliases", [])]

        if any(term == name.casefold() for name in names):
            return raga

    raise HTTPException(status_code=404, detail="Raga not found")
