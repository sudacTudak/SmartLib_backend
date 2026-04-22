import re
from collections.abc import Mapping
from typing import Any

__all__ = [
    "camel_to_snake",
    "snake_to_camel",
    "keys_to_snake_case",
    "keys_to_camel_case",
]


_re_first_cap = re.compile(r"(.)([A-Z][a-z]+)")
_re_all_cap = re.compile(r"([a-z0-9])([A-Z])")


def camel_to_snake(s: str) -> str:
    # Already looks like snake_case.
    if "_" in s:
        return s
    s = _re_first_cap.sub(r"\1_\2", s)
    s = _re_all_cap.sub(r"\1_\2", s)
    return s.lower()


def snake_to_camel(s: str) -> str:
    if "_" not in s:
        return s
    parts = s.split("_")
    if not parts:
        return s
    first, *rest = parts
    return first + "".join(p[:1].upper() + p[1:] for p in rest if p)


def keys_to_snake_case(obj: Any) -> Any:
    if isinstance(obj, list):
        return [keys_to_snake_case(v) for v in obj]
    if isinstance(obj, tuple):
        return tuple(keys_to_snake_case(v) for v in obj)
    if isinstance(obj, Mapping):
        out: dict[Any, Any] = {}
        for k, v in obj.items():
            nk = camel_to_snake(k) if isinstance(k, str) else k
            out[nk] = keys_to_snake_case(v)
        return out
    return obj


def keys_to_camel_case(obj: Any) -> Any:
    if isinstance(obj, list):
        return [keys_to_camel_case(v) for v in obj]
    if isinstance(obj, tuple):
        return tuple(keys_to_camel_case(v) for v in obj)
    if isinstance(obj, Mapping):
        out: dict[Any, Any] = {}
        for k, v in obj.items():
            nk = snake_to_camel(k) if isinstance(k, str) else k
            out[nk] = keys_to_camel_case(v)
        return out
    return obj

