from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email", 'age', 'gender')}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    list_display = ('email', 'username', 'gender', 'age', )
    list_filter = ('is_active', 'gender', )
    search_fields = ('email', 'username', 'first_name', 'last_name', )

