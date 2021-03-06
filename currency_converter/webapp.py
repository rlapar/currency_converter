#!/usr/bin/env python3

from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
from forex_python.converter import CurrencyCodes
from forex_python.converter import CurrencyRates

from converter import AmbiguousCurrencyError
from converter import CurrencyConverter
from converter import InvalidCurrencyError

application = Flask(__name__)


@application.errorhandler(400)
def bad_request(message=None):
    response = jsonify({
        'error': message
    })
    response.status_code = 400
    return response


@application.route('/currency_converter')
def currency_converter():
    amount = request.args.get('amount', type=float)
    input_currency = request.args.get('input_currency')
    output_currency = request.args.get('output_currency')

    converter = CurrencyConverter(CurrencyCodes(), CurrencyRates())
    try:
        conversion = {
            'input': {
                'amount': round(amount, 2),
                'currency': converter.symbol_to_code(input_currency)
            },
            'output': converter.convert(amount, input_currency, output_currency)
        }
    except ValueError as e:
        return bad_request(str(e))
    except (InvalidCurrencyError, AmbiguousCurrencyError) as e:
        return bad_request(e.message)

    return jsonify(conversion)


if __name__ == '__main__':
    application.run(
                host='0.0.0.0',
                port=5000
        )
