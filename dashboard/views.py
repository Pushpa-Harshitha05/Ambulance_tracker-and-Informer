from django.shortcuts import render,redirect
from .models import Hospital

patients_list = []

def homepage(request):
    return render(request, "dashboard/display_homepage.html")

def display(request):
    hsp_id = request.session.get('hsp_id')

    if hsp_id is not None:
        return render(request, 'dashboard/hospital.html', {'hospitalId': hsp_id})
    
    return render(request, 'dashboard/hospital_login.html')


def h_login(request):
    if request.method == 'POST':
        hospital_id = request.POST.get('hospital_id')
        password = request.POST.get('password')

        if Hospital.objects.filter(hospital_id=hospital_id).exists():
            hospital = Hospital.objects.get(hospital_id=hospital_id)

            if hospital.password != password:
                return render(request, "dashboard/hospital_login.html", {"error": "Wrong Password"})
            else:
                request.session['hsp_id'] = hospital_id
                return redirect("dashboard:display")

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

        return render(request, 'dashboard/success.html')

    return render(request, 'dashboard/hospital_login.html')
