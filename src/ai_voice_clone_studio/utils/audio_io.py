"""Audio I/O helpers built on soundfile + scipy."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import soundfile as sf


def read_mono(path: Path) -> tuple[np.ndarray, int]:
    """Read any wav/flac/ogg, downmix to mono float32."""
    audio, sr = sf.read(str(path), dtype="float32", always_2d=True)
    mono = audio.mean(axis=1)
    return mono.astype("float32"), sr


def resample(audio: np.ndarray, sr_in: int, sr_out: int) -> np.ndarray:
    if sr_in == sr_out:
        return audio
    from scipy.signal import resample_poly
    from math import gcd
    g = gcd(sr_in, sr_out)
    up, down = sr_out // g, sr_in // g
    return resample_poly(audio, up, down).astype("float32")


def peak_normalize(audio: np.ndarray, target_db: float = -1.0) -> np.ndarray:
    peak = float(np.max(np.abs(audio))) or 1.0
    target = 10 ** (target_db / 20.0)
    return (audio * (target / peak)).astype("float32")