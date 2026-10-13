"""Handler for voice-profile CRUD (list, enroll, delete)."""
from __future__ import annotations

from ai_voice_clone_studio.models.voice import VoiceProfile
from ai_voice_clone_studio.services.voice_service import VoiceService


class VoiceHandler:
    def __init__(self, voices: VoiceService) -> None:
        self._voices = voices

    def list(self) -> list[VoiceProfile]:
        return self._voices.list_profiles()

    def delete(self, voice_id: str) -> None:
        self._voices.delete(voice_id)

    def rename(self, voice_id: str, new_name: str) -> VoiceProfile:
        return self._voices.rename(voice_id, new_name)