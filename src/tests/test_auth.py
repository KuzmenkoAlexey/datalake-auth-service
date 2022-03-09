from uuid import uuid4

import httpx
import pytest
from faker import Faker

from api.app import get_application

fake = Faker()


@pytest.mark.asyncio
async def test_valid_register(event_loop):
    email = fake.ascii_email()
    password = str(uuid4())
    app = get_application(event_loop)
    async with httpx.AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.post(
            "/auth/register",
            json={
                "email": email,
                "password": password,
            },
        )
        assert response.status_code == 201, response.content
        register_data = response.json()
        user_id = register_data.pop("id")
        expected_data = {
            "email": email,
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "first_name": "",
            "last_name": "",
        }
        assert expected_data == register_data
        response = await async_client.post(
            "/auth/jwt/login",
            data={
                "username": email,
                "password": password,
            },
        )
        assert response.status_code == 200, response.content
        login_data = response.json()
        assert set(login_data.keys()) == {"access_token", "token_type"}
        access_token = login_data["access_token"]

        response = await async_client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200, response.content
        me_data = response.json()
        expected_data["id"] = user_id
        assert me_data == expected_data
