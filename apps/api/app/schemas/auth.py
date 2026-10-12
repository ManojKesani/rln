"""Request/response shapes for the auth routes. These become openapi.json,
which the frontend's typed client is generated from (`make openapi`)."""
from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class MeResponse(BaseModel):
    username: str
