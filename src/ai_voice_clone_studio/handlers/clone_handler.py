"""Handler for one-shot clone requests. No business logic — routes only."""
from __future__ import annotations

from pathlib import Path

from ai_voice_clone_studio.models.requests import CloneRequest
from ai_voice_clone_studio.services.synthesis_service import SynthesisService
from ai_voice_clone_studio.services.voice_service import VoiceService


class CloneHandler:
    def __init__(self, voices: VoiceService, synthesis: SynthesisService) -> None:
        self._voices = voices
        self._synth = synthesis

    def handle(self, req: CloneRequest) -> Path:
        profile = (
            self._voices.enroll(req.ref_path, name=req.voice_name)
            if req.voice_name
            else self._voices.ephemeral(req.ref_path)
        )
        return self._synth.speak(profile, req.text, req.out_path)