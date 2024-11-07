from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from dashboard.models import *
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required(login_url='employee_signin')
def employee_tripadd(request):
    if request.method == 'POST':
        place_name = request.POST.get('place_name')
        price = request.POST.get('price')
        no_of_days = request.POST.get('no_of_days')
        trip_pdf = request.FILES.get('trip_pdf')

        Trip.objects.create(place_name=place_name,price=price,no_of_days=no_of_days,trip_pdf=trip_pdf)
        messages.success(request,'Trip added successfully')
        return redirect('employee_packages')

    return render(request,'EmpPackages/employee_Trip_Add.html')


def employee_tripedit(request, id):
    trip = get_object_or_404(Trip, id=id)
    if request.method == 'POST':
        place_name = request.POST.get('place_name')
        price = request.POST.get('price')
        no_of_days = request.POST.get('no_of_days')
        
        # Handle file upload
        if 'trip_pdf' in request.FILES:
            # If a new file is uploaded, it will replace the old one
            trip.trip_pdf = request.FILES['trip_pdf']
        
        # Update other fields
        trip.place_name = place_name
        trip.price = price
        trip.no_of_days = no_of_days
        
        trip.save()
        
        messages.success(request, 'Trip details updated successfully')
        return redirect('employee_packages')
    
    return render(request, 'EmpPackages/employee_Trip_Edit.html', {'trip': trip})

@login_required(login_url='employee_signin')
def employee_packages(request):

    trip_query = request.GET.get('trip_q')
    stay_query = request.GET.get('stay_q')

    trips = Trip.objects.all().order_by('-id')
    stays = Stay.objects.all().order_by('-id')

    if trip_query:
        trips = trips.filter(place_name__icontains=trip_query)

    if stay_query:
        stays = stays.filter(
            Q(stay_type__icontains=stay_query) | 
            Q(location__icontains=stay_query) |
            Q(resort_name__icontains=stay_query)
        )

    trip_paginator = Paginator(trips, 20)  # Show 10 trips per page
    trip_page_number = request.GET.get('trip_page')
    trip_page_obj = trip_paginator.get_page(trip_page_number)

    # Pagination for stays
    stay_paginator = Paginator(stays, 20)  # Show 10 stays per page
    stay_page_number = request.GET.get('stay_page')
    stay_page_obj = stay_paginator.get_page(stay_page_number)

    trip_start_index = (trip_page_obj.number - 1) * trip_paginator.per_page
    stay_start_index = (stay_page_obj.number - 1) * stay_paginator.per_page

    return render(request, 'EmpPackages/employee_Package.html', {
        'trip': trip_page_obj,
        'stay': stay_page_obj,
        'trip_start_index': trip_start_index,
        'stay_start_index': stay_start_index,
        'trip_query': trip_query,
        'stay_query': stay_query

    })


@login_required(login_url='employee_signin')
def employee_tripdelete(request,id):
    trip=get_object_or_404(Trip,id=id)
    trip.delete()
    messages.success(request,'Trip deleted successfully')
    return redirect('employee_packages')


def employee_send_trip_email(request, trip_id):
    if request.method == 'POST':
        trip = get_object_or_404(Trip, id=trip_id)
        email = request.POST.get('email')
        
        # Generate the absolute URL for the PDF
        if trip.trip_pdf:
            trip_pdf_url = request.build_absolute_uri(trip.trip_pdf.url)
        else:
            trip_pdf_url = None

        context = {
            'trip': trip,
            'trip_pdf_url': trip_pdf_url,
        }

        # Render the email template
        html_message = render_to_string('EmpPackages/employee_trip_email_template.html', context)
        plain_message = strip_tags(html_message)
        
        subject = f"Trip Details for {trip.place_name}"
        from_email = settings.EMAIL_HOST_USER
        
        try:
            # Create the email message
            email = EmailMessage(subject, html_message, from_email, [email])
            email.content_subtype = "html"  # Main content is now text/html
            
            # Attach the PDF if it exists
            if trip.trip_pdf:
                email.attach_file(trip.trip_pdf.path)
            
            # Send the email
            email.send()
            messages.success(request, 'Email sent successfully')
        except Exception as e:
            messages.error(request, f'Failed to send email: {str(e)}')
        
    return redirect('employee_packages')



