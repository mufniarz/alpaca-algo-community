from ..data.data import Data
from .algo1 import AlgoOne
import alpaca_trade_api as tradeapi
import time

api = tradeapi.REST()
# api = tradeapi.REST('<key_id>', '<secret_key>')

def main():
    data = Data(api)
    algo = AlgoOne(api)
    while True:
        try:
            if(data.clock != None and data.orders != None):
                # Prepare Candidate stocks to trade.
                if(data.clock.beforeMarketOpen(minute=15)):
                    print('Executing get_and_filter_candidate_stocks')
                    data.candidates = algo.get_and_filter_candidate_stocks(data)
                    time.sleep(120)
                # Buy and Sell Stocks
                if(
                    data.clock.afterMarketOpen(minute=1) or
                    data.clock.afterMarketOpen(hour=1, minute=1) or
                    data.clock.afterMarketOpen(hour=2, minute=1) or
                    data.clock.afterMarketOpen(hour=3, minute=1) or
                    data.clock.afterMarketOpen(hour=4, minute=1) or
                    data.clock.afterMarketOpen(hour=5, minute=1) or
                    data.clock.afterMarketOpen(hour=6, minute=1)
                ):
                    print('Executing trade_stocks')
                    algo.trade_stocks(data)
                    time.sleep(120)
                    
                if(data.clock.beforeMarketClose(minute=10)):
                    print('Executing close_specifics')
                    algo.update_data(data)

                if(data.clock.afterMarketClose(minute=30)):
                    print('Executing close_specifics')
                    algo.close_specifics(data)

        except Exception as exc:
            print('Exception: {}'.format(exc))


