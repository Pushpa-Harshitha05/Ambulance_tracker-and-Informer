from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password,make_password
from .models import User
import requests


def form(request):
  return render(request,'driverForm/detailsForm.html')


def submit_patient_details(request):
  if request.method == 'POST':
        
        hospitals = []

        desp = request.POST.get('desp')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        url = f"https://overpass-api.de/api/interpreter"
        query = f"""
        [out:json];
        node[amenity=hospital](around:{10000},{latitude},{longitude});
        out;
        """
        response = requests.get(url, params={"data": query})
        if response.status_code == 200:
            data = response.json()
            hospitals = data.get("elements",[])
        else:
            print(f"Error: {response.status_code}")
            hospitals = []


        # Return a response or redirect to a success page
        return redirect(f"/dashboard/pushpa/?desp={desp}&latitude={latitude}&longitude={longitude}&hospitals={hospitals}")
    
  return HttpResponse("Form not submitted correctly.")


def login(request):
  if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            drivers = User.objects.filter(username=username)  # Get all with same username

            for driver in drivers:
                if check_password(password, driver.password):  # Securely verify
                    return render(request, 'driverForm/detailsForm.html')

            return render(request, "driverForm/login.html", {"error": "Invalid credentials"})

        except User.DoesNotExist:
            return HttpResponse("No data found")

  return render(request, 'driverForm/login.html')



def register(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee-id')
        username = request.POST.get('username')
        password = request.POST.get('password-reg')
        confirm_password = request.POST.get('confirm-password')

        # Check if passwords match
        if password != confirm_password:
            return render(request, 'driverForm/register.html', {'error': 'Passwords do not match'})

        # Check if employee ID or username already exists
        if User.objects.filter(employee_id=employee_id).exists():
            return render(request, 'register.html', {'error': 'Employee ID already exists'})
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})

        # Hash the password before saving
        hashed_password = make_password(password)

        # Create and save the new employee
        new_employee = User(employee_id=employee_id, username=username, password=hashed_password)
        new_employee.save()

        # Redirect to the login page after successful registration
        return redirect('driverForm:detailsForm.html')  # Redirect to login page (use the correct URL name here)

    return render(request, 'register.html')