
import asyncio
from types import SimpleNamespace

from app.services.llm import LLMService


class FakeResponse:
    def raise_for_status(self):
        pass

    def json(self):
        return {
            "message": {
                "role": "assistant",
                "content": (
                    "Raga Kalyani is a popular Carnatic raga."
                ),
            }
        }


class FakeClient:
    def __init__(self):
        self.request_url = None
        self.request_json = None

    async def post(self, url, json):
        self.request_url = url
        self.request_json = json
        return FakeResponse()

    async def aclose(self):
        pass


def test_llm_service_generates_response():
    service = LLMService.__new__(LLMService)

    service.model = "qwen2.5:3b"
    service.max_output_tokens = 1500
    service.client = FakeClient()

    result = asyncio.run(
        service.generate_response(
            "Explain Raga Kalyani."
        )
    )

    assert result == (
        "Raga Kalyani is a popular Carnatic raga."
    )

    assert service.client.request_url == "/api/chat"

    request_data = service.client.request_json

    assert request_data["model"] == "qwen2.5:3b"
    assert request_data["stream"] is False
    assert request_data["messages"][0]["role"] == "user"
    assert (
        request_data["messages"][0]["content"]
        == "Explain Raga Kalyani."
    )
    assert request_data["options"]["num_predict"] == 1500


def test_llm_service_includes_system_instructions():
    service = LLMService.__new__(LLMService)

    service.model = "qwen2.5:3b"
    service.max_output_tokens = 1500
    service.client = FakeClient()

    asyncio.run(
        service.generate_response(
            "Explain Kalyani.",
            instructions="You are RagaVerse.",
        )
    )

    messages = service.client.request_json["messages"]

    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == "You are RagaVerse."

    assert messages[1]["role"] == "user"


def test_llm_service_rejects_empty_response():
    class EmptyFakeResponse(FakeResponse):
        def json(self):
            return {
                "message": {
                    "role": "assistant",
                    "content": "",
                }
            }

    class EmptyFakeClient(FakeClient):
        async def post(self, url, json):
            return EmptyFakeResponse()

    service = LLMService.__new__(LLMService)

    service.model = "qwen2.5:3b"
    service.max_output_tokens = 1500
    service.client = EmptyFakeClient()

    try:
        asyncio.run(
            service.generate_response("Explain Kalyani.")
        )
        assert False, "Expected ValueError was not raised."
    except ValueError as exc:
        assert "empty response" in str(exc).lower()
