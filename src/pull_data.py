#Builds a local database of stock prices according to some parameterized time interval


from typing import Type
from yahooquery import Ticker
import pandas as pd
import datetime as dt
from date_utils import *

try:
    symbolfile = pd.read_csv("nasdaq-symbols.csv")
except:
    pass

#Takes a ticker and a parameterized time interval as input
#Returns a pandas series of its closing prices throughout the maximal elapsed time
#Elapsed time is hard coded for now for one minute price intervals
start_date_functions = {"1m": one_work_week_ago, "1h": one_month_ago, "1d": five_years_ago, "1wk": five_years_ago}
def close_prices(ticker, start_date=None, end_date=None, interval="1d"):
    
    start_date, end_date = default_start_end(start_date, end_date, interval)

    def print_no_data_found():
        print("No data found for %s" % ticker.symbols)

    try:
        history = ticker.history(start=start_date, end=end_date, interval=interval, adj_ohlc=True)
        if type(history) == pd.DataFrame:
            return history
        else:
            print_no_data_found()
    except KeyError:
        print_no_data_found()
        return None
    except TypeError:
        print_no_data_found()
        return None

def build_database():
    for symbol, name in symbolfile.values.tolist():

        try:
            ticker = Ticker(symbol)
            close_prices(ticker).to_csv("data/" + symbol)
        except AttributeError:
            #In case a stock doesn't have one week of minute-by-minute data, skip it
            continue
        except TypeError:
            continue
        