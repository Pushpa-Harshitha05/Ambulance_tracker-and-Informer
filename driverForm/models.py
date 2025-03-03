from django.db import models

# Create your models here.
class Driver(models.Model):
  password = models.CharField(max_length=25)

  def __str__(self):
    return self.password