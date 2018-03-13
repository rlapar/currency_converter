import pytest

from currency_converter.converter import CurrencyConverter, InvalidCurrencyError, AmbiguousCurrencyError

AMBIGUOUS_CURRENCY = '$'
INVALID_CURRENCY = 'INVALID_CURRENCY'
VALID_CURRENCY = 'EUR'
VALID_CURRENCY_2 = 'USD'

class TestConverter(object):
    def setup_method(self):
        self._converter = CurrencyConverter()

    def test_abiguous_currency(self):
        with pytest.raises(AmbiguousCurrencyError):
            self._converter.convert(1, AMBIGUOUS_CURRENCY)
        with pytest.raises(AmbiguousCurrencyError):
            self._converter.convert(1, VALID_CURRENCY, AMBIGUOUS_CURRENCY)

    def test_invalid_currency(self):
        with pytest.raises(InvalidCurrencyError):
            self._converter.convert(1, INVALID_CURRENCY)
        with pytest.raises(InvalidCurrencyError):
            self._converter.convert(1, VALID_CURRENCY, INVALID_CURRENCY)

    def test_negative_amount(self):
        with pytest.raises(ValueError):
            self._converter.convert(-2, VALID_CURRENCY, VALID_CURRENCY_2)

    def test_valid_currency_only_input(self):
        conversion = self._converter.convert(1, VALID_CURRENCY)
        assert 'input' in conversion.keys()
        assert 'output' in conversion.keys()
        assert 'amount' in conversion['input'].keys()
        assert 'currency' in conversion['input'].keys()
        assert conversion['input']['amount'] == 1
        assert conversion['input']['currency'] == VALID_CURRENCY

    def test_valid_currency(self):
        conversion = self._converter.convert(1, VALID_CURRENCY, VALID_CURRENCY_2)
        assert 'input' in conversion.keys()
        assert 'output' in conversion.keys()
        assert 'amount' in conversion['input'].keys()
        assert 'currency' in conversion['input'].keys()
        assert VALID_CURRENCY_2 in conversion['output'].keys()
        assert conversion['input']['amount'] == 1
        assert conversion['input']['currency'] == VALID_CURRENCY

