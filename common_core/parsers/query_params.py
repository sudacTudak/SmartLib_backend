__all__ = ['QueryParamsParser']

class QueryParamsParser:
    _valid_str_false_values = ('False', 'false', '0',)
    _valid_str_true_values = ('True', 'true', '1',)

    @classmethod
    def str_int_to_int(cls, param: str):
        if not isinstance(param, str):
            raise ValueError(f'Can`t parse {param} from string-int to int: Not string')

        try:
            int_value = int(param)
        except ValueError:
            raise ValueError(f'Can`t parse {param} from string-int to int: Not string-int')

        return int_value

    @classmethod
    def str_bool_to_bool(cls, param: str | bool):

        if isinstance(param, bool):
            return param

        if not isinstance(param, str):
            raise ValueError(f'Can`t parse {param} from string-bool to bool: Not string')

        if param in cls._valid_str_false_values:
            return False

        if param in cls._valid_str_true_values:
            return True

        raise ValueError(f'Can`t parse ${param} from string-bool to bool: Invalid string value')




