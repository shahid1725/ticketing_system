from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render,redirect,get_object_or_404
from dashboard.models import *
from django.contrib import messages
from django.db.models import Max, Q
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import requests
from django.contrib.auth.decorators import login_required
from decimal import Decimal, InvalidOperation
import datetime
from datetime import datetime


@login_required(login_url='employee_signin')
def employee_salevoucher(request):
    voucher_list = Voucher.objects.all().order_by('-id')
    query = request.GET.get('q')
    if query:
        voucher_list = voucher_list.filter(Q(customer__full_name__icontains=query) | Q(mobile__icontains=query))

    paginator = Paginator(voucher_list, 10)
    page_number = request.GET.get('page')
    try:
        voucher = paginator.page(page_number)
    except PageNotAnInteger:
        voucher = paginator.page(1)
    except EmptyPage:
        voucher = paginator.page(paginator.num_pages)

    return render(request,'EmpSales/EmpSale_voucher/employee_Sale_voucher.html',{'voucher': voucher, 'query':query})


@login_required(login_url='employee_signin')
def employee_salevoucheradd(request):
    if request.method == "POST":
        customer_id = request.POST.get('customer_id')
        sales_person_id = request.POST.get('sales_person')
        resort_id = request.POST.get('resort_id')
        account_id = request.POST.get('bank_account')
        meal_plan_id = request.POST.get('meal_plan')
        voucher_date = request.POST.get('voucher_date')
        checkin_date = request.POST.get('checkin_date')
        checkout_date = request.POST.get('checkout_date')
        mobile = request.POST.get('mobile')
        checkin_time = request.POST.get('checkin_time')
        checkout_time = request.POST.get('checkout_time')
        adults = request.POST.get('adults')
        children = request.POST.get('children')
        number_of_nights = request.POST.get('number_of_nights')
        room_type = request.POST.get('room_type')
        number_of_rooms = request.POST.get('number_of_rooms')

        # Handle decimal fields, converting None or invalid values to Decimal('0.00')
        try:
            package_price = Decimal(request.POST.get('package_price', '0.00'))
        except InvalidOperation:
            package_price = Decimal('0.00')

        try:
            resort_price = Decimal(request.POST.get('resort_price', '0.00'))
        except InvalidOperation:
            resort_price = Decimal('0.00')

        try:
            travel = Decimal(request.POST.get('travel', '0.00'))
        except InvalidOperation:
            travel = Decimal('0.00')

        try:
            total_amount = Decimal(request.POST.get('total_amount', '0.00'))
        except InvalidOperation:
            total_amount = Decimal('0.00')

        try:
            recieved_price = Decimal(request.POST.get('recieved_price', '0.00'))
        except InvalidOperation:
            recieved_price = Decimal('0.00')

        try:
            pending_price = Decimal(request.POST.get('pending_price', '0.00'))
        except InvalidOperation:
            pending_price = Decimal('0.00')

        try:
            profit = Decimal(request.POST.get('profit', '0.00'))
        except InvalidOperation:
            profit = Decimal('0.00')

        try:
            navigo = Decimal(request.POST.get('navigo', '0.00'))
        except InvalidOperation:
            navigo = Decimal('0.00')

        customer_instance = get_object_or_404(Customers, id=customer_id)
        sales_person = get_object_or_404(CustomUser, id=sales_person_id)
        resort_instance = get_object_or_404(Stay, id=resort_id)
        account_instance = get_object_or_404(BankAccount, id=account_id)
        meal_instance = get_object_or_404(MealPlans, id=meal_plan_id)

        voucher_number = generate_voucher_number()

        Voucher.objects.create(
            customer=customer_instance,
            sales_person=sales_person,
            resort_name=resort_instance,
            account_name=account_instance,
            meal_plan=meal_instance,
            voucher_number=voucher_number,
            voucher_date=voucher_date,
            checkin_date=checkin_date,
            checkout_date=checkout_date,
            mobile=mobile,
            checkin_time=checkin_time,
            checkout_time=checkout_time,
            adults=adults,
            children=children if children else 0,
            number_of_nights=number_of_nights,
            room_type=room_type,
            number_of_rooms=number_of_rooms,
            package_price=package_price,
            resort_price=resort_price,
            travel=travel,
            total_amount=total_amount,
            recieved_price=recieved_price,
            pending_price=pending_price,
            profit=profit,
            navigo=navigo,
        )
        messages.success(request,'Voucher created successfully')
        return redirect('employee_salevoucher')

    customers = Customers.objects.all()
    sales_persons = CustomUser.objects.all()
    resorts = Stay.objects.all()
    bank_accounts = BankAccount.objects.all()
    meals = MealPlans.objects.all()

    return render(request, 'EmpSales/EmpSale_voucher/employee_Sale_voucher_add.html', {
        'customers': customers,
        'sales_persons': sales_persons,
        'resorts': resorts,
        'bank_accounts': bank_accounts,
        'meals': meals,
        'next_voucher_number': generate_voucher_number()
    })

def generate_voucher_number():
    last_voucher = Voucher.objects.aggregate(Max('id'))
    last_id = last_voucher['id__max']
    if last_id:
        return f'VOC-{last_id + 1:04d}'
    else:
        return 'VOC-0001'
    

@login_required(login_url='employee_signin')
def employee_salevoucherview(request,voucher_id):
    voucher = get_object_or_404(Voucher, id=voucher_id)
    context = {
        'voucher': voucher
    }
    return render(request,'EmpSales/EmpSale_voucher/employee_Sale_voucher_view.html',context)


@login_required(login_url='employee_signin')
def employee_salevoucheredit(request,voucher_id):
    voucher = get_object_or_404(Voucher, id=voucher_id)

    if request.method == "POST":
        try:
            voucher.customer_id = request.POST.get('customer_id')
            voucher.sales_person_id = request.POST.get('sales_person')
            voucher.resort_name_id = request.POST.get('resort_id')
            voucher.account_name_id = request.POST.get('bank_account')
            voucher.meal_plan_id = request.POST.get('meal_plan')
            voucher.voucher_date = request.POST.get('voucher_date')
            voucher.checkin_date = request.POST.get('checkin_date')
            voucher.checkout_date = request.POST.get('checkout_date')
            voucher.mobile = request.POST.get('mobile')
            voucher.checkin_time = request.POST.get('checkin_time')
            voucher.checkout_time = request.POST.get('checkout_time')
            voucher.adults = request.POST.get('adults')
            voucher.children = request.POST.get('children')
            voucher.number_of_nights = request.POST.get('number_of_nights')
            voucher.room_type = request.POST.get('room_type')
            voucher.number_of_rooms = request.POST.get('number_of_rooms')

            # Handle decimal fields, converting None or invalid values to Decimal('0.00')
            try:
                voucher.package_price = Decimal(request.POST.get('package_price', '0.00'))
            except InvalidOperation:
                voucher.package_price = Decimal('0.00')

            try:
                voucher.resort_price = Decimal(request.POST.get('resort_price', '0.00'))
            except InvalidOperation:
                voucher.resort_price = Decimal('0.00')

            try:
                voucher.travel = Decimal(request.POST.get('travel', '0.00'))
            except InvalidOperation:
                voucher.travel = Decimal('0.00')

            try:
                voucher.total_amount = Decimal(request.POST.get('total_amount', '0.00'))
            except InvalidOperation:
                voucher.total_amount = Decimal('0.00')

            try:
                voucher.recieved_price = Decimal(request.POST.get('recieved_price', '0.00'))
            except InvalidOperation:
                voucher.recieved_price = Decimal('0.00')

            try:
                voucher.pending_price = Decimal(request.POST.get('pending_price', '0.00'))
            except InvalidOperation:
                voucher.pending_price = Decimal('0.00')

            try:
                voucher.profit = Decimal(request.POST.get('profit', '0.00'))
            except InvalidOperation:
                voucher.profit = Decimal('0.00')

            try:
                voucher.navigo = Decimal(request.POST.get('navigo', '0.00'))
            except InvalidOperation:
                voucher.navigo = Decimal('0.00')

            voucher.save()
            messages.success(request, 'Voucher updated successfully')
        except InvalidOperation:
            messages.error(request, 'Failed to update voucher due to invalid data')

        return redirect('salevoucher')

    customers = Customers.objects.all()
    sales_persons = CustomUser.objects.all()
    resorts = Stay.objects.all()
    bank_accounts = BankAccount.objects.all()
    meals = MealPlans.objects.all()
    selected_resort = voucher.resort_name

    return render(request, 'EmpSales/EmpSale_voucher/employee_Sale_voucher_edit.html', {
        'voucher': voucher,
        'customers': customers,
        'sales_persons': sales_persons,
        'resorts': resorts,
        'bank_accounts': bank_accounts,
        'meals': meals,
        'selected_resort': selected_resort
    })


@login_required(login_url='employee_signin')
def employee_salevoucherdelete(request, voucher_id):
    voucher = get_object_or_404(Voucher, id=voucher_id)
    if request.method == "POST":
        voucher.delete()
        messages.success(request, 'Voucher deleted successfully.')
        return redirect('employee_salevoucher')  # Adjust this redirect to your actual voucher list view name
    
#------------------------------------------------- Record Payment ------------------------------------

def employee_voucher_record_payment(request, id):
    voucher = get_object_or_404(Voucher, id=id)

    if request.method == 'POST':
        # Retrieve form data
        client_name = request.POST.get('client_name')
        voucher_number = request.POST.get('voucher_number')
        amount_received = request.POST.get('amount_received')
        payment_date = request.POST.get('payment_date')
        payment_mode = request.POST.get('payment_mode')

        # Save payment details to the database (adjust based on your models)
        VoucherPayment.objects.create(
            voucher=voucher,
            client_name=client_name,
            voucher_number=voucher_number,
            amount_received=amount_received,
            payment_date=payment_date,
            payment_mode=payment_mode
        )

        # Redirect back to the invoice view or any other desired page
        return redirect('employee_salevoucherview',  voucher_id=id)

    return render(request, 'EmpSales/EmpSale_voucher/employee_Sale_voucher_view.html', {'vouchers': voucher})

#------------------------------------- Send Voucher email --------------------------------------

def employee_send_voucher_email(request, voucher_id):
    voucher = get_object_or_404(Voucher, id=voucher_id)
    customer_email = voucher.customer.customer_email

    subject = f"Booking for {voucher.customer.full_name} - For {voucher.resort_name.resort_name}"
    voucher_id = voucher.id
    viewcolor_link = f'https://www.sales.navigotrips.com/voucher_emails/{voucher_id}/'
    
    message = f'Dear team, Greetings From Navigo !!! As per the telephonic conversation , Kindly Confirm as follows:'

   
    
    html_message = render_to_string('emailtemplates/emailvoucher.html', {'voucher': voucher, 'viewcolor_link': viewcolor_link,'subject': subject,
        'message': message})
    text_message = message

    email = EmailMultiAlternatives(subject, text_message, settings.DEFAULT_FROM_EMAIL, [customer_email])
    email.attach_alternative(html_message, "text/html")
    email.send()

    messages.success(request, 'Email sent successfully.')
    return redirect('employee_salevoucher')



def voucher_email_template(request,voucher_id):
    voucher = get_object_or_404(Voucher, id=voucher_id)
    return render(request,'voucher_email_template.html', {'voucher':voucher})


#----------------------------------------- Voucher wattsapp message --------------------------------------

# def send_voucher_whatsapp(customer_display_name, resort_name, checkin_date, checkin_time, voucher_id, mobile):
#     url = "https://live-mt-server.wati.io/304152/api/v1/sendTemplateMessages"

#     payload = {
#         "broadcast_name": "welcome",
#         "receivers": [
#             {
#                 "customParams": [
#                     {"name": "name", "value": customer_display_name},
#                     {"name": "resortname", "value": resort_name},
#                     {"name": "date", "value": checkin_date},
#                     {"name": "checkingtime", "value": checkin_time},
#                     {"name": "voucher_url", "value": f"http://127.0.0.1:8000/voucher_email/{voucher_id}/"}
#                 ],
#                 "whatsappNumber": "91" + mobile
#             }
#         ],
#         "template_name": "welcome_vchr"
#     }
#     headers = {
#         "content-type": "text/json",
#         "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJlZWYxZGUxNy0wZDNkLTRkY2UtYTg1My05ZmY0Y2ZiMWYyNTUiLCJ1bmlxdWVfbmFtZSI6InJlc2VydmF0aW9uc0B3aHl0ZWhvdXNlaG9saWRheXMuY29tIiwibmFtZWlkIjoicmVzZXJ2YXRpb25zQHdoeXRlaG91c2Vob2xpZGF5cy5jb20iLCJlbWFpbCI6InJlc2VydmF0aW9uc0B3aHl0ZWhvdXNlaG9saWRheXMuY29tIiwiYXV0aF90aW1lIjoiMDMvMjEvMjAyNCAwNjowMDoxMSIsImRiX25hbWUiOiJtdC1wcm9kLVRlbmFudHMiLCJ0ZW5hbnRfaWQiOiIzMDQxNTIiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6IkNsYXJlX0FJIiwiYXVkIjoiQ2xhcmVfQUkifQ.HzxDKryVrHFaIzuydZ4jYgVxs96m2QHZNAN5kxB1lPc"  # Replace with your actual token
#     }
#     response = requests.post(url, json=payload, headers=headers)
#     print(response.text)
#     if response.status_code == 200:
#         print("WhatsApp message sent successfully.")
#     else:
#         print(
#             f"Failed to send WhatsApp message. Status Code: {response.status_code}, Response: {response.text}")




# def send_voucher_whatsapp_message(request, voucher_id):
#     voucher = get_object_or_404(Voucher, id=voucher_id)

#     # Extract necessary data from the invoice object
#     customer_display_name = voucher.customer.customer_display_name
#     print(customer_display_name)
#     resort_name = voucher.resort_name.resort_name
#     print(resort_name)
#     checkin_date = voucher.checkin_date.strftime('%d-%B-%Y')  # Convert date to string
#     print(checkin_date)
#     checkin_time = voucher.checkin_time
#     mobile = voucher.customer.contact_number
#     print(mobile)
#     voucher_url = f"http://127.0.0.1:8000/voucher_email/{voucher.id}/"  # Assuming invoice id is unique

#     send_voucher_whatsapp(customer_display_name, resort_name, checkin_date, checkin_time, voucher_id, mobile)
#     messages.success(request, 'WhatsApp message sent successfully.')

#     return redirect('salevoucher')


#------------------------------------- Postpone Voucher wattssapp msg-------------------------------


# def employee_send_voucher_whatsapp_postpone_voucher(customer_display_name, resort_name, checkin_date, checkin_time, voucher_id, mobile):
#     url = "https://live-mt-server.wati.io/304152/api/v1/sendTemplateMessages"

#     payload = {
#         "broadcast_name": "welcome",
#         "receivers": [
#             {
#                 "customParams": [
#                     {"name": "name", "value": customer_display_name},
#                     {"name": "resortname", "value": resort_name},
#                     {"name": "date", "value": checkin_date},
#                     {"name": "time", "value": checkin_time},
#                     {"name": "vcr_url", "value": f"http://sales.whytehouseholidays.com/voucher_email/{voucher_id}/"}
#                 ],
#                 "whatsappNumber": "91" + mobile
#             }
#         ],
#         "template_name": "postpone_voucher"
#     }
#     headers = {
#         "content-type": "text/json",
#         "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJlZWYxZGUxNy0wZDNkLTRkY2UtYTg1My05ZmY0Y2ZiMWYyNTUiLCJ1bmlxdWVfbmFtZSI6InJlc2VydmF0aW9uc0B3aHl0ZWhvdXNlaG9saWRheXMuY29tIiwibmFtZWlkIjoicmVzZXJ2YXRpb25zQHdoeXRlaG91c2Vob2xpZGF5cy5jb20iLCJlbWFpbCI6InJlc2VydmF0aW9uc0B3aHl0ZWhvdXNlaG9saWRheXMuY29tIiwiYXV0aF90aW1lIjoiMDMvMjEvMjAyNCAwNjowMDoxMSIsImRiX25hbWUiOiJtdC1wcm9kLVRlbmFudHMiLCJ0ZW5hbnRfaWQiOiIzMDQxNTIiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6IkNsYXJlX0FJIiwiYXVkIjoiQ2xhcmVfQUkifQ.HzxDKryVrHFaIzuydZ4jYgVxs96m2QHZNAN5kxB1lPc"  # Replace with your actual token
#     }
#     response = requests.post(url, json=payload, headers=headers)
#     print(response.text)
#     if response.status_code == 200:
#         print("WhatsApp message sent successfully.")
#     else:
#         print(
#             f"Failed to send WhatsApp message. Status Code: {response.status_code}, Response: {response.text}")




# def send_voucher_whatsapp_postpone_voucher_message(request, voucher_id):
#     voucher = get_object_or_404(Voucher, id=voucher_id)

#     # Extract necessary data from the invoice object
#     customer_display_name = voucher.customer.customer_display_name
#     print(customer_display_name)
#     resort_name = voucher.resort_name.resort_name
#     print(resort_name)
#     checkin_date = voucher.checkin_date.strftime('%d-%B-%Y')  # Convert date to string
#     print(checkin_date)
#     checkin_time = voucher.checkin_time
#     mobile = voucher.customer.contact_number
#     print(mobile)
#     voucher_url = f"http://sales.whytehouseholidays.com/voucher_email/{voucher.id}/"  # Assuming invoice id is unique

#     employee_send_voucher_whatsapp_postpone_voucher(customer_display_name, resort_name, checkin_date, checkin_time, voucher_id, mobile)
#     messages.success(request, 'WhatsApp message sent successfully.')

#     return redirect('employee_salevoucher')

# #------------------------------------------ Postpone Voucher -----------------------------------------


# def employee_postpone_voucher(request, voucher_id):
#     voucher = get_object_or_404(Voucher, id=voucher_id)

#     if request.method == "POST":
#         try:
#             voucher.customer_id = request.POST.get('customer_id')
#             voucher.sales_person_id = request.POST.get('sales_person')
#             voucher.resort_name_id = request.POST.get('resort_name')
#             voucher.account_name_id = request.POST.get('bank_account')
#             voucher.meal_plan_id = request.POST.get('meal_plan')
#             voucher.voucher_date = request.POST.get('voucher_date')
#             voucher.checkin_date = request.POST.get('checkin_date')
#             voucher.checkout_date = request.POST.get('checkout_date')
#             voucher.mobile = request.POST.get('mobile')
#             voucher.checkin_time = request.POST.get('checkin_time')
#             voucher.checkout_time = request.POST.get('checkout_time')
#             voucher.adults = request.POST.get('adults')
#             voucher.children = request.POST.get('children')
#             voucher.number_of_nights = request.POST.get('number_of_nights')
#             voucher.room_type = request.POST.get('room_type')
#             voucher.number_of_rooms = request.POST.get('number_of_rooms')

#             # Handle decimal fields, converting None or invalid values to Decimal('0.00')
#             try:
#                 voucher.package_price = Decimal(request.POST.get('package_price', '0.00'))
#             except InvalidOperation:
#                 voucher.package_price = Decimal('0.00')
            
#             try:
#                 voucher.resort_price = Decimal(request.POST.get('resort_price', '0.00'))
#             except InvalidOperation:
#                 voucher.resort_price = Decimal('0.00')

#             try:
#                 voucher.travel = Decimal(request.POST.get('travel', '0.00'))
#             except InvalidOperation:
#                 voucher.travel = Decimal('0.00')

#             try:
#                 voucher.total_amount = Decimal(request.POST.get('total_amount', '0.00'))
#             except InvalidOperation:
#                 voucher.total_amount = Decimal('0.00')

#             try:
#                 voucher.recieved_price = Decimal(request.POST.get('recieved_price', '0.00'))
#             except InvalidOperation:
#                 voucher.recieved_price = Decimal('0.00')

#             try:
#                 voucher.pending_price = Decimal(request.POST.get('pending_price', '0.00'))
#             except InvalidOperation:
#                 voucher.pending_price = Decimal('0.00')

#             try:
#                 voucher.profit = Decimal(request.POST.get('profit', '0.00'))
#             except InvalidOperation:
#                 voucher.profit = Decimal('0.00')

#             try:
#                 voucher.navigo = Decimal(request.POST.get('navigo', '0.00'))
#             except InvalidOperation:
#                 voucher.navigo = Decimal('0.00')

#             voucher.save()
#             messages.success(request, 'Voucher updated successfully')
#             return redirect('employee_customerview',id=voucher.customer.id)
#         except InvalidOperation:
#             messages.error(request, 'Failed to update voucher due to invalid data')

#         return redirect('employee_postpone_voucher', voucher_id=voucher_id)

#     customers = Customers.objects.all()
#     sales_persons = CustomUser.objects.all()
#     resorts = Stay.objects.all()
#     bank_accounts = BankAccount.objects.all()
#     meals = MealPlans.objects.all()

#     return render(request, 'EmpPostpone/employee_postpone_voucher.html', {
#         'voucher': voucher,
#         'customers': customers,
#         'sales_persons': sales_persons,
#         'resorts': resorts,
#         'bank_accounts': bank_accounts,
#         'meals': meals,
#     })


# #------------------------------------------- Cancel Voucher --------------------------------------

# def employee_cancelvoucher(request, id):
#     voucher = get_object_or_404(Voucher, id=id)
    
#     if request.method == "POST":
#         # Perform any additional cancellation logic if needed
#         # For example, cancel_booking(request, id)
        
#         # Delete the invoice
#         voucher.delete()
        
#         # Add success message
#         messages.success(request, 'Voucher cancelled successfully.')
        
#         # Redirect back to customerview with the customer's ID
#         return redirect('employee_customerview', id=voucher.customer.id)
    
#     # If it's not a POST request, render the template with invoice details
#     return render(request, 'EmpSales/EmpCustomers/employee_Customers_View.html', {'voucher': voucher})

#----------------------------------------- Send Wttsapp --------------------------------------------

def send_whatsapps(customer_display_name, resort_name, checkin_date, checkin_time, voucher_id,location, whatsapp_number,country_code_whatsapp):
    url = "https://live-mt-server.wati.io/329541/api/v1/sendTemplateMessages"
    
    payload = {
        "broadcast_name": "Navigo Trips",
        "receivers": [
            {
                "customParams": [
                    {"name": "name", "value": customer_display_name},
                    {"name": "resort_name", "value": resort_name},
                    {"name": "date", "value": checkin_date},
                    {"name": "time", "value": checkin_time},
                    {"name": "inv_link", "value": f"voucher_whattsapp/{voucher_id}/"},
                    {"name": "location_url", "value": location}
                ],
                "whatsappNumber": country_code_whatsapp + whatsapp_number
            }
        ],
        "template_name": "stays_vouchers"
    }
    
    headers = {
        "content-type": "text/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI4MTMzMmU2OC0wODRkLTQ1MjMtODU0MS04MWYyMmI5ZWJiMDMiLCJ1bmlxdWVfbmFtZSI6Im5hdmlnb3RyaXBzQGdtYWlsLmNvbSIsIm5hbWVpZCI6Im5hdmlnb3RyaXBzQGdtYWlsLmNvbSIsImVtYWlsIjoibmF2aWdvdHJpcHNAZ21haWwuY29tIiwiYXV0aF90aW1lIjoiMDgvMDIvMjAyNCAwODo0Nzo1NCIsImRiX25hbWUiOiJtdC1wcm9kLVRlbmFudHMiLCJ0ZW5hbnRfaWQiOiIzMjk1NDEiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6IkNsYXJlX0FJIiwiYXVkIjoiQ2xhcmVfQUkifQ.wr78I9zQx18T6PovGICUHJhWWjofegZiGpdpfZlHFz8"  # Replace with your actual token
    }
    
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)
    if response.status_code == 200:
        print("WhatsApp message sent successfully.")
    else:
        print(f"Failed to send WhatsApp message. Status Code: {response.status_code}, Response: {response.text}")


def employee_send_stay_whatsapp_voucher_message(request, voucher_id):
    invoice = get_object_or_404(Voucher, id=voucher_id)

    # Extract necessary data from the invoice object
    customer_display_name = invoice.customer.customer_display_name
    resort_name = invoice.resort_name.resort_name
    checkin_date = invoice.checkin_date.strftime('%d-%B-%Y')  # Convert date to string
    checkin_time = invoice.checkin_time
    location = invoice.resort_name.location
    whatsapp_number = invoice.customer.whatsapp_number
    country_code_whatsapp = invoice.customer.country_code_whatsapp
    voucher__url = f"https://www.sales.navigotrips.com/voucher_whattsapp/{voucher_id}/"  # Assuming invoice id is unique

    missing_fields = {
        'Customer Display Name': customer_display_name,
        'Resort Name': resort_name,
        'Check-in Date': checkin_date,
        'Check-in Time': checkin_time,
        'Location': location,
        'WhatsApp Number': whatsapp_number,
        'Country Code for WhatsApp': country_code_whatsapp
    }

    # Identify missing values
    missing_values = [field for field, value in missing_fields.items() if not value]

    if missing_values:
        missing_values_str = ", ".join(missing_values)
        messages.error(request, f"Missing required values: {missing_values_str}. All values must be filled to send the WhatsApp message.")
        return redirect('employee_salevoucher')

    # Call the send_whatsapp_reminder function
    send_whatsapps(customer_display_name, resort_name, checkin_date, checkin_time, voucher_id,location, whatsapp_number,country_code_whatsapp)

    messages.success(request, 'WhatsApp message sent successfully.')
    return redirect('employee_salevoucher')







def employee_voucher_whatsapp(request,voucher_id):
    voucher = get_object_or_404(Voucher, id=voucher_id)
    return render(request,'whatsapp_templates/voucher_whattsapp.html', {'voucher':voucher})






#------------------------------------------ Postpone voucher ------------------------------------


def employee_send_whatsapp_postpone_voucher(voucher_id, new_date, new_resort_name=None):
    voucher = get_object_or_404(Voucher, id=voucher_id)
    
    customer_name = voucher.customer.customer_display_name
    original_resort_name = voucher.resort_name.resort_name
    resort_name = new_resort_name if new_resort_name else original_resort_name
    original_date = voucher.checkin_date.strftime('%d-%B-%Y')
    new_date = new_date.strftime('%d-%B-%Y')
    whatsapp_number = voucher.customer.whatsapp_number
    country_code_whatsapp = voucher.customer.country_code_whatsapp

    url = "https://live-mt-server.wati.io/329541/api/v1/sendTemplateMessages"
    payload = {
        "broadcast_name": "Navigo Trips",
        "receivers": [
            {
                "customParams": [
                    {"name": "name", "value": customer_name},
                    {"name": "resortname", "value": resort_name},
                    {"name": "date", "value": original_date},
                    {"name": "newdate", "value": new_date}
                ],
                "whatsappNumber": country_code_whatsapp + whatsapp_number
            }
        ],
        "template_name": "postpone_voucher_stay"
    }
    headers = {
        "content-type": "text/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI4MTMzMmU2OC0wODRkLTQ1MjMtODU0MS04MWYyMmI5ZWJiMDMiLCJ1bmlxdWVfbmFtZSI6Im5hdmlnb3RyaXBzQGdtYWlsLmNvbSIsIm5hbWVpZCI6Im5hdmlnb3RyaXBzQGdtYWlsLmNvbSIsImVtYWlsIjoibmF2aWdvdHJpcHNAZ21haWwuY29tIiwiYXV0aF90aW1lIjoiMDgvMDIvMjAyNCAwODo0Nzo1NCIsImRiX25hbWUiOiJtdC1wcm9kLVRlbmFudHMiLCJ0ZW5hbnRfaWQiOiIzMjk1NDEiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6IkNsYXJlX0FJIiwiYXVkIjoiQ2xhcmVfQUkifQ.wr78I9zQx18T6PovGICUHJhWWjofegZiGpdpfZlHFz8"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        print("WhatsApp message sent successfully.")
    else:
        print(f"Failed to send WhatsApp message. Status Code: {response.status_code}, Response: {response.text}")

def employee_send_whatsapp_postpone_voucher_message(request, voucher_id):
    voucher = get_object_or_404(Voucher, id=voucher_id)

    # Assuming 'new_checkin_date' is posted as 'YYYY-MM-DD'
    new_date_str = request.POST.get('new_checkin_date')
    new_date = datetime.strptime(new_date_str, '%Y-%m-%d').date()

    missing_fields = {
        'New Check-in Date': new_date_str,
        'Customer Display Name': voucher.customer.customer_display_name,
        'Resort Name': voucher.resort_name.resort_name,
        'Voucher ID': voucher_id,
    }

    # Identify missing values
    missing_values = [field for field, value in missing_fields.items() if not value]

    if missing_values:
        missing_values_str = ", ".join(missing_values)
        messages.error(request, f"Missing required values: {missing_values_str}. All values must be filled to send the WhatsApp postpone message.")
        return redirect('employee_voucher_detail', voucher_id=voucher_id)
    
    # Call the send_whatsapp_postpone_voucher function
    employee_send_whatsapp_postpone_voucher(voucher_id, new_date)
    
    # Update the voucher with the new check-in date
    voucher.checkin_date = new_date
    voucher.save()

    messages.success(request, 'WhatsApp postpone message sent successfully and voucher updated.')
    return redirect('employee_voucher_detail', voucher_id=voucher_id)



def employee_postpone_voucher(request, voucher_id):
    voucher = get_object_or_404(Voucher, id=voucher_id)

    if request.method == "POST":
        try:
            # Store the original check-in date and resort name
            original_checkin_date = voucher.checkin_date
            original_resort_name = voucher.resort_name

            # Update voucher fields
            voucher.customer_id = int(request.POST.get('customer_id'))
            voucher.sales_person_id = int(request.POST.get('sales_person'))
            new_resort_id = int(request.POST.get('resort_name'))
            voucher.resort_name_id = new_resort_id
            voucher.account_name_id = int(request.POST.get('bank_account'))
            voucher.meal_plan_id = int(request.POST.get('meal_plan'))
            voucher.voucher_date = request.POST.get('voucher_date')
            new_checkin_date = request.POST.get('checkin_date')
            voucher.checkin_date = new_checkin_date
            voucher.checkout_date = request.POST.get('checkout_date')
            voucher.mobile = request.POST.get('mobile')
            voucher.checkin_time = request.POST.get('checkin_time')
            voucher.checkout_time = request.POST.get('checkout_time')
            voucher.adults = int(request.POST.get('adults'))
            voucher.children = int(request.POST.get('children'))
            voucher.number_of_nights = int(request.POST.get('number_of_nights'))
            voucher.room_type = request.POST.get('room_type')
            voucher.number_of_rooms = int(request.POST.get('number_of_rooms'))
            
            # Handle decimal fields
            voucher.package_price = Decimal(request.POST.get('package_price') or 0)
            voucher.resort_price = Decimal(request.POST.get('resort_price') or 0)
            voucher.travel = Decimal(request.POST.get('travel') or 0)
            voucher.total_amount = Decimal(request.POST.get('total_amount') or 0)
            voucher.recieved_price = Decimal(request.POST.get('recieved_price') or 0)
            voucher.pending_price = Decimal(request.POST.get('pending_price') or 0)
            voucher.profit = Decimal(request.POST.get('profit') or 0)
            voucher.navigo = Decimal(request.POST.get('navigo') or 0)

            # Get the new resort name
            new_resort = Stay.objects.get(id=new_resort_id)
            new_resort_name = new_resort.resort_name if new_resort.id != original_resort_name.id else None

            # Send WhatsApp message with original and new check-in dates, and new resort name if changed
            employee_send_whatsapp_postpone_voucher(
                voucher.id, 
                datetime.strptime(new_checkin_date, '%Y-%m-%d').date(),
                new_resort_name
            )

            voucher.save()

            messages.success(request, 'Voucher updated successfully and WhatsApp message sent.')
            return redirect('employee_customerview', id=voucher.customer.id)

        except (ValueError, TypeError, InvalidOperation) as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('employee_postpone_voucher', voucher_id=voucher_id)

    # If it's a GET request, prepare the form
    customers = Customers.objects.all()
    sales_persons = CustomUser.objects.all()
    resorts = Stay.objects.all()
    bank_accounts = BankAccount.objects.all()
    meals = MealPlans.objects.all()

    return render(request, 'EmpPostpone/employee_postpone_voucher.html', {
        'voucher': voucher,
        'customers': customers,
        'sales_persons': sales_persons,
        'resorts': resorts,
        'bank_accounts': bank_accounts,
        'meals': meals,
    })





#-------------------------------------- Cancel Booking -----------------------------------


def employee_send_whatsapp_cancel_voucher_message(request, voucher_id, cancellation_date):
    voucher = get_object_or_404(Voucher, id=voucher_id)
    
    customer_name = voucher.customer.customer_display_name
    resort_name = voucher.resort_name.resort_name
    checkin_date = voucher.checkin_date.strftime('%d-%B-%Y')
    cancel_date = cancellation_date.strftime('%d-%B-%Y')
    whatsapp_number = voucher.customer.whatsapp_number
    country_code_whatsapp = voucher.customer.country_code_whatsapp
    
    url = "https://live-mt-server.wati.io/329541/api/v1/sendTemplateMessages"
    payload = {
        "broadcast_name": "Navigo Trips",
        "receivers": [
            {
                "customParams": [
                    {"name": "name", "value": customer_name},
                    {"name": "resortname", "value": resort_name},
                    {"name": "date", "value": checkin_date},
                    {"name": "canceldate", "value": cancel_date}
                ],
                "whatsappNumber": country_code_whatsapp + whatsapp_number
            }
        ],
        "template_name": "cancel_stay_voucher"
    }
    headers = {
        "content-type": "text/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI4MTMzMmU2OC0wODRkLTQ1MjMtODU0MS04MWYyMmI5ZWJiMDMiLCJ1bmlxdWVfbmFtZSI6Im5hdmlnb3RyaXBzQGdtYWlsLmNvbSIsIm5hbWVpZCI6Im5hdmlnb3RyaXBzQGdtYWlsLmNvbSIsImVtYWlsIjoibmF2aWdvdHJpcHNAZ21haWwuY29tIiwiYXV0aF90aW1lIjoiMDgvMDIvMjAyNCAwODo0Nzo1NCIsImRiX25hbWUiOiJtdC1wcm9kLVRlbmFudHMiLCJ0ZW5hbnRfaWQiOiIzMjk1NDEiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6IkNsYXJlX0FJIiwiYXVkIjoiQ2xhcmVfQUkifQ.wr78I9zQx18T6PovGICUHJhWWjofegZiGpdpfZlHFz8"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        print("WhatsApp cancellation message sent successfully.")
    else:
        print(f"Failed to send WhatsApp cancellation message. Status Code: {response.status_code}, Response: {response.text}")



def employee_cancelvoucher(request, voucher_id):
    voucher = get_object_or_404(Voucher, id=voucher_id)
    
    if request.method == "POST":
        try:
            # Update the cancellation date in the existing voucher record
            voucher.cancellation_date = datetime.now().date()

            # Send WhatsApp message
            employee_send_whatsapp_cancel_voucher_message(request, voucher.id, voucher.cancellation_date)
            
            # Save the updated voucher
            voucher.save()
            
            # Add success message
            messages.success(request, 'Voucher cancelled successfully and WhatsApp message sent.')
            
            # Redirect back to the customer view with the customer's ID
            return redirect('employee_customerview', id=voucher.customer.id)
        
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('employee_customerview', id=voucher.customer.id)
    
    # If it's not a POST request, render the template with voucher details
    return render(request, 'EmpSales/EmpCustomers/employee_Customers_View.html', {'voucher': voucher})
    