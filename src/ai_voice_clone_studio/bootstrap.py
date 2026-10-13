"""Entry/bootstrap layer. Loads config, wires services, hands control to CLI or GUI."""
from __future__ import annotations

from pathlib import Path

from loguru import logger

from ai_voice_clone_studio.config.loader import load_config
from ai_voice_clone_studio.services.voice_service import VoiceService
from ai_voice_clone_studio.services.synthesis_service import SynthesisService
from ai_voice_clone_studio.services.model_service import ModelService


class AppContext:
    """Holds wired services for the process lifetime. One per process."""

    def __init__(self, config_path: Path | None = None) -> None:
        self.config = load_config(config_path)
        logger.remove()
        logger.add(
            Path(self.config.app.data_dir) / "avcs.log",
            level=self.config.app.log_level,
            rotation="10 MB",
            retention=5,
        )
        self.models = ModelService(self.config)
        self.voices = VoiceService(self.config, self.models)
        self.synthesis = SynthesisService(self.config, self.models, self.voices)
        logger.info("ai-voice-clone-studio {} booted", self.config.app.version)


def build_context(config_path: Path | None = None) -> AppContext:
    return AppContext(config_path)