from typing import Dict

from fastapi.testclient import TestClient
from src.core.config import settings


def random_test_template(client: TestClient):
    r = client.get("/symbols")

    d = r.json()
    # INSERT MORE TESTS HERE
    assert r != None
    assert r.status_code == 200


# def test_get_access_token(client: TestClient) -> None:
#     login_data = {
#         "username": settings.FIRST_SUPERUSER,
#         "password": settings.FIRST_SUPERUSER_PASSWORD,
#     }
#     r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
#     tokens = r.json()
#     assert r.status_code == 200
#     assert "access_token" in tokens
#     assert tokens["access_token"]
