#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : 无服务器缓存
# @Time         : 2023/7/3 20:10
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
os.environ['MOMENTO_AUTH_TOKEN'] = 'eyJlbmRwb2ludCI6ImNlbGwtNC11cy13ZXN0LTItMS5wcm9kLmEubW9tZW50b2hxLmNvbSIsImFwaV9rZXkiOiJleUpoYkdjaU9pSklVekkxTmlKOS5leUp6ZFdJaU9pSXpNVE16TURNek1ETkFjWEV1WTI5dElpd2lkbVZ5SWpveExDSndJam9pUTBGQlBTSjkuSVRlX01ZRnBoVTBVb1I0SkdKOU92QXZ4dUJUOHBiQnpDWWlhZjlkZFYwdyJ9'

from datetime import timedelta

from momento import CacheClient, Configurations, CredentialProvider
from momento.responses import CacheGet, CacheSet, CreateCache

cache_client = CacheClient(
    configuration=Configurations.Laptop.v1(),
    credential_provider=CredentialProvider.from_environment_variable('MOMENTO_AUTH_TOKEN'),
    default_ttl=timedelta(seconds=60)
)
cache_client.create_cache("cache")
cache_client.set("cache", "myKey", "myValue")
get_response = cache_client.get("cache", "myKey")
if isinstance(get_response, CacheGet.Hit):
    print(f"Got value: {get_response.value_string}")
