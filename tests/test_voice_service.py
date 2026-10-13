"""Voice profile lifecycle tests — enroll, list, rename, delete."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import soundfile as sf

from ai_voice_clone_studio.bootstrap import build_context


def _write_ref(path: Path, seconds: float = 2.0, sr: int = 24000) -> Path:
    t = np.linspace(0, seconds, int(sr * seconds), endpoint=False)
    tone = 0.2 * np.sin(2 * np.pi * 220 * t).astype("float32")
    sf.write(path, tone, sr)
    return path


def test_enroll_and_list(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    cfg = tmp_path / "default.yaml"
    cfg.write_text(
        "storage:\n  voices_dir: voices\n  exports_dir: exports\n",
        encoding="utf-8",
    )
    ctx = build_context(cfg)
    ref = _write_ref(tmp_path / "ref.wav")
    profile = ctx.voices.enroll(ref, name="narrator")
    assert profile.name == "narrator"
    assert profile.ref_seconds > 0
    listed = ctx.voices.list_profiles()
    assert any(p.id == profile.id for p in listed)


def test_rename_and_delete(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    cfg = tmp_path / "default.yaml"
    cfg.write_text("storage:\n  voices_dir: voices\n", encoding="utf-8")
    ctx = build_context(cfg)
    ref = _write_ref(tmp_path / "ref.wav")
    profile = ctx.voices.enroll(ref, name="old")
    renamed = ctx.voices.rename(profile.id, "new")
    assert renamed.name == "new"
    ctx.voices.delete(profile.id)
    assert all(p.id != profile.id for p in ctx.voices.list_profiles())