import functools

import pytest
from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import Page


def snapshot_to_dict(snapshot: str):
    snapshot_counts = {}
    for line in snapshot.split("\n"):
        if len(line) == 0:
            continue
        key, count = line.split(" : ")
        snapshot_counts[key] = int(count)
    return snapshot_counts


def compare_violations(new_snapshot, old_snapshot, new_results):
    new_counts = snapshot_to_dict(new_snapshot)
    old_counts = snapshot_to_dict(old_snapshot)
    seen_keys = set()
    keys_diff = {"added": set(), "removed": set(), "increased": set(), "decreased": set()}
    for key in old_counts:
        if key not in new_counts:
            keys_diff["removed"].add(key)
        elif new_counts[key] < old_counts[key]:
            keys_diff["decreased"].add(key)
        elif new_counts[key] > old_counts[key]:
            keys_diff["increased"].add(key)
        seen_keys.add(key)
    for key in new_counts:
        if key not in seen_keys:
            keys_diff["added"].add(key)
    good_msg = "That's good news! 🎉 Run `pytest --snapshot-update` to update the snapshots.\n"
    bad_msg = "That's bad news! 😱 Either fix the issue or run `pytest --snapshot-update` to update the snapshots.\n"
    message = ""
    for keys_name in keys_diff:
        keys_diff[keys_name] = sorted(keys_diff[keys_name])
    if len(keys_diff["added"]) > 0:
        message += f"New violations found: {', '.join(keys_diff['added'])}\n{bad_msg}"
        for violation in keys_diff["added"]:
            violation_id = violation.split(" (")[0]
            message += new_results.generate_report(violation_id=violation_id)
    if len(keys_diff["removed"]) > 0:
        message += f"Old violations no longer found: {','.join(keys_diff['removed'])}.\n{good_msg}"
    if len(keys_diff["increased"]) > 0:
        message += (
            f"Additional instances of existing violations were found: {','.join(keys_diff['increased'])}\n{bad_msg}"
        )
        for violation in keys_diff["increased"]:
            violation_id = violation.split(" (")[0]
            message += new_results.generate_report(violation_id=violation_id)
    if len(keys_diff["decreased"]) > 0:
        message += f"Fewer instances of existing violations were found: {','.join(keys_diff['decreased'])}.\n{good_msg}"
    return message


def pytest_addoption(parser):
    group = parser.getgroup("axe_playwright_snapshot")
    group.addoption(
        "--print-reports", action="store_true", default=False, help="Print full reports for violations to stdout"
    )


@pytest.fixture
def axe_pytest_snapshot(request, snapshot):
    print_reports = request.config.getoption("print_reports")

    def run_assert(page: Page):
        results = Axe().run(page)
        if print_reports:
            print(f"\n\n** {request.node.name} report from axe-playwright **")
            print(results.generate_report())
        snapshot.assert_match(
            results.generate_snapshot(), message_generator=functools.partial(compare_violations, new_results=results)
        )

    return run_assert
