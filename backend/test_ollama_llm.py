
import asyncio

from app.services.llm import LLMService


async def main():
    service = LLMService()

    try:
        answer = await service.generate_response(
            "Explain Kalyani raga in Carnatic music. "
            "Include its arohanam, avarohanam and melakarta number."
        )

        print("\nRAGAVERSE AI RESPONSE:\n")
        print(answer)

    finally:
        await service.close()


if __name__ == "__main__":
    asyncio.run(main())
