import time
import datetime
import pytz
import math

import colorsys
from ccxt.base import decimal_to_precision as dtp


class Utils(object):
	@staticmethod
	def format_price(exchange, symbol, price):
		precision = 8 if (exchange.markets[symbol]["precision"]["price"] is None if "price" in exchange.markets[symbol]["precision"] else True) else exchange.markets[symbol]["precision"]["price"]
		price = float(dtp.decimal_to_precision(price, rounding_mode=dtp.ROUND, precision=precision, counting_mode=exchange.precisionMode, padding_mode=dtp.PAD_WITH_ZERO))
		return ("{:,.%df}" % Utils.num_of_decimal_places(exchange, price, precision)).format(price)

	@staticmethod
	def format_amount(exchange, symbol, amount):
		precision = exchange.markets[symbol]["precision"]["amount"]
		amount = float(dtp.decimal_to_precision(amount, rounding_mode=dtp.TRUNCATE, precision=precision, counting_mode=exchange.precisionMode, padding_mode=dtp.NO_PADDING))
		return ("{:,.%df}" % Utils.num_of_decimal_places(exchange, amount, precision)).format(amount)

	@staticmethod
	def num_of_decimal_places(exchange, price, precision):
		if exchange.id in ["bitmex", "ftx"]:
			s = str(precision)
			if "e" in s: return int(s.split("e-")[1])
			elif not '.' in s: return 0
			else: return len(s) - s.index('.') - 1
		elif exchange.id in ["bitfinex2"]:
			return precision - len(str(int(price)))
		else:
			return precision

	@staticmethod
	def add_decimal_zeros(number, digits=8):
		wholePart = str(int(number))
		return digits if wholePart == "0" else max(digits - len(wholePart), 0)

	@staticmethod
	def shortcuts(raw, allowsShortcuts):
		initial = raw
		isDeprecated = False
		if allowsShortcuts:
			if raw in ["mex"]: raw, isDeprecated = "p xbt, eth mex, xrp mex", True
			elif raw in ["fut", "futs", "futures"]: raw, isDeprecated = "p futures", True
			elif raw in ["funding", "fun"]: raw, isDeprecated = "p xbt fun, eth fun, xrp fun", True
			elif raw in ["oi", "ov"]: raw, isDeprecated = "p xbt oi, eth oi, xrp oi", True
			elif raw in ["mex xbt", "mex btc"]: raw, isDeprecated = "p xbt", True
			elif raw in ["mex eth"]: raw, isDeprecated = "p eth mex", True
			elif raw in ["mex xrp"]: raw, isDeprecated = "p xrp mex", True
			elif raw in ["mex bch"]: raw, isDeprecated = "p bch mex", True
			elif raw in ["mex ltc"]: raw, isDeprecated = "p ltc mex", True
			elif raw in ["mex link"]: raw, isDeprecated = "p link mex", True
			elif raw in ["mex eos"]: raw, isDeprecated = "p eos mex", True
			elif raw in ["mex trx"]: raw, isDeprecated = "p trx mex", True
			elif raw in ["mex ada"]: raw, isDeprecated = "p ada mex", True
			elif raw in ["prem", "prems", "premiums"]: raw, isDeprecated = "p btc prems", True
			elif raw in ["funding xbt", "fun xbt", "funding xbtusd", "fun xbtusd", "funding btc", "fun btc", "funding btcusd", "fun btcusd", "xbt funding", "xbt fun", "xbtusd funding", "xbtusd fun", "btc funding", "btc fun", "btcusd funding", "btcusd fun"]: raw, isDeprecated = "p xbt funding", True
			elif raw in ["funding eth", "fun eth", "funding ethusd", "fun ethusd", "eth funding", "eth fun", "ethusd funding", "ethusd fun"]: raw, isDeprecated = "p eth funding", True
			elif raw in ["funding xrp", "fun xrp", "funding xrpusd", "fun xrpusd", "xrp funding", "xrp fun", "xrpusd funding", "xrpusd fun"]: raw, isDeprecated = "p xrp funding", True
			elif raw in ["funding bch", "fun bch", "funding bchusd", "fun bchusd", "bch funding", "bch fun", "bchusd funding", "bchusd fun"]: raw, isDeprecated = "p bch funding", True
			elif raw in ["funding ltc", "fun ltc", "funding ltcusd", "fun ltcusd", "ltc funding", "ltc fun", "ltcusd funding", "ltcusd fun"]: raw, isDeprecated = "p ltc funding", True
			elif raw in ["funding link", "fun link", "funding linkusd", "fun linkusd", "link funding", "link fun", "linkusd funding", "linkusd fun"]: raw, isDeprecated = "p link funding", True
			elif raw in ["oi xbt", "oi xbtusd", "ov xbt", "ov xbtusd"]: raw, isDeprecated = "p xbt oi", True
			elif raw in ["oi eth", "oi ethusd", "ov eth", "ov ethusd"]: raw, isDeprecated = "p eth oi", True
			elif raw in ["oi xrp", "oi xrpusd", "ov xrp", "ov xrpusd"]: raw, isDeprecated = "p xrp oi", True
			elif raw in ["oi bch", "oi bchusd", "ov bch", "ov bchusd"]: raw, isDeprecated = "p bch oi", True
			elif raw in ["oi ltc", "oi ltcusd", "ov ltc", "ov ltcusd"]: raw, isDeprecated = "p ltc oi", True
			elif raw in ["oi link", "oi linkusd", "ov link", "ov linkusd"]: raw, isDeprecated = "p link oi", True

		shortcutUsed = initial != raw

		if raw in ["!help", "?help"]: raw = "alpha help"
		elif raw in ["!invite", "?invite"]: raw = "alpha invite"
		elif raw in ["c internals", "c internal"]: raw = "c uvol-dvol w, tick, dvn-decn, pcc d line"
		elif raw in ["c btc vol"]: raw = "c bvol"
		elif raw in ["c mcap"]: raw = "c total nv"
		elif raw in ["c alt mcap"]: raw = "c total2 nv"
		elif raw in ["hmap"]: raw = "hmap change"
		elif raw in ["flow"]: raw = "flow options"
		elif raw in ["p gindex", "p gi", "p findex", "p fi", "p fgindex", "p fgi", "p gfindex", "p gfi"]: raw = "p am fgi"
		elif raw in ["c gindex", "c gi", "c findex", "c fi", "c fgindex", "c fgi", "c gfindex", "c gfi"]: raw = "c am fgi"
		elif raw in ["c nvtr", "c nvt", "c nvt ratio", "c nvtratio"]: raw = "c wc nvt"
		elif raw in ["c drbns", "c drbn", "c rbns", "c rbn", "c dribbon", "c difficultyribbon"]: raw = "c wc drbn"
		elif raw in ["p fut", "p futs", "p futures"]: raw = "p xbtz20, xbth21"

		raw = raw.replace("line break", "break")

		return raw, shortcutUsed, isDeprecated

	@staticmethod
	def seconds_until_cycle(every=15, offset=0):
		n = datetime.datetime.now().astimezone(pytz.utc)
		return (every - (n.second + offset) % every) - ((time.time() * 1000) % 1000) / 1000

	@staticmethod
	def get_accepted_timeframes(t):
		acceptedTimeframes = []
		for timeframe in ["1m", "2m", "3m", "5m", "10m", "15m", "20m", "30m", "1H", "2H", "3H", "4H", "6H", "8H", "12H", "1D"]:
			if t.second % 60 == 0 and (t.hour * 60 + t.minute) * 60 % Utils.get_frequency_time(timeframe) == 0:
				acceptedTimeframes.append(timeframe)
		return acceptedTimeframes

	@staticmethod
	def get_frequency_time(t):
		if t == "1D": return 86400
		elif t == "12H": return 43200
		elif t == "8H": return 28800
		elif t == "6H": return 21600
		elif t == "4H": return 14400
		elif t == "3H": return 10800
		elif t == "2H": return 7200
		elif t == "1H": return 3600
		elif t == "30m": return 1800
		elif t == "20m": return 1200
		elif t == "15m": return 900
		elif t == "10m": return 600
		elif t == "5m": return 300
		elif t == "3m": return 180
		elif t == "2m": return 120
		elif t == "1m": return 60

	@staticmethod
	def timestamp_to_date(timestamp):
		return datetime.datetime.utcfromtimestamp(timestamp).strftime("%m. %d. %Y, %H:%M")

	@staticmethod
	def get_current_date():
		return datetime.datetime.now().astimezone(pytz.utc).strftime("%m. %d. %Y, %H:%M:%S")
