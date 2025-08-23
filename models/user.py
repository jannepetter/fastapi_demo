from tortoise import fields
from tortoise.models import Model
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()


class User(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=50)
    created_at = fields.DatetimeField(auto_now_add=True)
    email = fields.CharField(max_length=50)
    password = fields.CharField(max_length=128)
    is_superuser = fields.BooleanField(default=False)
    is_staff = fields.BooleanField(default=False)

    def __str__(self):
        return self.name

    def set_password(self, raw_password: str):
        """Hash and store the password"""
        self.password = ph.hash(raw_password)

    def verify_password(self, raw_password: str) -> bool:
        """Check password against the hash"""
        try:
            return ph.verify(self.password, raw_password)
        except VerifyMismatchError:
            return False

    class Meta:
        table = "users"
