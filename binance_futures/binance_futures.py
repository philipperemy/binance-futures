import json
import threading
import time
from typing import Union, List, Set, Dict

import attr
from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager


class BinanceMarketDataMessage:
    @staticmethod
    def from_dict(data: dict, obj_type):
        obj = obj_type()
        attributes = {
            'desc': ('e', str),
            'symbol': ('s', str),
            'close': ('c', float),
            'open': ('o', float),
            'price': ('p', float),
            'quantity': ('q', float),
            'high': ('h', float),
            'low': ('l', float),
            'first_trade_id': ('f', float),
            'is_buyer_market_marker': ('m', bool),
            'order_book_update_id': ('u', int),
            'best_bid_price': ('b', float),
            'best_bid_qty': ('B', float),
            'best_ask_price': ('a', float),
            'best_ask_qty': ('A', float),
            'last_trade_id': ('l', float),
            'trade_time': ('T', str),
            'total_traded_base_asset_volume': ('v', float),
            'total_traded_quote_asset_volume': ('q', float),
            'number_of_trades': ('n', float),
            'close_time': ('C', str),
            'open_time': ('O', str),
            'last_quantity': ('Q', float),
            'vwap': ('w', float),
            'price_change_pct': ('P', float),
            'price_change': ('p', float),
            'event_time': ('E', str)
        }
        for attribute, key in attributes.items():
            k, attr_type = key
            if k in data:
                setattr(obj, attribute, attr_type(data[k]))

        return obj

    def __str__(self):
        message_type = type(self).__name__
        return message_type + ' - ' + json.dumps(self.__dict__)


@attr.s()
class BinanceTicker:
    symbol = attr.ib(type=str)
    best_bid_price = attr.ib(type=float)
    best_ask_price = attr.ib(type=float)
    best_bid_qty = attr.ib(type=float)
    best_ask_qty = attr.ib(type=float)

    def __str__(self):
        return f'{self.symbol} | {self.best_bid_qty:.4f} @ {self.best_bid_price:.2f} | ' \
               f'{self.best_ask_qty:.4f} @ {self.best_ask_price:.2f}'

    def same_prices(self, obj1):
        return obj1.best_bid_price == self.best_bid_price and obj1.best_ask_price == self.best_ask_price


class AggTrade(BinanceMarketDataMessage):
    pass


class Ticker(BinanceMarketDataMessage):
    pass


class MiniTicker(BinanceMarketDataMessage):
    pass


class BookTicker(BinanceMarketDataMessage):
    pass


class BinanceMarketDataFuturesAPI:

    def __init__(self):
        self.binance_websocket_api_manager = BinanceWebSocketApiManager(exchange='binance.com-futures')

    @property
    def markets(self):
        # noinspection SpellCheckingInspection
        return {'btcusdt', 'bchusdt', 'ethusdt'}

    def register_channels(self, channels: Union[str, List, Set], markets: Union[str, List, Set]):
        self.binance_websocket_api_manager.create_stream(channels, markets)

    def start(self, on_new_message=None):
        threading.Thread(target=self.handle_messages, name='binance_futures_handle_messages',
                         args=(on_new_message,)).start()

    @staticmethod
    def on_new_message(data):
        print(data)

    def handle_messages(self, on_new_message=None):
        if on_new_message is None:
            on_new_message = self.on_new_message
        while True:
            if self.binance_websocket_api_manager.is_manager_stopping():
                exit(0)
            data = self.binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
            if data is False:
                time.sleep(0.01)
            else:
                data_as_json = json.loads(data)
                if 'stream' in data_as_json:
                    on_new_message(data_as_json)


class BinanceFuturesBBO:

    def __init__(self, symbols: Union[str, List] = 'btcusdt'):
        # ticker: refreshed once per second. (1000ms).
        # miniTicker: refreshed once per second (1000ms).
        # aggTrade: The Aggregate Trade Streams push trade information that is aggregated for a single taker order (RT)
        # bookTicker: Pushes any update to the best bid or ask's price or quantity in real-time
        # for a specified symbol (RT)
        if isinstance(symbols, str):
            symbols = [symbols]
        self.symbols = [s.lower() for s in symbols]
        self.messages_type = {}
        for s in self.symbols:
            self.messages_type.update({
                f'{s}@ticker': Ticker,
                f'{s}@bookTicker': BookTicker,
                f'{s}@miniTicker': MiniTicker,
                f'{s}@aggTrade': AggTrade,
            })
        self.api = BinanceMarketDataFuturesAPI()
        self.api.register_channels(['bookTicker'], self.symbols)
        self.api.start(on_new_message=self.on_new_message)
        self._last_update = {}
        while len(self._last_update) != len(self.symbols):
            time.sleep(0.001)

    def on_new_message(self, data):
        message_type = self.messages_type[data['stream']]
        payload = data['data']
        msg = BinanceMarketDataMessage.from_dict(payload, message_type)
        symbol = msg.symbol.lower()
        self._last_update[symbol] = msg

    def ticker(self, symbol) -> BinanceTicker:
        symbol = symbol.lower()
        return BinanceTicker(
            symbol=symbol,
            best_bid_price=self._last_update[symbol].best_bid_price,
            best_ask_price=self._last_update[symbol].best_ask_price,
            best_bid_qty=self._last_update[symbol].best_bid_qty,
            best_ask_qty=self._last_update[symbol].best_ask_qty,
        )

    @property
    def tickers(self) -> Dict[str, BinanceTicker]:
        return {s: self.ticker(s) for s in self.symbols}

    def print_new_tickers(self):
        last_tickers = self.tickers
        while True:
            new_tickers = self.tickers
            for symbol in new_tickers:
                if not new_tickers[symbol].same_prices(last_tickers[symbol]):
                    print('futures | ' + str(new_tickers[symbol]))
                    last_tickers[symbol] = new_tickers[symbol]
