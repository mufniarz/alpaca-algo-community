import concurrent.futures
import logging
import math
import numpy
import pandas as pd
import time
import datetime
import statistics

class PennyAlgo(object):
    
    def __init__(self, api):
        """Return a new PennyAlgo object."""
        self.api = api
        self.BuyFactor = .99
        self.SellFactor = 1.01
        self.NY = 'America/New_York'

    def update_data(self, data=None):
        '''Updates position age and trading clock.'''
        print('ran update_data')
        return data.requestClock()
        
    def get_and_filter_candidate_stocks(self, data=None):
        '''Filters stocks based on price'''
        print('ran get_and_filter_candidate_stocks')
        return []

    def trade_stocks(self, data=None):
        print('ran trade_stocks')
        pass

    
    def close_specifics(self, data=None):
        print('ran close_specifics')
        pass