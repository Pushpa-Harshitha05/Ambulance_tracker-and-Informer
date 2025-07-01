from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
  path("",views.homepage,name='homepage'),
  path("hospitals/",views.display,name='display'),
  path("hospital_login/",views.h_login,name="h_login"),
  path('hospital_register/',views.h_register,name="h_register"),
]