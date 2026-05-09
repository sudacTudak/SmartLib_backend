from typing import Annotated, TypeAlias, TypeVar

from pydantic import BeforeValidator

__all__ = ['OptionalListQueryParam']


def _as_list(value):
    """
    Нормализация query-параметров к ``list``:

    - ``None`` → ``None``
    - одиночная строка → список из одного элемента; если в строке есть запятые — разбиение по ним
      (удобно для ``?ids=a,b`` и для фронтового ``URLSearchParams`` с ``join(',')``)
    - список (несколько ключей в QueryDict / Axios ``params``) — сохраняется; элементы со запятыми
      дополнительно разбиваются.
    """
    if value is None:
        return None
    if isinstance(value, list):
        parts: list[str] = []
        for item in value:
            if isinstance(item, str) and ',' in item:
                parts.extend(s.strip() for s in item.split(',') if s.strip())
            elif item is not None and str(item).strip():
                parts.append(str(item).strip())
        return parts or None
    if isinstance(value, str):
        split = [s.strip() for s in value.split(',') if s.strip()]
        return split or None
    return value
    return value


T = TypeVar('T')

OptionalListQueryParam: TypeAlias = Annotated[list[T] | None, BeforeValidator(_as_list)]
