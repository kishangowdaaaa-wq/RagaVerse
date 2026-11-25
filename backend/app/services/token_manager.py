
import tiktoken


class TokenManager:
    """Estimate and manage LLM conversation token usage."""

    def __init__(
        self,
        model: str = "gpt-5.5",
        max_input_tokens: int = 8000,
        reserved_output_tokens: int = 1500,
    ) -> None:
        if max_input_tokens < 1:
            raise ValueError("max_input_tokens must be positive.")

        if reserved_output_tokens < 0:
            raise ValueError(
                "reserved_output_tokens cannot be negative."
            )

        if reserved_output_tokens >= max_input_tokens:
            raise ValueError(
                "Reserved output tokens must be smaller "
                "than the input token budget."
            )

        self.model = model
        self.max_input_tokens = max_input_tokens
        self.reserved_output_tokens = reserved_output_tokens

        try:
            self.encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            self.encoding = tiktoken.get_encoding("o200k_base")

    def count_tokens(self, text: str) -> int:
        """Estimate tokens in a text string."""
        return len(self.encoding.encode(text))

    def count_messages(
        self,
        messages: list[dict[str, str]],
    ) -> int:
        """Estimate tokens in structured conversation messages."""
        total = 0

        for message in messages:
            total += 4
            total += self.count_tokens(message.get("role", ""))
            total += self.count_tokens(message.get("content", ""))

        return total + 2

    def count_context(
        self,
        messages: list[dict[str, str]],
        instructions: str = "",
    ) -> int:
        """Estimate total input tokens, including instructions."""
        instruction_tokens = self.count_tokens(instructions)

        if instructions:
            instruction_tokens += 4

        return instruction_tokens + self.count_messages(messages)

    def trim_messages(
        self,
        messages: list[dict[str, str]],
        instructions: str = "",
    ) -> list[dict[str, str]]:
        """
        Keep the newest messages within the available token budget.

        The final message is treated as the current user message
        and is never silently removed.
        """
        if not messages:
            return []

        available_tokens = (
            self.max_input_tokens - self.reserved_output_tokens
        )

        instruction_tokens = self.count_tokens(instructions)

        if instructions:
            instruction_tokens += 4

        remaining_budget = available_tokens - instruction_tokens

        if remaining_budget <= 0:
            raise ValueError(
                "System instructions exceed the available "
                "LLM context budget."
            )

        current_message = messages[-1]
        current_tokens = self.count_messages([current_message])

        if current_tokens > remaining_budget:
            raise ValueError(
                "The latest message exceeds the available "
                "LLM context budget. Please shorten your message."
            )

        selected = [current_message]
        used_tokens = current_tokens

        # Add older messages, starting with the most recent.
        for message in reversed(messages[:-1]):
            message_tokens = self.count_messages([message])

            if used_tokens + message_tokens > remaining_budget:
                break

            selected.insert(0, message)
            used_tokens += message_tokens

        return selected
