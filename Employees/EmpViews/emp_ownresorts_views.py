from django.contrib import messages
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from dashboard.models import *
from django.contrib.auth.decorators import login_required


@login_required(login_url='employee_signin')
def employee_ownresortlist(request):
    ownresort_list=OwnResorts.objects.all().order_by('-id')

    paginator = Paginator(ownresort_list, 10)
    page_number = request.GET.get('page')
    try:
        ownresort = paginator.page(page_number)
    except PageNotAnInteger:
        ownresort = paginator.page(1)
    except EmptyPage:
        ownresort = paginator.page(paginator.num_pages)

    has_ownresort = paginator.count > 0


    return render(request,'EmpSales/EmpOwn_Resort/employee_Own_resort_list.html',{'ownresort':ownresort, 'has_ownresort':has_ownresort})

@login_required(login_url='employee_signin')
def employee_ownresortadd(request):
    if request.method=='POST':
        ownresort_name = request.POST.get('ownresort_name')
        ownresort_place = request.POST.get('ownresort_place')
        ownresort_email = request.POST.get('ownresort_email')
        ownresort_mobile = request.POST.get('ownresort_mobile')

        if OwnResorts.objects.filter(ownresort_mobile=ownresort_mobile).exists():
            messages.error(request,'A ownresort with this contact number already exists')
            return render(request,'EmpSales/EmpOwn_Resort/employee_Own_Resort_Add.html')
        
        if OwnResorts.objects.filter(ownresort_email=ownresort_email).exists():
            messages.error(request,'A ownresort with this email already exists')
            return render(request,'EmpSales/EmpOwn_Resort/employee_Own_Resort_Add.html')
        
        if len(ownresort_mobile) < 10:
            messages.error(request,'Contact number must be at least 10 numbers long')
            return render(request,'EmpSales/EmpOwn_Resort/employee_Own_Resort_Add.html')


        try:
            OwnResorts.objects.create(ownresort_name=ownresort_name,ownresort_place=ownresort_place,ownresort_email=ownresort_email,ownresort_mobile=ownresort_mobile)
            messages.success(request,'Own resort added successfully')
            return redirect('employee_ownresortlist')
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}")
    return render(request,'EmpSales/EmpOwn_Resort/employee_Own_Resort_Add.html')


@login_required(login_url='employee_signin')
def employee_ownresortedit(request,id):
    ownresorts=get_object_or_404(OwnResorts,id=id)
    if request.method=='POST':
        ownresort_name=request.POST.get('ownresort_name')
        ownresort_place=request.POST.get('ownresort_place')
        ownresort_email=request.POST.get('ownresort_email')
        ownresort_mobile=request.POST.get('ownresort_mobile')
        if OwnResorts.objects.filter(ownresort_mobile=ownresorts.ownresort_mobile).exclude(id=ownresorts.id).exists():
            messages.error(request,'A ownresort with this contact number already exists')
            return render(request,'EmpSales/EmpOwn_Resort/employee_Own_Resort_Edit.html',{'ownresorts':ownresorts})
        
        if OwnResorts.objects.filter(ownresort_email=ownresorts.ownresort_email).exclude(id=ownresorts.id).exists():
            messages.error(request,'A ownresort with this email already exists')
            return render(request,'EmpSales/EmpOwn_Resort/employee_Own_Resort_Edit.html',{'ownresorts':ownresorts})
        
        if len(ownresorts.ownresort_mobile) < 10:
            messages.error(request,'Contact number must be at least 10 numbers long')
            return render(request,'EmpSales/EmpOwn_Resort/employee_Own_Resort_Edit.html')
        OwnResorts.objects.filter(id=id).update(ownresort_name=ownresort_name,ownresort_place=ownresort_place,ownresort_email=ownresort_email,ownresort_mobile=ownresort_mobile)
        messages.success(request,'Own resort details updated successfully')
        return redirect('employee_ownresortlist')
    return render(request,'EmpSales/EmpOwn_Resort/employee_Own_Resort_Edit.html',{'ownresorts':ownresorts})


@login_required(login_url='employee_signin')
def employee_ownresortdelete(request,id):
    ownresorts=get_object_or_404(OwnResorts,id=id)
    if request.method=='POST':
        ownresorts.delete()
        messages.success(request,'own resort deleted successfully')
        return redirect('employee_ownresortlist')

