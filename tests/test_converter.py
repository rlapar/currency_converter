from forex_python.converter import CurrencyCodes
from forex_python.converter import CurrencyRates
from mock import Mock
import pytest

from currency_converter.converter import AmbiguousCurrencyError
from currency_converter.converter import CurrencyConverter
from currency_converter.converter import InvalidCurrencyError

AMBIGUOUS_CURRENCY = '$'
INVALID_CURRENCY = 'INVALID_CURRENCY'
VALID_CURRENCY = 'EUR'
VALID_CURRENCY_2 = 'USD'
VALID_CURRENCY_3 = 'CAD'
CONVERSION_RATES = {
    VALID_CURRENCY: {
        VALID_CURRENCY: 1,  # EUR -> EUR
        VALID_CURRENCY_2: 5,  # EUR -> USD
        VALID_CURRENCY_3: 7  # EUR -> CAD
    }
}


def cc_get_symbol_se(code):
    values = {VALID_CURRENCY: '€', VALID_CURRENCY_2: AMBIGUOUS_CURRENCY,
              VALID_CURRENCY_3: AMBIGUOUS_CURRENCY}
    return values[code]


def cr_convert_se(input_currency, output_currency, amount):
    return CONVERSION_RATES[input_currency][output_currency] * amount


class TestConverter(object):
    def setup_method(self):
        mock_cc = Mock(spec=CurrencyCodes)
        mock_cr = Mock(spec=CurrencyRates)
        mock_cr.get_rates.return_value = {
            VALID_CURRENCY_2: 0,
            VALID_CURRENCY_3: 0
        }
        mock_cc.get_symbol.side_effect = cc_get_symbol_se
        mock_cr.convert.side_effect = cr_convert_se
        self._converter = CurrencyConverter(mock_cc, mock_cr)

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
            self._converter.convert(-2, VALID_CURRENCY)
        with pytest.raises(ValueError):
            self._converter.convert(-2, VALID_CURRENCY, VALID_CURRENCY_2)

    def test_valid_currency_only_input(self):
        conversion = self._converter.convert(3, VALID_CURRENCY)
        assert conversion[VALID_CURRENCY_2] == 15
        assert conversion[VALID_CURRENCY_3] == 21
        assert len(conversion.keys()) == 2

    def test_valid_currency(self):
        conversion = self._converter.convert(
            3, VALID_CURRENCY, VALID_CURRENCY_2)
        assert conversion[VALID_CURRENCY_2] == 15
        assert len(conversion.keys()) == 1
