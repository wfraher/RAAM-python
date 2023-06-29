### HOW TO RUN RAAM FOR AD-HOC RESULTS

##### Parameters
If you type !run-raam it will run RAAM with the default parameters 
The default parameters are:
assets = AAPL,GOOG,AMZN,TSLA,META,NVDA,PEP,COST,GOOGL,AVGO
end_date = today's date in YYYY-MM-DD format
start_date = amount of periods specified before today 
periods = 84 (four months of business days for lookback period)

```!run-raam```
```  Symbol  Momentum  Volatility  Correlation  ATR  Combined  Rank
0   AAPL       8.0         2.0          7.0  0.0      5.61   7.5
1   GOOG       4.0         4.0          8.0  0.0      5.28   5.0
2   AMZN       6.0         6.0         10.0  0.0      7.26  10.0
3   TSLA       7.0         7.0          1.0  0.0      4.95   2.5
4   META       2.0         8.0          5.0  0.0      4.95   2.5
5   NVDA       1.0         9.0          6.0  0.0      5.28   5.0
6    PEP       9.0         1.0          2.0  0.0      3.96   1.0
7   COST      10.0         3.0          3.0  0.0      5.28   5.0
8  GOOGL       5.0         5.0          9.0  0.0      6.27   9.0
9   AVGO       3.0        10.0          4.0  0.0      5.61   7.5```

You can change the parameters by typing them in alongside !run-raam, for example
```!run-raam assets=QQQ,SPY periods=42```
will run RAAM with QQQ and SPY for 42 business days of lookback.

Make sure not to use spaces in between each parameter, it throws off the way Discord parses commands 
For passing in dates, make sure to use yyyy-mm-dd format
```!run-raam start_date=2021-04-02```

##### Other parameters
You can specify how RAAM weighs momentum, volatility, and correlation in its final calculation with momentum_weight, correlation_weight, and volatility_weight.
```momentum_weight=0.2 volatility_weight=0.4 correlation_weight=0.4```
 will weigh momentum_weight with twice the importance as volatility and correlation, since higher values in the final calculation mean lower overall rank.

Additionally, when backtesting, you can add 
```verbose=True```
to see how RAAM ranks each asset during each backtesting step.



#### How RAAM works
RAAM works by testing given assets over a given date range and ranking them according to the momentum, volatility, correlation, and ATR (average true return) of those assets.

When backtesting, RAAM takes the top 5 assets and splits its value between all of them. It then calculates how those assets performed over the course of a month, takes profit/losses, and re-allocates its holdings.