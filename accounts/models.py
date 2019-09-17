from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet_balance = models.PositiveIntegerField(default=0)
    hospital_id = models.CharField(
        max_length=12,
        validators=[RegexValidator(regex="^HOS[0-9]{6}$", message="The hospital ID must be unique")],
        unique=True,
    )
    is_patient = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email', 'hospital_id', 'first_name', 'last_name']

