from django.db import models
from django.contrib.auth.hashers import make_password
  

class User(models.Model):
  employee_id = models.CharField(max_length=100, unique=True)
  username = models.CharField(max_length=30)
  password = models.CharField(max_length=256)  # Make sure to hash the password

  def __str__(self):
        return self.employee_id
