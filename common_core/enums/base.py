from enum import Enum, StrEnum, IntEnum

from typing import cast, TypeVar, Generic, Type, Iterable

__all__ = ['AppStrEnum', 'AppIntEnum']

ValueT = TypeVar('ValueT', str, int)


class AppEnumMixin(Generic[ValueT]):
    @classmethod
    def as_django_model_choices(cls: Type[Enum]) -> tuple[tuple[ValueT, str], ...]:
        return tuple((cast(ValueT, pair.value), cast(str, pair.name)) for pair in cls)

    @classmethod
    def items(cls: Type[Enum]) -> Iterable[ValueT]:
        yield from [cast(ValueT, pair.value) for pair in cls]

    @classmethod
    def as_django_serializer_choices(cls) -> tuple[ValueT, ...]:
        return tuple(cls.items())


class AppStrEnum(AppEnumMixin[str], StrEnum):
    pass


class AppIntEnum(AppEnumMixin[int], IntEnum):
    pass
