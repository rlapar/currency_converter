#!/usr/bin/env python3

from forex_python.converter import CurrencyCodes, CurrencyRates

class InvalidCurrencyError(Exception):
    """Exception for not recognized currency."""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)

class AmbiguousCurrencyError(Exception):
    """Exception for ambiguous currency."""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)

class CurrencyConverter(object):  
    """Currency Converter class."""  
    def __init__(self):
        self._list_of_codes = list(CurrencyRates().get_rates('EUR').keys()) + [u'EUR']
        self._symbols = {}
        for code in self._list_of_codes: #create {symbol:[codes]} dict
            symbol = CurrencyCodes().get_symbol(code)
            if symbol not in self._symbols.keys():
                self._symbols[symbol] = []
            self._symbols[symbol].append(code)

    def _symbol_to_code(self, symbol):
        if symbol not in self._symbols:
            raise InvalidCurrencyError('Invalid currency {}'.format(symbol))
        if len(self._symbols[symbol]) > 1:
            raise AmbiguousCurrencyError('Ambiguous options for {}: {}'.format(symbol, self._symbols[symbol]))
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
        if input_currency not in self._list_of_codes: #try if it's a symbol or raise
            input_currency = self._symbol_to_code(input_currency)
        if output_currency and output_currency not in self._list_of_codes: #try if it's a symbol or raise
            output_currency = self._symbol_to_code(output_currency)

        conversion = {
            'input': {
                'amount': round(amount, precision),
                'currency': input_currency
            },
            'output': {}
        }
        if output_currency:
            conversion['output'][output_currency] = round(CurrencyRates().convert(input_currency, output_currency, amount), precision)
        else:
            for code in self._list_of_codes:
                if code != input_currency:
                    conversion['output'][code] = round(CurrencyRates().convert(input_currency, code, amount), precision)
        
        return conversion