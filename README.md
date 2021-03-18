# Binance Futures
Straightforward API endpoint to receive market data for Binance Futures

## Installation

```bash
pip install binance-future
```

## Example

```python
from binance_futures import BinanceFuturesBBO

bbo = BinanceFuturesBBO(symbols=['btcusdt', 'ethusdt', 'ltcusdt'])
bbo.print_new_tickers()

# futures | btcusdt | 0.9230 @ 58875.57 | 0.0040 @ 58875.58
# futures | ltcusdt | 2.2270 @ 207.15 | 28.5200 @ 207.16
```
