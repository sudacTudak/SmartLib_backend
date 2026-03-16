from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Any, Iterable, Mapping, TypeVar


@dataclass(frozen=True, slots=True)
class ArgumentSpec:
    flag: str
    kwargs: Mapping[str, Any] = ()


class ArgumentSpecSet:
    def __init__(self, specs: Iterable[ArgumentSpec]):
        self._specs = tuple(specs)

    def add_to_parser(self, parser) -> None:
        for spec in self._specs:
            parser.add_argument(spec.flag, **dict(spec.kwargs))


T = TypeVar("T")


def dataclass_from_options(dataclass_type: type[T], options: Mapping[str, Any]) -> T:
    """
    Build a dataclass instance from Django command options.
    Ignores unrelated keys like 'verbosity' etc.
    """
    allowed = {f.name for f in fields(dataclass_type)}
    payload = {k: v for k, v in options.items() if k in allowed}
    return dataclass_type(**payload)

