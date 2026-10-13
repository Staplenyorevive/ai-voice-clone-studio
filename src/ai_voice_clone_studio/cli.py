"""Typer entrypoint. Thin — every command delegates to a service."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from loguru import logger

from ai_voice_clone_studio.bootstrap import build_context

app = typer.Typer(help="AI voice cloning generator — zero-shot & few-shot studio.")


@app.command("clone")
def clone(
    ref: Path = typer.Option(..., "--ref", help="Reference voice sample (wav/flac)."),
    text: str = typer.Option(..., "--text", help="Text to synthesize in the cloned voice."),
    out: Path = typer.Option(Path("exports/out.wav"), "--out"),
    name: Optional[str] = typer.Option(None, "--name", help="Save as a reusable voice profile."),
) -> None:
    ctx = build_context()
    profile = ctx.voices.enroll(ref, name=name) if name else ctx.voices.ephemeral(ref)
    ctx.synthesis.speak(profile, text, out)
    logger.success("wrote {}", out)


@app.command("voices")
def voices() -> None:
    ctx = build_context()
    for v in ctx.voices.list_profiles():
        typer.echo(f"{v.id}\t{v.name}\t{v.ref_seconds:.1f}s\t{v.created_at}")


@app.command("devices")
def devices() -> None:
    ctx = build_context()
    typer.echo(f"backend={ctx.models.active_backend()}  cuda={ctx.models.cuda_available()}")


if __name__ == "__main__":
    app()