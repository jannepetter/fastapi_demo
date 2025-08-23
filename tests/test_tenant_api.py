import pytest
from models import User, Tenant, TenantUser, TenantUserRole, Role
from tests.tools import generate_auth_headers


@pytest.fixture
async def tenant_fixture():

    user1 = await User.create(name="John", email="juu@juu.fi", password="jeps")
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
async def test_get_tenants(client, tenant_fixture):

    basic_user = tenant_fixture["tenant1_user1"]
    headers = await generate_auth_headers(basic_user)
    response = await client.get("/api/base/tenants", headers=headers)
    data = response.json()

    assert data == [
        {
            "id": data[0]["id"],
            "name": "Test tenant",
        },
        {
            "id": data[1]["id"],
            "name": "Other tenant",
        },
    ]


@pytest.mark.anyio
async def test_get_tenant_users_with_basic_account(client, tenant_fixture):

    tenant = tenant_fixture["tenant"]
    basic_user = tenant_fixture["tenant1_user1"]
    headers = await generate_auth_headers(basic_user)
    response = await client.get(f"/api/base/tenant_users/{tenant.id}", headers=headers)
    data = response.json()

    assert response.status_code == 403
    assert data == {"detail": "Not authorized"}


@pytest.mark.anyio
async def test_get_tenant_users(client, tenant_fixture):

    tenant = tenant_fixture["tenant"]
    manager_user = tenant_fixture["tenant1_user2"]
    headers = await generate_auth_headers(manager_user)
    response = await client.get(f"/api/base/tenant_users/{tenant.id}", headers=headers)
    data = response.json()

    assert data == [
        {"id": data[0]["id"], "user_id": data[0]["user_id"], "tenant_id": tenant.id},
        {"id": data[1]["id"], "user_id": data[1]["user_id"], "tenant_id": tenant.id},
    ]
