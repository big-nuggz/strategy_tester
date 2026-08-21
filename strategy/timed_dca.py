from datetime import datetime
from collections import deque

from strategy.strategy import Strategy


class TimedDCA(Strategy):
    # DCA, but also with timing strategy combined
    # invests portion of budget monthly regardless of the market condition
    # withholds portion of budget when the market is close to (default) 52-week high
    # invests all withheld cash when the market drops to certain threshold
    def __init__(
            self, 
            budget, 
            years: int,
            dca_portion=0.5,
            threshold=0.95,
            months=12):
        super().__init__(budget)

        self.years = years # first years to split investment
        self.dca_portion = dca_portion # portion of money to always invest every month
        self.threshold = threshold # drawdown threshold to invest all cash reserve

        self.remaining = budget
        self.contribution = budget / years / 12
        self.reserve = 0.0
        self.shares = []
        self.final_price = 0.0
        self.last_month = -1
        self.prices = deque(maxlen=months)
        self.prices.append(0.0)

    def __call__(
            self, 
            date: datetime, 
            open_: float, 
            high: float, 
            low: float, 
            close: float) -> None:
        self.final_price = close

        # buy at the start of new month
        if date.month == self.last_month:
            return

        # only buy if budget is available
        if self.remaining <= 0.0:
            return

        self.last_month = date.month # update month if trade has occured

        # invest everything if remaining balance is lower than contribution value
        if self.remaining < self.contribution:
            self.shares += [self.remaining / close]
            self.shares += [self.reserve / close]
            self.remaining = 0.0
            return

        contribution = self.contribution * self.dca_portion
        self.reserve += self.contribution - contribution

        if close <= (max(self.prices) * self.threshold):
            contribution += self.reserve
            self.reserve = 0.0

        self.shares += [contribution/ close]
        self.remaining -= self.contribution

        # calculate previous high
        self.prices.append(close)

    def get_results(self):
        # calculate the average share price and number of total shares
        total_shares = sum(self.shares)

        portfolio_value = self.final_price * total_shares
        final_return = (portfolio_value - self.budget) / self.budget

        return portfolio_value, final_return
        