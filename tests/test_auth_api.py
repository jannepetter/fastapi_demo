import pytest
from models import User, Tenant, TenantUser, TenantUserRole, Role
from utils.tokens import decode_token


@pytest.fixture
async def tenant_fixture():

    user1 = User(name="John", email="juu@juu.fi")
    user1.set_password("jeps")
    await user1.save()

    user2 = await User.create(name="Mia", email="juu2@juu.fi", password="jeps")
    user3 = await User.create(name="jussipussi", email="juu3@juu.fi", password="jeps")

    tenant = await Tenant.create(name="Test tenant")
    tenant2 = await Tenant.create(name="Other tenant")

    tu1 = await TenantUser.create(tenant=tenant, user=user1)
    tu2 = await TenantUser.create(tenant=tenant, user=user2)
    tu3 = await TenantUser.create(tenant=tenant2, user=user3)

    user_role = await Role.create(name="user")
    manager_role = await Role.create(name="manager")

    tur = [
        TenantUserRole(tenant_user=tu1, role=user_role),
        TenantUserRole(tenant_user=tu2, role=manager_role),
        TenantUserRole(tenant_user=tu3, role=user_role),
    ]
    await TenantUserRole.bulk_create(tur)

    return {
        "tenant1_user1": user1,
        "tenant1_user2": user2,
        "tenant2_user1": user3,
        "tenant": tenant,
    }


@pytest.mark.anyio
async def test_login(client, tenant_fixture):

    tenant = tenant_fixture["tenant"]
    user = tenant_fixture["tenant1_user1"]

    data = {"username": "juu@juu.fi", "password": "jeps"}
    response = await client.post("/api/auth/login", json=data)
    refresh_token = response.cookies.get("refresh_token")
    data = response.json()

    access_token = data["access"]
    da = decode_token(access_token)
    assert da == {
        "data": {str(tenant.id): "user"},
        "exp": 1755951300,
        "user": {"id": user.id, "roles": []},
    }
    dr = decode_token(refresh_token)
    assert dr == {"exp": 1756036800, "user": {"id": user.id, "roles": []}}
