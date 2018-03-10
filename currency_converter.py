#!/usr/bin/env python3

import json
import sys

import click

from converter import CurrencyConverter, InvalidCurrencyError, AmbiguousCurrencyError

@click.command()
@click.option('--amount', '-a', required=True, type=float, help='amount to convert')
@click.option('--input_currency', '-i', required=True, help='input currency - 3 letters name or currency symbol')
@click.option('--output_currency', '-o', help='requested/output currency - 3 letters name or currency symbol')
def main(amount, input_currency, output_currency):
    converter = CurrencyConverter()
    try:
        conversion = converter.convert(amount, input_currency, output_currency)
    except ValueError as e:
        click.echo(e, err=True)
        sys.exit(1)
    except InvalidCurrencyError as e:
        click.echo(e.message, err=True)
        sys.exit(1)
    except AmbiguousCurrencyError as e:
        click.echo(e.message, err=True)
        sys.exit(1)
    print(json.dumps(conversion, indent=4, sort_keys=True))

if __name__ == '__main__':
    main()