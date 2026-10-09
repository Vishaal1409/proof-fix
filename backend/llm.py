"""Token Factory client wrapper (OpenAI-compatible API)."""
from openai import OpenAI
import config

_client = None


def get_client() -> OpenAI:
    global _client
    if _client is None:
        if not config.NEBIUS_API_KEY:
            raise RuntimeError("NEBIUS_API_KEY is missing. Add it to backend/.env")
        _client = OpenAI(base_url=config.NEBIUS_BASE_URL, api_key=config.NEBIUS_API_KEY)
    return _client


def complete(prompt: str, model: str, system: str | None = None,
             temperature: float = 0.2, max_tokens: int = 1024) -> str:
    """Send one prompt to a model and return the reply text."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = get_client().chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content or ""
