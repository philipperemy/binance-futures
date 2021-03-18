from binance_futures import BinanceFuturesBBO

# noinspection PyArgumentEqualDefault,SpellCheckingInspection
bbo = BinanceFuturesBBO(symbols=['btcusdt', 'ethusdt', 'ltcusdt'])

# prints the bid/ask of BTCUSDT along with its volumes (best bid offer).
print(bbo.ticker('btcusdt'))

# prints any ticker update for the symbols defined above, on the future instruments.
bbo.print_on_ticker_update()
