from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from .models import Driver

def form(request):
  return render(request,'driverForm/detailsForm.html')


def submit_patient_details(request):
  if request.method == 'POST':
        
        name = request.POST.get('name')
        number = request.POST.get('number')
        distance = float(request.POST.get('distance'))
        desp = request.POST.get('desp')

        # Return a response or redirect to a success page
        return redirect(f"/dashboard/?name={name}&number={number}&distance={distance}&desp={desp}")
    
  return HttpResponse("Form not submitted correctly.")


def login(request):
   if request.method == 'POST':
      password = request.POST['password']

      try:
        driver = Driver.objects.get(password=password)
        
        if password == driver.password:
          return render(request,'driverForm/detailsForm.html')
        else:
          return render(request, "driverForm/login.html")
        
      except:
         return HttpResponse("no data")
      
   return render(request,'driverForm/login.html')