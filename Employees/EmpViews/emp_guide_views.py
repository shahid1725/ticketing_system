from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from dashboard.models import *

@login_required(login_url='employee_signin')
def employee_guide_list(request):
    guide = Guide.objects.all().order_by('-id')
    return render(request, 'EmpSales/EmpGuide/employee_guide_list.html',{'guide': guide})

@login_required(login_url='employee_signin')
def employee_guide_add(request):
    if request.method == 'POST':
        guide_name = request.POST.get('guide_name')

        if Guide.objects.filter(guide_name=guide_name).exists():
            messages.error(request, 'This name already exists')
            return render(request, 'EmpSales/EmpGuide/employee_guide_add.html')

        Guide.objects.create(guide_name=guide_name)
        messages.success(request, 'Guide name created successfully')
        return redirect('employee_guide_list')
    return render(request, 'EmpSales/EmpGuide/employee_guide_add.html')

@login_required(login_url='employee_signin')
def employee_guide_delete(request,guide_id):
    guide = get_object_or_404(Guide,id=guide_id)
    guide.delete()
    messages.success(request,'Guide name deleted successfully')
    return redirect('employee_guide_list')

