"""Artifact descriptors — outputs written to exports/."""
from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel


class SynthesisArtifact(BaseModel):
    path: Path
    voice_id: str
    duration_s: float
    sample_rate: int
    bytes_written: int