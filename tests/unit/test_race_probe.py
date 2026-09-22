import importlib.util
from pathlib import Path

import pytest

PROBE_PATH = Path(__file__).resolve().parents[2] / "scripts" / "race_transfer.py"
spec = importlib.util.spec_from_file_location("race_probe", PROBE_PATH)
assert spec is not None and spec.loader is not None
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


@pytest.mark.parametrize("statuses", [[], [500] * 20, [200, 409], [404] * 20])
def test_failed_transfers_cannot_pass_probe(statuses: list[int]) -> None:
    with pytest.raises(SystemExit, match="TRANSFER FAILURE"):
        probe.validate_transfer_statuses(statuses)


def test_successful_transfer_statuses_pass_gate() -> None:
    probe.validate_transfer_statuses([200, 201, 204])
