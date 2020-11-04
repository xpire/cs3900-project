from typing import Dict

from fastapi.testclient import TestClient
from src.core.config import settings

"""
#!/bin/sh
# husky

# Created by Husky v4.3.0 (https://github.com/typicode/husky#readme)
#   At: 11/2/2020, 3:07:16 AM
#   From: /home/yeet/sandbox/COMP3900/project/capstone-project-comp3900-f13a-ecksdee/web/node_modules/husky (https://github.com/typicode/husky#readme)

. "$(dirname "$0")/husky.sh"
"""


def test_random_template(client: TestClient):
    assert True == True
    # assert False


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
