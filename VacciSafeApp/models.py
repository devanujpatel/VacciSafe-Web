from django.db import models
from social_django import models as oauth_models
from django.contrib.auth.models import AbstractUser
# Create your models here.


# class User(AbstractUser):
#    pass


class Recipients(models.Model):
    # oauth_models.USER_MODEL
    user_fk = models.ForeignKey(oauth_models.USER_MODEL,
                                on_delete=models.CASCADE)
    fname = models.CharField(max_length=64, null=False)
    lname = models.CharField(max_length=64, null=False)
    dob = models.DateField(null=False)
    gender = models.CharField(max_length=3, null=False)

    class Meta:
        unique_together = ('user_fk', 'fname', 'lname',)


class Vaccines(models.Model):
    name = models.CharField(max_length=128, null=False)
    given_at_age_from_year = models.IntegerField(null=False)
    given_at_age_from_month = models.IntegerField(null=False)
    given_at_age_from_weeks = models.IntegerField(null=False)
    details = models.CharField(max_length=512, null=False)
    gender = models.CharField(max_length=10, null=False)


class VaccineRecords(models.Model):
    vaccine_fk = models.ForeignKey(Vaccines, on_delete=models.CASCADE)
    recipient_pk = models.ForeignKey(Recipients, on_delete=models.CASCADE)
    reminder_date = models.DateField(null=False)
    vac_taken_date = models.DateField(null=True)
