from fastapi import APIRouter, Request
from models import Tenant, TenantUser
from utils.authentication import require_any_role

base_router = APIRouter()


@base_router.get("/tenants")
async def get_tenants():
    tenants = await Tenant.all()
    return tenants


@base_router.get("/tenant_users/{tenant_id}")
@require_any_role("manager")
async def get_tenant_users(tenant_id, request: Request):
    tenant_users = await TenantUser.filter(tenant_id=tenant_id)
    return tenant_users
