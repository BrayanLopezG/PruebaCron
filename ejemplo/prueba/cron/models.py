from unittest.util import _MAX_LENGTH
from django.db import models
from django.utils import timezone
# Create your models here.

class Email(models.Model):
    from_name = models.CharField( max_length = 100)
    fecha = timezone.now()
    asunto = models.TextField()
    cuerpo = models.TextField()

    def __str__(self):
        return self.from_name