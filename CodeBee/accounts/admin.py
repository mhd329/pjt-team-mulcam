from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(get_user_model(), UserAdmin)
UserAdmin.fieldsets += (("Nickname fields", {"fields":("nickname", "profile_picture",)}),)