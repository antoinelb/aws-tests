async def test_ping(client):
    resp = await client.get("/ping")
    assert resp.status_code == 200
