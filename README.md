Currency Converter task for kiwi.com
===================
[![Build Status](https://travis-ci.com/rlapar/currency_converter.svg?token=vUsoGc5nHkiRLYxMxxyK&branch=master)](https://travis-ci.com/rlapar/currency_converter)

Assignment: https://gist.github.com/MichalCab/c1dce3149d5131d89c5bbddbc602777c

Developed on Ubuntu 16.04 LTS

# Installation
```
python3 setup.py install
```
# Tests
```
python3 setup.py test
```

# CLI Usage
Installation will create executable bin `curreny_converter`.
```
Usage: currency_converter [OPTIONS]

Options:
  -a, --amount FLOAT          amount to convert  [required]
  -i, --input_currency TEXT   input currency - 3 letters name or currency
                              symbol  [required]
  -o, --output_currency TEXT  requested/output currency - 3 letters name or
                              currency symbol
  --help                      Show this message and exit.

```
# Web API

Start uWSGI server:

```
cd currency_converter
uwsgi --ini wsgi_config.ini
```
Config available at `currency_converter/wsgi_config.ini`.
By default wsgi communicate with web server via socket `app.socket`.

**Author**: Radovan Lapár

