# How to contribute

## Development

Install the project dependencies:

```sh
python3 -m pip install -e '.[dev]'
pre-commit install
```

Run the tests:

```sh
python3 -m pytest
```

## Publishing

1. Update the version number in pyproject.toml

2. Push the changes to the main branch

3. Publish to PyPi:

    ```shell
    export FLIT_USERNAME=__token__
    export FLIT_PASSWORD=<your-pypi-token>
    flit publish
    ```
