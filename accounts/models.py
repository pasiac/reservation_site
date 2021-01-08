from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, int_list_validator

class BusinessProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nip = models.CharField(max_length=10, validators=[int_list_validator(sep=''),MinLengthValidator(10),])
    verified = models.BooleanField(default=False)

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
class CreditCard(models.Model):
    number = models.CharField(max_length=64)
    expire_by = models.CharField(max_length=64)
    cvv = models.CharField(max_length=64)
    owner = CustomerProfile



# Sygnały w ktorych bedziemy dostawac jaki typ profilu wybral rejestrujacy sie i w zaleznosci od tego
# tworzyc odpowiedni profil biznesowy/konsumencki 
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()