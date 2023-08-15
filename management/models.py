from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from django.core.validators import FileExtensionValidator
from phonenumber_field.modelfields import PhoneNumberField


from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding



# Create your models here.
class Province(models.Model):
    province_name = models.CharField(verbose_name="Province Name", max_length=50, unique=True, blank=False)

    def __str__(self):
        return self.province_name


class Commune(models.Model):
    province = models.ForeignKey(Province, verbose_name="Province", related_name="communes", on_delete=models.CASCADE)
    commune_name = models.CharField(verbose_name="Commune Name", max_length=50, unique=True, blank=False)

    def __str__(self):
        return self.commune_name


class Colline(models.Model):
    commune = models.ForeignKey(Commune, verbose_name="Commune", related_name="collines", on_delete=models.CASCADE)
    colline_name = models.CharField(verbose_name="Colline Name", max_length=50, unique=True, blank=False)

    def __str__(self):
        return self.colline_name



class Citizen(models.Model):
    class Gender(models.TextChoices):
        SELECT = "", "Select Gender"
        MALE = "Male", "Male"
        FEMALE = "Female", "Female"

    first_name = models.CharField(verbose_name="First Name", max_length=50, blank=False)
    last_name = models.CharField(verbose_name="Last Name", max_length=50, blank=False)
    gender = models.CharField(verbose_name="Gender", choices=Gender.choices, default=Gender.SELECT, max_length=10)
    birth_place = models.ForeignKey(Colline, verbose_name="Resident Address", on_delete=models.SET_NULL, blank=True, null=True)
    nationality = models.CharField(verbose_name="Nationality", max_length=50, blank=False)
    nid_number = models.CharField(verbose_name="National ID Number", max_length=50, unique=True, blank=True)
    birthdate = models.DateField(verbose_name="Birthdate", blank=False)
    picture = models.ImageField(
        verbose_name="Image",
        upload_to="citizen/images/",
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        blank=True, null=True
    )
    createdDate = models.DateField(verbose_name="Created Date", auto_now_add=True)

    def image(self):
        return mark_safe('<img src="/../../media/%s" width="70" />' % (self.picture))

    image.allow_tags = True

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class CitizenParent(models.Model):
    class Parent(models.TextChoices):
        SELECT = "", "Select Parent"
        FATHER = "Father", "Father"
        MOTHER = "Mother", "Mother"

    citizen = models.ForeignKey(Citizen, verbose_name="Citizen", related_name="parents", on_delete=models.CASCADE)
    parent = models.CharField(verbose_name="Parent", choices=Parent.choices, default=Parent.SELECT, max_length=10)
    first_name = models.CharField(verbose_name="First Name", max_length=50, blank=True)
    last_name = models.CharField(verbose_name="Last Name", max_length=50, blank=True)

    def __str__(self):
        return "{} {}".format(self.citizen.first_name, self.citizen.last_name)


class IDCardRegistration(models.Model):
    citizen = models.ForeignKey(Citizen, verbose_name="Citizen", on_delete=models.CASCADE)
    resident_address = models.ForeignKey(Colline, verbose_name="Resident Address", related_name="registrations", on_delete=models.SET_NULL, blank=True, null=True)
    picture = models.ImageField(
        verbose_name="Citizen Image",
        upload_to="registration/citizen/images/",
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        blank=True, null=True
    )
    signature = models.BinaryField()  # Store the digital signature
    data_hash = models.BinaryField()  # Store the hash of the signed data
    registration_date = models.DateField(verbose_name="Registration Date", auto_now_add=True)

    def verify_signature(self, public_key):
        """
        Verify the digital signature using a public key.
        """
        verifier = public_key.verifier(
            self.signature,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        verifier.update(self.data_hash)
        return verifier.verify()

    def image(self):
        return mark_safe('<img src="/../../media/%s" width="70" />' % (self.picture))

    image.allow_tags = True

    def __str__(self):
        return "{} {}".format(self.citizen.first_name, self.citizen.last_name)



class LostIDCardReport(models.Model):
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    citizen = models.ForeignKey(Citizen, verbose_name="Citizen", related_name="lost_reports", on_delete=models.CASCADE)
    card_number = models.CharField(max_length=20, verbose_name="Lost Card ID number",)
    date_lost = models.DateField(verbose_name="When lost")
    description = models.TextField(verbose_name="Description")
    contact_info = PhoneNumberField(verbose_name="Contact Info", blank=True, null=True)
    created_date = models.DateField(verbose_name="Created Date", auto_now_add=True)

    def __str__(self):
        return f"Lost ID Card Report - Card Number: {self.card_number}, Citizen: {self.citizen}"