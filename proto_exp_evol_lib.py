from plotly.subplots import make_subplots
import plotly.graph_objects as go
from ta.trend import SMAIndicator
import yfinance as yf
import pandas as pd
import json

import numpy as np

class finance_manager:
    def __init__(self) -> None:
        self.data = {}

    def get_data(self,company_id,meashure,_start_period,_end_period):
        self.data[company_id]=yf.download(company_id,interval=meashure,start=_start_period,end=_end_period)
        self.data[company_id] = self.data[company_id].fillna(method='bfill')
        self.data[company_id] = self.data[company_id].fillna(method='ffill')

    def print_data(self,company_id,*param):
        temp_df = self.data[company_id].copy()
        fig = go.Figure()
        for item in param:
            if("position" in item):
                fig.add_trace(go.Scatter(x=temp_df.index,y=temp_df[item],name=item))
            elif("ret_acum" in item):
                fig.add_trace(go.Scatter(x=temp_df.index,y=temp_df[item],name=item))
            else:
                fig.add_trace(go.Scatter(x=temp_df.index,y=temp_df[item],name=item))
                
        fig.show()

class khalman_signal_filter:
    def __init__(self,new_info=0.5,old_info=0.5):
        self.new_info = new_info
        self.old_info = old_info

    def filter(self,Data:pd.DataFrame):
        temp_vector = []
        self.y_n=Data[0]
        self.y_n1=Data[0]
        for x_0 in Data:
            temp_val = self.y_n
            self.y_n = self.new_info*x_0 + self.old_info*self.y_n1
            self.y_n1 = temp_val
            temp_vector.append(self.y_n)
        return temp_vector

class exponential_signal_filter:
    def __init__(self,_a=0.5):
        self.a = _a

    def filter(self,Data:pd.DataFrame):
        temp_vector = []
        self.y_n=Data[0]
        self.y_n1=Data[0]
        for x_n in Data:
            temp_val = self.y_n
            self.y_n = self.a*self.y_n1+(1-self.a)*x_n
            self.y_n1 = temp_val
            temp_vector.append(self.y_n)
        return temp_vector

class Dexponential_signal_filter:#doble
    def __init__(self,_a=0.5,_b=0.5):
        self.a = _a
        self.b = _b

    def filter(self,Data:pd.DataFrame):
        temp_vector = []
        self.y_n=Data[0]
        self.s_n=Data[0]
        self.t_n=1
        for x_n in Data:
            s_n1 = self.s_n
            t_n1 = self.t_n
            self.s_n = self.a*x_n+(1-self.a)*(s_n1+t_n1)
            self.t_n = self.b*(self.s_n-s_n1)+(1-self.b)*t_n1
            self.y_n = self.s_n+self.t_n
            temp_vector.append(self.y_n)
        return temp_vector
    def reset(self):
        self.y_n=1
        self.s_n=1
        self.t_n=1

class Texponential_signal_filter:#triple
    def __init__(self,_a=0.5,_b=0.5,_c=0.5):
        self.a = _a
        self.b = _b
        self.c = _c

    def filter(self,Data:pd.DataFrame):
        temp_vector = []
        self.y_n=Data[0]
        self.s_n=Data[0]
        self.t_n=1
        self.p_n=1
        for x_n in Data:
            s_n1 = self.s_n
            t_n1 = self.t_n
            p_n1 = self.p_n
            self.s_n = self.a*(x_n-p_n1)+(1-self.a)*(s_n1+t_n1)
            self.t_n = self.b*(self.s_n-s_n1)+(1-self.b)*t_n1
            self.p_n = self.c*(x_n-self.s_n)+(1-self.c)*p_n1
            self.y_n = self.s_n+self.t_n+self.p_n
            temp_vector.append(self.y_n)
        return temp_vector

def function_retard(data,index):
    return data.shift(index)

def get_position(x_low,x_high):
    temp_vector=[]
    for index in range(len(x_low)):
        if x_low[index]>x_high[index]:
            temp_vector.append(1)
        else:
            temp_vector.append(0)
    return temp_vector