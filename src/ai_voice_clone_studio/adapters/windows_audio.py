"""Windows WASAPI / sounddevice adapter for live playback and capture."""
from __future__ import annotations

from pathlib import Path

from loguru import logger


class WindowsAudioAdapter:
    """Live playback + mic capture. No-ops cleanly on non-Windows hosts."""

    def __init__(self, sample_rate: int = 24000) -> None:
        self._sr = sample_rate
        self._available = self._probe()

    def _probe(self) -> bool:
        try:
            import sounddevice as sd
            sd.query_devices()
            return True
        except Exception as exc:
            logger.warning("audio adapter unavailable: {}", exc)
            return False

    def play(self, wav: Path) -> None:
        if not self._available:
            logger.info("playback skipped (no audio device)")
            return
        import sounddevice as sd
        import soundfile as sf
        data, sr = sf.read(wav, dtype="float32")
        sd.play(data, sr)
        sd.wait()

    def record(self, seconds: float, out: Path) -> Path:
        if not self._available:
            raise RuntimeError("no capture device")
        import sounddevice as sd
        import soundfile as sf
        frames = int(seconds * self._sr)
        capture = sd.rec(frames, samplerate=self._sr, channels=1, dtype="float32")
        sd.wait()
        sf.write(out, capture, self._sr)
        return out