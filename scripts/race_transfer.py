from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

import httpx

BASE_URL = "http://localhost:8000"


def transfer(parcel_id: str, attempt: int) -> int:
    payload = {
        "owner_tax_number": f"{attempt:09d}",
        "request_id": str(uuid4()),
    }
    response = httpx.post(f"{BASE_URL}/parcels/{parcel_id}/transfer", json=payload, timeout=10)
    return response.status_code


def validate_transfer_statuses(statuses: list[int]) -> None:
    if not statuses or any(not 200 <= status < 300 for status in statuses):
        raise SystemExit(f"TRANSFER FAILURE: expected successful transfers, got {statuses}")


def main() -> None:
    created = httpx.post(
        f"{BASE_URL}/parcels",
        json={"code": f"RACE-{uuid4().hex[:8]}", "owner_tax_number": "100000000", "area": 1.0},
        timeout=10,
    )
    created.raise_for_status()
    parcel_id = created.json()["id"]

    with ThreadPoolExecutor(max_workers=20) as executor:
        statuses = list(executor.map(lambda n: transfer(parcel_id, n), range(20)))

    history = httpx.get(f"{BASE_URL}/parcels/{parcel_id}/ownership-history", timeout=10)
    if history.status_code == 404:
        raise SystemExit("Race probe unavailable: implement the demo endpoints first")
    history.raise_for_status()
    validate_transfer_statuses(statuses)
    active = [item for item in history.json() if item["valid_until"] is None]

    print(f"transfer statuses: {statuses}")
    print(f"active owners: {len(active)}")
    if len(active) != 1:
        raise SystemExit("INVARIANT VIOLATED: expected exactly one active owner")
    print("PROBE PASSED: successful transfers and one active owner in this run")


if __name__ == "__main__":
    main()

