from datetime import datetime

from strategy.strategy import Strategy


class DCA(Strategy):
    # simple DCA (dollar cost average)
    # invests monthly regardless of the market condition
    def __init__(self, budget, years: int):
        super().__init__(budget)

        self.years = years # first years to split investment
        self.remaining = budget
        self.contribution = budget / years / 12
        self.shares = []
        self.final_price = 0.0
        self.last_month = -1

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
            self.remaining = 0.0
            return

        self.shares += [self.contribution / close]
        self.remaining -= self.contribution

    def get_results(self):
        # calculate the average share price and number of total shares
        total_shares = sum(self.shares)

        portfolio_value = self.final_price * total_shares
        final_return = (portfolio_value - self.budget) / self.budget

        return portfolio_value, final_return
        