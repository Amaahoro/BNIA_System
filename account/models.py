from django.utils.safestring import mark_safe
from django.core.validators import FileExtensionValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.db import models

from management.models import Commune

from . manager import UserManager


# Create your models here.
class User(AbstractUser):
    class Gender(models.TextChoices):
        SELECT = "", "Select Gender"
        MALE = "Male", "Male"
        FEMALE = "Female", "Female"

    first_name = models.CharField(verbose_name="First Name", max_length=50, blank=False)
    last_name = models.CharField(verbose_name="Last Name", max_length=50, blank=False)
    email = models.EmailField(verbose_name="Email", max_length=255, unique=True, blank=False)
    gender = models.CharField(verbose_name="Gender", choices=Gender.choices, default=Gender.SELECT, max_length=10)
    is_chief_commune = models.BooleanField(verbose_name="Is Chief Commune", default=False)
    is_nationalAdministrator = models.BooleanField(verbose_name="Is National Administrator", default=False)
    commune = models.ForeignKey(Commune, verbose_name="Commune in charge", related_name="chiefs", on_delete=models.SET_NULL, blank=True, null=True)
    phone = PhoneNumberField(verbose_name="Phone Number", blank=True, null=True)
    profilePicture = models.ImageField(
        verbose_name="Image",
        upload_to="profile/images/",
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        blank=True, null=True
    )

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    # update django about user model
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def image(self):
        return mark_safe('<img src="/../../media/%s" width="70" />' % (self.profilePicture))

    image.allow_tags = True

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
