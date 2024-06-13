from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    """
    Profile model to extend the user model with additional user-specific information.

    Attributes:
        user (OneToOneField): A one-to-one relationship with the user model.
        user_type (CharField): Stores the type of user, restricted to predefined choices.
    """
    class UserType(models.TextChoices):
        """
        Enumeration to define different types of users.

        Attributes:
            ADMIN (str): Represents an admin user.
            OPERATOR (str): Represents an operator user.
        """
        ADMIN = 'admin', _('Admin')
        OPERATOR = 'operator', _('Operator')

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        on_delete=models.CASCADE,
        related_name='profile',
        primary_key=True,
        editable=False,
    )
    user_type = models.CharField(
        verbose_name=_('Type of user'),
        max_length=255,
        choices=UserType.choices,
    )

    def __str__(self):
        return self.user.username
