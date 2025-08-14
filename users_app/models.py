from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
import shortuuid

USER_ROLE_CHOICES = [
    ("superadmin", "Super Admin"),
    ("admin", "Admin"),
    ("agent", "Agent"),
]

class UserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'superadmin')
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    phone_number = PhoneNumberField(_("phone number"), blank=True, null=True)
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={"unique": _("A user with that email address already exists.")} 
    )
    password = models.CharField(_("password"), max_length=128)
    role = models.CharField(_("role"), max_length=10, choices=USER_ROLE_CHOICES)
    is_active = models.BooleanField(_("active"), default=True)
    last_login = models.DateTimeField(_("last login"), blank=True, null=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def clean(self):
        for field in ["first_name", "last_name", "email"]:
            value = getattr(self, field, None)
            if value:
                setattr(self, field, value.lower())
    
    class Meta:
        db_table = "users"

class Tenant(models.Model):
    key = models.CharField(
        _("key"),
        max_length=22,
        unique=True,
        default=shortuuid.uuid,
    )
    name = models.CharField(_("name"), max_length=255)
    address = models.TextField(_("address"))
    contact_number = PhoneNumberField(_("contact number"), blank=True, null=True)
    is_active = models.BooleanField(_("active"), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        db_table = "tenants"

class AdminProfile(models.Model):
    user = models.OneToOneField(
        User,
        related_name="admin_profile",
        on_delete=models.CASCADE,
        verbose_name='user'
    )
    tenant = models.ForeignKey(
        Tenant, 
        related_name="admin_profiles", 
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='tenant'
    )
    
    class Meta:
        db_table = "admin_profiles"

class AgentProfile(models.Model):
    user = models.OneToOneField(
        User,
        related_name="agent_profile",
        on_delete=models.CASCADE,
        verbose_name='user'
    )
    tenant = models.ForeignKey(
        Tenant,
        related_name="agent_profiles",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='tenant'
    )
    is_online = models.BooleanField(_("online"), default=False)

    class Meta:
        db_table = "agent_profiles"