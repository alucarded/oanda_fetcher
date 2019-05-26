# -*- coding: utf-8 -*-
"""
The MIT License (MIT)

Copyright (c) 2014 OANDA Corporation

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from datetime import datetime

class CandlePrinter(object):
    def __init__(self):
        self.width = {
            'time' : 19,
            'type' : 4,
            'price' : 8,
            'volume' : 6,
        }
        # setattr(self.width, "time", 19)
        self.time_width = 19

    def print_header(self):
        print("{:<{width[time]}} {:<{width[type]}} {:<{width[price]}} {:<{width[price]}} {:<{width[price]}} {:<{width[price]}} {:<{width[volume]}}".format(
            "Time",
            "Type",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            width=self.width
        ))

        print("{} {} {} {} {} {} {}".format(
            "=" * self.width['time'],
            "=" * self.width['type'],
            "=" * self.width['price'],
            "=" * self.width['price'],
            "=" * self.width['price'],
            "=" * self.width['price'],
            "=" * self.width['volume']
        ))
        
    def print_candle(self, candle):
        try:
            time = str(
                datetime.strptime(
                    candle.time,
                    "%Y-%m-%dT%H:%M:%S.000000000Z"
                )
            )
        except:
            time = candle.time.split(".")[0]

        volume = candle.volume

        for price in ["mid", "bid", "ask"]:
            c = getattr(candle, price, None)

            if c is None:
                continue

            print("{:>{width[time]}} {:>{width[type]}} {:>{width[price]}} {:>{width[price]}} {:>{width[price]}} {:>{width[price]}} {:>{width[volume]}}".format(
                time,
                price,
                c.o,
                c.h,
                c.l,
                c.c,
                volume,
                width=self.width
            ))

            volume = ""
            time = ""