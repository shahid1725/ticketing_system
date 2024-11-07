from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from dashboard.models import *
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import EmailMessage
import requests
from django.db.models import Q

@login_required(login_url='admin_loginview')
def tripadd(request):
    if request.method == 'POST':
        place_name = request.POST.get('place_name')
        price = request.POST.get('price')
        no_of_days = request.POST.get('no_of_days')
        trip_pdf = request.FILES.get('trip_pdf')

        Trip.objects.create(place_name=place_name,price=price,no_of_days=no_of_days,trip_pdf=trip_pdf)
        messages.success(request,'Trip added successfully')
        return redirect('packages')

    return render(request,'Packages/Trip_Add.html')

def tripedit(request, id):
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
        return redirect('packages')
    
    return render(request, 'Packages/Trip_Edit.html', {'trip': trip})

@login_required(login_url='admin_loginview')
def packages(request):

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


    # Pagination for trips
    trip_paginator = Paginator(trips, 20)  # Show 10 trips per page
    trip_page_number = request.GET.get('trip_page')
    trip_page_obj = trip_paginator.get_page(trip_page_number)

    # Pagination for stays
    stay_paginator = Paginator(stays, 20)  # Show 10 stays per page
    stay_page_number = request.GET.get('stay_page')
    stay_page_obj = stay_paginator.get_page(stay_page_number)

    trip_start_index = (trip_page_obj.number - 1) * trip_paginator.per_page
    stay_start_index = (stay_page_obj.number - 1) * stay_paginator.per_page

    return render(request, 'Packages/Package.html', {
        'trip': trip_page_obj,
        'stay': stay_page_obj,
        'trip_start_index': trip_start_index,
        'stay_start_index': stay_start_index,
        'trip_query': trip_query,
        'stay_query': stay_query
    })

@login_required(login_url='admin_loginview')
def tripdelete(request,id):
    trip=get_object_or_404(Trip,id=id)
    trip.delete()
    messages.success(request,'Trip deleted successfully')
    return redirect('packages')


def send_trip_email(request, trip_id):
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
        html_message = render_to_string('Packages/trip_email_template.html',context)
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
        
    return redirect('packages')













def send_whatsapps(customer_display_name, destination, start_date, end_date, invoice_id, contact_number):
    url = "https://live-mt-server.wati.io/304152/api/v1/sendTemplateMessages"

    payload = {
        "broadcast_name": "welcome",
        "receivers": [
            {
                "customParams": [
                    {"name": "name", "value": customer_display_name},
                    {"name": "resortname", "value": destination},
                    {"name": "date", "value": start_date},
                    {"name": "checkingtime", "value": end_date},
                    {"name": "invoice_url", "value": f"http://127.0.0.1:8000/invoice_email/{invoice_id}/"}
                ],
                "whatsappNumber": "91" + contact_number

            }
        ],
        "template_name": "welcome_inv"
    }
    headers = {
        "content-type": "text/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0Njc3ZTM1ZC0xMWQ0LTRlMzktYjM1MS1jNmUyNWQ0OGIwMGMiLCJ1bmlxdWVfbmFtZSI6InJlc2VydmF0aW9uc0B3aHl0ZWhvdXNlaG9saWRheXMuY29tIiwibmFtZWlkIjoicmVzZXJ2YXRpb25zQHdoeXRlaG91c2Vob2xpZGF5cy5jb20iLCJlbWFpbCI6InJlc2VydmF0aW9uc0B3aHl0ZWhvdXNlaG9saWRheXMuY29tIiwiYXV0aF90aW1lIjoiMDIvMTkvMjAyNCAxMjoyMDowMSIsImRiX25hbWUiOiJtdC1wcm9kLVRlbmFudHMiLCJ0ZW5hbnRfaWQiOiIzMDQxNTIiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6IkNsYXJlX0FJIiwiYXVkIjoiQ2xhcmVfQUkifQ.PUEsx0BCoFO4KL2-KK7vPTh-55tKLnOtM74oXF1bnjw"  # Replace with your actual token
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.text)
    if response.status_code == 200:
        print("WhatsApp message sent successfully.")
    else:
        print(
            f"Failed to send WhatsApp message. Status Code: {response.status_code}, Response: {response.text}")



def trip_send_whatsapp_message(request, invoice_id):
    invoice = get_object_or_404(TripInvoice, id=invoice_id)

    # Extract necessary data from the invoice object
    customer_display_name = invoice.customer.customer_display_name
    destination = invoice.destination.place_name
    start_date = invoice.start_date.strftime('%d-%B-%Y')  # Convert date to string
    end_date = invoice.end_date.strftime('%d-%B-%Y')
    contact_number = invoice.customer.contact_number
    invoice_url = f"http://127.0.0.1:8000/invoice_email/{invoice.id}/"  # Assuming invoice id is unique

    # Call the send_whatsapp_reminder function
    send_whatsapps(customer_display_name, destination, start_date, end_date, invoice_id, contact_number)

    messages.success(request, 'WhatsApp message sent successfully.')
    return redirect('tripinvoice')




#---------------------------------------- PostPone Invoice wattsapp message----------------------------

def send_whatsapp(customer_display_name, resort_name, checkin_date, checkin_time, invoice_id, mobile):
    url = "https://live-mt-server.wati.io/304152/api/v1/sendTemplateMessages"

    payload = {
        "broadcast_name": "welcome",
        "receivers": [
            {
                "customParams": [
                    {"name": "name", "value": customer_display_name},
                    {"name": "resortname", "value": resort_name},
                    {"name": "date", "value": checkin_date},
                    {"name": "time", "value": checkin_time},
                    {"name": "invoice_url", "value": f"http://sales.whytehouseholidays.com/invoice_email/{invoice_id}/"}
                ],
                "whatsappNumber": "91" + mobile

            }
        ],
        "template_name": "cancel_inv"
    }
    headers = {
        "content-type": "text/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0Njc3ZTM1ZC0xMWQ0LTRlMzktYjM1MS1jNmUyNWQ0OGIwMGMiLCJ1bmlxdWVfbmFtZSI6InJlc2VydmF0aW9uc0B3aHl0ZWhvdXNlaG9saWRheXMuY29tIiwibmFtZWlkIjoicmVzZXJ2YXRpb25zQHdoeXRlaG91c2Vob2xpZGF5cy5jb20iLCJlbWFpbCI6InJlc2VydmF0aW9uc0B3aHl0ZWhvdXNlaG9saWRheXMuY29tIiwiYXV0aF90aW1lIjoiMDIvMTkvMjAyNCAxMjoyMDowMSIsImRiX25hbWUiOiJtdC1wcm9kLVRlbmFudHMiLCJ0ZW5hbnRfaWQiOiIzMDQxNTIiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6IkNsYXJlX0FJIiwiYXVkIjoiQ2xhcmVfQUkifQ.PUEsx0BCoFO4KL2-KK7vPTh-55tKLnOtM74oXF1bnjw"  # Replace with your actual token
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.text)
    if response.status_code == 200:
        print("WhatsApp message sent successfully.")
    else:
        print(
            f"Failed to send WhatsApp message. Status Code: {response.status_code}, Response: {response.text}")


def send_whatsapp_messages(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)

    # Extract necessary data from the invoice object
    customer_display_name = invoice.customer.customer_display_name
    resort_name = invoice.resort_name.resort_name
    checkin_date = invoice.checkin_date.strftime('%d-%B-%Y')  # Convert date to string
    checkin_time = invoice.checkin_time
    mobile = invoice.customer.contact_number
    invoice_url = f"http://sales.whytehouseholidays.com/invoice_email/{invoice.id}/"  # Assuming invoice id is unique

    # Call the send_whatsapp_reminder function
    send_whatsapp(customer_display_name, resort_name, checkin_date, checkin_time, invoice_id, mobile)

    messages.success(request, 'WhatsApp message sent successfully.')
    return redirect('saleinvoice')