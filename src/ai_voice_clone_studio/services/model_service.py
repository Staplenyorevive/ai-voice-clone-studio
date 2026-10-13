"""ModelService — backend selection, checkpoint loading, device probing."""
from __future__ import annotations

from pathlib import Path

from loguru import logger

from ai_voice_clone_studio.config.loader import Config


class ModelService:
    """Owns the runtime backend. Thread-safe for read; load is single-shot."""

    def __init__(self, config: Config) -> None:
        self._cfg = config
        self._backend = self._resolve_backend()
        self._loaded: dict[str, object] = {}

    def _resolve_backend(self) -> str:
        want = self._cfg.model.backend
        if want != "auto":
            return want
        try:
            import torch  # noqa: WPS433
            if torch.cuda.is_available():
                return "cuda"
        except Exception:  # torch missing or broken install
            logger.warning("torch probe failed; falling back to cpu")
        return "cpu"

    def active_backend(self) -> str:
        return self._backend

    def cuda_available(self) -> bool:
        try:
            import torch
            return bool(torch.cuda.is_available())
        except Exception:
            return False

    def checkpoint_path(self, voice_id: str) -> Path:
        return Path(self._cfg.model.checkpoint_dir) / f"{voice_id}.pth"

    def load(self, voice_id: str) -> object | None:
        """Loads a checkpoint once; returns cached handle afterwards."""
        if voice_id in self._loaded:
            return self._loaded[voice_id]
        path = self.checkpoint_path(voice_id)
        if not path.exists():
            logger.debug("no checkpoint for {} — zero-shot path", voice_id)
            return None
        import torch
        blob = torch.load(path, map_location=self._backend, weights_only=True)
        self._loaded[voice_id] = blob
        return blob