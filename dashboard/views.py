from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password, make_password
from .models import Hospital

patients_list = []

def homepage(request):
    return render(request, "dashboard/display_homepage.html")

def display(request):
    desp = request.session.get('desp')
    latitude = request.session.get('latitude')
    longitude = request.session.get('longitude')
    hospitals = request.session.get('hospitals')

    if desp and latitude and longitude:
        try:
            latitude = float(latitude)
            longitude = float(longitude)

            context = {
                'desp': desp,
                'latitude': latitude,
                'longitude': longitude,
                'hospitals' : hospitals
            }

            if context not in patients_list:
                patients_list.append(context)

        except ValueError:
            return HttpResponse("Invalid latitude or longitude format.", status=400)

    return render(request, "dashboard/hospital.html", {'patients_list': patients_list})

def h_login(request):
    if request.method == 'POST':
        hospital_id = request.POST.get('hospital_id')
        password = request.POST.get('password')

        hospitals = Hospital.objects.filter(hospital_id=hospital_id)

        for hospital in hospitals:
            if check_password(password,hospital.password):
                return render(request, 'dashboard/hospital.html', {'name' : hospital.hospital_name})

        return render(request, "dashboard/hospital_login.html", {"error": "Invalid credentials"})

    return render(request, 'dashboard/hospital_login.html')

def h_register(request):
    if request.method == 'POST':
        hospitalname = request.POST.get('hospitalname')
        ipaddr = request.POST.get('ipaddr')
        hospitalid = request.POST.get('hospitalid')
        password = request.POST.get('password-reg')
        confirm_password = request.POST.get('confirm-password')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if password != confirm_password:
            return render(request, 'dashboard/hospital_login.html', {'error': 'Passwords do not match'})

        if Hospital.objects.filter(hospital_id=hospitalid).exists():
            return render(request, 'dashboard/hospital_login.html', {'error': 'Hospital ID already exists'})

        Hospital.objects.create(
            hospital_name = hospitalname,
            hospital_id = hospitalid,
            ip_address = ipaddr,
            password = password,
            latitude = latitude,
            longitude = longitude
        )

        return render(request, 'dashboard/success.html', {'name' : hospitalname})  # Redirect to dashboard after successful registration

    return render(request, 'dashboard/hospital_login.html')
