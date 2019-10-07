from . import Account, Asset, Calendar, Clock, EarningsDate, Order, Position, PolygonSymbol, Filter
from .yahoo_earnings_calendar import YahooEarningsCalendar
import datetime
import pandas as pd


class Data(object):
    
    def __init__(self, api):
        """Return a new Data object."""
        self.api = api
        self.account = self.requestAccount()
        self.assets = self.requestAssets()
        self.calendar_dates = self.requestCalendar()
        self.candidate_stocks = []
        self.clock = self.requestClock()
        self.earnings = self.requestEarnings()
        self.filter = Filter(self.api)
        self.orders = self.requestOrders()
        self.polygon_symbols = self.requestPolygonSymbols()
        self.positions = self.requestPositions()
        self.created_at = datetime.datetime.now()


    def requestAccount(self):
        a = self.api.get_account()
        account = Account(
            a.account_blocked,
            a.buying_power,
            a.cash,
            a.created_at,
            a.currency,
            a.daytrade_count,
            a.daytrading_buying_power,
            a.equity,
            a.id,
            a.initial_margin,
            a.last_equity,
            a.last_maintenance_margin,
            a.long_market_value,
            a.maintenance_margin,
            a.multiplier,
            a.pattern_day_trader,
            a.portfolio_value,
            a.regt_buying_power,
            a.short_market_value,
            a.shorting_enabled,
            a.sma,
            a.status,
            a.trade_suspended_by_user,
            a.trading_blocked,
            a.transfers_blocked)
        return account


    def requestAssets(self, status='active', asset_class='us_equity'):
        '''
        Requests Assets data from Alpaca and returns it as a list of Asset objects.
        '''
        assets = []
        assets_json = self.api.list_assets(status=status)

        for asset in assets_json:
            assets.append(
                Asset(
                    asset.id,
                    getattr(asset, 'class'),
                    asset.exchange,
                    asset.symbol,
                    asset.status,
                    asset.tradable,
                    asset.marginable,
                    asset.shortable,
                    asset.easy_to_borrow
                )
            )
        return assets


    def requestCalendar(self, start='2018-01-01', end=None):
        '''
        Requests Dates data from Alpaca and returns it as a list of Calendar objects.
        '''
        dates = []
        calendar_json = self.api.get_calendar(start, end)
        
        for date in calendar_json:
            dates.append(
                Calendar(date.date, date.open, date.close)
            )
        return dates


    def requestClock(self):
        clock = self.api.get_clock()
        clk = Clock(
            clock.timestamp,
            clock.is_open,
            clock.next_open,
            clock.next_close)
        return clk
    
    def requestEarnings(self, next_market_close=None):
        NY = 'America/New_York'
        yec = YahooEarningsCalendar()
        now = pd.Timestamp.now(tz=NY)
        earningsDateList = []
        
        if now.dayofweek == 4:
            todate = now + datetime.timedelta(days=3)
        else:
            todate = now + datetime.timedelta(days=1)
        date_from = datetime.datetime(
            now.year, now.month, now.day, 0, 0)
        date_to = datetime.datetime(
            todate.year, todate.month, todate.day, 23, 59)
        earnings_json = yec.earnings_between(date_from, date_to)
        
        for ed in earnings_json:
            earningsDateList.append(
                EarningsDate(
                    ed['ticker'],
                    ed['companyshortname'],
                    ed['startdatetime'],
                    ed['startdatetimetype'],
                    ed['epsestimate'],
                    ed['epsactual'],
                    ed['epssurprisepct'],
                    ed['gmtOffsetMilliSeconds']
                )
            )
        
        return earningsDateList


    def requestOrders(self):
        '''
        Requests Orders data from Alpaca and returns it as a list of Order objects.
        '''
        orders = []
        orders_json = self.api.list_orders( status='all' )

        for order in orders_json:
            orders.append(
                Order(
                    order.id,
                    order.client_order_id,
                    order.created_at,
                    order.updated_at,
                    order.submitted_at,
                    order.filled_at,
                    order.expired_at,
                    order.canceled_at,
                    order.failed_at,
                    order.asset_id,
                    order.symbol,
                    order.asset_class,
                    order.qty,
                    order.filled_qty,
                    order.type,
                    order.side,
                    order.time_in_force,
                    order.limit_price,
                    order.stop_price,
                    order.filled_avg_price,
                    order.status,
                    order.extended_hours,
                    self.api
                )
            )
        return orders


    #DONE: Equities not trading over-the-counter.
    #DONE: Equities listed as common stock (as opposed to, say, preferred stock). 
    #     'ST00000001' indicates common stock.
    def requestPolygonSymbols(self, SORT='symbol', TYPE='cs', PER_PAGE=50, page=1, ISOTC='false'):
        '''Pulls data from Polygon on current stocks.
        Loops several time through the api get request to pull 50 records at a time 
        of common over-the-counter stocks.
        Breaks out of loop after the volumn of stock data is less than 50.
        Returns the full list of stocks.
        '''
        # 'cs' Common Stock
        # 'ISOTC' Is Over-The-Counter stock
        page=page
        polygonSymbolList = []
        partialData = None
        PATH = '/meta/symbols'
        
        while True:
            partialData = self.api.polygon.get(
                path=PATH,
                params={'sort':SORT, 
                        'type':TYPE, 
                        'perpage':PER_PAGE, 
                        'page':page, 
                        'isOTC':ISOTC})

            for partial in partialData['symbols']:
                polygonSymbolList.append(
                    PolygonSymbol(
                        partial['symbol'], 
                        partial['name'], 
                        partial['type'], 
                        partial['isOTC'], 
                        partial['updated'], 
                        partial['url'])
                )
                
            if(len(partialData['symbols']) == 50):
                page += 1
            else:
                return polygonSymbolList


    def requestPositions(self):
        '''
        Requests Positions data from Alpaca and returns it as a list of Order objects.
        '''
        positions = []
        positions_json = self.api.list_positions()

        for position in positions_json:
            positions.append(
                Position(
                    position.asset_id,
                    position.symbol,
                    position.exchange,
                    position.asset_class,
                    position.avg_entry_price,
                    position.qty,
                    position.side,
                    position.market_value,
                    position.cost_basis,
                    position.unrealized_pl,
                    position.unrealized_plpc,
                    position.unrealized_intraday_pl,
                    position.unrealized_intraday_plpc,
                    position.current_price,
                    position.lastday_price,
                    position.change_today,
                    self.setPositionAge(position.symbol)
                )
            )
        return positions


    def canTradeStock(self, symbol=None):
        '''Checks to see if an asset is tradable.'''
        for asset in self.assets:
            if(asset.symbol == symbol):
                print(asset.symbol)
                print(asset.tradable)
                if(asset.tradable == True):
                    return True
                return False
        return False


    def setPositionAge(self, symbol=None):
        if(hasattr(self, 'positions')):
            for position in self.positions:
                if(position.symbol == symbol):
                    return position.age
        return 0


    def updatePositions(self):
        new_postions = self.requestPositions()
        positions = []
        for new_position in new_postions:
            for position in self.positions:
                if(new_position.symbol == position.symbol):
                    new_position.age = position.age + 1
                    positions.append(new_position)
                    break
        return positions


    def __str__(self):
        # Override to print a readable string presentation of your object
        # below is a dynamic way of doing this without explicity constructing the string manually
        return ', '.join(['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])

