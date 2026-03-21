from typing import TypeVar, Annotated, List, Type, TypeAlias
from pydantic import BeforeValidator
from typing_extensions import TypeAliasType

__all__ = ['OptionalListQueryParam']


def _as_list(value):
    if value is None:
        return value
    if isinstance(value, str):
        return [value]
    return value


T = TypeVar("T")

OptionalListQueryParam: TypeAlias = Annotated[list[T] | None, BeforeValidator(_as_list)]

# OptionalListQueryParam: TypeAliasType = TypeAliasType(
#     "OptionalListQueryParam",
#     Annotated[list[T] | None, BeforeValidator(_as_list)], type_params=(T,)
# )
