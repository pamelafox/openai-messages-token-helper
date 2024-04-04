# pytest-axe-playwright-snapshot

A pytest plugin that runs Axe-core on Playwright pages and takes snapshots of the results.

## Installation

1. Install the plugin:

    ```sh
    python3 -m pip install pytest-axe-playwright-snapshot
    ```

2. Install Playwright browsers:

    ```sh
    python3 -m playwright install --with-deps
    ```

## Usage

In your tests, use the `page` fixture from pytest-playwright along with our plugin's`axe_pytest_snapshot` fixture. Once you've navigated to a page, call `axe_pytest_snapshot` with the `page` fixture as an argument:

```python
from playwright.sync_api import Page

def test_violations(page: Page, axe_pytest_snapshot):
    page.goto("https://www.example.com")
    axe_pytest_snapshot(page)
```

When you run a test for the first time, you must tell it explicitly to save a snapshot:

```sh
pytest --snapshot-update
```

The plugin will take a snapshot of the page and save it to a file in the `snapshots` directory. The snapshot directory will be named after the test function, and the file will be named 'violations.txt'.

On subsequent runs, the plugin will compare the latest snapshot against the snapshot and report any difference in the violations.
