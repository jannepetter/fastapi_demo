from tortoise import fields
from tortoise.models import Model


class Role(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=50)


class Tenant(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=50)

    class Meta:
        ordering = ["id"]


class TenantUser(Model):
    id = fields.IntField(primary_key=True)
    tenant = fields.ForeignKeyField(
        "models.Tenant", on_delete=fields.CASCADE, related_name="tenant_users"
    )
    user = fields.ForeignKeyField(
        "models.User", on_delete=fields.CASCADE, related_name="tenant_users"
    )


class TenantUserRole(Model):
    id = fields.IntField(primary_key=True)

    tenant_user = fields.ForeignKeyField(
        "models.TenantUser", on_delete=fields.CASCADE, related_name="tenant_user_roles"
    )
    role = fields.ForeignKeyField("models.Role", on_delete=fields.CASCADE)
