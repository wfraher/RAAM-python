import pandas as pd 
from yahooquery import *
from pull_data import *
from calculations import *

def test_pull_data():
    qqq_ticker = Ticker("QQQ")

    history = close_prices(qqq_ticker)
    assert len(history) != 0


### TESTS FOR MOMENTUM

def test_momentum_calc():
    history = pd.read_csv("test_inputs/qqq_history_5_31_2023.csv")
    assert momentum_calc(history) == 1.2473764962781488

def test_momentum_rank():
    assets = ["QQQ", "BTC", "SPY", "AAPL", "GOOG", "VTI"]

    df = momentum_rank(assets, read_in_file=True)

    def momentum_equals(symbol, momentum):
        print(round(df[df["Symbol"] == symbol]["Value"].values[0], 14))
        return round(df[df["Symbol"] == symbol]["Value"].values[0], 14) == momentum

    def rank_equals(symbol, rank):
        return df[df["Symbol"] == symbol]["Rank"].values[0] == rank

    assert momentum_equals("QQQ", 1.24737649627815)
    assert momentum_equals("BTC", 1.00645711997743)
    assert momentum_equals("SPY", 1.07589689018473)
    assert momentum_equals("AAPL", 1.24425384869501)
    assert momentum_equals("GOOG", 1.28085502534925)
    assert momentum_equals("VTI", 1.06750708451962)

    assert rank_equals("QQQ", 2)
    assert rank_equals("BTC", 6)
    assert rank_equals("SPY", 4)
    assert rank_equals("AAPL", 3)
    assert rank_equals("GOOG", 1)
    assert rank_equals("VTI", 5)


### TESTS FOR VOLATILITY

def test_expected_return():
    history = pd.read_csv("test_inputs/QQQ_history_5_31_2023.csv")
    history = gen_next_close(history)

    assert history["next_close"].iloc[0] == 168.41061401367188

    history["expected_return"] = history.apply(lambda row: expected_return(row), axis=1)
    history.to_csv("test.csv")

    assert history["expected_return"].iloc[0] == 0.009030846730675446
    assert pd.isna(history["expected_return"].iloc[-1])
    assert history["expected_return"].iloc[-2] == 0.004535066353397177
    assert history["expected_return"].iloc[-3] == 0.025550431663110107

def test_volatility_rank():
    assets = ["QQQ", "BTC", "SPY", "AAPL", "GOOG", "VTI"]

    # hist_2 = add_volatility(pd.read_csv("test_inputs/QQQ_history_5_31_2023.csv"))
    # print(hist_2["expected_return"].std(ddof = 1))
    # print(hist_2["expected_return"].describe())

    df = volatility_rank(assets, read_in_file = True)

    def stdev_equals(symbol, stdev):
        print(df[df["Symbol"] == symbol]["Value"].values[0])
        return round(df[df["Symbol"] == symbol]["Value"].values[0], 6) == stdev

    def rank_equals(symbol, rank):
        return df[df["Symbol"] == symbol]["Rank"].values[0] == rank

    assert stdev_equals("QQQ", 0.016452)
    assert rank_equals("QQQ", 4.0)


### TESTS FOR CORRELATION

def test_correlation_rank():
    assets = ["QQQ", "BTC", "SPY", "AAPL", "GOOG", "VTI"]
    print(build_corr_matrix(assets, read_in_file = True))
    rank = correlation_rank(assets, read_in_file = True)
    print(rank)
    assert False