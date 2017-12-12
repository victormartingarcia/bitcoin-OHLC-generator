
A simple python script for aggregating bitcoin raw trade data from several exchanges, 
and combine them into a single CSV file containing minute OHCLV candlesticks


# Installing

```Bash
# Install dependencies from requirements.txt file
$ pip install -r requirements.txt
```

# Usage

```Bash
$ python bitcoin-OHLC-generator.py --compression 1 -o bitcoin.csv
```

Required args:
* -c (--compression) _num_ : Aggregate data into __num__ minute OHLCV candlesticks
* -o (--output) _file_ : Save generated candlesticks into __file__ CSV format file


# Motivation

[Bitcoin cryptocurrency](https://es.wikipedia.org/wiki/Bitcoin) is trading into different spot-exchanges, 
each of those with its _last_ price, usually defined by the mid-price between its best bid and its bets
offer (ask) prices.

The closest thing to an "official" [BTCUSD](http://www.cmegroup.com/trading/cf-bitcoin-reference-rate.html) 
price is the [Bitcoin Reference Rate](http://www.cmegroup.com/trading/cf-bitcoin-reference-rate.html) 
published by the [Chicago Mercantile Exchange](http://www.cmegroup.com/).

This reference price (and CME CF Bitcoin Real-time index) is calculated aggregating the trade flow of 5 major
bitcoin spot exchanges:

```
* bitstamp
* coinbase
* bitfinex
* kraken
* itbit
```

__This is the approach I followed__ to build this script, creating a tool that generates "official"
historical OHLC candlestick data. 

![Aggregation](media/BTCUSD_aggregation.png?raw=true "Bitcoin aggregation")

I hope you find this useful. __Enjoy the ride!__

![Bitcoin explosive growth](media/BTCUSD.png?raw=true "Bitcoin explosive growth")
