"""Request DTOs — the shape handlers accept."""
from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class CloneRequest(BaseModel):
    ref_path: Path
    text: str = Field(min_length=1, max_length=8000)
    out_path: Path
    voice_name: str | None = None
    pitch_shift: int = 0
    index_rate: float = Field(0.75, ge=0.0, le=1.0)


class BatchRequest(BaseModel):
    jobs: list[CloneRequest]
    workers: int = Field(1, ge=1, le=8)