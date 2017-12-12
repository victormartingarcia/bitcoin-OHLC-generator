import pandas as pd
from tqdm import *
import argparse


def generate_ohlcv_bars(exchange, compression):
    """
    Download exchange raw trade data from bitcoincharts.com and resamples them to OHLCV candlesticks

    Parameters
    ----------
    exchange : str
        Exchange name as appears into http://api.bitcoincharts.com/v1/csv/
    df_backtest_results : pd.DataFrame
        Strategy portfolio and compounded daily PL. One row per session.
         - See full explanation in :func:`~backtest.perform_backtest`
    interest_rate : float
        Interest rate for the current day
    isDailyPerformanceScript : bool
        True if the function is being called by the daily performance calculation script

    Returns
    -------
    df_bars : pd.DataFrame
        Dataframe containing historical OHLCV bars from the exchange
    """
    bitcoincharts_url = "https://api.bitcoincharts.com/v1/csv/{}USD.csv.gz".format(exchange)

    print("Downloading {} trade data from URL {}".format(exchange, bitcoincharts_url))
    df_trades = pd.read_csv(bitcoincharts_url,
                            names=["unixtime", "price", "amount"],
                            compression='gzip')

    df_trades["datetime"] = pd.to_datetime(df_trades["unixtime"], unit="s")
    df_trades = df_trades.drop("unixtime", axis=1).set_index("datetime").sort_index()

    df_bars = df_trades

    df_bars["open"] = df_bars["price"]
    df_bars["high"] = df_bars["price"]
    df_bars["low"] = df_bars["price"]
    df_bars["close"] = df_bars["price"]
    df_bars["volume"] = df_bars["amount"]

    df_bars = df_bars.drop(["price", "amount"], axis=1)

    df_bars = df_bars.resample(str(compression) + "min").agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum"
    }).dropna()

    return df_bars[["open", "high", "low", "close", "volume"]]


def join_exchanges_ohlcv(list_dfs):
    """
    Download exchange raw trade data from bitcoincharts.com and resamples them to OHLCV candlesticks

    Parameters
    ----------
    list_fds : list of pd.DataFrame
        List of exchanges OHLCV bars as returned by :func:`~generate_ohlcv_bars`

    Returns
    -------
    df_joined : pd.DataFrame
        Dataframe containing aggregated OHLCV bars from all exchanges
    """

    print("Aggregating OHLCV history data from {} exchanges into a single dataframe".format(len(list_dfs)))

    df_concat = pd.concat(tuple(list_dfs))

    grp = df_concat.groupby(df_concat.index)
    df_joined = grp[["open", "high", "low", "close"]].mean()
    df_joined = df_joined.join(grp["volume"].sum())

    # Round decimals
    return df_joined.round({
        "open": 2,
        "high": 2,
        "low": 2,
        "close": 2,
        "volume": 6,
    })


def main():
    parser = argparse.ArgumentParser(description='Generate aggregated historical OHLC candlesticks for BTCUSD')

    parser.add_argument("-c", "--compression", type=int, required=True, help="Minutes compression for generated candlestick bars")
    parser.add_argument("-o", "--output", required=True, help="Directs the output to a name of your choice")

    args = parser.parse_args()

    # Define the exchanges we want to aggregate
    exchanges = [
        "bitstamp",
        "coinbase",
        "bitfinex",
        "kraken",
        "itbit"
    ]

    print("Aggregating bitcoin trade data from {} exchanges and create {} file containing {}min OHLC bars".format(
        len(exchanges),
        args.output,
        args.compression
        )
    )

    bars = {}

    for exchange in tqdm(exchanges):
        bars[exchange] = generate_ohlcv_bars(exchange, args.compression)

    df_bitcoin = join_exchanges_ohlcv(tuple(bars.values()))

    print("Saving {} rows to file {}".format(len(df_bitcoin), args.output))
    df_bitcoin.to_csv(args.output)


if __name__ == '__main__':
    main()
