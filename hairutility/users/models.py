import uuid
import secrets
import string
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from phonenumber_field.modelfields import PhoneNumberField
from localflavor.us.models import USZipCodeField, USStateField
from rest_framework.authtoken.models import Token
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase


class Company(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    state = USStateField(blank=True)
    city = models.CharField(max_length=255)
    zip_code = USZipCodeField(blank=True)
    phone_number = PhoneNumberField(blank=True)
    banner_image_url = models.URLField(max_length=500, blank=True)
    created = models.DateTimeField(default=timezone.now, blank=True)
    bio = models.CharField(max_length=500, blank=True)

    def save(self, *args, **kwargs):

        self.created = timezone.now()

        return super(Company, self).save(*args, **kwargs)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, is_stylist=False):
        """
        Creates and saves a user with the email as the username and a password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),

        )
        user.is_stylist = is_stylist

        # Token.objects.create(user=user)

        user.set_password(password)
        user.save(using=self._db)
        return user

    # Could have create_stylist_user

    def create_superuser(self, email, password, is_stylist=bool):
        """
        Creates and saves a superuser
        """
        user = self.create_user(
            email,
            password=password,

        )
        user.is_stylist = True
        user.is_admin = True
        user.save(using=self._db)
        return user

    #    def activate_user(**activation_ramblings):
    #         .... #Method ramblings that somehow gave us a user instance
    #     Token.objects.create(user=user)


phone_regex = RegexValidator(regex=r'^\+?\d{9,15}$', message="Please use a number in the format 000-000-0000")


@python_2_unicode_compatible
class User(AbstractBaseUser):

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(blank=True, max_length=70)
    last_name = models.CharField(blank=True, max_length=70)
    phone_number = PhoneNumberField(blank=True)
    profile_image_url = models.URLField(blank=True, max_length=500)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    USERNAME_FIELD = 'email'

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_stylist = models.BooleanField(default=False)
    company_pk = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # All admins are staff
        return self.is_admin


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    # If you only inherit GenericUUIDTaggedItemBase, you need to define
    # a tag field. e.g.
    # tag = models.ForeignKey(Tag, related_name="uuid_tagged_items", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class HairProfile(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name='hair_profiles', blank=True,
                             on_delete=models.CASCADE, editable=False)
    creator = models.CharField(max_length=100, default="")
    hairstyle_name = models.CharField(max_length=75, default="")
    first_image_url = models.URLField(max_length=300, default="")
    second_image_url = models.URLField(max_length=300, default="")
    third_image_url = models.URLField(max_length=300, default="")
    fourth_image_url = models.URLField(max_length=300, default="")
    profile_description = models.CharField(max_length=300, default="")
    gender = models.CharField(max_length=5, default="")
    length = models.CharField(max_length=6, default="")
    access_code = models.CharField(max_length=5, default="")
    created = models.DateTimeField(default=timezone.now, blank=True)
    is_displayable = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    tags = TaggableManager(blank=True, through=UUIDTaggedItem)

    def save(self, *args, **kwargs):

        if not self.id:
            self.created = timezone.now()

        if not self.creator:
            self.creator = "{} {}".format(self.user.first_name, self.user.last_name)

        self.access_code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        #     Problem is now they are stored in db

        return super(HairProfile, self).save(*args, **kwargs)
