# Binance Futures
Straightforward API endpoint to receive market data for Binance Futures

```bash
pip install binance-future
```

```python
from binance_futures import BinanceFuturesBBO
bbo = BinanceFuturesBBO()
print(bbo.ticker)
# 0.0140 @ 58784.87 | 0.0880 @ 58785.84
```