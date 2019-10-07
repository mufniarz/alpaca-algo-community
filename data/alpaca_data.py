import pandas as pd

class Account(object):
    '''
    id
        string<uuid>
        Account ID.
    account_number
        string
        Account number.
    status
        string<account_status>
        See Account Status
    currency
        string
        “USD”
    cash
        string<number>
        Cash balance
    portfolio_value
        string<number>
        Total value of cash + holding positions (This field is deprecated. It is equivalent to the equity field.)
    pattern_day_trader
        boolean
        Whether or not the account has been flagged as a pattern day trader
    trade_suspended_by_user
        boolean
        User setting. If true, the account is not allowed to place orders.
    trading_blocked
        boolean
        If true, the account is not allowed to place orders.
    transfers_blocked
        boolean
        If true, the account is not allowed to request money transfers.
    account_blocked
        boolean
        If true, the account activity by user is prohibited.
    created_at
        string<timestamp>
        Timestamp this account was created at
    shorting_enabled
        boolean
        Flag to denote whether or not the account is permitted to short
    long_market_value
        string<number>
        Real-time MtM value of all long positions held in the account
    short_market_value
        string<number>
        Real-time MtM value of all short positions held in the account
    equity
        string<number>
        Cash + long_market_value + short_market_value
    last_equity
        string<number>
        Equity as of previous trading day at 16:00:00 ET
    multiplier
        string<number>
        Buying power multiplier that represents account margin classification; valid values 1 (standard limited margin account with 1x buying power), 2 (reg T margin account with 2x intraday and overnight buying power; this is the default for all non-PDT accounts with $2,000 or more equity), 4 (PDT account with 4x intraday buying power and 2x reg T overnight buying power)
    buying_power
        string<number>
        Current available $ buying power; If multiplier = 4, this is your daytrade buying power which is calculated as (last_equity - (last) maintenance_margin) * 4; If multiplier = 2, buying_power = max(equity – initial_margin,0) * 2; If multiplier = 1, buying_power = cash
    initial_margin
        string<number>
        Reg T initial margin requirement (continuously updated value)
    maintenance_margin
        string<number>
        Maintenance margin requirement (continuously updated value)
    sma
        string<number>
        Value of special memorandum account (will be used at a later date to provide additional buying_power)
    daytrade_count
        string<int>
        The current number of daytrades that have been made in the last 5 trading days (inclusive of today)
    last_maintenance_margin
        string<number>
        Your maintenance margin requirement on the previous trading day
    daytrading_buying_power
        string<number>
        Your buying power for day trades (continuously updated value)
    regt_buying_power
        string<number>
        Your buying power under Regulation T (your excess equity - equity minus margin value - times your margin multiplier)
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
        '''
        Checks to see if account can day trade.
        Needs to be updated to look at previous date's equity value.
        '''
        if(float(self.portfolio_value) > 25000.00):
            return True
        return False


    def __str__(self):
        # Override to print a readable string presentation of your object
        # below is a dynamic way of doing this without explicity constructing the string manually
        return ', '.join(['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])


class Asset(object):
    '''
    id
        string<uuid>
        Asset ID.
    class
        string
        “us_equity”
    exchange
        string
        AMEX, ARCA, BATS, NYSE, NASDAQ or NYSEARCA
    symbol
        string
    status
        string
        active or inactive
    tradable
        boolean
        Asset is tradable on Alpaca or not.
    marginable
        boolean
        Asset is marginable or not.
    shortable
        boolean
        Asset is shortable or not.
    easy_to_borrow
        boolean
        Asset is easy-to-borrow or not (filtering for easy_to_borrow = True is the best way to check whether the name is currently available to short at Alpaca).
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
    date
        string
        Date string in “%Y-%m-%d” format
    open
        string
        The time the market opens at on this date in “%H:%M” format
    close
        string
        The time the market closes at on this date in “%H:%M” format
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
    timestamp
        string<timestamp>
        Current timestamp
    is_open
        boolean
        Whether or not the market is open
    next_open
        string<timestamp
        Next market open timestamp
    next_close
        string<timestamp>
        Next market close timestamp
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
    
    '''
    afterMarketClose and afterMarketOpen these methods will not specify a day due to these dates changing if the data is pulled after market opens or closes to the next date.
    '''
    def afterMarketClose(self, timezone='America/New_York', hour=0, minute=0, second=0):
        now = pd.Timestamp.now(tz=timezone)
        nextClose = self.next_close
        if( now.hour == nextClose.hour + hour and 
            now.minute == nextClose.minute + minute and 
            now.second == nextClose.second + second):
            return True
        return False
        
    def afterMarketOpen(self, timezone='America/New_York', hour=0, minute=0, second=0):
        now = pd.Timestamp.now(tz=timezone)
        nextOpen = self.next_open
        if( now.hour == nextOpen.hour + hour and 
            now.minute == nextOpen.minute + minute and 
            now.second == nextOpen.second + second):
            return True
        return False
    
    def duringMarketHoursRunPerMinute(self, timezone='America/New_York', second=1):
        now = pd.Timestamp.now(tz=timezone)
        nextOpen = self.next_open
        nextClose = self.next_close
        if( now.hour >= nextOpen.hour and
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
        if( now.hour >= nextOpen.hour and
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
    id
        string<uuid>
        order id
    client_order_id
        string
        client unique order id
    created_at
        string<timestamp>
    updated_at
        string<timestamp> (Nullable)
    submitted_at
        string<timestamp> (Nullable)
    filled_at
        string<timestamp> (Nullable)
    expired_at
        string<timestamp> (Nullable)
    canceled_at
        string<timestamp> (Nullable)
    asset_id
        string<uuid>
        asset ID
    symbol
        string
        Asset symbol
    asset_class
        string
        Asset class
    qty
        string<number>
        Ordered quantity
    filled_qty
        string<number>
        Filled quantity
    type
        string<order_type>
        Valid values: market, limit, stop, stop_limit
    side
        string<side>
        Valid values: buy, sell
    time_in_force
        string<time_in_force>
        See Orders page
    limit_price
        string<number> (Nullable)
        Limit price
    stop_price
        string<number> (Nullable)
        Stop price
    status
        string<order_status>
        See Orders page
    extended_hours
        boolean
        If true, eligible for execution outside regular trading hours.
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
    asset_id
        string<uuid>
        Asset ID
    symbol
        string
        Symbol name of the asset
    exchange
        string
        Exchange name of the asset
    asset_class
        string
        Asset class name
    avg_entry_price
        string
        Average entry price of the position
    qty
        string<int>
        The number of shares
    side
        string
        “long”
    market_value
        string<number>
        Total dollar amount of the position
    cost_basis
        string<number>
        Total cost basis in dollar
    unrealized_pl
        string<number>
        Unrealized profit/loss in dollars
    unrealized_plpc
        string<number>
        Unrealized profit/loss percent (by a factor of 1)
    unrealized_intraday_pl
        string<number>
        Unrealized profit/loss in dollars for the day
    unrealized_intraday_plpc
        string<number>
        Unrealized profit/loss percent (by a factor of 1)
    current_price
        string<number>
        Current asset price per share
    lastday_price
        string<number>
        Last day’s asset price per share based on the closing value of the last trading day
    change_today
        string<number>
        Percent change from last day price (by a factor of 1)
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
