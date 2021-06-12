from django.db import models


# Create your models here.
class RegisterDna(models.Model):
    dna = models.CharField(max_length=4000)
    isMutant = models.BooleanField()

    class Meta:
        db_table = 'register_dna'