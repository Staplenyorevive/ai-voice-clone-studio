"""Synthesis pipeline smoke tests — deterministic, no GPU required."""
from __future__ import annotations

from pathlib import Path

import soundfile as sf

from ai_voice_clone_studio.bootstrap import build_context
from ai_voice_clone_studio.models.requests import CloneRequest
from ai_voice_clone_studio.handlers.clone_handler import CloneHandler


def test_speak_writes_artifact(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    cfg = tmp_path / "default.yaml"
    cfg.write_text("storage:\n  voices_dir: voices\n  exports_dir: exports\n", encoding="utf-8")
    ctx = build_context(cfg)

    ref = tmp_path / "ref.wav"
    import numpy as np
    sf.write(ref, np.zeros(24000, dtype="float32"), 24000)

    out = tmp_path / "exports" / "hello.wav"
    handler = CloneHandler(ctx.voices, ctx.synthesis)
    result = handler.handle(CloneRequest(ref_path=ref, text="hello world", out_path=out))
    assert result.exists()
    data, sr = sf.read(result)
    assert sr == ctx.config.audio.sample_rate
    assert len(data) >= 1