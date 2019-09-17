from django.contrib import admin
from . import models as m
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(m.User, UserAdmin)
