
import asyncio

from app.services.semantic_search import SemanticSearchService


QUESTIONS = [
    "Explain the ascending and descending scale of Kalyani raga",
    "Which tala has eight beats?",
    "What are the seven basic swaras in Carnatic music?",
    "Who composed Vatapi Ganapatim?",
]


async def main():
    service = SemanticSearchService()

    for question in QUESTIONS:
        print("\n" + "=" * 70)
        print("QUESTION:", question)

        results = await service.search(
            question=question,
            limit=7,
        )

        for index, result in enumerate(results, start=1):
            print(
                f"{index}. "
                f"{result['metadata'].get('name')} "
                f"({result['source_type']}) "
                f"Similarity: {result['similarity']}"
            )


if __name__ == "__main__":
    asyncio.run(main())
