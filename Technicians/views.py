from django.shortcuts import render
from dashboard.models import *
from django.contrib.auth import authenticate, login
from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db.models import Sum


# Create your views here.


def signup(request):
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
            return redirect('signup')
        if not terms_agreed:
            messages.error(request, "You must agree to the terms of service.")
            return redirect('signup')

        # Create User and Profile
        try:
            user = User.objects.create_user(
                username=email,  # Ensure your CustomUser model has a username field or adapt accordingly
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            Profile.objects.create(user=user, mobile=mobile, terms_agreed=terms_agreed)
            login(request, user)  # Log in the user after signup
            messages.success(request, "Signup successful!")
            return redirect('signin')  # Redirect to the desired page after signup

        except Exception as e:
            print(f"Error: {e}")  # Log the error in the terminal for debugging
            messages.error(request, f"Error creating account: {str(e)}")
            return redirect('signup')
    return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('email')  # Use email as the username
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)  # Authenticate user
        if user is not None:
            login(request, user)  # Log in the user
            return redirect('index')  # Redirect to the desired page after login
        else:
            messages.error(request, 'Invalid email or password')  # Use 'email' for clarity
            return redirect('signin')

    return render(request, 'SignIn.html')


def logout(request):
    auth_logout(request)
    return redirect("admin_loginview")

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
    def get_model_stats(model, date_field):
        current_month_count = model.objects.filter(**{f"{date_field}__gte": first_day_this_month}).count()
        last_month_count = model.objects.filter(
            **{f"{date_field}__gte": last_month, f"{date_field}__lt": first_day_this_month}).count()
        percentage_change = get_percentage_change(current_month_count, last_month_count)
        return current_month_count, percentage_change

    vouchers_this_month, voucher_percentage_change = get_model_stats(Voucher, 'voucher_date')
    invoices_this_month, invoice_percentage_change = get_model_stats(Invoice, 'invoice_date')
    leads_this_month, leads_percentage_change = get_model_stats(Leads, 'lead_date')

    customers_this_month = Customers.objects.filter(id__gte=1).count()
    customers_last_month = Customers.objects.filter(id__gte=1).exclude(
        id__in=Customers.objects.filter(id__gte=1).order_by('-id')[:customers_this_month]).count()
    customers_percentage_change = get_percentage_change(customers_this_month, customers_last_month)

    bookings_this_month, bookings_percentage_change = get_model_stats(Invoice, 'invoice_date')

    profit_this_month = Invoice.objects.filter(invoice_date__gte=first_day_this_month).aggregate(Sum('profit'))[
                            'profit__sum'] or 0
    profit_last_month = \
    Invoice.objects.filter(invoice_date__gte=last_month, invoice_date__lt=first_day_this_month).aggregate(
        Sum('profit'))['profit__sum'] or 0
    total_profit = Invoice.objects.aggregate(Sum('profit'))['profit__sum'] or 0
    profit_percentage_change = get_percentage_change(profit_this_month, profit_last_month)

    bookings_count = Invoice.objects.count()
    vouchers_count = Voucher.objects.count()  # Get the total count of Voucher instances
    invoices_count = Invoice.objects.count()
    customers_count = Customers.objects.count()
    leads_count = Leads.objects.count()
    recent_customers = Customers.objects.order_by('-id')[:2]
    recent_leads = Leads.objects.order_by('-id')[:2]
    upcoming_bookings = Invoice.objects.order_by('-id')[:4]
    document_type = request.GET.get('document_type', 'Invoice')  # Default to Invoice

    if document_type == 'Invoice':
        recent_invoices = Invoice.objects.order_by('-id')[:2]
        recent_vouchers = []  # Empty queryset for vouchers
    else:
        recent_vouchers = Voucher.objects.order_by('-id')[:2]
        recent_invoices = []  # Empty queryset for invoices
    return render(request, 'employee_index.html',
                  {'bookings_count': bookings_count, 'vouchers_count': vouchers_count, 'invoices_count': invoices_count,
                   'customers_count': customers_count, 'leads_count': leads_count, 'recent_customers': recent_customers,
                   'recent_leads': recent_leads, 'recent_invoices': recent_invoices,
                   'recent_vouchers': recent_vouchers,
                   'document_type': document_type, 'upcoming_bookings': upcoming_bookings,
                   'voucher_percentage_change': round(voucher_percentage_change, 2),
                   'invoice_percentage_change': round(invoice_percentage_change, 2),
                   'leads_percentage_change': round(leads_percentage_change, 2),
                   'customers_percentage_change': round(customers_percentage_change, 2),
                   'bookings_percentage_change': round(bookings_percentage_change, 2),
                   'total_profit': total_profit,
                   'profit_percentage_change': round(profit_percentage_change, 2)})


#------------------------------------------------------------------------------------------------


from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from dashboard.models import *
from datetime import datetime
from django.contrib.auth.decorators import login_required

@login_required(login_url='admin_loginview')
def leadadd(request):
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
            return redirect('leadlist')
        except Exception as  e:
            return HttpResponse(f"An error occurred: {str(e)}")

    return render(request,'Lead/Lead_Add.html')

@login_required(login_url='admin_loginview')
def leadlist(request):
    lead_list=Leads.objects.all().order_by('-id')
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
    todays_leads = Leads.objects.filter(lead_date__date=today).order_by('-lead_date')

    has_lead=paginator.count > 0

    return render(request,'Lead/Lead_List.html',{'lead':lead, 'has_lead': has_lead, 'todays_leads': todays_leads, 'query': query})

@login_required(login_url='admin_loginview')
def lead_details(request,id):
    lead=get_object_or_404(Leads,id=id)
    return render(request,'Lead/Lead_Details.html',{'lead':lead})

@login_required(login_url='admin_loginview')
def leadedit(request,id):
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
        return redirect('leadlist')

    return render(request,'Lead/Lead_Edit.html',{'lead':lead})

@login_required(login_url='admin_loginview')
def scriptanswer(request, id):
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
            return redirect('leadattend', id=id)
        except Exception as e:
            return HttpResponse(f'An error occurred: {str(e)}')

    return render(request, 'Lead/Lead_Attend.html', {'lead': lead, 'tag': tag})



def update_lead_date(request, id):
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

    return redirect('leadattend', id=id)

