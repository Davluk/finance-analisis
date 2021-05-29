import pandas_datareader as pd_web

assets = ["TSLA"]
data = pd_web.DataReader(assets,data_source= 'yahoo',start='2015-01-01',end='2021-01-01')