# The four calculations used to rank assets in RAAM
# Momentum, correlation, volume, and volatility

import arch
import pandas as pd
import datetime as dt
from yahooquery import *
from constants import *
from date_utils import *
from pull_data import *

# Filter the GARCH warning message
import warnings

# GENERAL CALCULATIONS


def load_history(asset, start_date, end_date, read_in_file=False):
    ticker = Ticker(asset)
    try:
        if read_in_file:
            history = pd.read_csv(
                "test_inputs/%s_history_6_2_2023.csv" % asset)
        else:
            history = close_prices(ticker, interval="1d",
                                   start_date=start_date, end_date=end_date)
    except FileNotFoundError:
        return None
    return history


def get_ranked_df(assets, rank_fn, read_in_file=False, ascending=False, alter_history_fn=None, start_date=None, end_date=None, **kwargs):
    ranked_df = pd.DataFrame(columns=["Symbol", "Value"])
    for asset in assets:
        history = load_history(asset, start_date, end_date,
                               read_in_file=read_in_file)

        # if there isn't enough data to evaluate the stock, skip it
        if history is None:
            continue

        history = history.dropna()

        if alter_history_fn:
            history = alter_history_fn(history)

        ranked_vals = rank_fn(history, **kwargs)
        ranked_df.loc[len(ranked_df)] = [asset, ranked_vals]

    ranked_df["Rank"] = ranked_df["Value"].rank(ascending=ascending)
    return ranked_df


# MOMENTUM CALCULATIONS

# input: history, a dataframe of close prices, sorted by date, ascending order
# output: momentum for most recent
def momentum_calc(history, periods=84):
    return history["close"].iloc[-1] / history["close"].iloc[-min(periods, history.shape[0])]


def momentum_rank(assets, periods=84, read_in_file=False, start_date=None, end_date=None):
    ranks = get_ranked_df(assets, momentum_calc, read_in_file=read_in_file,
                          periods=periods, start_date=start_date, end_date=end_date)
    ranks = ranks[ranks["Value"] > 1.00] #filter out stocks with negative momentum
    return ranks

# VOLATILITY CALCULATIONS


def expected_return(row):
    if row["close"] != 0.00:
        return row["next_close"]/row["close"] - 1
    else:
        return None


def gen_next_close(history):
    history["next_close"] = history["close"].shift(-1)
    return history


def expected_return_volatility(history):
    history = gen_next_close(history)
    history["expected_return"] = history.apply(
        lambda row: expected_return(row), axis=1)
    return history


def garch_volatility(history):
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')
        # Create GARCH model
        model = arch.arch_model(history['close'], vol='Garch', p=1, q=1)

        # Fit the model
        results = model.fit(disp="off")

        # Predict volatility
        volatility = results.conditional_volatility

        return volatility[-1]


def volatility_rank(assets, periods=84, read_in_file=False, start_date=None, end_date=None):
    # isolates GARCH to periods datapoints, probably redundant
    def periodic_window(x): return x.iloc[-min(periods, len(x)):]
    return get_ranked_df(assets, garch_volatility, alter_history_fn=None, read_in_file=read_in_file, ascending=True, start_date=start_date, end_date=end_date)

    # USE THIS FOR STDEV INSTEAD OF GARCH
    # stdev_calc = lambda x: x["expected_return"].std()
    # return get_ranked_df(assets, stdev_calc, read_in_file=read_in_file, ascending=True, alter_history_fn=expected_return_volatility, start_date=start_date, end_date=end_date)


# CORRELATION CALCULATIONS

def build_corr_matrix(assets, read_in_file=False, start_date=None, end_date=None, periods=84, drop_unmatched=True):
    prices_df = pd.DataFrame(columns=["Date"])
    for asset in assets:
        history = load_history(asset, start_date, end_date,
                               read_in_file=read_in_file)

        # Disregard stocks for which data is not available
        if history is None:
            continue

        history = history.iloc[-min(periods, len(history)):]

        # bring in all entries regardless of if the indices match
        prices_df = prices_df.merge(history["close"], left_on=[
                                    "Date"], right_on=history["close"].index.get_level_values("date"), how="outer")
        prices_df = prices_df.rename(columns={"close": asset})

    # Filter down to just rows with a common index across all assets
    if drop_unmatched:
        prices_df = prices_df.dropna()

    return prices_df.corr()


def correlation_rank(assets, read_in_file=False, start_date=None, end_date=None, periods=84, drop_unmatched=True):
    ranked_df = pd.DataFrame(columns=["Symbol", "Value"])
    corr = build_corr_matrix(assets, read_in_file=read_in_file, start_date=start_date,
                             end_date=end_date, periods=periods, drop_unmatched=drop_unmatched)

    for asset in assets:
        try:
            ranked_df.loc[len(ranked_df)] = [asset, corr[asset].mean()]
        except KeyError:
            continue

    ranked_df["Rank"] = ranked_df["Value"].rank(ascending=True)
    return ranked_df


# MOVING AVERAGE CALCULATIONS

# def calculate_moving_average(history, window):
#     history['MA'] = history['close'].rolling(window=window).mean()
#     return history

# def moving_average_signal(assets, read_in_file = read_in_file, start_date=start_date, end_date=end_date):
#     for asset in assets:
#         history = load_history(asset, start_date, end_date, read_in_file=read_in_file)


# ATR CALCULATIONS

def calculate_atr_signal(history, periods=84, atr_multiplier=1):
    # Calculate the true range
    history['TrueRange'] = history['high'] - history['low']
    history['HighToClose'] = abs(history['high'] - history['close'].shift(1))
    history['LowToClose'] = abs(history['low'] - history['close'].shift(1))
    history['TrueRange'] = history[['TrueRange',
                                    'HighToClose', 'LowToClose']].max(axis=1)

    # Calculate the ATR
    history['ATR'] = history['TrueRange'].rolling(periods).mean()

    # Initialize the signal column
    history['Signal'] = 0

    # Set signal to 1 for buy signals
    history.loc[history['high'] > history['close'].shift(
        1) + atr_multiplier * history['ATR'], 'Signal'] = 1

    # Set signal to -1 for sell signals
    history.loc[history['low'] < history['close'].shift(
        1) - atr_multiplier * history['ATR'], 'Signal'] = -1

    # Drop intermediate columns
    history.drop(['TrueRange', 'HighToClose', 'LowToClose'],
                 axis=1, inplace=True)

    return history


def atr_rank(assets, read_in_file=False, start_date=None, end_date=None, periods=84, atr_multiplier=1):
    signal_df = pd.DataFrame(columns=["Symbol", "Value"])
    for asset in assets:
        try:
            history = load_history(
                asset, start_date, end_date, read_in_file=read_in_file)

            if history is None:
                continue

            history = calculate_atr_signal(
                history, periods=periods, atr_multiplier=atr_multiplier)
            signal_df.loc[len(signal_df)] = [asset, history.iloc[-1]["Signal"]]
        except KeyError:
            continue

    return signal_df


# FINAL RANKING
# Takes all three _rank functions and combines them for a final weighted ranking
# Weights are stored in constants.py

def combine_signals(assets, read_in_file=False, start_date=None, end_date=None, drop_unmatched_corr=True, save_results=True, periods=84, atr_multiplier=1, momentum_weight=MOMENTUM_WEIGHT, volatility_weight=VOLATILITY_WEIGHT, correlation_weight=CORRELATION_WEIGHT, atr_weight=ATR_WEIGHT, verbose=False):
    # , "Momentum", "Correlation", "Volatility", "Combined", "Rank"]
    combined_df = pd.DataFrame(columns=["Symbol"])
    combined_df["Symbol"] = assets
    momentum_df = momentum_rank(assets, read_in_file=read_in_file,
                                periods=periods, start_date=start_date, end_date=end_date)
    volatility_df = volatility_rank(
        assets, read_in_file=read_in_file, start_date=start_date, end_date=end_date)
    correlation_df = correlation_rank(assets, read_in_file=read_in_file, start_date=start_date,
                                      end_date=end_date, periods=periods, drop_unmatched=drop_unmatched_corr)

    def values_from(combined_df, values_df, new_field_name):
        combined_df = combined_df.merge(
            values_df[["Symbol", "Rank"]], left_on="Symbol", right_on="Symbol")
        combined_df = combined_df.rename(columns={"Rank": new_field_name})
        return combined_df

    # Add in values from each indicator
    combined_df = values_from(combined_df, momentum_df, "Momentum")
    combined_df = values_from(combined_df, volatility_df, "Volatility")
    combined_df = values_from(combined_df, correlation_df, "Correlation")
    combined_df = combined_df.dropna()

    # Add in ATR
    atr_df = atr_rank(assets, read_in_file=read_in_file, start_date=start_date,
                      end_date=end_date, periods=periods, atr_multiplier=atr_multiplier)
    combined_df = combined_df.merge(
        atr_df[["Symbol", "Value"]], left_on="Symbol", right_on="Symbol")
    combined_df = combined_df.rename(columns={"Value": "ATR"})

    combined_df["Combined"] = combined_df["Momentum"] * momentum_weight + combined_df["Volatility"] * volatility_weight + combined_df["Correlation"] * correlation_weight + combined_df["ATR"] * atr_weight
    combined_df["Rank"] = combined_df["Combined"].rank(ascending=True)

    if save_results:
        combined_df.to_csv("../outputs/results.csv")

    if verbose:
        print(momentum_df)
        print(volatility_df)
        print(correlation_df)
        print(combined_df)

    return combined_df

# Returns a truncated dataframe for discord messaging
# Takes the top 20 values to avoid discord's message limits
def truncate_dataframe(df):
    df = df[df["Rank"] <= 20].sort_values("Rank")
    formatted =  discord_string(df)
    return formatted

# Formats a dataframe as a string for discord's formatting
def discord_string(df):
    code_format_str = '```'
    response = code_format_str + df.to_string() + code_format_str
    return response 

# assets = pd.read_csv("nasdaq-100.csv")["Symbol"]
# assets = ["AAPL", "GOOG", "AMZN", "TSLA", "META", "NVDA", "PEP", "COST", "BTC-USD", "ETH-USD"]
# nasdaq_10 = ["AAPL", "GOOG", "AMZN", "TSLA", "META", "NVDA", "PEP", "COST", "GOOGL", "AVGO"]
# djia_10 = ["UNH", "MSFT", "GS", "MCD", "HD", "CRM", "V", "AMGN", "CAT", "BA"]
# morningstar_10 = ["META", "CRM", "GOOGL", "AMZN", "MSFT", "LRCX", "NOW", "ADBE", "TYL", "TRU"]

# assets = list(set(nasdaq_10 + djia_10 + morningstar_10))

# start_date=make_date("2022-12-15"), end_date=make_date("2023-02-15"),
# combine_signals(assets, periods=84, drop_unmatched_corr=True, read_in_file=False)
