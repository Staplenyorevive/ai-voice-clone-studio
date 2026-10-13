"""Timing helpers for synthesis stages."""
from __future__ import annotations

import time
from contextlib import contextmanager


@contextmanager
def stage(label: str):
    t0 = time.perf_counter()
    try:
        yield
    finally:
        dt = (time.perf_counter() - t0) * 1000
        print(f"[avcs] {label}: {dt:.1f}ms")