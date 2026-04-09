from __future__ import annotations

from pathlib import Path


def safe_join_path(*parts: str) -> str:
    cleaned = [str(part).strip('/').strip('\\') for part in parts if part]
    return str(Path(*cleaned))