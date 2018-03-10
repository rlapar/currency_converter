#!/usr/bin/env python3

from flask import Flask, request, jsonify

from converter import CurrencyConverter, InvalidCurrencyError, AmbiguousCurrencyError

app = Flask(__name__)

@app.errorhandler(400)
def bad_request(message=None):
    response = jsonify({
        'error': message
    })
    response.status_code = 400
    return response

@app.route('/currency_converter')
def currency_converter():
    amount = request.args.get('amount', type=float)
    input_currency = request.args.get('input_currency')
    output_currency = request.args.get('output_currency')

    converter = CurrencyConverter()
    try:
        conversion = converter.convert(amount, input_currency, output_currency)
    except ValueError as e:
        return bad_request(str(e))
    except InvalidCurrencyError as e:
        return bad_request(e.message)
    except AmbiguousCurrencyError as e:
        return bad_request(e.message)

    return jsonify(conversion)

if __name__ == '__main__':
    app.run(
		host='0.0.0.0',
		port=5000,
		debug=True
	)