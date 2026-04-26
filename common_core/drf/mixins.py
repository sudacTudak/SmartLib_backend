from __future__ import annotations

__all__ = ["AbsoluteMediaUrlMixin"]


class AbsoluteMediaUrlMixin:
    """
    Converts selected File/ImageField values to absolute URLs using request.build_absolute_uri.

    Set `absolute_url_fields = ("preview_link", ...)` in serializer.
    """

    absolute_url_fields: tuple[str, ...] = ()

    def to_representation(self, instance):  # noqa: ANN001 - DRF instance type
        data = super().to_representation(instance)  # type: ignore[misc]
        request = getattr(self, "context", {}).get("request")
        if request is None:
            return data

        for field in self.absolute_url_fields:
            value = data.get(field)
            if value and isinstance(value, str) and value.startswith("/"):
                data[field] = request.build_absolute_uri(value)
        return data

