"""YAML config loader with pydantic validation and env overrides."""
from __future__ import annotations

import os
from pathlib import Path

import yaml
from pydantic import BaseModel, Field

_DEFAULT = Path(__file__).resolve().parents[3] / "config" / "default.yaml"


class AppCfg(BaseModel):
    name: str = "ai-voice-clone-studio"
    version: str = "0.6.2"
    data_dir: str = "data"
    log_level: str = "INFO"


class AudioCfg(BaseModel):
    sample_rate: int = 24000
    bit_depth: int = 16
    channels: int = 1
    chunk_ms: int = 40
    denoise: bool = True
    normalize_lufs: float = -16.0


class ModelCfg(BaseModel):
    backend: str = "auto"
    checkpoint_dir: str = "models/checkpoints"
    embedding_dir: str = "models/embeddings"
    default_voice: str = "neutral_v1"
    zero_shot: bool = True
    max_ref_seconds: int = 30


class SynthesisCfg(BaseModel):
    f0_method: str = "rmvpe"
    pitch_shift: int = 0
    index_rate: float = Field(0.75, ge=0.0, le=1.0)
    protect: float = Field(0.33, ge=0.0, le=0.5)
    temperature: float = Field(0.6, ge=0.1, le=1.5)
    seed: int = 6767


class StorageCfg(BaseModel):
    voices_dir: str = "voices"
    exports_dir: str = "exports"
    max_voice_profiles: int = 128


class Config(BaseModel):
    app: AppCfg = AppCfg()
    audio: AudioCfg = AudioCfg()
    model: ModelCfg = ModelCfg()
    synthesis: SynthesisCfg = SynthesisCfg()
    storage: StorageCfg = StorageCfg()


def load_config(path: Path | None = None) -> Config:
    src = path or _DEFAULT
    raw: dict = {}
    if src.exists():
        with src.open("r", encoding="utf-8") as fh:
            raw = yaml.safe_load(fh) or {}
    # env override: AVCS__APP__LOG_LEVEL=DEBUG
    for key, val in os.environ.items():
        if not key.startswith("AVCS__"):
            continue
        parts = [p.lower() for p in key[len("AVCS__"):].split("__")]
        node = raw
        for p in parts[:-1]:
            node = node.setdefault(p, {})
        node[parts[-1]] = val
    return Config(**raw)