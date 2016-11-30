######################################################################
#
# File: b2/account_info/in_memory.py
#
# Copyright 2016 Backblaze Inc. All Rights Reserved.
#
# License https://www.backblaze.com/using_b2_code.html
#
######################################################################

from .exception import MissingAccountData
from .upload_url_pool import UrlPoolAccountInfo

from functools import wraps


def _raise_missing_if_result_is_none(function):
    @wraps(function)
    def inner(*args, **kwargs):
        assert function.__name__.startswith('get_')
        result = function(*args, **kwargs)
        if result is None:
            # *magic*: assumes that it is a "get_field_name"
            raise MissingAccountData(function.__name__[4:])
        return result

    return inner


class InMemoryAccountInfo(UrlPoolAccountInfo):
    def __init__(self, *args, **kwargs):
        self.clear()
        super(InMemoryAccountInfo, self).__init__(*args, **kwargs)

    def clear(self):
        self.set_auth_data(None, None, None, None, None, None, None)
        self._buckets = {}
        return super(InMemoryAccountInfo, self).clear()

    def set_auth_data(
        self, account_id, auth_token, api_url, download_url, minimum_part_size, application_key,
        realm
    ):
        self._account_id = account_id
        self._auth_token = auth_token
        self._api_url = api_url
        self._download_url = download_url
        self._minimum_part_size = minimum_part_size
        self._application_key = application_key
        self._realm = realm

    def refresh_entire_bucket_name_cache(self, name_id_iterable):
        self._buckets = dict(name_id_iterable)

    def get_bucket_id_or_none_from_bucket_name(self, bucket_name):
        return self._buckets.get(bucket_name)

    def save_bucket(self, bucket):
        self._buckets[bucket.name] = bucket.id_

    def remove_bucket_name(self, bucket_name):
        if bucket_name in self._buckets:
            del self._buckets[bucket_name]

    @_raise_missing_if_result_is_none
    def get_account_id(self):
        return self._account_id

    @_raise_missing_if_result_is_none
    def get_account_auth_token(self):
        return self._auth_token

    @_raise_missing_if_result_is_none
    def get_api_url(self):
        return self._api_url

    @_raise_missing_if_result_is_none
    def get_application_key(self):
        return self._application_key

    @_raise_missing_if_result_is_none
    def get_download_url(self):
        return self._download_url

    @_raise_missing_if_result_is_none
    def get_minimum_part_size(self):
        return self._minimum_part_size

    @_raise_missing_if_result_is_none
    def get_realm(self):
        return self._realm
