import pandas as pd

class Strat():

    def __init__(self) -> None:
        pass

    # Finds the last signal in the signals list
    # Defaults to selling position if there is no signal
    # No error is thrown if there is no position to start with
    def findLastSignal(self,signals) -> int:
        signals.reverse()
        for i in signals:
            if i != 0:
                return i
        return -1

    def findFirstBuyIndex(self, signals) -> int:
        for i in range(signals.shape[0]):
            if signals.iloc[i] == 1:
                return i

    # Calculates the profit multiplier given a dataframe appended with the appropriate signals
    def calcStrategyProfits(self, data: pd.DataFrame, trades: pd.DataFrame) -> float:
        firstBuyIndex = self.findFirstBuyIndex(trades['signal'])
        if firstBuyIndex == None:
            return 1
            
        profit = 1
        
        for i in range(firstBuyIndex,trades.shape[0] - 1,2):
            profit = profit*( trades.iloc[i+1,4]/trades.iloc[i,4] - 0.001*(1 + trades.iloc[i+1,4]/trades.iloc[i,4]) )
        if trades.shape[0] % 2 == 1:
            profit = profit*( data.iloc[-1,4]/trades.iloc[-1,4] - 0.001*(1 + data.iloc[-1,4]/trades.iloc[-1,4]) )
        return profit
