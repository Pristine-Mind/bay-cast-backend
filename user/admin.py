from django.contrib import admin

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from user.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    # verbose_name_plural = _("user profile")
    fk_name = "user"
    # readonly_fields = ("last_frontend_login",)


class GoUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, GoUserAdmin)
