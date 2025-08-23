from fastapi import APIRouter
from models import Tenant, TenantUser

base_router = APIRouter()


@base_router.get("/tenants")
async def get_tenants():
    tenants = await Tenant.all()
    return tenants


@base_router.get("/tenant_users/{tenant_id}")
async def get_tenant_users(tenant_id):
    tenant_users = await TenantUser.filter(tenant_id=tenant_id)
    return tenant_users
