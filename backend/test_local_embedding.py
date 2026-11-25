
import asyncio

from app.services.embedding import EmbeddingService


async def main():
    service = EmbeddingService()

    try:
        embedding = await service.generate_embedding(
            "Shankarabharanam is a Carnatic music raga."
        )

        print("Embedding generated successfully.")
        print("Dimensions:", len(embedding))
        print("First five values:", embedding[:5])

    finally:
        await service.close()


if __name__ == "__main__":
    asyncio.run(main())
