# coding:utf-8

# 格式化时间
from datetime import datetime, timedelta


def get_strf_time(days=0, weeks=0, hours=0, minutes=0, seconds=0, milliseconds=0, microseconds=0,
                  strf='%Y-%m-%d %H:%M:%S'):
    strf_time = (datetime.now() + timedelta(days=days, seconds=seconds, microseconds=microseconds,
                                            milliseconds=milliseconds,
                                            minutes=minutes, hours=hours, weeks=weeks)).strftime(strf)
    return str(strf_time)
