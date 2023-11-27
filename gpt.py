from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
)


def get_gpt_response(system_prompt, query, max_tokens=64):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": query,
            }
        ],
        model="gpt-3.5-turbo",
        temperature=0,
        max_tokens=max_tokens
    )

    return chat_completion.choices[0].message.content
