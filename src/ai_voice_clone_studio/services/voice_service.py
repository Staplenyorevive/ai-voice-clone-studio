"""VoiceService — enroll reference samples into voice profiles."""
from __future__ import annotations

import hashlib
import time
import uuid
from pathlib import Path

import soundfile as sf
from loguru import logger

from ai_voice_clone_studio.config.loader import Config
from ai_voice_clone_studio.models.voice import VoiceProfile
from ai_voice_clone_studio.services.model_service import ModelService
from ai_voice_clone_studio.utils.audio_io import read_mono, resample


class VoiceService:
    """Manages voice profiles on disk under storage.voices_dir."""

    def __init__(self, config: Config, models: ModelService) -> None:
        self._cfg = config
        self._models = models
        self._root = Path(config.storage.voices_dir)
        self._root.mkdir(parents=True, exist_ok=True)

    def _profile_dir(self, voice_id: str) -> Path:
        return self._root / voice_id

    def enroll(self, ref_path: Path, name: str | None = None) -> VoiceProfile:
        """Persist a reference sample as a named, reusable voice profile."""
        audio, sr = read_mono(ref_path)
        audio = resample(audio, sr, self._cfg.audio.sample_rate)
        max_s = self._cfg.model.max_ref_seconds
        audio = audio[: max_s * self._cfg.audio.sample_rate]

        voice_id = uuid.uuid4().hex[:12]
        pdir = self._profile_dir(voice_id)
        pdir.mkdir(parents=True, exist_ok=True)
        sf.write(pdir / "reference.wav", audio, self._cfg.audio.sample_rate)

        digest = hashlib.sha256(audio.tobytes()).hexdigest()[:16]
        profile = VoiceProfile(
            id=voice_id,
            name=name or f"voice_{voice_id[:6]}",
            ref_seconds=len(audio) / self._cfg.audio.sample_rate,
            sample_rate=self._cfg.audio.sample_rate,
            digest=digest,
            created_at=time.strftime("%Y-%m-%dT%H:%M:%S"),
        )
        (pdir / "profile.json").write_text(profile.model_dump_json(indent=2), encoding="utf-8")
        logger.info("enrolled voice {} ({:.1f}s)", profile.id, profile.ref_seconds)
        return profile

    def ephemeral(self, ref_path: Path) -> VoiceProfile:
        """One-shot profile — never written to disk. Used by batch/clone."""
        audio, sr = read_mono(ref_path)
        audio = resample(audio, sr, self._cfg.audio.sample_rate)
        digest = hashlib.sha256(audio.tobytes()).hexdigest()[:16]
        return VoiceProfile(
            id="ephemeral",
            name=ref_path.stem,
            ref_seconds=len(audio) / self._cfg.audio.sample_rate,
            sample_rate=self._cfg.audio.sample_rate,
            digest=digest,
            created_at="ephemeral",
        )

    def list_profiles(self) -> list[VoiceProfile]:
        out: list[VoiceProfile] = []
        for pdir in sorted(self._root.iterdir()):
            meta = pdir / "profile.json"
            if meta.exists():
                out.append(VoiceProfile.model_validate_json(meta.read_text(encoding="utf-8")))
        return out

    def delete(self, voice_id: str) -> None:
        import shutil
        shutil.rmtree(self._profile_dir(voice_id), ignore_errors=True)
        logger.info("deleted voice {}", voice_id)

    def rename(self, voice_id: str, new_name: str) -> VoiceProfile:
        pdir = self._profile_dir(voice_id)
        meta = pdir / "profile.json"
        profile = VoiceProfile.model_validate_json(meta.read_text(encoding="utf-8"))
        profile.name = new_name
        meta.write_text(profile.model_dump_json(indent=2), encoding="utf-8")
        return profile