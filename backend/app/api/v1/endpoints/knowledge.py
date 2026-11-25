
"""API endpoints for Carnatic music knowledge resources."""

from fastapi import APIRouter, Query

from app.knowledge import (
    ALL_COMPOSITIONS,
    ALL_SWARAS,
    ALL_TALAS,
)

router = APIRouter()


@router.get("/talas")
def search_talas(
    q: str | None = Query(default=None),
):
    results = ALL_TALAS

    if q:
        term = q.casefold().strip()
        results = [
            tala
            for tala in results
            if term in tala["name"].casefold()
            or any(
                term in alias.casefold()
                for alias in tala.get("aliases", [])
            )
            or term in tala.get("description", "").casefold()
        ]

    return {
        "count": len(results),
        "results": results,
    }


@router.get("/swaras")
def search_swaras(
    q: str | None = Query(default=None),
):
    results = ALL_SWARAS

    if q:
        term = q.casefold().strip()
        results = [
            swara
            for swara in results
            if term in swara["symbol"].casefold()
            or term in swara["name"].casefold()
            or any(
                term in variant.casefold()
                for variant in swara.get("variants", [])
            )
        ]

    return {
        "count": len(results),
        "results": results,
    }


@router.get("/compositions")
def search_compositions(
    q: str | None = Query(default=None),
    raga: str | None = Query(default=None),
    composer: str | None = Query(default=None),
    tala: str | None = Query(default=None),
):
    results = ALL_COMPOSITIONS

    if q:
        term = q.casefold().strip()
        results = [
            composition
            for composition in results
            if any(
                term in str(value).casefold()
                for value in composition.values()
            )
        ]

    if raga:
        term = raga.casefold().strip()
        results = [
            composition
            for composition in results
            if term in composition["raga"].casefold()
        ]

    if composer:
        term = composer.casefold().strip()
        results = [
            composition
            for composition in results
            if term in composition["composer"].casefold()
        ]

    if tala:
        term = tala.casefold().strip()
        results = [
            composition
            for composition in results
            if term in composition["tala"].casefold()
        ]

    return {
        "count": len(results),
        "results": results,
    }
