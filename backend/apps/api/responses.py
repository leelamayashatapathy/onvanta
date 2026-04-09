from __future__ import annotations

from typing import Any


def success_response(message: str, data: Any = None, metadata: dict | None = None) -> dict:
    payload = {'message': message, 'data': data}
    if metadata is not None:
        payload['metadata'] = metadata
    return payload