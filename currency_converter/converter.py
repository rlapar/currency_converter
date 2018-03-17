#!/usr/bin/env python3


class InvalidCurrencyError(Exception):
    """Exception for not recognized currency."""

    def __init__(self, message):
        self.message = message


class AmbiguousCurrencyError(Exception):
    """Exception for ambiguous currency."""

    def __init__(self, message):
        self.message = message


class CurrencyConverter(object):
    """Currency Converter class."""

    def __init__(self, currency_codes, currency_rates):
        """
        Args:
            currency_codes (forex_python.converter.CurrencyCodes)
            currency_rates (forex_python.converter.CurrencyRates)
        """
        self._currency_codes = currency_codes
        self._currency_rates = currency_rates
        self._list_of_codes = list(
            currency_rates.get_rates('EUR').keys()) + ['EUR']
        self._initialize_symbols_dict()

    def _initialize_symbols_dict(self):
        self._symbols = {}
        for code in self._list_of_codes:  # create {symbol:[codes]} dict
            symbol = self._currency_codes.get_symbol(code)
            if symbol not in self._symbols.keys():
                self._symbols[symbol] = []
            self._symbols[symbol].append(code)

    def symbol_to_code(self, symbol):
        """Substitute symbol with 3 letter currency code

        Args:
            symbol (str)
        Returns:
            str: 3 letter currency code
        Raises:
            InvalidCurrencyError if currency is not recognized 
            AmbiguousCurrencyError if currency symbol correspond to more than one currency
        """
        if symbol in self._list_of_codes:
            return symbol
        if symbol not in self._symbols:
            raise InvalidCurrencyError('Invalid currency {}'.format(symbol))
        if len(self._symbols[symbol]) > 1:
            raise AmbiguousCurrencyError(
                'Ambiguous options for {}: {}'.format(symbol, self._symbols[symbol]))
        return self._symbols[symbol][0]

    def convert(self, amount, input_currency, output_currency=None, precision=2):
        """Convert input currency to output currency or all known 
        currencies if output currency is None.

        Args:
            amount (float)
            input_currency (str)
            output_currency (str)
            precision (int)
        Returns:
            dict: 
        Raises: 
            ValueError if amount is negative
            InvalidCurrencyError if currency is not recognized 
            AmbiguousCurrencyError if currency symbol correspond to more than one currency
        """
        if not amount or amount < 0:
            raise ValueError('Amount must be a non-negative number')
        input_currency = self.symbol_to_code(input_currency)
        if output_currency:
            output_currency = self.symbol_to_code(output_currency)

        conversion = {}
        if output_currency:
            conversion[output_currency] = round(
                self._currency_rates.convert(input_currency, output_currency, amount), precision)
            return conversion

        for code in self._list_of_codes:
            if code != input_currency:
                conversion[code] = round(
                    self._currency_rates.convert(input_currency, code, amount), precision)

        return conversion
