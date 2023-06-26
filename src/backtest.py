from calculations import combine_signals

import pandas as pd
import datetime as dt
from yahooquery import *
from date_utils import *
from pull_data import *
from calculations import *

def get_selection_symbols(selection, selection_size):
    return selection[selection["Rank"] <= selection_size]["Symbol"].values

async def backtest(assets, risk_free=["SHY"], periods=84, period=4, window=16, start_date = None, end_date = None, selection_size = 5, interval = "1d", ctx = None,  momentum_weight = MOMENTUM_WEIGHT, volatility_weight = VOLATILITY_WEIGHT, correlation_weight = CORRELATION_WEIGHT, atr_weight = ATR_WEIGHT, verbose = False):

    start_date, end_date = default_start_end(start_date, end_date, interval)

    end_date_iter = start_date
    start_date_iter = end_date_iter - dt.timedelta(weeks=window)
    money = 100 # split 100 dollars between the top 5 stocks chosen, at the end of this experiment, this will demonstrate % gain
    price_points = pd.DataFrame(columns={"Earnings", "Starting date", "Ending date"})

    #Main backtesting loop
    while end_date_iter < end_date:

        #Get new allocations
        selection = combine_signals(assets, start_date=start_date_iter, end_date=end_date_iter, periods=periods, drop_unmatched_corr=True, read_in_file=False, save_results=False, momentum_weight = MOMENTUM_WEIGHT, volatility_weight = VOLATILITY_WEIGHT, correlation_weight = CORRELATION_WEIGHT, atr_weight = ATR_WEIGHT)
        
        #Select just the tickers
        selection = get_selection_symbols(selection, selection_size).tolist()

        #Add risk free assets to fill in allocations when not enough stocks have positive momentum
        counter_risk_free = 0
        for i in range(selection_size - len(selection)):
            selection.append(risk_free[counter_risk_free])
            counter_risk_free = (counter_risk_free + 1) % len(risk_free)

        #Print final selection if verbose
        if verbose:
            allocations_df = pd.DataFrame(columns={"Symbol", "% Allocation"})
            for symbol in selection:
                allocations_df = allocations_df.append({"Symbol": symbol, "% Allocation": 100 / selection_size}, ignore_index=True)
            if ctx is not None:
                await ctx.send(discord_string(allocations_df))
            else:
                print(allocations_df)

        start_date_test = end_date_iter
        end_date_test = end_date_iter + dt.timedelta(weeks=period)

        #Buy stocks loop
        price_results = []
        counter_risk_free = 0
        for asset in selection:
            asset_ticker = Ticker(asset)
            prices = close_prices(asset_ticker, start_date=start_date_test, end_date=end_date_test, interval="1d")
            #add a risk free asset if no data is available
            if prices is None:
                asset_ticker = Ticker(risk_free[counter_risk_free])
                prices = close_prices(asset_ticker, start_date=start_date_test, end_date=end_date_test, interval="1d")
                selection.remove(asset)
                selection.append(risk_free[counter_risk_free])
                counter_risk_free = (counter_risk_free + 1) % len(risk_free)
            
            prices = prices.dropna()

            # calculate money made / lost, save to list
            shares_start = (money / len(selection)) / prices.iloc[0]["open"] 
            price_end = shares_start * prices.iloc[-1]["close"]
            price_results.append(price_end)

        #Count earnings / losses
        money = sum(price_results)
        price_points = price_points.append({"Earnings": money, "Starting date": start_date_test, "Ending date": end_date_test, "Start of window": start_date_iter, "End of window": end_date_iter}, ignore_index = True)
        
        #Print status and earnings
        print("Earnings: %s for %s through %s..." % (money, start_date_iter, end_date_iter))

        if ctx is not None:
            await ctx.send("Earnings: %s for %s through %s..." % (money, start_date_iter, end_date_iter))

        #Adjust window of data used to make allocations, when the loop starts again these wil lbe used
        start_date_iter = start_date_iter + dt.timedelta(weeks=period)
        end_date_iter = end_date_iter + dt.timedelta(weeks=period)

    price_points.to_csv("../outputs/earnings_backtest.csv")

    return money, selection, price_points

#assets = ["AAPL", "GOOG", "AMZN", "TSLA", "META", "NVDA", "PEP", "COST", "BTC-USD", "ETH-USD"]
# assets = ["AAPL", "GOOG", "AMZN", "TSLA", "META", "NVDA", "PEP", "COST", "GOOGL", "AVGO"]
#assets = ["BYND", "TWLO", "ROKU", "CVAC", "W", "BBBY", "FTCH"]

#assets = pd.read_csv("nasdaq-100.csv")["Symbol"]
#assets = ["QQQ", "SPY", "AAPL"]
#assets = ["VV", "IJH", "IJR", "EFA", "EEM", "RWR", "DBC", "VAW", "AGG", "TIP", "IGOV", "SHY"]
#money, selection, price_points = backtest(assets, start_date=make_date("2004-07-01"), end_date=make_date("2017-11-28"), selection_size = 5)

#plot_line_graphs(price_points, QQQ_prices, BTC_prices)
#print(close_prices(Ticker("SPY"), start_date=make_date("2021-06-07"), end_date=make_date("2023-06-07"), interval="1d"))