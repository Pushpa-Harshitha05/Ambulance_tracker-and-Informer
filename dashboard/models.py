from django.db import models

# Create your models here.
class Hospital(models.Model):
  hospital_name = models.CharField(max_length=100, unique=True)
  hospital_id = models.CharField(max_length=100, primary_key=True)
  ip_addr = models.CharField(max_length=30)
  password = models.CharField(max_length=256)  # Make sure to hash the password

  def __str__(self):
        return self.ip_addr