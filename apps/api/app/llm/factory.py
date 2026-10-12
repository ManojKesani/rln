"""build_chat_model(provider, model) -> a LangChain chat model.

Everything else in the app (agent, streaming, callbacks) works with whatever this
returns and never needs to know which provider it is. That is why switching model
mid-conversation is just calling this with different strings.
"""
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_openai import ChatOpenAI

from app.llm.providers import PROVIDERS, make_fake_model


class UnknownProviderError(ValueError):
    pass


class ProviderUnavailableError(RuntimeError):
    pass


def build_chat_model(provider: str, model: str, **params):
    """Raises UnknownProviderError / ProviderUnavailableError, which the services
    turn into BadModel (HTTP 400). Extra **params (temperature, ...) go to ChatOpenAI."""
    if provider not in PROVIDERS:
        raise UnknownProviderError(f"Unknown provider '{provider}'. Options: {list(PROVIDERS)}")
    if provider == "fake":
        return make_fake_model()  # the model id is ignored for the fake

    p = PROVIDERS[provider]
    if not p.available:
        raise ProviderUnavailableError(f"{p.key_env} is not set in .env")

    # Optional client-side rate limit, in requests per minute (converted to per second).
    rpm = params.pop("rpm", None)
    if rpm:
        params["rate_limiter"] = InMemoryRateLimiter(
            requests_per_second=rpm / 60, check_every_n_seconds=0.1, max_bucket_size=1)
    # No automatic retries inside the client: when we add retry logic ourselves,
    # every attempt will show up as its own span in Phoenix.
    params.setdefault("max_retries", 0)
    # Note: the model id is NOT checked here; a wrong id fails at call time (error event).
    return ChatOpenAI(model=model, api_key=p.api_key, base_url=p.base_url, **params)
