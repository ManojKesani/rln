# Importing every model here is what registers its table on Base.metadata,
# which alembic/env.py needs in order to see the tables. Add new models to this list.
from app.db.models.conversation import Conversation
from app.db.models.llm_call import LlmCall

__all__ = ["Conversation", "LlmCall"]
