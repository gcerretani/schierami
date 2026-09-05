#!/usr/bin/env python3
"""Strict helpers shared by Schierami's deterministic calculators."""
from __future__ import annotations

from decimal import Decimal, InvalidOperation
import math
from typing import Any, Iterable


class ContractError(ValueError):
    """Raised when an input does not match an explicitly supported contract."""


def require_object(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ContractError(f"{path} must be an object")
    return value


def require_array(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        raise ContractError(f"{path} must be an array")
    return value


def reject_unknown(obj: dict[str, Any], allowed: Iterable[str], path: str) -> None:
    unknown = sorted(set(obj) - set(allowed))
    if unknown:
        raise ContractError(f"unsupported keys at {path}: {', '.join(unknown)}")


def require_bool(value: Any, path: str) -> bool:
    if type(value) is not bool:
        raise ContractError(f"{path} must be a boolean")
    return value


def require_int(value: Any, path: str, minimum: int | None = None) -> int:
    if type(value) is not int:
        raise ContractError(f"{path} must be an integer")
    if minimum is not None and value < minimum:
        raise ContractError(f"{path} must be >= {minimum}")
    return value


def require_string(value: Any, path: str, *, nonempty: bool = True) -> str:
    if not isinstance(value, str):
        raise ContractError(f"{path} must be a string")
    if nonempty and not value.strip():
        raise ContractError(f"{path} must not be empty")
    return value


def normalize_id(value: Any, path: str) -> str:
    if isinstance(value, bool) or value is None:
        raise ContractError(f"{path} must be a string or integer identifier")
    if isinstance(value, (str, int)):
        text = str(value).strip()
        if text:
            return text
    raise ContractError(f"{path} must be a non-empty string or integer identifier")


def require_string_list(value: Any, path: str, *, nonempty: bool = False) -> list[str]:
    rows = require_array(value, path)
    if nonempty and not rows:
        raise ContractError(f"{path} must not be empty")
    out: list[str] = []
    for i, item in enumerate(rows):
        out.append(require_string(item, f"{path}[{i}]"))
    if len(out) != len(set(out)):
        raise ContractError(f"{path} must not contain duplicates")
    return out


def require_decimal(value: Any, path: str) -> Decimal:
    if isinstance(value, bool) or value is None:
        raise ContractError(f"{path} must be a finite number")
    if not isinstance(value, (int, float, str)):
        raise ContractError(f"{path} must be a finite number")
    if isinstance(value, float) and not math.isfinite(value):
        raise ContractError(f"{path} must be a finite number")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ContractError(f"{path} must be a finite number") from None
    if not result.is_finite():
        raise ContractError(f"{path} must be a finite number")
    return result


def decimal_number(value: Decimal) -> float:
    """Return JSON-friendly numeric output after exact Decimal computation."""
    return float(value)
