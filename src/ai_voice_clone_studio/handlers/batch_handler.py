"""Handler for batch synthesis jobs (queue of CloneRequests)."""
from __future__ import annotations

from pathlib import Path

from loguru import logger

from ai_voice_clone_studio.models.requests import CloneRequest
from ai_voice_clone_studio.services.synthesis_service import SynthesisService
from ai_voice_clone_studio.services.voice_service import VoiceService


class BatchHandler:
    def __init__(self, voices: VoiceService, synthesis: SynthesisService) -> None:
        self._voices = voices
        self._synth = synthesis

    def handle(self, jobs: list[CloneRequest]) -> list[Path]:
        results: list[Path] = []
        for i, job in enumerate(jobs, 1):
            logger.info("batch {}/{}: {}", i, len(jobs), job.out_path.name)
            profile = self._voices.ephemeral(job.ref_path)
            results.append(self._synth.speak(profile, job.text, job.out_path))
        return results