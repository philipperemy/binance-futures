from binance_futures import BinanceFuturesBBO

# noinspection PyArgumentEqualDefault,SpellCheckingInspection
bbo = BinanceFuturesBBO(symbols=['btcusdt', 'ethusdt', 'ltcusdt'])
bbo.print_new_tickers()
