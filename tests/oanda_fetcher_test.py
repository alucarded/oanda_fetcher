# -*- coding: utf-8 -*-
"""
Created on Wed May 22 07:45:53 2019

@author: Tomasz Posluszny <tefposluszny at gmail dot com>
"""

import datetime
import pytest

from oanda_fetcher.oanda_fetcher import OandaFetcher
from oanda_fetcher import oanda_fetcher

def test_fetch_hourly_gold():
    fetcher = OandaFetcher()
    param_dict = {'name': 'XAU_USD',
                  'price': 'M',
                  'smooth': 'true',
                  'granularity': 'H1',
                  'fromTime' : '2019-04-25',
                  'toTime': '2019-05-22'
                  }
    candles = fetcher.fetch(**param_dict)
    for candle in candles:
        dt = datetime.datetime.strptime(candle.time, OandaFetcher.RFC3339_DATETIME_FORMAT)
        if dt == datetime.datetime(2019, 5, 17, hour = 20):
            assert candle.mid.o == 1278.059

@pytest.fixture
def candles():
    fetcher = OandaFetcher()
    param_dict = {'name': 'EUR_USD',
                  'price': 'M',
                  'smooth': 'true',
                  'granularity': 'D',
                  'fromTime' : '2015-04-25',
                  'toTime': '2019-05-22'
                  }
    return fetcher.fetch(**param_dict)

def test_fetch_daily_eurusd(candles):
    for candle in candles:
        dt = datetime.datetime.strptime(candle.time, OandaFetcher.RFC3339_DATETIME_FORMAT)
        if dt == datetime.datetime(2018, 5, 15):
            assert candle.mid.h == 1.19387

def test_fetch_chained():
    fetcher = OandaFetcher()
    now = datetime.datetime.utcnow().replace(minute = 0, second = 0)
    now_str = now.strftime(OandaFetcher.RFC3339_DATETIME_FORMAT)
    param_dict = {'name': 'EUR_USD',
                  'price': 'M',
                  'smooth': 'true',
                  'granularity': 'H1',
                  'fromTime' : '2005-01-03T00:00:00.000000000Z',
                  'toTime': now_str
                  }
    candles = fetcher.fetch_chained(**param_dict)
    dt = datetime.datetime.strptime(candles[0].time, OandaFetcher.RFC3339_DATETIME_FORMAT)
    dt -= datetime.timedelta(hours = 1)
    gap_count = 0
    max_gap = datetime.timedelta(0)
    for candle in candles:
        prev_dt = dt
        dt = datetime.datetime.strptime(candle.time, OandaFetcher.RFC3339_DATETIME_FORMAT)
        diff = dt - prev_dt
        assert diff % datetime.timedelta(hours = 1) == datetime.timedelta(0)
        assert diff > datetime.timedelta(0)
        if diff != datetime.timedelta(hours = 1):
            gap_count += 1
            if diff > max_gap:
                max_gap = diff
        if dt == datetime.datetime(2005, 1, 3, hour = 11):
            assert candle.mid.c == 1.3513
    print("Candles count: {},number of gaps: {}, max gap: {}".format(len(candles), gap_count, max_gap))

def test_candles_chronological(candles):
    prev_dt = datetime.datetime(1970, 1, 1)
    dt = prev_dt
    for candle in candles:
        dt = datetime.datetime.strptime(candle.time, OandaFetcher.RFC3339_DATETIME_FORMAT)
        assert dt > prev_dt
        prev_dt = dt

def test_candles_to_dataframe(candles):
    df = oanda_fetcher.candles_to_dataframe(candles)
    for i in range(0, len(candles)):
        dt = datetime.datetime.strptime(candles[i].time, OandaFetcher.RFC3339_DATETIME_FORMAT)
        assert dt == df.iloc[i, 0]
        assert candles[i].mid.o == df.iloc[i, 1]
        assert candles[i].mid.h == df.iloc[i, 2]
        assert candles[i].mid.l == df.iloc[i, 3]
        assert candles[i].mid.c == df.iloc[i, 4]
    