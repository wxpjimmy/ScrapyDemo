#!/usr/bin/python
#-*-coding:utf-8-*-

import redis
import time
#from scrapy import log

from scrapy.dupefilter import BaseDupeFilter
from scrapy.utils.request import request_fingerprint


class RFPDupeFilter(BaseDupeFilter):
    """Redis-based request duplication filter"""

    def __init__(self, server, key, extra_filter_keys=None, key_exist = False, key_expire=2):
        """Initialize duplication filter

        Parameters
        ----------
        server : Redis instance
        key : str
            Where to store fingerprints
        """
        self.server = server
        self.key = key
        self.extra_filter_keys = extra_filter_keys
        self.key_exist = key_exist
        self.key_expire = key_expire

    @classmethod
    def from_settings(cls, settings):
        host = settings.get('REDIS_HOST', 'localhost')
        port = settings.get('REDIS_PORT', 6379)
        server = redis.Redis(host, port)
        # create one-time key. needed to support to use this
        # class as standalone dupefilter with scrapy's default scheduler
        # if scrapy passes spider on open() method this wouldn't be needed
        key = "dupefilter:%s" % int(time.time())
        return cls(server, key)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def request_seen(self, request):
        """
            use sismember judge whether fp is duplicate.
        """
 #       log.msg("Duplicate key: %s" % self.key)
        fp = request_fingerprint(request)
        if self.key_exist:
            if self.server.sismember(self.key,fp):
                return True
            if self.extra_filter_keys is not None:
                for extra_key in self.extra_filter_keys:
                    if self.server.sismember(extra_key, fp):
                        return True
            self.server.sadd(self.key, fp)
            return False
        else:
            self.server.sadd(self.key, fp)
            self.server.expire(self.key, self.key_expire)

    def close(self, reason):
        """Delete data on close. Called by scrapy's scheduler"""
        self.clear()

    def clear(self):
        """Clears fingerprints data"""
        self.server.delete(self.key)
        if self.extra_filter_keys is not None:
            for extra_key in self.extra_filter_keys:
                self.server.delete(self.extra_key)
