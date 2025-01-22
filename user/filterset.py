import django_filters as filters
from django.contrib.auth.models import User

from user.models import Profile


class UserFilter(filters.FilterSet):
    username = filters.CharFilter(field_name="username", lookup_expr="icontains")
    role = filters.MultipleChoiceFilter(
        choices=Profile.UserType.choices,
        widget=filters.widgets.CSVWidget,
        field_name="profile__user_type",
    )

    class Meta:
        model = User
        fields = ()
