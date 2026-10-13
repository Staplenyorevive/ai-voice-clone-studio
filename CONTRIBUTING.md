# Contributing to ai-voice-clone-studio

Thanks for wanting to help build the AI voice cloning generator. This is a
hobbyist + research project. PRs, bug reports, and voice-model experiments
are all welcome.

## Ground rules

- One feature per PR. Keep diffs small and reviewable.
- Every new service gets a matching handler and at least one test.
- No voice profile samples committed to the repo. Reference audio stays local.
- Run `ruff check .` and `pytest -q` before opening a PR.

## Layout

```
src/ai_voice_clone_studio/
  bootstrap.py        # process wiring
  cli.py              # typer entrypoint
  config/             # yaml + pydantic config
  handlers/           # thin request routers
  services/           # business logic
  models/             # pydantic DTOs
  adapters/           # windows audio, torch backend
  utils/              # audio io, seeding, profiling
native/voice_dsp/     # optional C++ DSP kernel
tests/                # pytest suite
```

## Adding a new synthesis backend

1. Drop the engine under `services/` and expose a `speak()` method.
2. Register it in `bootstrap.AppContext`.
3. Add a handler in `handlers/` if it needs a CLI surface.
4. Add a smoke test in `tests/`.

## Voice model contributions

If you've trained a checkpoint that clones cleanly from a 10s reference,
open an issue with: reference length, f0 method, index rate, and a
subjective quality note. Do not attach the checkpoint — link it.