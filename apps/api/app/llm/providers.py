"""Which LLM providers exist, and the fake model for free development.

Groq, OpenRouter and NVIDIA NIM all expose an OpenAI-compatible API, so one
LangChain class (ChatOpenAI) talks to all of them: only base_url and the API key
differ. That is the whole "provider layer". Adding another compatible provider
means adding one entry to PROVIDERS and one key to config.py.

The fake model needs no key and no network, so development costs zero tokens.
"""
import itertools
from dataclasses import dataclass

from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage

from app.config import settings

FAKE_MODEL_ID = "fake-echo"


@dataclass(frozen=True)
class ProviderConfig:
    name: str
    base_url: str | None     # where ChatOpenAI sends requests
    key_env: str | None      # name of the env var holding the key; None means no key needed (fake)
    models_url: str | None   # where to list available models

    @property
    def api_key(self) -> str:
        if not self.key_env:
            return ""
        # "GROQ_API_KEY" -> settings.groq_api_key
        return getattr(settings, self.key_env.lower(), "") or ""

    @property
    def available(self) -> bool:
        """Usable = no key needed, or a key is set. A missing key is "unavailable", not an error."""
        return self.key_env is None or bool(self.api_key)


PROVIDERS: dict[str, ProviderConfig] = {
    "groq": ProviderConfig("groq", "https://api.groq.com/openai/v1", "GROQ_API_KEY",
                           "https://api.groq.com/openai/v1/models"),
    # OpenRouter and NVIDIA URLs are not verified yet (no keys were available to test).
    "openrouter": ProviderConfig("openrouter", "https://openrouter.ai/api/v1", "OPENROUTER_API_KEY",
                                 "https://openrouter.ai/api/v1/models"),
    "nvidia": ProviderConfig("nvidia", "https://integrate.api.nvidia.com/v1", "NVIDIA_API_KEY",
                             "https://integrate.api.nvidia.com/v1/models"),
    "fake": ProviderConfig("fake", None, None, None),
}


def make_fake_model() -> GenericFakeChatModel:
    """A chat model that always answers the same canned text.

    GenericFakeChatModel pulls replies from an iterator; itertools.cycle makes it
    repeat forever. It streams word by word, which exercises the streaming UI.
    Zero usage is reported explicitly so llm_calls rows show 0 tokens.
    """
    reply = AIMessage(
        content="This is the fake model. No network, zero tokens.",
        usage_metadata={"input_tokens": 0, "output_tokens": 0, "total_tokens": 0},
    )
    return GenericFakeChatModel(messages=itertools.cycle([reply]))
