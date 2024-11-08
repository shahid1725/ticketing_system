from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from dashboard.models import *
from datetime import datetime
from django.contrib.auth.decorators import login_required

@login_required(login_url='employee_signin')
def employee_leadadd(request):
    if request.method=='POST':
        full_name=request.POST.get('full_name')
        medium=request.POST.get('medium')
        email=request.POST.get('email')
        mobile=request.POST.get('mobile')
        place = request.POST.get('place')
        remarks = request.POST.get('remarks')
        try:
            Leads.objects.create(full_name=full_name,medium=medium,email=email,mobile=mobile,place=place,remarks=remarks)
            messages.success(request,'Lead added successfully')
            return redirect('employee_leadlist')
        except Exception as  e:
            return HttpResponse(f"An error occurred: {str(e)}")

    return render(request,'EmpLead/employee_Lead_Add.html')

# @login_required(login_url='employee_signin')
# def employee_leadlist(request):
#     lead_list=Leads.objects.all().order_by('-id')
#     query = request.GET.get('q')
#     if query:
#         lead_list = lead_list.filter(Q(full_name__icontains=query) | Q(mobile__icontains=query))
#
#     paginator=Paginator(lead_list, 10)
#     page_number=request.GET.get('page')
#     try:
#         lead=paginator.page(page_number)
#     except PageNotAnInteger:
#         lead=paginator.page(1)
#     except EmptyPage:
#         lead=paginator.page(paginator.num_pages)
#
#     today = timezone.now().date()
#     todays_leads = Leads.objects.filter(lead_date__date=today).order_by('-lead_date')
#
#     has_lead=paginator.count > 0
#
#     return render(request,'EmpLead/employee_Lead_List.html',{'lead':lead, 'has_lead': has_lead, 'todays_leads': todays_leads, 'query': query})


@login_required(login_url='employee_signin')
def employee_lead_details(request,id):
    lead=get_object_or_404(Leads,id=id)
    return render(request,'EmpLead/employee_Lead_Details.html',{'lead':lead})


@login_required(login_url='employee_signin')
def employee_leadedit(request,id):
    lead=get_object_or_404(Leads,id=id)
    if request.method=='POST':
        full_name = request.POST.get('full_name')
        medium = request.POST.get('medium')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        place = request.POST.get('place')
        remarks = request.POST.get('remarks')

        Leads.objects.filter(id=id).update(full_name=full_name,medium=medium,email=email,mobile=mobile,place=place,remarks=remarks)
        messages.success(request,'Lead updated successfully')
        return redirect('employee_leadlist')

    return render(request,'EmpLead/employee_Lead_Edit.html',{'lead':lead})


@login_required(login_url='employee_signin')
def employee_scriptanswer(request, id):
    lead = get_object_or_404(Leads, id=id)
    tag = Tag.objects.all()

    if request.method == 'POST':
        answer1 = request.POST.get('answer1')
        answer2 = request.POST.get('answer2')
        answer3 = request.POST.get('answer3')
        answer4 = request.POST.get('answer4')
        answer5 = request.POST.get('answer5')
        answer6 = request.POST.get('answer6')
        tag_id = request.POST.get('tag')

        try:
            if answer1:
                lead.answer1 = answer1
            if answer2:
                lead.answer2 = answer2
            if answer3:
                lead.answer3 = answer3
            if answer4:
                lead.answer4 = answer4
            if answer5:
                lead.answer5 = answer5
            if answer6:
                lead.answer6 = answer6
            if tag_id:
                tag = Tag.objects.get(id=tag_id)
                lead.tag = tag
            lead.attended_by = request.user
            lead.save()
            messages.success(request, 'Your response submitted successfully')
            return redirect('employee_leadattend', id=id)
        except Exception as e:
            return HttpResponse(f'An error occurred: {str(e)}')

    return render(request, 'EmpLead/employee_Lead_Attend.html', {'lead': lead, 'tag': tag})


@login_required(login_url='employee_signin')
def employee_update_lead_date(request, id):
    # Get the object you want to update
    instance = get_object_or_404(Leads, id=id)

    if request.method == 'POST':
        try:
            hour = request.POST.get('hour').zfill(2)
            minute = request.POST.get('minute').zfill(2)
            when = request.POST.get('when')
            current_date = request.POST.get('currentDate')  # Expecting format '20/06/2024'

            # Replace any dashes with slashes in the current_date
            current_date = current_date.replace('-', '/')

            # Combine date and time components into a single string
            datetime_str = f"{current_date} {hour}:{minute} {when}"  # Example: '20/06/2024 08:50 AM'

            # Convert the string to a datetime object
            combined_datetime = datetime.strptime(datetime_str, '%d/%m/%Y %I:%M %p')

            # Set the new datetime
            instance.lead_date = combined_datetime

            # Save the instance
            instance.save()
            messages.success(request, 'Lead date updated successfully')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

    return redirect('employee_leadattend', id=id)
