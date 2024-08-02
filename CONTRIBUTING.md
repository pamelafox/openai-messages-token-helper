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

1. Update the CHANGELOG with description of changes

2. Update the version number in pyproject.toml

3. Push the changes to the main branch

4. Publish to PyPi:

    ```shell
    export FLIT_USERNAME=__token__
    export FLIT_PASSWORD=<your-pypi-token>
    flit publish
    ```
