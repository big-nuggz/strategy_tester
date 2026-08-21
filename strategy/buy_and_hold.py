from datetime import datetime

from strategy.strategy import Strategy


class BuyAndHold(Strategy):
    # lump sum investing
    def __init__(self, budget):
        super().__init__(budget)
        self.traded = False
        self.buy_price = 0.0
        self.final_price = 0.0

    def __call__(
            self, 
            date: datetime, 
            open_: float, 
            high: float, 
            low: float, 
            close: float) -> None:
        if self.traded:
            self.final_price = close
            return
        
        self.traded = True
        self.buy_price = open_

    def get_results(self) -> float:
        final_return = (self.final_price - self.buy_price) / self.buy_price
        portfolio_value = self.final_price * self.budget

        return portfolio_value, final_return