from collections import defaultdict
from typing import Dict, List


class ConversationMemoryService:
    def __init__(self) -> None:
        self.store: Dict[str, List[dict]] = defaultdict(list)
        self.max_turns = 5

    def add_turn(self, conversation_id: str, question: str, answer: str) -> None:
        self.store[conversation_id].append(
            {
                "question": question,
                "answer": answer,
            }
        )

        if len(self.store[conversation_id]) > self.max_turns:
            self.store[conversation_id] = self.store[conversation_id][-self.max_turns :]

    def get_history(self, conversation_id: str) -> List[dict]:
        return self.store.get(conversation_id, [])

    def format_history(self, conversation_id: str) -> str:
        history = self.get_history(conversation_id)

        if not history:
            return ""

        formatted_turns = []
        for i, turn in enumerate(history, start=1):
            formatted_turns.append(
                f"Turn {i}\n"
                f"User: {turn['question']}\n"
                f"Assistant: {turn['answer']}"
            )

        return "\n\n".join(formatted_turns)