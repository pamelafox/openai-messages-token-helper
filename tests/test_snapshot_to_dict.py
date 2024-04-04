from pytest_axe_playwright_snapshot import snapshot_to_dict


def test_empty_string():
    assert snapshot_to_dict("") == {}


def test_single_line():
    assert snapshot_to_dict("html-has-lang (serious) : 1") == {"html-has-lang (serious)": 1}


def test_multiple_lines():
    assert snapshot_to_dict("html-has-lang (serious) : 1\ncolor-contrast (moderate) : 2") == {
        "html-has-lang (serious)": 1,
        "color-contrast (moderate)": 2,
    }
