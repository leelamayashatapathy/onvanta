from __future__ import annotations

from typing import Any


def success_response(message: str, data: Any = None, metadata: dict | None = None) -> dict:
    payload = {'message': message, 'data': data}
    if metadata is not None:
        payload['metadata'] = metadata
    return payload


def error_response(message: str, error_code: str, field_errors: dict | None = None) -> dict:
    payload = {'message': message, 'error_code': error_code}
    if field_errors is not None:
        payload['field_errors'] = field_errors
    return payload
