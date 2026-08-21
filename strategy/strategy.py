from datetime import datetime


class Strategy:
    # strategy base class
    def __init__(self, budget):
        # internal parameters
        self.budget = budget # total money allowed to spend

        pass

    def __call__(
            self, 
            date: datetime, 
            open_: float, 
            high: float, 
            low: float, 
            close: float) -> None:
        # trading loop
        # trade and update the internal state
        pass

    def get_results(self) -> tuple:
        # return the return
        portfolio_value = None
        final_return = None

        return portfolio_value, final_return