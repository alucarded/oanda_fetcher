# -*- coding: utf-8 -*-
"""
Created on Wed May  8 18:46:18 2019

@author: Tomasz Posluszny <tefposluszny at gmail dot com>
"""
from typing import NamedTuple

'''
  configuration: dictionary of configuration values
  
  'name' - instrument name
'''
class OhlcvFetcher:
    def fetch(self, **kwargs):
        raise NotImplementedError