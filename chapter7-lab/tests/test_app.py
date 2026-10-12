def test_health(client):
    assert client.get("/health").get_json() == {"status": "ok"}


def test_item_lookup(client):
    resp = client.get("/items", query_string={"name": "rfid-reader"})
    assert resp.status_code == 200
    assert resp.get_json() == [{"id": 2, "name": "rfid-reader", "qty": 12}]


def test_unknown_item_returns_empty_list(client):
    assert client.get("/items", query_string={"name": "forklift"}).get_json() == []


def test_daily_report(client):
    resp = client.get("/reports")
    assert resp.status_code == 200
    assert b"Daily stock report" in resp.data
    resp.close()
