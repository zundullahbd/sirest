from django.db import models

# Create your models here.
from django.forms import ModelForm, Textarea
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class user(models.Model):
    provinsi = models.CharField('Provinsi', max_length=120, null=True)
    tarif_motor = models.CharField('Tarif Motor', max_length=120, blank=True)
    tarif_mobil = models.CharField('Tarif Mobil', max_length=120, blank=True)

    class Meta:
        db_table = "user"

