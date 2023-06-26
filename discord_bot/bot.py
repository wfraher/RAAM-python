# bot.py
import os
import sys

# RAAM calculation imports
sys.path.append("../src")
from constants import *
from backtest import *
from date_utils import *
from calculations import *

# Discord API imports
from discord.ext import commands
from dotenv import load_dotenv
import discord

# Other imports
import pandas as pd
from pandas.tseries.offsets import BDay


# Constants
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix=os.getenv('COMMAND_PREFIX'), intents=intents)


@bot.event
async def on_ready():
    for guild in bot.guilds:
        print(
            f'{bot.user} is connected to the following guild: {guild.name} with ID {guild.id}')

    print('Connected to Discord!')


def process_args(args, interval="1d"):
    # Default paramseters
    assets = ["AAPL", "GOOG", "AMZN", "TSLA", "META",
              "NVDA", "PEP", "COST", "GOOGL", "AVGO"]
    drop_unmatched_corr = True
    save_results = True
    periods = 84
    start_date, end_date = default_start_end(None, None, interval)
    atr_multiplier = 1
    selection_size = 5
    period = 4
    window = 16
    momentum_weight = MOMENTUM_WEIGHT
    volatility_weight = VOLATILITY_WEIGHT
    correlation_weight = CORRELATION_WEIGHT
    atr_weight = ATR_WEIGHT
    verbose = False

    def process_arg(arg):
        both = arg.strip().split("=")
        return both[0], both[1]

    for arg in args:
        try:
            keyword, arg = process_arg(arg)
        except:
            print("Processing an argument %s failed!" % str(arg))
            continue
        if "assets" in keyword.lower():
            assets = arg.split(",")
        elif "risk_free" in keyword.lower():
            risk_free = arg.split(",")
        elif "start_date" in keyword.lower():
            start_date = make_date(arg)
        elif "end_date" in keyword.lower():
            end_date = make_date(arg)
        elif "periods" in keyword.lower():
            periods = int(arg)
        elif "selection_size" in keyword.lower():
            selection_size = int(arg)
        # crucial detail: period is for the backtesting function, periods is for the RAAM function. Condition was left here as a reminder
        elif "period" in keyword.lower() and "s" not in keyword.lower():
            period = int(arg)
        elif "window" in keyword.lower():
            window = int(arg)
        elif "momentum_weight" in keyword.lower():
            momentum_weight = float(arg)
        elif "volatility_weight" in keyword.lower():
            volatility_weight = float(arg)
        elif "correlation_weight" in keyword.lower():
            correlation_weight = float(arg)
        elif "atr_weight" in keyword.lower():
            atr_weight = float(arg)
        elif "verbose" in keyword.lower():
            verbose = bool(arg)

    return assets, risk_free, drop_unmatched_corr, save_results, periods, end_date, start_date, atr_multiplier, selection_size, period, window, momentum_weight, volatility_weight, correlation_weight, atr_weight, verbose


@bot.command(name='run-raam', help='Returns the results on running RAAM with the top 10 nasdaq stocks. Allocations are determined from four months of historical data.')
async def get_results(ctx, *args):

    # Process arguments and send status message
    assets, risk_free, drop_unmatched_corr, save_results, periods, end_date, start_date, atr_multiplier, selection_size, period, window, momentum_weight, volatility_weight, correlation_weight, atr_weight, verbose = process_args(
        args)
    await ctx.send("Fetching RAAM results for %s on %s through %s for periods of %s business days" % (str(assets), str(start_date), str(end_date), str(periods)))

    # Run RAAM, format output as a string
    raam_results = combine_signals(assets, read_in_file=False, start_date=start_date, end_date=end_date, drop_unmatched_corr=drop_unmatched_corr, save_results=save_results, periods=periods,
                                   atr_multiplier=atr_multiplier, momentum_weight=momentum_weight, volatility_weight=volatility_weight, correlation_weight=correlation_weight, atr_weight=atr_weight, verbose=verbose)
    response = truncate_dataframe(raam_results)

    # Send response and message explaining truncated output
    await ctx.send(response)
    if len(raam_results) > 20:
        await ctx.send("More than twenty assets were tested, only the top twenty are shown due to discord message size limits. Ask Rut if you want the whole results.")

# assets, period=4, window=16, start_date = None, end_date = None, selection_size = 5


@bot.command(name='backtest', help='Backtests the bot.')
async def backtest_bot(ctx, *args):

    # Process arguments
    assets, risk_free, drop_unmatched_corr, save_results, periods, end_date, start_date, atr_multiplier, selection_size, period, window, momentum_weight, volatility_weight, correlation_weight, atr_weight, verbose = process_args(
        args)

    # Run backtesting process, print status messages
    await ctx.send("Backtesting for %s, over range %s to %s, please be patient and await results." % (str(assets), str(start_date), str(end_date)))
    money, selection, price_points = await backtest(assets, risk_free=risk_free, periods=periods, period=period, window=window, start_date=start_date, end_date=end_date, selection_size=selection_size, interval="1d", ctx=ctx, momentum_weight=momentum_weight, volatility_weight=volatility_weight, correlation_weight=correlation_weight, atr_weight=atr_weight, verbose=verbose)
    await ctx.send("Backtesting complete")

    # Print output
    await ctx.send("Assets tested: %s" % str(assets))
    await ctx.send("Percent of starting value earned from backtesting over %s to %s: %s" % (start_date, end_date, money))
    # await ctx.send("Final selection: %s" % allocation_to_output(selection))

    # Print history
    # for _, row in price_points.iterrows():
    #     await ctx.send(row.to_string())

@bot.command(name='get-history', help='return daily closing price points over a date range')
async def get_history(ctx, *args):
    assets, drop_unmatched_corr, save_results, periods, end_date, start_date, atr_multiplier, selection_size, period, window, momentum_weight, volatility_weight, correlation_weight, atr_weight, verbose = process_args(args)

    history = close_prices(Ticker(assets), start_date=start_date, end_date=end_date)
    if history is not None:
        await ctx.send(discord_string(history.head()))
        await ctx.send(discord_string(history.tail()))
    else:
        await ctx.send("Error! No data was found.")

@bot.command(name='jew', help='prints a quirky little message for the bot\'s purpose')
async def purpose(ctx):
    await ctx.send('YOUR FREE MONEY, SIR!')

@bot.event
async def on_error(event, *args):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

bot.run(TOKEN)
