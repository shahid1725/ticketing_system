from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from dashboard.models import *
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

#------------------------------------------ Resorts -----------------------------------------
@login_required(login_url='admin_loginview')
def resortlist(request):
    resort=Resorts.objects.all().order_by('-id')

    paginator = Paginator(resort, 10)
    page_number=request.GET.get('page')
    try:
        resorts = paginator.page(page_number)
    except PageNotAnInteger:
        resorts = paginator.page(1)
    except EmptyPage:
        resorts = paginator.page(paginator.num_pages)

    has_resorts = paginator.count > 0

    return render(request,'Sales/Resorts/Resorts_List.html',{'resorts':resorts, 'has_resorts': has_resorts})

@login_required(login_url='admin_loginview')
def resortadd(request):
    if request.method=='POST':
        resort_name = request.POST.get('resort_name')
        resort_place = request.POST.get('resort_place')
        resort_email = request.POST.get('resort_email')
        resort_mobile = request.POST.get('resort_mobile')
        resort_location = request.POST.get('resort_location')
        is_own_resort = request.POST.get('is_own_resort') == 'on'

        if Resorts.objects.filter(resort_mobile=resort_mobile).exists():
            messages.error(request,'A resort with this contact number already exists')
            return render(request,'Sales/Resorts/Resorts_Add.html')
        
        if Resorts.objects.filter(resort_email=resort_email).exists():
            messages.error(request,'A resort with this email already exists')
            return render(request,'Sales/Resorts/Resorts_Add.html')
        
        if len(resort_mobile) < 10:
            messages.error(request,'Contact number must be at least 10 numbers long')
            return render(request,'Sales/Resorts/Resorts_Add.html')

        try:
            Resorts.objects.create(resort_name=resort_name,resort_place=resort_place,resort_email=resort_email,resort_mobile=resort_mobile,resort_location=resort_location,is_resort=not is_own_resort,
                is_own_resort=is_own_resort)
            messages.success(request,'Resort created successfully')
            return redirect('resortlist')
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}")
    return render(request,'Sales/Resorts/Resorts_Add.html')

@login_required(login_url='admin_loginview')
def resortedit(request,id):
    resorts=get_object_or_404(Resorts,id=id)
    if request.method=='POST':
        resort_name=request.POST.get('resort_name')
        resort_place=request.POST.get('resort_place')
        resort_email=request.POST.get('resort_email')
        resort_mobile=request.POST.get('resort_mobile')
        resort_location = request.POST.get('resort_location')
        is_own_resort = request.POST.get('is_own_resort') == 'on'

        if Resorts.objects.filter(resort_mobile=resorts.resort_mobile).exclude(id=resorts.id).exists():
            messages.error(request,'A resort with this contact number already exists')
            return render(request,'Sales/Resorts/Resorts_Edit.html',{'resorts':resorts})
        
        if Resorts.objects.filter(resort_email=resorts.resort_email).exclude(id=resorts.id).exists():
            messages.error(request,'A resort with this email already exists')
            return render(request,'Sales/Resorts/Resorts_Edit.html',{'resorts':resorts})
        
        if len(resorts.resort_mobile) < 10:
            messages.error(request,'Contact number must be at least 10 numbers long')
            return render(request,'Sales/Resorts/Resorts_Edit.html')
        
        Resorts.objects.filter(id=id).update(resort_name=resort_name,resort_place=resort_place,resort_email=resort_email,resort_mobile=resort_mobile,resort_location=resort_location,is_resort=not is_own_resort,
                is_own_resort=is_own_resort)
        messages.success(request,'Resort details updated successfully')
        return redirect('resortlist')
    return render(request,'Sales/Resorts/Resorts_Edit.html',{'resorts':resorts})

@login_required(login_url='admin_loginview')
def resortdelete(request,id):
    resorts=get_object_or_404(Resorts,id=id)
    if request.method=='POST':
        resorts.delete()
        messages.success(request,'resort deleted successfully')
        return redirect('resortlist')