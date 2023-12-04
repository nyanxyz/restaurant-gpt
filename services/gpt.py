from openai import OpenAI
import os
from utils.chat_history import ChatHistory

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
)


class GPTManager:
    def __init__(self):
        self.chat_history = ChatHistory()

    def generate(self, system_prompt, query, max_tokens=64, stream=False):
        history = self.chat_history.get_messages()
        messages = [
            *history,
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ]

        result = client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo",
            temperature=0,
            max_tokens=max_tokens,
            stream=stream,
        )

        if stream:
            return result

        return result.choices[0].message.content
