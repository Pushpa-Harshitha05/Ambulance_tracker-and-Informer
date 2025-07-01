from django.db import models

# Create your models here.
class Hospital(models.Model):
  hospital_name = models.CharField(max_length=100)
  hospital_id = models.CharField(max_length=100, primary_key=True)
  ip_address = models.GenericIPAddressField()
  password = models.CharField(max_length=256)
  latitude = models.FloatField()
  longitude = models.FloatField()

  def __str__(self):
        return self.ip_addr