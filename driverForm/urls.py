from django.urls import path
from . import views

app_name = 'driverForm' 

urlpatterns = [
    path("login/",views.login,name="login"),
    path('register/',views.register,name="register"),
    path("", views.form, name='form'),  
    path("submit_patient_details/", views.submit_patient_details, name="submit_patient_details"),
    path('driver_dashboard/',views.display_hospitals, name="driver_dashboard"),
    path('receive_ip/',views.receive_ip,name="receive_ip")
]
