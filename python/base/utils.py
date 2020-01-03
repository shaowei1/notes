
from datetime import datetime as dt
import typing

def to_iso_date(date: dt.date) -> str:
    return dt.date.isoformat(date)


def ensure_text_type(val: typing.Union[str, bytes]) -> str:
    if isinstance(val, bytes):
        val = val.decode("utf-8")
    return str(val)

def pluck(dictlist: typing.List[typing.Dict[str, typing.Any]], key: str):
    """Extracts a list of dictionary values from a list of dictionaries.
    ::

        >>> dlist = [{'id': 1, 'name': 'foo'}, {'id': 2, 'name': 'bar'}]
        >>> pluck(dlist, 'id')
        [1, 2]
    """
    return [d[key] for d in dictlist]
