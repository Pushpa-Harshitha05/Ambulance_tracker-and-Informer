from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password,make_password
from .models import User
import requests
from math import radians, sin, cos, sqrt, atan2


def form(request):
  return render(request,'driverForm/detailsForm.html')


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def submit_patient_details(request):
  if request.method == 'POST':
        
        hospitals = []

        desp = request.POST.get('desp')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        url = f"https://overpass-api.de/api/interpreter"
        query = f"""
        [out:json];
        node[amenity=hospital](around:{2000},{latitude},{longitude});
        out;
        """

        response = requests.get(url, params={'data':query})
        if response.status_code == 200:
            data = response.json()
            raw_hospitals = data.get("elements",[])

            if raw_hospitals:
                for hospital in raw_hospitals:
                    lat1 = hospital.get('lat')
                    lon1 = hospital.get('lon')
                    print(lat1,lon1)
                    
                    if lat1 is not None and lon1 is not None:
                        distance = haversine(float(latitude),float(longitude),lat1,lon1)
                        hospital['distance'] = distance
                        hospitals.append(hospital)       
                
                hospitals.sort(key=lambda h:h['distance'])
                
            else:
                hospitals = []
        else:
            hospitals = []

        request.session['desp'] = desp
        request.session['latitude'] = latitude
        request.session['longitude'] = longitude
        request.session['hospitals'] = hospitals

        # Return a response or redirect to a success page
        return redirect(f"/dashboard/hospitals/")
    
  return HttpResponse("Form not submitted correctly.")


def login(request):
  if request.method == 'POST':
        emp_id = request.POST.get('emp_id')
        password = request.POST.get('password')

        try:
            if User.objects.filter(employee_id=emp_id).exists():  # Get all with same username
                user = User.objects.get(employee_id=emp_id)
                if user.password == password:  # Securely verify
                    return render(request, 'driverForm/detailsForm.html')
                else:
                    return render(request, 'driverForm/login.html', {'error' : 'Password is incorrect.'})

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

        # if passwords did not match
        if password != confirm_password:
            return render(request, 'driverForm/login.html', {'error': 'Passwords do not match'})
        
        # if username exists
        if User.objects.filter(employee_id=employee_id).exists():
            return render(request, 'driverForm/login.html', {'error': 'Driver with this employee id already exists.'})
        
        # create and save the driver
        User.objects.create(
            employee_id=employee_id,
            username=username,
            password=password
        )

        return render(request, 'driverForm/detailsForm.html')

    return render(request, 'login.html')