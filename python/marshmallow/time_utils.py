import uuid
import time
import datetime
from binascii import crc32
from typing import Iterable
from marshmallow import fields
import pytz
from werkzeug.datastructures import ImmutableMultiDict


class TimeCased(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        shanghai = pytz.timezone("Asia/Shanghai")
        return pytz.utc.localize(value).astimezone(shanghai).strftime('%Y-%m-%d %H:%M:%S')

    def _deserialize(self, value, attr, data, **kwargs):
        return value


def create_uuid_and_crc32():
    uuid_ = str(uuid.uuid4())
    uuid_crc32 = crc32(uuid_.encode())
    return uuid_, uuid_crc32


def get_crc32(string):
    return crc32(string.encode())


def localtime_to_utctime(localtime: datetime) -> datetime:
    timestamp = time.mktime(localtime.timetuple())
    utc_datetime = datetime.utcfromtimestamp(timestamp)
    return utc_datetime


def utctime_to_localtime(utctime: datetime) -> datetime:
    shanghai = pytz.timezone("Asia/Shanghai")
    return pytz.utc.localize(utctime).astimezone(shanghai)


def pagination_slice(list_, page, page_size):
    start = (page - 1) * page_size
    return list_[start: start + page_size]


def drop_duplicates(iterator: Iterable) -> list:
    return list(set(iterator))


def delete_empty_data(data):
    new_args = dict()
    for key, value in data.items():
        if key not in ["", None] and value not in ["", None]:
            new_args[key] = value
    return ImmutableMultiDict(
        list(
            zip(
                new_args.keys(),
                new_args.values()
            )
        )
    )


def string_to_list(ids: str):
    if ids is not None:
        ids = ids.split(",")
        ids = list(map(lambda id_: int(id_), ids))
        return ids
    return None


def expire_time(expire_in):
    shanghai = pytz.timezone("Asia/Shanghai")
    cos_policy_expiration = pytz.utc.localize(datetime.datetime.now().replace(
        microsecond=0) + datetime.timedelta(
        seconds=expire_in)).astimezone(shanghai).strftime('%Y-%m-%dT%H:%M:%S')
    return cos_policy_expiration
