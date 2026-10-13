"""VoiceProfile — the persisted descriptor of a cloned voice."""
from __future__ import annotations

from pydantic import BaseModel, Field


class VoiceProfile(BaseModel):
    id: str
    name: str
    ref_seconds: float = Field(ge=0.0, le=120.0)
    sample_rate: int = Field(ge=8000, le=48000)
    digest: str
    created_at: str
    tags: list[str] = []
    notes: str | None = None