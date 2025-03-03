from django.urls import path
from . import views

app_name = 'driverForm' 

urlpatterns = [
    path("login/",views.login,name="login"),
    path("", views.form, name='form'),  
    path("submit_patient_details/", views.submit_patient_details, name="submit_patient_details"),  
]
