import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_create_session(client):
    response = await client.post("/api/v1/sessions")
    assert response.status_code == 201
    data = response.json()
    assert "session_id" in data


@pytest.mark.asyncio
async def test_upload_non_pdf_rejected(client):
    response = await client.post("/api/v1/sessions")
    session_id = response.json()["session_id"]

    response = await client.post(
        f"/api/v1/sessions/{session_id}/documents",
        files={"file": ("test.txt", b"hello", "text/plain")},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_session_not_found(client):
    response = await client.post(
        "/api/v1/sessions/nonexistent/documents",
        files={"file": ("test.pdf", b"%PDF-1.4", "application/pdf")},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_nonexistent_session(client):
    response = await client.delete("/api/v1/sessions/nonexistent")
    assert response.status_code == 404
