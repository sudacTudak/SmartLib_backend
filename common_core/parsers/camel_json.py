from __future__ import annotations

from rest_framework.parsers import JSONParser

from common_core.case import keys_to_snake_case

__all__ = ["CamelCaseJSONParser"]


class CamelCaseJSONParser(JSONParser):
    """
    Accept camelCase JSON from clients, convert keys to snake_case for DRF/Django.
    """

    def parse(self, stream, media_type=None, parser_context=None):
        data = super().parse(stream, media_type=media_type, parser_context=parser_context)
        return keys_to_snake_case(data)

