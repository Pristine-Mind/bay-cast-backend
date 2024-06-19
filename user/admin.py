from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
#from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from django.contrib.auth.models import User
import user.models as models
from django.utils.translation import gettext_lazy as _


class ProfileInline(admin.StackedInline):
    model = models.Profile
    can_delete = False
    verbose_name_plural = _("user profile")
    fk_name = "user"


class GoUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    # list_filter = (
    #     ("profile__country__region", RelatedDropdownFilter),
    #     ("profile__country", RelatedDropdownFilter),
    #     ("groups", RelatedDropdownFilter),
    #     "is_staff",
    #     "is_superuser",
    #     "is_active",
    # )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, GoUserAdmin)
