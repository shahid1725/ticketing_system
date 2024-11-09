from django.shortcuts import render
from dashboard.models import *
from django.contrib.auth import authenticate, login,logout as auth_logout, get_user_model
from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db.models import Sum
from dashboard.models import Ticket

# Create your views here.

def tech_signup(request):
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        terms_agreed = request.POST.get('terms_agreed') == 'on'

        # Validate form data
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('tech_signup')
        if not terms_agreed:
            messages.error(request, "You must agree to the terms of service.")
            return redirect('tech_signup')

        # Create User and Profile
        try:
            User = get_user_model()  # Get the custom user model
            user = User.objects.create_user(
                username=email,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            Profile.objects.create(user=user, mobile=mobile, terms_agreed=terms_agreed)
            login(request, user)  # Log in the user after signup
            messages.success(request, "Signup successful!")
            return redirect('tech_signin')

        except Exception as e:
            print(f"Error: {e}")
            messages.error(request, f"Error creating account: {str(e)}")
            return redirect('tech_signup')
    return render(request, 'tech_signup.html')

def tech_signin(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('tech_index')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('tech_signin')

    return render(request, 'tech_signin.html')


def tech_logout(request):
    auth_logout(request)
    return redirect("tech_signin")

def tech_base(request):
    return render(request, 'tech_base.html')



@login_required(login_url='tech_signin')
def tech_index(request):
    today = timezone.now().date()
    first_day_this_month = today.replace(day=1)
    last_month = first_day_this_month - relativedelta(months=1)

    def get_percentage_change(current, previous):
        if previous > 0:
            return ((current - previous) / previous) * 100
        return 100 if current > 0 else 0

    # Fetch counts and calculate percentage changes

    return render(request, 'tech_index.html',
                  {})


#------------------------------------------------------------------------------------------------


from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from dashboard.models import *
from datetime import datetime
from django.contrib.auth.decorators import login_required


def tech_ticketadd(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        status = request.POST.get('status', 'IN_PROGRESS')  # Default to "IN_PROGRESS" if not provided
        description = request.POST.get('description')
        attended_by_id = request.POST.get('attended_by')
        created_by = request.user

        # Fetch the attended_by user if provided
        attended_by = None
        if attended_by_id:
            try:
                attended_by = CustomUser.objects.get(id=attended_by_id)
            except CustomUser.DoesNotExist:
                attended_by = None

        try:
            # Create the ticket
            Ticket.objects.create(
                title=title,
                status=status,
                description=description,
                attended_by=attended_by,
                created_by=created_by
            )
            messages.success(request, 'Ticket added successfully')
            return redirect('tech_ticketlist')
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}")

    return render(request, 'Ticket/Tech_Ticket_Add.html')



def tech_ticketlist(request):
    current_user = request.user
    lead_list = Ticket.objects.filter(created_by=current_user).exclude(status='Attended').order_by('-id')
    solved_ticket = Ticket.objects.filter(created_by=current_user, status='Attended')
    query = request.GET.get('q')
    if query:
        lead_list = lead_list.filter(Q(full_name__icontains=query) | Q(mobile__icontains=query))

    paginator=Paginator(lead_list, 10)
    page_number=request.GET.get('page')
    try:
        lead=paginator.page(page_number)
    except PageNotAnInteger:
        lead=paginator.page(1)
    except EmptyPage:
        lead=paginator.page(paginator.num_pages)

    today = timezone.now().date()
    # todays_leads = Leads.objects.filter(lead_date__date=today).order_by('-lead_date')

    has_lead=paginator.count > 0

    return render(request,'Ticket/Tech_Ticket_List.html',{'lead':lead, 'has_lead': has_lead, 'query': query,'solved_ticket':solved_ticket})


def tech_lead_details(request,id):
    lead=get_object_or_404(Leads,id=id)
    return render(request,'Lead/Lead_Details.html',{'lead':lead})


# def tech_leadedit(request,id):
#     lead=get_object_or_404(Leads,id=id)
#     if request.method=='POST':
#         full_name = request.POST.get('full_name')
#         medium = request.POST.get('medium')
#         email = request.POST.get('email')
#         mobile = request.POST.get('mobile')
#         place = request.POST.get('place')
#         remarks = request.POST.get('remarks')
#
#         Leads.objects.filter(id=id).update(full_name=full_name,medium=medium,email=email,mobile=mobile,place=place,remarks=remarks)
#         messages.success(request,'Lead updated successfully')
#         return redirect('tech_leadlist')
#
#     return render(request,'Lead/Lead_Edit.html',{'lead':lead})
#
#
#
#
#
# def update_lead_date(request, id):
#     # Get the object you want to update
#     instance = get_object_or_404(Leads, id=id)
#
#     if request.method == 'POST':
#         try:
#             hour = request.POST.get('hour').zfill(2)
#             minute = request.POST.get('minute').zfill(2)
#             when = request.POST.get('when')
#             current_date = request.POST.get('currentDate')  # Expecting format '20/06/2024'
#
#             # Replace any dashes with slashes in the current_date
#             current_date = current_date.replace('-', '/')
#
#             # Combine date and time components into a single string
#             datetime_str = f"{current_date} {hour}:{minute} {when}"  # Example: '20/06/2024 08:50 AM'
#
#             # Convert the string to a datetime object
#             combined_datetime = datetime.strptime(datetime_str, '%d/%m/%Y %I:%M %p')
#
#             # Set the new datetime
#             instance.lead_date = combined_datetime
#
#             # Save the instance
#             instance.save()
#             messages.success(request, 'Lead date updated successfully')
#         except Exception as e:
#             messages.error(request, f'An error occurred: {str(e)}')
#
#     return redirect('leadattend', id=id)


def tech_ticket_details(request,id):
    ticket=get_object_or_404(Ticket,id=id)
    return render(request,'Ticket/Tech_Ticket_Details.html',{'ticket':ticket})