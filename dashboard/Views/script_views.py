from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from dashboard.models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required(login_url='admin_loginview')
def addscript(request):
    if request.method=='POST':
        script1 = request.POST.get('script1')
        script2 = request.POST.get('script2')
        script3 = request.POST.get('script3')
        script4 = request.POST.get('script4')
        script5 = request.POST.get('script5')
        script6 = request.POST.get('script6')

        if Script.objects.exists():
            messages.error(request, 'Data already exists. No new script can be added.')
        else:
            Script.objects.create(script1=script1, script2=script2, script3=script3, script4=script4, script5=script5,
                                  script6=script6)
            messages.success(request, 'Script added successfully')
        return redirect('addscript')

    script=Script.objects.all()
    return render(request,'Script/Script_Add.html', {'script': script})

@login_required(login_url='admin_loginview')
def editscript(request,id):
    script = get_object_or_404(Script,id=id)
    if request.method == 'POST':
        script1 = request.POST.get('script1')
        script2 = request.POST.get('script2')
        script3 = request.POST.get('script3')
        script4 = request.POST.get('script4')
        script5 = request.POST.get('script5')
        script6 = request.POST.get('script6')

        Script.objects.filter(id=id).update(script1=script1, script2=script2, script3=script3, script4=script4, script5=script5,
                                            script6=script6)
        messages.success(request,'Script updated successfully')
        return redirect('addscript')
    return render(request, 'Script/Script_Edit.html', {'script': script})


#--------script listings are in this page-----------------------
@login_required(login_url='admin_loginview')
def leadattend(request,id):
    lead = get_object_or_404(Leads,id=id)
    script=Script.objects.all()
    tag=Tag.objects.all()

    trip = Trip.objects.all()
    search_query = request.GET.get('q')
    from_price = request.GET.get('from_price')
    to_price = request.GET.get('to_price')
    days = request.GET.get('days')

    stay = Stay.objects.all()
    stay_search_query = request.GET.get('stay_q')
    stay_from_price = request.GET.get('stay_from_price')
    stay_to_price = request.GET.get('stay_to_price')
    persons = request.GET.get('persons')
    stay_type = request.GET.get('stay_type')

    if search_query:
        trip=trip.filter(Q(place_name__icontains=search_query))

    if from_price and to_price:
        try:
            from_price = float(from_price)
            to_price = float(to_price)
            trip=trip.filter(price__gte=from_price, price__lte=to_price)
        except ValueError:
            pass

    if days:
        try:
            days = int(days)
            if days > 0:
                trip = trip.filter(no_of_days=days)
        except ValueError:
            pass

    if stay_search_query:
        stay=stay.filter(Q(location__icontains=stay_search_query))

    if stay_from_price and stay_to_price:
        try:
            stay_from_price = float(stay_from_price)
            stay_to_price = float(stay_to_price)
            stay = stay.filter(price1__gte=stay_from_price, price1__lte=stay_to_price)
        except ValueError:
            pass

    if persons:
        try:
            persons = int(persons)
            if persons > 0:
                stay = stay.filter(no_of_persons=persons)
        except ValueError:
            pass

    if stay_type:
        stay = stay.filter(stay_type=stay_type)

    return render(request,'Lead/Lead_Attend.html',{'script':script, 'tag':tag, 'trip':trip, 'lead': lead,
                                                   'search_query': search_query,
                                                   'from_price': from_price, 'to_price': to_price, 'days':days,
                                                   'stay': stay, 'stay_search_query': stay_search_query,
                                                   'stay_from_price': stay_from_price, 'stay_to_price': stay_to_price,
                                                   'persons': persons, 'stay_type': stay_type})

