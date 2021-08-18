import SMAstrat
import pandas as pd

def f(x,*args) -> float:
    SMA_SHORTWINDOW, SMA_RATIO = x
    data = pd.DataFrame(args[0])
    strat = SMAstrat.SMAstrat(data, SMA_SHORTWINDOW,SMA_RATIO)
    return -(strat.profits)