# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 10:39:02 2019

@author: Tomasz Posluszny <tefposluszny at gmail dot com>
"""

import v20
import datetime
import logging
import pandas as pd

from .oanda_view import CandlePrinter
from .ohlcv_fetcher import OhlcvFetcher

class OandaFetcher(OhlcvFetcher):
    RFC3339_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.000000000Z";
    
    def __init__(self,
                 hostname = "api-fxpractice.oanda.com",
                 port = 443,
                 authtoken =  "xxx-xxx",
                 datetime_format = "RFC3339"):
        """
        Initialize a streaming API context
        """
        self.ctx = v20.Context(
            hostname,
            port,
            True,
            application = "sample_code",
            token = authtoken,
            datetime_format = datetime_format
        )
        
        self.granularity_to_delta = {
                'D' : datetime.timedelta(days = 1),
                'H1': datetime.timedelta(hours = 1)
                }

    def fetch(self, **kwargs):
        
        name = kwargs['name']
        #name = kwargs.pop('name', None)
        if not name:
            raise ValueError("\'name\' is required")

        if not 'price' in kwargs:
            logging.info('Default: midpoint')
            kwargs['price'] = 'M'
        if not 'granularity' in kwargs:
            logging.info('Default: daily candles')
            kwargs['granularity'] = 'D'
        if not 'count' in kwargs:
            kwargs['count'] = None
        if not 'fromTime' in kwargs:
            kwargs['fromTime'] = None
        if not 'toTime' in kwargs:
            kwargs['toTime'] = None
        if not 'smooth' in kwargs:
            kwargs['smooth'] = 'false'
        if not 'includeFirst' in kwargs:
            kwargs['includeFirst'] = 'true'
        if not 'dailyAlignment' in kwargs:
            logging.info('Default: daily alignment is 21')
            kwargs['dailyAlignment'] = 21
        if not 'alignmentTimezone' in kwargs:
            logging.info('Default: alignment timezone is Etc/GMT')
            kwargs['alignmentTimezone'] = 'Etc/GMT'
        if not 'weeklyAlignment' in kwargs:
            logging.info('Default: weekly alignment is Friday')
            kwargs['weeklyAlignment'] = 'Friday'

        response = self.ctx.instrument.candles(name, **kwargs)
        candles = response.get("candles", 200)

        return candles

    def fetch_chained(self, **kwargs):
        from_time = kwargs['fromTime']
        to_time = kwargs['toTime']
        granularity = kwargs['granularity']
        from_dt = datetime.datetime.strptime(from_time,
                                             self.RFC3339_DATETIME_FORMAT)
        to_dt = datetime.datetime.strptime(to_time,
                                           self.RFC3339_DATETIME_FORMAT)
        delta = self.granularity_to_delta[granularity]
        
        ret_candles = []
        prev_dt = from_dt
        dt = from_dt
        while dt < to_dt:
            prev_dt = dt
            dt =  min(dt + 5000 * delta, to_dt)

            logging.info("from {} to {}".format(prev_dt, dt))
            kwargs['fromTime'] = prev_dt.strftime(self.RFC3339_DATETIME_FORMAT)
            kwargs['toTime'] = dt.strftime(self.RFC3339_DATETIME_FORMAT)
            candles = self.fetch(**kwargs)
            ret_candles.extend(candles)
        
        return ret_candles

def candles_to_dicts(candles, price = "mid", date_only = False):
    open_dict = {}
    high_dict = {}
    low_dict = {}
    close_dict = {}
    volume_dict = {}
    for candle in candles:
        c = getattr(candle, price, None)
        dt = datetime.datetime.strptime(candle.time,
                                        OandaFetcher.RFC3339_DATETIME_FORMAT)
        if date_only:
            dt = dt.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        open_dict[dt] = c.o
        high_dict[dt] = c.h
        low_dict[dt] = c.l
        close_dict[dt] = c.c
        volume_dict[dt] = candle.volume

    return open_dict, high_dict, low_dict, close_dict, volume_dict

def candles_to_dataframe(candles, price = "mid"):
    dts = []
    open_values = []
    high_values = []
    low_values = []
    close_values = []
    volume_values = []
    for candle in candles:
        dt = datetime.datetime.strptime(candle.time,
                                        OandaFetcher.RFC3339_DATETIME_FORMAT)
        dts.append(dt)
        c = getattr(candle, price, None)
        open_values.append(c.o)
        high_values.append(c.h)
        low_values.append(c.l)
        close_values.append(c.c)
        volume_values.append(candle.volume)
    columns_dict = { 'Datetime': dts,\
                    'Open': open_values,\
                    'High': high_values,\
                    'Low': low_values,\
                    'Close': close_values,\
                    'Volume': volume_values }
    return pd.DataFrame(columns_dict)

if __name__ == "__main__":
    oanda = OandaFetcher()
    param_dict = {'name': 'XAU_USD',
                  'granularity': 'H1',
                 # 'fromTime' : '2015-06-25',
                 # 'toTime': '2019-05-22',
                  'count': 5000,
                  'dailyAlignment': 21,
                  'alignmentTimezone': 'Etc/GMT'}
    candles = oanda.fetch(**param_dict)
    printer = CandlePrinter()
    for candle in candles:
        printer.print_candle(candle)
    candles_to_dicts(candles)