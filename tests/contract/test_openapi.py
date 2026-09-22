from parcel_api.main import app


def test_openapi_preserves_current_parcel_contract() -> None:
    schema = app.openapi()

    assert "/parcels" in schema["paths"]
    assert "/parcels/{parcel_id}" in schema["paths"]
    assert "get" in schema["paths"]["/parcels/{parcel_id}"]
    assert "post" in schema["paths"]["/parcels"]

