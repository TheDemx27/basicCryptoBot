import pandas as pd
from pandas.core.indexes import period
from Strat import Strat
import math
from finta import TA

class SMAstrat(Strat):

    def __init__(self, data: pd.DataFrame, SMA_SHORTWINDOW: float, SMA_RATIO: float):
        self.data = data
        self.currentSignal = self.calcSignal(SMA_SHORTWINDOW,SMA_RATIO)
        self.profits = Strat.calcStrategyProfits(self,self.data,self.data[self.data['signal']!=0])

    # Maps a change from (1 -> 0) => 1, and (0 -> 1) => -1
    # Mapping from data['lt'] => data['signal'], lt stands for "less than"
    # # In the domain, 1 means the short term SMA is above the long term SMA, and zero means its not
    # 1 corresponds to buying, -1 corresponds to selling
    def signal(*args):
        prev, curr = args[1]

        if (prev == 1 and curr == 0):
            return 1
        if (prev == 0 and curr == 1):
            return -1
        else: 
            return 0

    def calcSignal(self, SMA_SHORTWINDOW: float, SMA_RATIO: float) -> int:

        self.data['SMA_SHORT'] = TA.SMA(self.data, period=math.floor(SMA_SHORTWINDOW))
        self.data['SMA_LONG'] = TA.SMA(self.data, period=math.floor(SMA_SHORTWINDOW*SMA_RATIO))

        # GENERATE SIGNAL COLUMN AND EXTRACT THE LATEST SIGNAL
        self.data['lt'] = self.data['SMA_SHORT'] < self.data['SMA_LONG']
        self.data['signal'] = self.data.loc[:,'lt'].rolling(window=2).apply(self.signal)

        current_signal = self.findLastSignal(self.data['signal'].to_list())
        return current_signal
