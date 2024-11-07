from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from dashboard.models import *
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from decimal import Decimal, InvalidOperation
from datetime import datetime, timedelta
import requests

def stayadd(request):
    if request.method == 'POST':
        try:
            stay_type = request.POST.get('stay_type')
            no_of_rooms = request.POST.get('no_of_rooms')
            price1 = request.POST.get('price1')
            price2 = request.POST.get('price2')
            price3 = request.POST.get('price3')
            price4 = request.POST.get('price4')
            price5 = request.POST.get('price5')
            price6 = request.POST.get('price6')
            price7 = request.POST.get('price7')
            price8 = request.POST.get('price8')
            price9 = request.POST.get('price9')
            price10 = request.POST.get('price10')

            room_type1 = request.POST.get('room_type1')
            room_type2 = request.POST.get('room_type2')
            room_type3 = request.POST.get('room_type3')
            room_type4 = request.POST.get('room_type4')
            room_type5 = request.POST.get('room_type5')
            room_type6 = request.POST.get('room_type6')
            room_type7 = request.POST.get('room_type7')
            room_type8 = request.POST.get('room_type8')
            room_type9 = request.POST.get('room_type9')
            room_type10 = request.POST.get('room_type10')
            location = request.POST.get('location')
            no_of_persons = request.POST.get('no_of_persons')
            checkin_time = request.POST.get('checkin_time')
            checkout_time = request.POST.get('checkout_time')
            stay_pdf = request.FILES.get('stay_pdf')
            amenities = request.POST.get('amenities')
            resort_name = request.POST.get('resort_name')
            resort_email = request.POST.get('resort_email')
            resort_mobile = request.POST.get('resort_mobile')
            is_own_resort = request.POST.get('is_own_resort') == 'on'
            
            # Convert fields to appropriate types, with default values if necessary
            no_of_rooms = int(no_of_rooms) if no_of_rooms else None
            no_of_persons = int(no_of_persons) if no_of_persons else None
            price1 = Decimal(price1) if price1 else None
            price2 = Decimal(price2) if price2 else None
            price3 = Decimal(price3) if price3 else None
            price4 = Decimal(price4) if price4 else None
            
            Stay.objects.create(
                stay_type=stay_type, no_of_rooms=no_of_rooms, price1=price1, price2=price2, 
                price3=price3, price4=price4,price5=price5,price6=price6,price7=price7,price8=price8,price9=price9,price10=price10, room_type1=room_type1, room_type2=room_type2, 
                room_type3=room_type3, room_type4=room_type4,room_type5=room_type5,room_type6=room_type6,room_type7=room_type7,room_type8=room_type8,
                room_type9=room_type9,room_type10=room_type10, location=location, 
                no_of_persons=no_of_persons, checkin_time=checkin_time, 
                checkout_time=checkout_time, stay_pdf=stay_pdf, amenities=amenities, 
                resort_name=resort_name, resort_email=resort_email, resort_mobile=resort_mobile, 
                is_resort=not is_own_resort, is_own_resort=is_own_resort
            )
            messages.success(request, 'Stay details added successfully')
            return redirect('packages')
        except (ValueError, InvalidOperation, TypeError) as e:
            messages.error(request, f"Invalid input: {e}")
    return render(request, 'Packages/Stay_Add.html')

@login_required(login_url='admin_loginview')
def stayedit(request, stay_id):
    stay = get_object_or_404(Stay, id=stay_id)

    if request.method == 'POST':
        try:
            stay.stay_type = request.POST.get('stay_type')
            stay.no_of_days = int(request.POST.get('no_of_days')) if request.POST.get('no_of_days') else None
            stay.location = request.POST.get('location')
            stay.no_of_persons = int(request.POST.get('no_of_persons')) if request.POST.get('no_of_persons') else None
            stay.checkin_time = request.POST.get('checkin_time')
            stay.checkout_time = request.POST.get('checkout_time')
            stay.amenities = request.POST.get('amenities')
            stay.resort_name = request.POST.get('resort_name')
            stay.resort_email = request.POST.get('resort_email')
            stay.resort_mobile = request.POST.get('resort_mobile')
            stay.is_own_resort = request.POST.get('is_own_resort') == 'on'

            for i in range(1, 11):
                room_type_key = f'room_type{i}'
                price_key = f'price{i}'

                setattr(stay, room_type_key, request.POST.get(room_type_key, ''))
                price_value = request.POST.get(price_key)

                if price_value:
                    try:
                        setattr(stay, price_key, Decimal(price_value))
                    except (InvalidOperation, ValueError):
                        setattr(stay, price_key, None)
                else:
                    setattr(stay, price_key, None)

            if 'stay_pdf' in request.FILES:
                stay.stay_pdf = request.FILES['stay_pdf']

            stay.save()
            messages.success(request, 'Stay details updated successfully')
            return redirect('packages')
        except (ValueError, TypeError, InvalidOperation) as e:
            messages.error(request, f'Invalid input: {e}')

    # Prepare room data for the template
    room_data = []
    for i in range(1, 11):
        room_type = getattr(stay, f'room_type{i}', '')
        price = getattr(stay, f'price{i}', '')
        room_data.append({
            'index': i,
            'room_type': room_type,
            'price': price
        })

    return render(request, 'Packages/Stay_Edit.html', {
        'stay': stay,
        'room_data': room_data,
    })

@login_required(login_url='admin_loginview')
def staydelete(request,id):
    stay=get_object_or_404(Stay, id=id)
    stay.delete()
    messages.success(request,'Stay deleted successfully')
    return redirect('packages')


def send_stay_email(request, stay_id):
    if request.method == 'POST':
        stay = get_object_or_404(Stay, id=stay_id)
        email = request.POST.get('email')
        
        # Generate the absolute URL for the PDF
        if stay.stay_pdf:
            stay_pdf_url = request.build_absolute_uri(stay.stay_pdf.url)
        else:
            stay_pdf_url = None

        context = {
            'stay': stay,
            'stay_pdf_url': stay_pdf_url,
        }

        # Render the email template
        html_message = render_to_string('Packages/stay_email_template.html', context)
        plain_message = strip_tags(html_message)
        
        subject = f"Stay Details for {stay.location}"
        from_email = settings.EMAIL_HOST_USER
        
        try:
            # Create the email message
            email = EmailMessage(subject, html_message, from_email, [email])
            email.content_subtype = "html"  # Main content is now text/html
            
            # Attach the PDF if it exists

            if stay.stay_pdf:
                email.attach_file(stay.stay_pdf.path)
            
            
            # Send the email
            email.send()
            messages.success(request, 'Email sent successfully')
        except Exception as e:
            messages.error(request, f'Failed to send email: {str(e)}')
        
    return redirect('packages')




#-------------------------------------- whatsapp message -------------------------------------------

def send_whatsapps(whatsapp_number, checkin_time, checkout_time, stay_type, no_of_rooms, location,amenities,price1,resort_name,stay_id):
    url = "https://live-mt-server.wati.io/329541/api/v1/sendTemplateMessages"
    
    payload = {
        "broadcast_name": "Navigo Trips",
        "receivers": [
            {
                "whatsappNumber": whatsapp_number,
                "customParams": [
                    
                    {"name": "checkin_time", "value": checkin_time},
                    {"name": "checkout_time", "value": checkout_time},
                    {"name": "stay_type", "value": stay_type},
                    {"name": "no_of_rooms", "value": str(no_of_rooms)},
                    {"name": "location", "value": location},
                    {"name": "amenities", "value": amenities},
                    {"name": "price1", "value": price1},
                    {"name": "resort_name", "value": resort_name},
                    {"name": "inv_link", "value": f"send_stay_whatsapp/{stay_id}/"}
                    
                ],
            }
        ],
        "template_name": "stay_message_sends"
    }
    
    headers = {
        "content-type": "text/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI4MTMzMmU2OC0wODRkLTQ1MjMtODU0MS04MWYyMmI5ZWJiMDMiLCJ1bmlxdWVfbmFtZSI6Im5hdmlnb3RyaXBzQGdtYWlsLmNvbSIsIm5hbWVpZCI6Im5hdmlnb3RyaXBzQGdtYWlsLmNvbSIsImVtYWlsIjoibmF2aWdvdHJpcHNAZ21haWwuY29tIiwiYXV0aF90aW1lIjoiMDgvMDIvMjAyNCAwODo0Nzo1NCIsImRiX25hbWUiOiJtdC1wcm9kLVRlbmFudHMiLCJ0ZW5hbnRfaWQiOiIzMjk1NDEiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6IkNsYXJlX0FJIiwiYXVkIjoiQ2xhcmVfQUkifQ.wr78I9zQx18T6PovGICUHJhWWjofegZiGpdpfZlHFz8"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response

# Your view remains mostly the same
def send_stay_whatsapp_message(request, stay_id):
    if request.method == 'POST':
        stay = get_object_or_404(Stay, id=stay_id)
        whatsapp_number = request.POST.get('whatsapp_number')

        if not whatsapp_number:
            messages.error(request, 'WhatsApp number is required.')
            return redirect('packages')

        # Prepare the data
        checkin_time = stay.checkin_time.strftime('%I:%M %p')
        checkout_time = stay.checkout_time.strftime('%I:%M %p')
        stay_type = stay.stay_type or 'Not specified'
        no_of_rooms = stay.no_of_rooms or 'Not specified'
        location = stay.location or 'Location not specified'
        amenities = stay.amenities or 'Amenities not specified'
        resort_name = stay.resort_name or 'Resort'
        stay__url = f"https://www.sales.navigotrips.com/send_stay_whatsapp/{stay_id}/" 
        
        # Convert Decimal to string or float
        price1 = str(stay.price1) if stay.price1 else 'Price not specified'

        # Send the WhatsApp message
        try:
            response = send_whatsapps(
                whatsapp_number,
                checkin_time,
                checkout_time,
                stay_type,
                no_of_rooms,
                location,
                amenities,
                price1,
                resort_name,
                stay_id
            )
            
            if response.status_code == 200:
                messages.success(request, 'WhatsApp message sent successfully.')
            else:
                messages.error(request, f'Failed to send WhatsApp message. Status Code: {response.status_code}, Response: {response.text}')
        
        except Exception as e:
            messages.error(request, f'Error sending WhatsApp message: {str(e)}')

    else:
        messages.error(request, 'Invalid request method.')

    return redirect('packages')








# def send_whatsapps(whatsapp_number, resort_name, checkin_time, checkout_time, stay_id, stay_type, no_of_rooms, location):
#     url = "https://live-mt-server.wati.io/329541/api/v1/sendTemplateMessages"
    
#     payload = {
#         "broadcast_name": "Navigo Trips",
#         "receivers": [
#             {
#                 "whatsappNumber": whatsapp_number,
#                 "customParams": [
#                     {"name": "resort_name", "value": resort_name},
#                     {"name": "checkin_time", "value": checkin_time},
#                     {"name": "checkout_time", "value": checkout_time},
#                     {"name": "stay_type", "value": stay_type},
#                     {"name": "no_of_rooms", "value": str(no_of_rooms)},
#                     {"name": "location", "value": location},
#                     {"name": "inv_link", "value": f"send_stay_whatsapp/{stay_id}/"},
#                 ],
#             }
#         ],
#         "template_name": "stay_send_messages"
#     }
    
#     headers = {
#         "content-type": "text/json",
#         "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI4MTMzMmU2OC0wODRkLTQ1MjMtODU0MS04MWYyMmI5ZWJiMDMiLCJ1bmlxdWVfbmFtZSI6Im5hdmlnb3RyaXBzQGdtYWlsLmNvbSIsIm5hbWVpZCI6Im5hdmlnb3RyaXBzQGdtYWlsLmNvbSIsImVtYWlsIjoibmF2aWdvdHJpcHNAZ21haWwuY29tIiwiYXV0aF90aW1lIjoiMDgvMDIvMjAyNCAwODo0Nzo1NCIsImRiX25hbWUiOiJtdC1wcm9kLVRlbmFudHMiLCJ0ZW5hbnRfaWQiOiIzMjk1NDEiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6IkNsYXJlX0FJIiwiYXVkIjoiQ2xhcmVfQUkifQ.wr78I9zQx18T6PovGICUHJhWWjofegZiGpdpfZlHFz8"
#     }
    
#     response = requests.post(url, json=payload, headers=headers)
#     return response

# # Your view remains mostly the same
# def send_stay_whatsapp_message(request, stay_id):
#     if request.method == 'POST':
#         stay = get_object_or_404(Stay, id=stay_id)
#         whatsapp_number = request.POST.get('whatsapp_number')

#         if not whatsapp_number:
#             messages.error(request, 'WhatsApp number is required.')
#             return redirect('packages')

#         # Prepare the data
#         resort_name = stay.resort_name or 'Resort'
#         checkin_time = stay.checkin_time.strftime('%I:%M %p')
#         checkout_time = stay.checkout_time.strftime('%I:%M %p')
#         stay_type = stay.stay_type or 'Not specified'
#         no_of_rooms = stay.no_of_rooms or 'Not specified'
#         location = stay.location or 'Location not specified'
#         stay__url = f"https://www.sales.navigotrips.com/send_stay_whatsapp/{stay_id}/"  # Assuming invoice id is unique

#         # Send the WhatsApp message
#         try:
#             response = send_whatsapps(
#                 whatsapp_number,
#                 resort_name,
#                 checkin_time,
#                 checkout_time,
#                 stay_id,
#                 stay_type,
#                 no_of_rooms,
#                 location
#             )
            
#             if response.status_code == 200:
#                 messages.success(request, 'WhatsApp message sent successfully.')
#             else:
#                 messages.error(request, f'Failed to send WhatsApp message. Status Code: {response.status_code}, Response: {response.text}')
        
#         except Exception as e:
#             messages.error(request, f'Error sending WhatsApp message: {str(e)}')

#     else:
#         messages.error(request, 'Invalid request method.')

#     return redirect('packages')

