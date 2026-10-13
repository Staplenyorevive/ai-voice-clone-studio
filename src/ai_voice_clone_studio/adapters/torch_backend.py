"""Torch backend adapter — device placement and dtype policy."""
from __future__ import annotations

from loguru import logger


class TorchBackend:
    def __init__(self, backend: str = "cpu") -> None:
        self.backend = backend

    def device(self):
        import torch
        if self.backend == "cuda" and torch.cuda.is_available():
            return torch.device("cuda")
        return torch.device("cpu")

    def autocast(self):
        import torch
        if self.device().type == "cuda":
            return torch.autocast("cuda", dtype=torch.float16)
        return torch.autocast("cpu", dtype=torch.bfloat16)

    def warm(self) -> None:
        logger.debug("torch backend warmed on {}", self.device())