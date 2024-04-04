from playwright.sync_api import Page


def test_violations_same(page: Page, axe_pytest_snapshot):
    page.goto("https://www.example.com")
    axe_pytest_snapshot(page)


def test_violations_new_from_empty(page: Page, axe_pytest_snapshot):
    page.goto("https://www.example.com")
    try:
        axe_pytest_snapshot(page)
    except AssertionError as err:
        assert (
            str(err)
            == """\
New violations found: html-has-lang (serious), landmark-one-main (moderate), region (moderate)
That's bad news! 😱 Either fix the issue or run `pytest --snapshot-update` to update the snapshots.
Rule Violated:
html-has-lang - Ensures every HTML document has a lang attribute
	URL: https://dequeuniversity.com/rules/axe/4.4/html-has-lang?application=axeAPI
	Impact Level: serious
	Tags: ['cat.language', 'wcag2a', 'wcag311', 'ACT']
	Elements Affected:


	1)	Target: html
		Snippet: <html>
		Messages:
		* The <html> element does not have a lang attribute
Rule Violated:
landmark-one-main - Ensures the document has a main landmark
	URL: https://dequeuniversity.com/rules/axe/4.4/landmark-one-main?application=axeAPI
	Impact Level: moderate
	Tags: ['cat.semantics', 'best-practice']
	Elements Affected:


	1)	Target: html
		Snippet: <html>
		Messages:
		* Document does not have a main landmark
Rule Violated:
region - Ensures all page content is contained by landmarks
	URL: https://dequeuniversity.com/rules/axe/4.4/region?application=axeAPI
	Impact Level: moderate
	Tags: ['cat.keyboard', 'best-practice']
	Elements Affected:


	1)	Target: div
		Snippet: <div>    <h1>Example Domain</h1>    <p>This domain is for use in illustrative examples in documents. You may use this    domain in literature without prior coordination or asking for permission.</p>    <p><a href="https://www.iana.org/domains/example">More information...</a></p></div>
		Messages:
		* Some page content is not contained by landmarks
"""
        )


def test_violations_new(page: Page, axe_pytest_snapshot):
    page.goto("https://www.example.com")
    try:
        axe_pytest_snapshot(page)
    except AssertionError as err:
        assert (
            str(err)
            == """\
New violations found: html-has-lang (serious)
That's bad news! 😱 Either fix the issue or run `pytest --snapshot-update` to update the snapshots.
Rule Violated:
html-has-lang - Ensures every HTML document has a lang attribute
	URL: https://dequeuniversity.com/rules/axe/4.4/html-has-lang?application=axeAPI
	Impact Level: serious
	Tags: ['cat.language', 'wcag2a', 'wcag311', 'ACT']
	Elements Affected:


	1)	Target: html
		Snippet: <html>
		Messages:
		* The <html> element does not have a lang attribute
"""
        )


def test_violations_fixed(page: Page, axe_pytest_snapshot):
    page.goto("https://www.example.com")
    try:
        axe_pytest_snapshot(page)
    except AssertionError as err:
        assert (
            str(err)
            == """\
Old violations no longer found: color-contrast (moderate).
That's good news! 🎉 Run `pytest --snapshot-update` to update the snapshots.
"""
        )


def test_violations_more_instances(page: Page, axe_pytest_snapshot):
    page.goto("https://www.example.com")
    try:
        axe_pytest_snapshot(page)
    except AssertionError as err:
        assert (
            str(err)
            == """\
Additional instances of existing violations were found: html-has-lang (serious)
That's bad news! 😱 Either fix the issue or run `pytest --snapshot-update` to update the snapshots.
Rule Violated:
html-has-lang - Ensures every HTML document has a lang attribute
	URL: https://dequeuniversity.com/rules/axe/4.4/html-has-lang?application=axeAPI
	Impact Level: serious
	Tags: ['cat.language', 'wcag2a', 'wcag311', 'ACT']
	Elements Affected:


	1)	Target: html
		Snippet: <html>
		Messages:
		* The <html> element does not have a lang attribute
"""
        )


def test_violations_fewer_instances(page: Page, axe_pytest_snapshot):
    page.goto("https://www.example.com")
    try:
        axe_pytest_snapshot(page)
    except AssertionError as err:
        assert (
            str(err)
            == """\
Fewer instances of existing violations were found: region (moderate).
That's good news! 🎉 Run `pytest --snapshot-update` to update the snapshots.
"""
        )
