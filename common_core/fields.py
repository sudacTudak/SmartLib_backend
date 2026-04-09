from typing import TypeVar, Annotated, TypeAlias
from pydantic import BeforeValidator

__all__ = ['OptionalListQueryParam']


def _as_list(value):
    if value is None:
        return value
    if isinstance(value, str):
        return [value]
    return value


T = TypeVar("T")

OptionalListQueryParam: TypeAlias = Annotated[list[T] | None, BeforeValidator(_as_list)]
