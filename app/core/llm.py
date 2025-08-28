from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_answer(query: str, context: list[str], history: list[dict]) -> str:
    """
    Generate an answer to a query using a language model.
    """
    system_prompt = (
        "You are a helpful assistant. Use the following context to answer the user's query."
        "If you don't know the answer, just say that you don't know."
        "Don't try to make up an answer."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Context:\n{''.join(context)}\n\n---\n\nQuery: {query}"},
    ]

    # Add chat history to the prompt
    for message in history:
        messages.append(message)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    return response.choices[0].message.content