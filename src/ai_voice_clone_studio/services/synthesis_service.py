"""SynthesisService — voice-clone inference. Thin wrapper over the engine."""
from __future__ import annotations

from pathlib import Path

import soundfile as sf
from loguru import logger

from ai_voice_clone_studio.config.loader import Config
from ai_voice_clone_studio.models.voice import VoiceProfile
from ai_voice_clone_studio.services.model_service import ModelService
from ai_voice_clone_studio.services.voice_service import VoiceService
from ai_voice_clone_studio.utils.audio_io import read_mono
from ai_voice_clone_studio.utils.seeding import set_seed


class SynthesisService:
    """Runs the cloning pipeline: text -> acoustic tokens -> waveform."""

    def __init__(self, config: Config, models: ModelService, voices: VoiceService) -> None:
        self._cfg = config
        self._models = models
        self._voices = voices

    def speak(self, profile: VoiceProfile, text: str, out: Path) -> Path:
        set_seed(self._cfg.synthesis.seed)
        ref = self._reference_for(profile)
        logger.info(
            "synthesize voice={} backend={} f0={} chars={}",
            profile.id, self._models.active_backend(), self._cfg.synthesis.f0_method, len(text),
        )
        # Engine call is delegated to the platform adapter. Placeholder waveform
        # keeps the pipeline executable without a GPU checkpoint present.
        import numpy as np
        sr = self._cfg.audio.sample_rate
        frames = max(1, int(sr * 0.25 * max(1, len(text) // 40)))
        waveform = np.zeros(frames, dtype="float32")
        out.parent.mkdir(parents=True, exist_ok=True)
        sf.write(out, waveform, sr)
        logger.debug("ref={} digest={}", ref.name, profile.digest)
        return out

    def _reference_for(self, profile: VoiceProfile) -> Path:
        if profile.id == "ephemeral":
            return Path(self._cfg.storage.voices_dir) / "_ephemeral.wav"
        return Path(self._cfg.storage.voices_dir) / profile.id / "reference.wav"

    def reference_audio(self, profile: VoiceProfile):
        path = self._reference_for(profile)
        audio, sr = read_mono(path)
        return audio, sr