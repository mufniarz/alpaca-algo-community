# import datetime
import pandas as pd

class Account(object):
    '''
    The accounts API serves important account related information for a given API key, 
    including account status, funds available for trade, funds available for withdrawal, 
    and various flags relevant to an account's ability to trade. 
    An account maybe be blocked for just for trades (trades_blocked flag) or 
    for both trades and transfers (account_blocked flag) if Alpaca identifies the account to 
    engaging in any suspicious activity. Also, in accordance with FINRA's pattern day trading rule, 
    an account may be flagged for pattern day trading (pattern_day_trader flag), 
    which would inhibit an account from placing any further day-trades.
    '''
    def __init__(
        self,
        account_blocked,
        buying_power,
        cash,
        created_at,
        currency,
        daytrade_count,
        daytrading_buying_power,
        equity,
        id,
        initial_margin,
        last_equity,
        last_maintenance_margin,
        long_market_value,
        maintenance_margin,
        multiplier,
        pattern_day_trader,
        portfolio_value,
        regt_buying_power,
        short_market_value,
        shorting_enabled,
        sma,
        status,
        trade_suspended_by_user,
        trading_blocked,
        transfers_blocked):
        """Return a new Account object."""
        self.account_blocked = account_blocked
        self.buying_power = buying_power
        self.cash = cash
        self.created_at = created_at
        self.currency = currency
        self.daytrade_count = daytrade_count
        self.daytrading_buying_power = daytrading_buying_power
        self.equity = equity
        self.id = id
        self.initial_margin = initial_margin
        self.last_equity = last_equity
        self.last_maintenance_margin = last_maintenance_margin
        self.long_market_value = long_market_value
        self.maintenance_margin = maintenance_margin
        self.multiplier = multiplier
        self.pattern_day_trader = pattern_day_trader
        self.portfolio_value = portfolio_value
        self.regt_buying_power = regt_buying_power
        self.short_market_value = short_market_value
        self.shorting_enabled = shorting_enabled
        self.sma = sma
        self.status = status
        self.trade_suspended_by_user = trade_suspended_by_user
        self.trading_blocked = trading_blocked
        self.transfers_blocked = transfers_blocked


    def canDayTrade(self):
        '''Checks to see if account can day trade.'''
        if(float(self.portfolio_value) > 25000.00):
            return True
        return False


    def __str__(self):
        # Override to print a readable string presentation of your object
        # below is a dynamic way of doing this without explicity constructing the string manually
        return ', '.join(['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])


class Asset(object):
    '''
    The assets API serves as the master list of assets available for trade and data consumption from Alpaca. 
    Assets are sorted by asset class, exchange and symbol. Some assets are only available for data consumption via 
    Polygon, and are not tradable with Alpaca. These assets will be marked with the flag tradable=false.
    '''
    def __init__(
        self, 
        id,
        asset_class,
        exchange,
        symbol,
        status,
        tradable,
        marginable,
        shortable,
        easy_to_borrow):
        """Return a new Asset object."""
        self.id = id
        self.asset_class = asset_class
        self.exchange = exchange
        self.symbol = symbol
        self.status = status
        self.tradable = tradable
        self.marginable = marginable
        self.shortable = shortable
        self.easy_to_borrow = easy_to_borrow


    def __str__(self):
        # Override to print a readable string presentation of your object
        # below is a dynamic way of doing this without explicity constructing the string manually
        return ', '.join(['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])


class Calendar(object):
    '''
    The calendar API serves the full list of market days from 1970 to 2029. 
    It can also be queried by specifying a start and/or end time to narrow down the results. 
    In addition to the dates, the response also contains the specific open and close times for the market days, 
    taking into account early closures.
    '''

    def __init__(self, date, _open, close):
        """Return a new Calendar object."""
        self.date = date
        self._open = _open
        self.close = close


    def __str__(self):
        # Override to print a readable string presentation of your object
        # below is a dynamic way of doing this without explicity constructing the string manually
        return ', '.join(['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])


class Clock(object):
    '''
    The clock API serves the current market timestamp, whether or not the market is currently open, 
    as well as the times of the next market open and close.
    '''

    def __init__(
        self, 
        timestamp,
        is_open,
        next_open,
        next_close):
        """Return a new Clock object."""
        self.timestamp = timestamp
        self.is_open = is_open
        self.next_open = next_open
        self.next_close = next_close
        
    def afterMarketClose(self, timezone='America/New_York', hour=0, minute=0, second=0):
        now = pd.Timestamp.now(tz=timezone)
        nextClose = self.next_close
        if( now.day == nextClose.day and
            now.hour == nextClose.hour + hour and 
            now.minute == nextClose.minute + minute and 
            now.second == nextClose.second + second):
            return True
        return False
        
    def afterMarketOpen(self, timezone='America/New_York', hour=0, minute=0, second=0):
        now = pd.Timestamp.now(tz=timezone)
        nextOpen = self.next_open
        if( now.day == nextOpen.day and
            now.hour == nextOpen.hour + hour and 
            now.minute == nextOpen.minute + minute and 
            now.second == nextOpen.second + second):
            return True
        return False
    
    def duringMarketHoursRunPerMinute(self, timezone='America/New_York', second=1):
        now = pd.Timestamp.now(tz=timezone)
        nextOpen = self.next_open
        nextClose = self.next_close
        if( now.day == nextOpen.day and
            now.hour >= nextOpen.hour and
            now.hour <= nextClose.hour and
            now.second == second):
            if ((nextClose.hour == now.hour and
                nextClose.minute < now.minute) or
                (nextOpen.hour == now.hour and
                nextOpen.minute > now.minute)):
                return False
            if ((nextClose.hour == now.hour and
                nextClose.minute == now.minute and
                nextClose.second < second) or
                (nextOpen.hour == now.hour and
                nextOpen.minute == now.minute and
                nextOpen.second > second)):
                return False
            return True
        return False
    
    def duringMarketHoursRunPerHour(self, timezone='America/New_York', minute=1, second=1):
        now = pd.Timestamp.now(tz=timezone)
        nextOpen = self.next_open
        nextClose = self.next_close
        if( now.day == nextOpen.day and
            now.hour >= nextOpen.hour and
            now.hour <= nextClose.hour and
            now.minute == minute and
            now.second == second):
            if ((nextClose.hour == now.hour and
                nextClose.minute < now.minute) or
                (nextOpen.hour == now.hour and
                nextOpen.minute > now.minute)):
                return False
            return True
        return False
        
    def beforeMarketClose(self, timezone='America/New_York', hour=0, minute=0, second=0):
        now = pd.Timestamp.now(tz=timezone)
        nextClose = self.next_close
        if( now.day == nextClose.day and
            now.hour == nextClose.hour - hour and 
            now.minute == nextClose.minute - minute and 
            now.second == nextClose.second - second):
            return True
        return False
        
    def beforeMarketOpen(self, timezone='America/New_York', hour=0, minute=0, second=0):
        now = pd.Timestamp.now(tz=timezone)
        nextOpen = self.next_open
        if( now.day == nextOpen.day and
            now.hour == nextOpen.hour - hour and 
            now.minute == nextOpen.minute - minute and 
            now.second == nextOpen.second - second):
            return True
        return False
        
    def testHours(self, timezone='America/New_York', hour=0, minute=0, second=0):
        now = pd.Timestamp.now(tz=timezone)
        if( now.hour == now.hour - hour and 
            now.minute == now.minute - minute and 
            now.second == now.second - second):
            print('run ')
            return True
        print('done')
        return False


    def __str__(self):
        # Override to print a readable string presentation of your object
        # below is a dynamic way of doing this without explicity constructing the string manually
        return ', '.join(['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])


class Order(object):
    '''
    An order executed through Alpaca can experience several status changes during its lifecycle. 
    These most common statuses are described in detail below:

    new
    The order has been received by Alpaca, and routed to exchanges for execution. 
    This is the usual initial state of an order.
    partially_filled
    The order has been partially filled.
    filled
    The order has been filled, and no further updates will occur for the order.
    done_for_day
    The order is done executing for the day, and will not receive further updates until the next trading day.
    canceled
    The order has been canceled, and no further updates will occur for the order. 
    This can be either due to a cancel request by the user, or the order has been canceled by 
    the exchanges due to its time-in-force.
    expired
    The order has expired, and no further updates will occur for the order.
    Less common states are described below. Note that these states only occur on very rare occasions, 
    and most users will likely never see their orders reach these states:

    accepted
    The order has been received by Alpaca, but hasn't yet been routed to exchanges. 
    This state only occurs on rare occasions.
    pending_new
    The order has been received by Alpaca, and routed to the exchanges, but has not yet been accepted for execution. 
    This state only occurs on rare occasions.
    accepted_for_bidding
    The order has been received by exchanges, and is evaluated for pricing. This state only occurs on rare occasions.
    pending_cancel
    The order is waiting to be canceled. This state only occurs on rare occasions.
    stopped
    The order has been stopped, and a trade is guaranteed for the order, usually at a stated price or better, 
    but has not yet occurred. This state only occurs on rare occasions.
    rejected
    The order has been rejected, and no further updates will occur for the order. This state occurs on rare occasions, 
    and may occur based on various conditions decided by the exchanges.
    suspended
    The order has been suspended, and is not eligible for trading. This state only occurs on rare occasions.
    calculated
    The order has been completed for the day (either filled or done for day), 
    but remaining settlement calcuations are still pending. This state only occurs on rare occasions.
    An order may be canceled through the API up until the point it reaches a state of either filled, canceled, or expired.
    '''

    def __init__(
        self,
        id,
        client_order_id,
        created_at,
        updated_at,
        submitted_at,
        filled_at,
        expired_at,
        canceled_at,
        failed_at,
        asset_id,
        symbol,
        asset_class,
        qty,
        filled_qty,
        _type,
        side,
        time_in_force,
        limit_price,
        stop_price,
        filled_avg_price,
        status,
        extended_hours,
        api):
        """Return a new Order object."""
        self.id = id
        self.client_order_id = client_order_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.submitted_at = submitted_at
        self.filled_at = filled_at
        self.expired_at = expired_at
        self.canceled_at = canceled_at
        self.failed_at = failed_at
        self.asset_id = asset_id
        self.symbol = symbol
        self.asset_class = asset_class
        self.qty = qty
        self.filled_qty = filled_qty
        self._type = _type
        self.side = side
        self.time_in_force = time_in_force
        self.limit_price = limit_price
        self.stop_price = stop_price
        self.filled_avg_price = filled_avg_price
        self.status = status
        self.extended_hours = extended_hours
        self.api = api


    def cancelOrder(self):
        if(self.status == 'open' or self.status == 'partially_filled'):
            self.api.cancel_order(order_id=self.id)

    def __str__(self):
        # Override to print a readable string presentation of your object
        # below is a dynamic way of doing this without explicity constructing the string manually
        return ', '.join(['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])


class Position(object):
    '''
    The positions API provides information about an account's current open positions. 
    The response will include information such as cost basis, shares traded, and market value, 
    which will be updated live as price information is updated. Once a position is closed, 
    it will no longer be queryable through this API.
    '''
    def __init__(
        self,
        asset_id,
        symbol,
        exchange,
        asset_class,
        avg_entry_price,
        qty,
        side,
        market_value,
        cost_basis,
        unrealized_pl,
        unrealized_plpc,
        unrealized_intraday_pl,
        unrealized_intraday_plpc,
        current_price,
        lastday_price,
        change_today,
        age):
        """Return a new Position object."""
        self.asset_id = asset_id
        self.symbol = symbol
        self.exchange = exchange
        self.asset_class = asset_class
        self.avg_entry_price = avg_entry_price
        self.qty = qty
        self.side = side
        self.market_value = market_value
        self.cost_basis = cost_basis
        self.unrealized_pl = unrealized_pl
        self.unrealized_plpc = unrealized_plpc
        self.unrealized_intraday_pl = unrealized_intraday_pl
        self.unrealized_intraday_plpc = unrealized_intraday_plpc
        self.current_price = current_price
        self.lastday_price = lastday_price
        self.change_today = change_today
        self.age = age


    def canSellStockShares(self, orders=[], canDayTrade=False):
        '''
        Passes in a list of exectured orders.  Checks to see if the current symbol has a filled or partially_filled order already. 
        If account cannot day trade and criteria is met, the stock cannot be sold today.
        Returns False or True.
        '''
        if(canDayTrade == False):
            for order in orders:
                if(self.symbol==order.symbol and (order.status=='filled' or order.status=='partially_filled')):
                    return False
            return True
        return True


    def __str__(self):
        # Override to print a readable string presentation of your object
        # below is a dynamic way of doing this without explicity constructing the string manually
        return ', '.join(['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])
