# import concurrent.futures
import logging
import math
import numpy
import pandas as pd
import time
import datetime

class Filter(object):
    
    def __init__(self, api):
        """Return a new Filter object."""
        self.api = api
    
    def getAlpacaAssetsWith(self, alpaca_assets=[], attribute_name=None, attribute_value=None):
        assets = []
        for asset in alpaca_assets:
            attr = getattr(asset, attribute_name)
            if(attr == attribute_value):
                print(asset)
                assets.append(asset)
        return assets


    def crossReferenceAlpacaPolygonData(self, data=None):
        '''
        Compares alpaca and polygon data.  Filters out stocks that alpaca doesn't support.
        '''
        new_asset_list = []
        if(data != None):
            for asset in data.assets:
                for polygon in data.polygon_symbols:
                    if(asset.symbol == polygon.symbol):
                        new_asset_list.append(asset)
                        break
        return new_asset_list


    #DONE: At least a certain price
    def filterPriceRange(self, assets=None, min_price=None, max_price=None):
        '''
        Queries the prices for each stock and only keeps stocks within a specific range.
        '''
        new_assets = []
        if(assets != None and min_price != None and max_price != None):
            for asset in assets:
                try:
                    # trade = self.api.polygon.last_trade(asset.symbol)
                    PH = self.api.polygon.historic_agg(
                        size='day',
                        symbol=asset.symbol,
                        _from=(datetime.date.today() - datetime.timedelta(days=5)),
                        to=datetime.date.today(),
                        limit=5)
                    if(len(PH) > 0):
                        # Yesterday's Closing Price
                        lastTradePrice = float(PH[-1:][0].close)
                        # lastTradePrice = getattr(trade, 'price')

                        if(lastTradePrice >= min_price and lastTradePrice <= max_price):
                            new_assets.append(asset)
                        
                except Exception as exc:
                    logging.warning('{} generated an exception: {}'.format( asset.symbol, exc))
                
        return new_assets


    def filterSMA(self, assets=None):
        new_assets = []
        percent_difference = 0
        for asset in assets:
            agg = self.api.polygon.historic_agg(
                size='day',
                symbol=asset.symbol,
                _from=(datetime.date.today() - datetime.timedelta(days=100)),
                to=datetime.date.today(),
                limit=100)

            # Short close price average.
            ShortAvg = self.getSimpleMovingAverage(agg, days=3)

            # Long close price average.
            LongAvg = self.getSimpleMovingAverage(agg, days=45)

            if(ShortAvg != 0 and LongAvg != 0):
                percent_difference = ((ShortAvg - LongAvg) / LongAvg) * 100
                if(percent_difference >= 6 and percent_difference <= 40):
                    new_assets.append(asset)

        return new_assets


    def getSimpleMovingAverage(self, values=None, days=3):
        """
        Compute simple moving average.
        """
        average = 0
        try:
            for aggregate in values[-days:]:
                average = aggregate.close + average
            average = average / days
        except Exception as exc:
            logging.warning('Exception: {}'.format(exc))
            pass
        
        return average


    #TODO: Equities with a null value in the limited_partnership Morningstar
    # fundamental field.
    #TODO: Check Data Against MorningStar Data
    #TODO: Equities whose most recent Morningstar market cap is not null have
    # fundamental data and therefore are not ETFs.
    #TODO: Not when-issued equities.
    #TODO: Equities without LP in their name, .matches does a match using a regular
    # expression
    # def filterStocksWithMorningStarData(symbolDataList=None):
    #     '''This function filters the data based on if the stock has a LP status or .WI
    #     However, this filter is not acturate for this data and NEEDS enhancing.
    #     '''
    #     filteredSymbolList = symbolDataList
    #     for symbol in symbolDataList['symbols']:
    #         if('.* L[. ]?P.?$' in symbol['name'] or symbol['symbol'].endswith('.WI')):
    #             filteredSymbolList.remove(symbol)
        
    #     return filteredSymbolList
    #     #not_lp_name = ~morningstar.company_reference.standard_name.latest.matches('.* L[. ]?P.?$')
    #     #not_wi = ~morningstar.share_class_reference.symbol.latest.endswith('.WI')

