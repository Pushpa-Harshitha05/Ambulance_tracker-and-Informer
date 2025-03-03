from django.shortcuts import render

patients_list = []

# Create your views here.
def display(request):
  if(request.GET.get('name') != None):
    context = {
      'name' : request.GET.get('name'),
      'number' : request.GET.get('number'),
      'distance' : float(request.GET.get('distance')),
      'desp' : request.GET.get('desp')
    }

    if((context['name'] != None) and (context not in patients_list)):
      patients_list.append(context)

    patients_list.sort(key=lambda x:x['distance'])  

  return render(request, "dashboard/hospital.html", {'patients_list': patients_list})