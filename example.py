from binance_futures import BinanceFuturesBBO

bbo = BinanceFuturesBBO()
last_ticker = None
while True:
    new_ticker = bbo.ticker
    if last_ticker is None:
        last_ticker = new_ticker
    if not new_ticker.same_prices(last_ticker):
        last_ticker = new_ticker
        print(last_ticker)
