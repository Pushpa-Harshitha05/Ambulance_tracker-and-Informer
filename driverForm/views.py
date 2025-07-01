from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password,make_password
from .models import User
from dashboard.models import Hospital
import requests
from math import radians, sin, cos, sqrt, atan2

hospitals_list = []

def form(request):
  return render(request,'driverForm/detailsForm.html')


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def display_hospitals(request):
    desp = request.session.get('desp')
    latitude = request.session.get('latitude')
    longitude = request.session.get('longitude')
    hospitals = request.session.get('hospitals',[])
    registered = request.session.get('registered_hospitals',[])

    if desp and latitude and longitude:
        try:
            latitude = float(latitude)
            longitude = float(longitude)

            context = {
                'desp': desp,
                'latitude': latitude,
                'longitude': longitude,
                'hospitals' : hospitals,
                'registered_hospitals' : registered
            }

            if context not in hospitals_list:
                hospitals_list.append(context)

        except ValueError:
            return HttpResponse("Invalid latitude or longitude format.", status=400)

    return render(request, "driverForm/nearby_hospitals.html", {'hospitals_list': hospitals_list})


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
                    
                    if lat1 is not None and lon1 is not None:
                        distance = haversine(float(latitude),float(longitude),lat1,lon1)
                        hospital['distance'] = distance
                        hospitals.append(hospital)       
                
                hospitals.sort(key=lambda h:h['distance'])
        else:
            hospitals = []

        registered = []
        if Hospital.objects.exists():
            for hosp in Hospital.objects.all():
                dist = haversine(float(latitude),float(longitude),hosp.latitude,hosp.longitude)
                print(dist)
                if(dist <= 3):
                    registered.append({
                        "name": hosp.hospital_name,
                        "latitude": hosp.latitude,
                        "longitude": hosp.longitude,
                        "distance": dist,
                        "ip_addr": hosp.ip_address,
                        "type": "registered"
                    })
            registered.sort(key=lambda x: x["distance"])

        request.session['desp'] = desp
        request.session['latitude'] = latitude
        request.session['longitude'] = longitude
        request.session['hospitals'] = hospitals
        request.session['registered_hospitals'] = registered

        return redirect(f"/driverForm/driver_dashboard/")
    
  return HttpResponse("Form not submitted correctly.")


def login(request):
  if request.method == 'POST':
        emp_id = request.POST.get('emp_id')
        password = request.POST.get('password')

        try:
            if User.objects.filter(employee_id=emp_id).exists():
                user = User.objects.get(employee_id=emp_id)
                if user.password == password:
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