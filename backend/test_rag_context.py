
import asyncio

from app.services.knowledge import get_rag_knowledge_context


async def main():
    question = "Explain Kalyani raga and its arohanam and avarohanam."

    context = await get_rag_knowledge_context(
        question,
        limit=5,
    )

    print("RAG context generated successfully.")
    print("Context length:", len(context))
    print("\nRetrieved context:\n")
    print(context[:3000])


if __name__ == "__main__":
    asyncio.run(main())
