# How to contribute

## Development

Install the project dependencies:

```sh
python3 -m pip install -e '.[dev]'
python3 -m playwright install --with-deps
pre-commit install
```

Run the tests:

```sh
python3 -m pytest
```

## Publishing

Publish to PyPi:

```sh
flit publish
```