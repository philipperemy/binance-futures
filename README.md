## Binance Futures

Straightforward API endpoint to receive market data for Binance Futures.

### Installation

```bash
pip install binance-future
```

### Example

```python
from binance_futures import BinanceFuturesBBO

bbo = BinanceFuturesBBO(symbols=['btcusdt', 'ethusdt', 'ltcusdt'])

# prints the bid/ask of BTCUSDT along with its volumes (best bid offer).
print(bbo.ticker('btcusdt'))

# futures | btcusdt | 0.9230 @ 58875.57 | 0.0040 @ 58875.58

# prints any ticker update for the future instruments defined above.
bbo.print_on_ticker_update()

# futures | btcusdt | 0.9230 @ 58875.57 | 0.0040 @ 58875.58
# futures | ltcusdt | 2.2270 @ 207.15 | 28.5200 @ 207.16
```
