from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from propylon_document_manager.castorage import CAStorage


class User(AbstractUser):
    """
    Default custom user model for Propylon Document Manager.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})


class FileVersion(models.Model):
    uploaded_file = models.FileField(CAStorage(location="files"), upload_to="files", null=True)
    path = models.fields.CharField(max_length=1024, db_index=True)
    content_type = models.fields.CharField(max_length=255, null=True)
    file_name = models.fields.CharField(max_length=512)
    version_number = models.fields.IntegerField()
    archived = models.fields.BooleanField(default=False, db_index=True)
    user = models.ForeignKey("User", related_name="uploaded_files", on_delete=models.SET_NULL, blank=True, null=True)
