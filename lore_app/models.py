from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="media/profile_pics", blank=True)

    def __str__(self):
        return self.user.username


class Attack(models.Model):
    datetime = models.DateTimeField()
    host = models.CharField(max_length=20)
    src = models.CharField(max_length=20)
    proto = models.CharField(max_length=5)
    type = models.IntegerField(null=True)
    spt = models.IntegerField(null=True)
    dpt = models.IntegerField(null=True)
    srcstr = models.GenericIPAddressField()
    cc = models.CharField(max_length=5)
    country = models.CharField(max_length=50)
    locale = models.CharField(max_length=200, null=True)
    localeabbr = models.CharField(max_length=10, null=True)
    postalcode = models.CharField(max_length=10, null=True)
    latitude = models.DecimalField(decimal_places=5, max_digits=10, null=True)
    longitude = models.DecimalField(decimal_places=5, max_digits=10, null=True)

