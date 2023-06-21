QQQ_prices = close_prices(Ticker("QQQ"), start_date=make_date("2018-06-07"), end_date=make_date("2023-06-07"), interval="1wk")["close"].reset_index(level="symbol").rolling(4).mean()
BTC_prices = close_prices(Ticker("BTC-USD"), start_date=make_date("2018-06-07"), end_date=make_date("2023-06-07"), interval="1wk")["close"].reset_index(level="symbol").rolling(4).mean()
BTC_prices = BTC_prices[BTC_prices.index.isin(QQQ_prices.index)]

print(QQQ_prices)
print(BTC_prices)

#Convert to percent gains
def convert_to_percent(df):
    df = df["close"].values
    return df / df[0] * 100

QQQ_prices = convert_to_percent(QQQ_prices)
BTC_prices = convert_to_percent(BTC_prices)

import matplotlib.pyplot as plt

def plot_line_graphs(*args):
    # Create a new figure
    fig, ax = plt.subplots()

    # Plot line graphs for each set of y-values
    for y_values in args:
        x_values = range(1, len(y_values) + 1)
        ax.plot(x_values, y_values)

    # Set labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Earnings percentage')
    ax.set_title('Earnings comparison')

    # Show the plot
    plt.show()