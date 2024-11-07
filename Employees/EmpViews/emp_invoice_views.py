import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,redirect,get_object_or_404
from dashboard.models import *
from django.http import JsonResponse
from django.db.models import Max, Q
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.decorators import login_required
from decimal import Decimal, InvalidOperation
import datetime
from datetime import datetime


@login_required(login_url='employee_signin')
def employee_saleinvoice(request):
    invoices_list = Invoice.objects.all().order_by('-id')
    query = request.GET.get('q')
    if query:
        invoices_list = invoices_list.filter(Q(customer__full_name__icontains=query) | Q(mobile__icontains=query))

    paginator = Paginator(invoices_list, 10)
    page_number = request.GET.get('page')
    try:
        invoices = paginator.page(page_number)
    except PageNotAnInteger:
        invoices = paginator.page(1)
    except EmptyPage:
        invoices = paginator.page(paginator.num_pages)
    return render(request, 'EmpSales/EmpSale_invoice/employee_Sale_invoice.html', {'invoices': invoices, 'query': query})

@login_required(login_url='employee_signin')
def employee_saleinvoiceadd(request):
    if request.method == "POST":
        try:
            customer_id = request.POST.get('customer_id')
            sales_person_id = request.POST.get('sales_person')
            resort_id = request.POST.get('resort_name')
            account_id = request.POST.get('bank_account')
            meal_plan_id = request.POST.get('meal_plan')
            invoice_date = request.POST.get('invoice_date')
            due_date = request.POST.get('due_date')
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
            decimal_fields = ['package_price', 'resort_price', 'travel', 'total_amount', 
                              'tax', 'recieved_price', 'pending_price', 'profit', 'navigo']
            
            decimal_values = {}
            for field in decimal_fields:
                try:
                    decimal_values[field] = Decimal(request.POST.get(field, '0.00'))
                except InvalidOperation:
                    decimal_values[field] = Decimal('0.00')

            customer_instance = get_object_or_404(Customers, id=customer_id)
            sales_person = get_object_or_404(CustomUser, id=sales_person_id)
            resort_instance = get_object_or_404(Stay, id=resort_id)
            account_instance = get_object_or_404(BankAccount, id=account_id)
            meal_instance = get_object_or_404(MealPlans, id=meal_plan_id)

            invoice_number = generate_invoice_number()

            Invoice.objects.create(
                customer=customer_instance,
                sales_person=sales_person,
                resort_name=resort_instance,
                account_name=account_instance,
                meal_plan=meal_instance,
                invoice_number=invoice_number,
                invoice_date=invoice_date,
                due_date=due_date,
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
                **decimal_values
            )
            messages.success(request, 'Invoice created successfully')
            return redirect('employee_saleinvoice')
        except Exception as e:
            messages.error(request, f'Failed to create invoice: {str(e)}')

    # This part handles both GET requests and failed POST requests
    customers = Customers.objects.all()
    sales_persons = CustomUser.objects.all()
    resorts = Stay.objects.all()
    bank_accounts = BankAccount.objects.all()
    meals = MealPlans.objects.all()

    return render(request, 'EmpSales/EmpSale_invoice/employee_Sale_invoice_add.html', {
        'customers': customers,
        'sales_persons': sales_persons,
        'resorts': resorts,
        'bank_accounts': bank_accounts,
        'meals': meals,
        'next_invoice_number': generate_invoice_number()
    })

def generate_invoice_number():
    last_invoice = Invoice.objects.aggregate(Max('id'))
    last_id = last_invoice['id__max']
    if last_id:
        return f'INV-{last_id + 1:04d}'
    else:
        return 'INV-0001'


def search_customer(request):
    if 'term' in request.GET:
        qs = Customers.objects.filter(name__icontains=request.GET.get('term'))
        names = list()
        for customer in qs:
            names.append({'label': customer.name, 'value': customer.id})
        return JsonResponse(names, safe=False)
    return JsonResponse([], safe=False)

@login_required(login_url='employee_signin')
def employee_saleinvoiceview(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    context = {
        'invoice': invoice
    }
    return render(request, 'EmpSales/EmpSale_invoice/employee_Sale_invoice_view.html', context)


@login_required(login_url='employee_signin')
def employee_saleinvoiceedit(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    if request.method == "POST":
        try:
            invoice.customer_id = request.POST.get('customer_id')
            invoice.sales_person_id = request.POST.get('sales_person')
            invoice.resort_name_id = request.POST.get('resort_name')
            invoice.account_name_id = request.POST.get('bank_account')
            invoice.meal_plan_id = request.POST.get('meal_plan')
            invoice.invoice_date = request.POST.get('invoice_date')
            invoice.due_date = request.POST.get('due_date')
            invoice.checkin_date = request.POST.get('checkin_date')
            invoice.checkout_date = request.POST.get('checkout_date')
            invoice.mobile = request.POST.get('mobile')
            invoice.checkin_time = request.POST.get('checkin_time')
            invoice.checkout_time = request.POST.get('checkout_time')
            invoice.adults = request.POST.get('adults')
            invoice.children = request.POST.get('children')
            invoice.number_of_nights = request.POST.get('number_of_nights')
            invoice.room_type = request.POST.get('room_type')
            invoice.number_of_rooms = request.POST.get('number_of_rooms')
            
            # Handle decimal fields, converting None or invalid values to Decimal('0.00')
            decimal_fields = ['package_price', 'resort_price', 'travel', 'total_amount', 
                              'tax', 'recieved_price', 'pending_price', 'profit', 'navigo']
            
            for field in decimal_fields:
                try:
                    setattr(invoice, field, Decimal(request.POST.get(field, '0.00')))
                except InvalidOperation:
                    setattr(invoice, field, Decimal('0.00'))
            
            invoice.save()
            messages.success(request, 'Invoice updated successfully')
        except InvalidOperation:
            messages.error(request, 'Failed to update invoice due to invalid data')
        
        return redirect('employee_saleinvoice')
    
    # This part is for GET requests
    customers = Customers.objects.all()
    sales_persons = CustomUser.objects.all()
    resorts = Stay.objects.all()
    bank_accounts = BankAccount.objects.all()
    meals = MealPlans.objects.all()
    
    context = {
        'invoice': invoice,
        'customers': customers,
        'sales_persons': sales_persons,
        'resorts': resorts,
        'bank_accounts': bank_accounts,
        'meals': meals,
    }
    
    return render(request, 'EmpSales/EmpSale_invoice/employee_Sale_invoice_edit.html', context)



@login_required(login_url='employee_signin')
def employee_saleinvoicedelete(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if request.method == "POST":
        invoice.delete()
        messages.success(request, 'Invoice deleted successfully.')
        return redirect('employee_saleinvoice')  # Adjust this redirect to your actual voucher list view name
    

#----------------------------------------------- Record Payment -------------------------------------

def employee_invoice_record_payment(request, id):
    invoice = get_object_or_404(Invoice, id=id)

    if request.method == 'POST':
        # Retrieve form data
        client_name = request.POST.get('client_name')
        invoice_number = request.POST.get('invoice_number')
        amount_received = request.POST.get('amount_received')
        payment_date = request.POST.get('payment_date')
        payment_mode = request.POST.get('payment_mode')

        # Save payment details to the database (adjust based on your models)
        InvoicePayment.objects.create(
            invoice=invoice,
            client_name=client_name,
            invoice_number=invoice_number,
            amount_received=amount_received,
            payment_date=payment_date,
            payment_mode=payment_mode
        )

        # Redirect back to the invoice view or any other desired page
        return redirect('employee_saleinvoiceview', invoice_id=id)

    return render(request, 'EmpSales/EmpSale_invoice/employee_Sale_invoice_view.html', {'invoice': invoice})


#-------------------------------------- Sending Invoice mail --------------------------------------


def employee_send_invoice_email(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    subject = f"Booking for {invoice.customer.full_name}  - For {invoice.resort_name.resort_name}"
    viewcolor_link = f'https://www.sales.navigotrips.com/invoice_emails/{invoice.id}/'
    message = f'Dear team, Greetings From Navigo! As per the telephonic conversation, kindly confirm the following:'

    
    
    html_message = render_to_string('emailtemplates/emailinvoice.html', {'invoices': invoice, 'viewcolor_link': viewcolor_link,'subject': subject,
        'message': message})
    text_message = message
    customer_email = invoice.customer.customer_email
    email = EmailMultiAlternatives(subject, text_message, settings.DEFAULT_FROM_EMAIL, [customer_email])
    email.attach_alternative(html_message, "text/html")
    email.send()

    # Add success message
    messages.success(request, 'Email sent successfully.')

    # Redirect back to list_invoice view
    return redirect('employee_saleinvoice')



def invoice_email(request, invoice_id):
    invoices = get_object_or_404(Invoice, id=invoice_id)
    return render(request, 'invoice_email_template.html', {'invoices': invoices})


#--------------------------------------- Sending Invoice Wattsapp ------------------------------------------

# def send_whatsapps(customer_display_name, resort_name, checkin_date, checkin_time, invoice_id, mobile):
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
#                     {"name": "invoice_url", "value": f"http://127.0.0.1:8000/invoice_email/{invoice_id}/"}
#                 ],
#                 "whatsappNumber": "91" + mobile

#             }
#         ],
#         "template_name": "welcome_inv"
#     }
#     headers = {
#         "content-type": "text/json",
#         "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0Njc3ZTM1ZC0xMWQ0LTRlMzktYjM1MS1jNmUyNWQ0OGIwMGMiLCJ1bmlxdWVfbmFtZSI6InJlc2VydmF0aW9uc0B3aHl0ZWhvdXNlaG9saWRheXMuY29tIiwibmFtZWlkIjoicmVzZXJ2YXRpb25zQHdoeXRlaG91c2Vob2xpZGF5cy5jb20iLCJlbWFpbCI6InJlc2VydmF0aW9uc0B3aHl0ZWhvdXNlaG9saWRheXMuY29tIiwiYXV0aF90aW1lIjoiMDIvMTkvMjAyNCAxMjoyMDowMSIsImRiX25hbWUiOiJtdC1wcm9kLVRlbmFudHMiLCJ0ZW5hbnRfaWQiOiIzMDQxNTIiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6IkNsYXJlX0FJIiwiYXVkIjoiQ2xhcmVfQUkifQ.PUEsx0BCoFO4KL2-KK7vPTh-55tKLnOtM74oXF1bnjw"  # Replace with your actual token
#     }

#     response = requests.post(url, json=payload, headers=headers)
#     print(response.text)
#     if response.status_code == 200:
#         print("WhatsApp message sent successfully.")
#     else:
#         print(
#             f"Failed to send WhatsApp message. Status Code: {response.status_code}, Response: {response.text}")



# def send_whatsapp_message(request, invoice_id):
#     invoice = get_object_or_404(Invoice, id=invoice_id)

#     # Extract necessary data from the invoice object
#     customer_display_name = invoice.customer.customer_display_name
#     resort_name = invoice.resort_name.resort_name
#     checkin_date = invoice.checkin_date.strftime('%d-%B-%Y')  # Convert date to string
#     checkin_time = invoice.checkin_time
#     mobile = invoice.customer.contact_number
#     invoice_url = f"http://127.0.0.1:8000/invoice_email/{invoice.id}/"  # Assuming invoice id is unique

#     # Call the send_whatsapp_reminder function
#     send_whatsapps(customer_display_name, resort_name, checkin_date, checkin_time, invoice_id, mobile)

#     messages.success(request, 'WhatsApp message sent successfully.')
#     return redirect('saleinvoice')
    


#---------------------------------------- PostPone Invoice wattsapp msg -----------------------------------------

# def employee_send_whatsapp(customer_display_name, resort_name, checkin_date, checkin_time, invoice_id, mobile):
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
#                     {"name": "invoice_url", "value": f"http://sales.whytehouseholidays.com/invoice_email/{invoice_id}/"}
#                 ],
#                 "whatsappNumber": "91" + mobile

#             }
#         ],
#         "template_name": "cancel_inv"
#     }
#     headers = {
#         "content-type": "text/json",
#         "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0Njc3ZTM1ZC0xMWQ0LTRlMzktYjM1MS1jNmUyNWQ0OGIwMGMiLCJ1bmlxdWVfbmFtZSI6InJlc2VydmF0aW9uc0B3aHl0ZWhvdXNlaG9saWRheXMuY29tIiwibmFtZWlkIjoicmVzZXJ2YXRpb25zQHdoeXRlaG91c2Vob2xpZGF5cy5jb20iLCJlbWFpbCI6InJlc2VydmF0aW9uc0B3aHl0ZWhvdXNlaG9saWRheXMuY29tIiwiYXV0aF90aW1lIjoiMDIvMTkvMjAyNCAxMjoyMDowMSIsImRiX25hbWUiOiJtdC1wcm9kLVRlbmFudHMiLCJ0ZW5hbnRfaWQiOiIzMDQxNTIiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6IkNsYXJlX0FJIiwiYXVkIjoiQ2xhcmVfQUkifQ.PUEsx0BCoFO4KL2-KK7vPTh-55tKLnOtM74oXF1bnjw"  # Replace with your actual token
#     }

#     response = requests.post(url, json=payload, headers=headers)
#     print(response.text)
#     if response.status_code == 200:
#         print("WhatsApp message sent successfully.")
#     else:
#         print(
#             f"Failed to send WhatsApp message. Status Code: {response.status_code}, Response: {response.text}")


# def send_whatsapp_messages(request, invoice_id):
#     invoice = get_object_or_404(Invoice, id=invoice_id)

#     # Extract necessary data from the invoice object
#     customer_display_name = invoice.customer.customer_display_name
#     resort_name = invoice.resort_name.resort_name
#     checkin_date = invoice.checkin_date.strftime('%d-%B-%Y')  # Convert date to string
#     checkin_time = invoice.checkin_time
#     mobile = invoice.customer.contact_number
#     invoice_url = f"http://sales.whytehouseholidays.com/invoice_email/{invoice.id}/"  # Assuming invoice id is unique

#     # Call the send_whatsapp_reminder function
#     employee_send_whatsapp(customer_display_name, resort_name, checkin_date, checkin_time, invoice_id, mobile)

#     messages.success(request, 'WhatsApp message sent successfully.')
#     return redirect('employee_saleinvoice')

# #--------------------------------------- Postpone Invoice --------------------------------

# def employee_postpone_invoice(request, invoice_id):
#     invoice = get_object_or_404(Invoice, id=invoice_id)

#     if request.method == "POST":
#         try:
#             invoice.customer_id = int(request.POST.get('customer_id'))
#             invoice.sales_person_id = int(request.POST.get('sales_person'))
#             invoice.resort_name_id = int(request.POST.get('resort_name'))
#             invoice.account_name_id = int(request.POST.get('bank_account'))
#             invoice.meal_plan_id = int(request.POST.get('meal_plan'))
#             invoice.invoice_date = request.POST.get('invoice_date')
#             invoice.due_date = request.POST.get('due_date')
#             invoice.checkin_date = request.POST.get('checkin_date')
#             invoice.checkout_date = request.POST.get('checkout_date')
#             invoice.mobile = request.POST.get('mobile')
#             invoice.checkin_time = request.POST.get('checkin_time')
#             invoice.checkout_time = request.POST.get('checkout_time')
#             invoice.adults = int(request.POST.get('adults'))
#             invoice.children = int(request.POST.get('children'))
#             invoice.number_of_nights = int(request.POST.get('number_of_nights'))
#             invoice.room_type = request.POST.get('room_type')
#             invoice.number_of_rooms = int(request.POST.get('number_of_rooms'))
#             invoice.package_price = float(request.POST.get('package_price'))
#             invoice.resort_price = float(request.POST.get('resort_price'))
#             invoice.total_amount = float(request.POST.get('total_amount'))
#             invoice.tax = request.POST.get('tax')
#             invoice.recieved_price = float(request.POST.get('recieved_price'))
#             invoice.pending_price = float(request.POST.get('pending_price'))
#             invoice.profit = float(request.POST.get('profit'))
#             invoice.navigo = request.POST.get('navigo')
#             invoice.save()
#             send_whatsapp_messages(request, invoice.id)
#             messages.success(request, 'Invoice updated successfully.')

#             return redirect('employee_customerview', id=invoice.customer.id)
#         except (ValueError, TypeError) as e:
#             messages.error(request, f"An error occurred: {e}")
#             return redirect('employee_postpone_invoice', invoice_id=invoice_id)

#     customers = Customers.objects.all()
#     sales_persons = CustomUser.objects.all()
#     resorts = Stay.objects.all()
#     bank_accounts = BankAccount.objects.all()
#     meals = MealPlans.objects.all()

#     return render(request, 'EmpPostpone/employee_postpone_invoice.html', {
#         'invoice': invoice,
#         'customers': customers,
#         'sales_persons': sales_persons,
#         'resorts': resorts,
#         'bank_accounts': bank_accounts,
#         'meals': meals,
#     })

# #------------------------------------- Cancel Invoice wattsapp msg ---------------------------------------

# def employee_send_whatsapp_invoice_delete(customer_display_name, resort_name, checkin_date, checkin_time, invoice_id, mobile):
#     url = "https://live-mt-server.wati.io/304152/api/v1/sendTemplateMessages"

#     payload = {
#         "broadcast_name": "welcome",
#         "receivers": [
#             {
#                 "customParams": [
#                     {"name": "name", "value": customer_display_name},
#                     {"name": "resortname", "value": resort_name},
#                     {"name": "date", "value": checkin_date},

#                 ],
#                 "whatsappNumber": "91" + mobile

#             }
#         ],
#         "template_name": "cancel"
#     }
#     headers = {
#         "content-type": "text/json",
#         "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0Njc3ZTM1ZC0xMWQ0LTRlMzktYjM1MS1jNmUyNWQ0OGIwMGMiLCJ1bmlxdWVfbmFtZSI6InJlc2VydmF0aW9uc0B3aHl0ZWhvdXNlaG9saWRheXMuY29tIiwibmFtZWlkIjoicmVzZXJ2YXRpb25zQHdoeXRlaG91c2Vob2xpZGF5cy5jb20iLCJlbWFpbCI6InJlc2VydmF0aW9uc0B3aHl0ZWhvdXNlaG9saWRheXMuY29tIiwiYXV0aF90aW1lIjoiMDIvMTkvMjAyNCAxMjoyMDowMSIsImRiX25hbWUiOiJtdC1wcm9kLVRlbmFudHMiLCJ0ZW5hbnRfaWQiOiIzMDQxNTIiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6IkNsYXJlX0FJIiwiYXVkIjoiQ2xhcmVfQUkifQ.PUEsx0BCoFO4KL2-KK7vPTh-55tKLnOtM74oXF1bnjw"  # Replace with your actual token
#     }

#     response = requests.post(url, json=payload, headers=headers)
#     print(response.text)
#     if response.status_code == 200:
#         print("WhatsApp message sent successfully.")
#     else:
#         print(
#             f"Failed to send WhatsApp message. Status Code: {response.status_code}, Response: {response.text}")


# def cancel_booking(request, invoice_id):
#     invoice = get_object_or_404(Invoice, id=invoice_id)

#     # Extract necessary data from the invoice object
#     customer_display_name = invoice.customer.customer_display_name
#     resort_name = invoice.resort_name.resort_name
#     checkin_date = invoice.checkin_date.strftime('%d-%m-%Y')  # Convert date to string
#     checkin_time = invoice.checkin_time
#     mobile = invoice.customer.contact_number
#     invoice_url = f"http://sales.whytehouseholidays.com/invoice_email/{invoice.id}/"  # Assuming invoice id is unique

#     # Call the send_whatsapp_reminder function
#     employee_send_whatsapp_invoice_delete(customer_display_name, resort_name, checkin_date, checkin_time, invoice_id, mobile)

#     messages.success(request, 'WhatsApp message sent successfully.')
#     return redirect('employee_saleinvoice')

# # def cancelinvoice(request, id):
# #     invoice = get_object_or_404(Invoice, id=id)
# #     if request.method == "POST":
# #         cancel_booking(request, id)
# #         invoice.delete()
# #         messages.success(request, 'Invoice cancelled successfully.')
# #         return redirect('customerview', id=invoice.customer.id)
# #     return render(request, 'Sales/Customers/Customers_View.html', {'invoice': invoice})

# #------------------------------------------ Cancel Invoice --------------------------------------

# def employee_cancelinvoice(request, id):
#     invoice = get_object_or_404(Invoice, id=id)
    
#     if request.method == "POST":
#         # Perform any additional cancellation logic if needed
#         # For example, cancel_booking(request, id)
        
#         # Delete the invoice
#         invoice.delete()
        
#         # Add success message
#         messages.success(request, 'Invoice cancelled successfully.')
        
#         # Redirect back to customerview with the customer's ID
#         return redirect('employee_customerview', id=invoice.customer.id)
    
#     # If it's not a POST request, render the template with invoice details
#     return render(request, 'EmpSales/EmpCustomers/employee_Customers_View.html', {'invoice': invoice})





#------------------------------------------ wattsapp message -----------------------------------------

def send_whatsapps(customer_display_name, resort_name, checkin_date, checkin_time, invoice_id,location, whatsapp_number,country_code_whatsapp):
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
                    {"name": "inv_link", "value": f"invoice_whattsapp/{invoice_id}/"},
                    {"name": "location_url", "value": location}
                ],
                "whatsappNumber": country_code_whatsapp + whatsapp_number
            }
        ],
        "template_name": "stay_invoice"
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


def employee_send_whatsapp_message(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)

    # Extract necessary data from the invoice object
    customer_display_name = invoice.customer.customer_display_name
    resort_name = invoice.resort_name.resort_name
    checkin_date = invoice.checkin_date.strftime('%d-%B-%Y')  # Convert date to string
    checkin_time = invoice.checkin_time
    location = invoice.resort_name.location
    whatsapp_number = invoice.customer.whatsapp_number
    country_code_whatsapp = invoice.customer.country_code_whatsapp
    invoice_url = f"https://www.sales.navigotrips.com/invoice_whattsapp/{invoice_id}/"  # Assuming invoice id is unique

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
        return redirect('employee_saleinvoice')

    # Call the send_whatsapp_reminder function
    send_whatsapps(customer_display_name, resort_name, checkin_date, checkin_time, invoice_id,location, whatsapp_number,country_code_whatsapp)

    messages.success(request, 'WhatsApp message sent successfully.')
    return redirect('employee_saleinvoice')



def employee_invoice_whattsapp(request, invoice_id):
    invoices = get_object_or_404(Invoice, id=invoice_id)
    package_price = invoices.package_price
    tax_percentage = invoices.tax
    
    # Calculate CGST and SGST based on tax percentage and package price
    if tax_percentage == 12:
        cgst_percentage = sgst_percentage = 6
    elif tax_percentage == 18:
        cgst_percentage = sgst_percentage = 9
    else:
        cgst_percentage = sgst_percentage = 0
    
    cgst = (package_price * cgst_percentage) / 100
    sgst = (package_price * sgst_percentage) / 100
    return render(request, 'whatsapp_templates/invoice_whattsapp.html', {'invoices': invoices,'package_price': package_price,
        'cgst': cgst,
        'sgst': sgst})




#------------------------------------------------------------------  Postpone ------------------------------------------------------------


def employee_send_whatsapp_postpone_invoice(invoice_id, new_date,new_resort_name=None):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    customer_name = invoice.customer.customer_display_name
    original_resort_name = invoice.resort_name.resort_name
    resort_name = new_resort_name if new_resort_name else original_resort_name
    original_date = invoice.checkin_date.strftime('%d-%B-%Y')
    new_date = new_date.strftime('%d-%B-%Y')
    whatsapp_number = invoice.customer.whatsapp_number
    country_code_whatsapp = invoice.customer.country_code_whatsapp

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
        "template_name": "postpone_invoice_stay"
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

def employee_send_whatsapp_postpone_invoice_message(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)

    # Assuming 'new_checkin_date' is posted as 'YYYY-MM-DD'
    new_date_str = request.POST.get('new_checkin_date')
    new_date = datetime.strptime(new_date_str, '%Y-%m-%d').date()

    missing_fields = {
        'New Check-in Date': new_date_str,
        'Customer Display Name': invoice.customer.customer_display_name,
        'Invoice ID': invoice_id,
    }

    # Identify missing values
    missing_values = [field for field, value in missing_fields.items() if not value]

    if missing_values:
        missing_values_str = ", ".join(missing_values)
        messages.error(request, f"Missing required values: {missing_values_str}. All values must be filled to send the WhatsApp postpone message.")
        return redirect('employee_invoice_detail', invoice_id=invoice_id)
    
    # Call the send_whatsapp_postpone_invoice function
    employee_send_whatsapp_postpone_invoice(invoice_id, new_date)
    
    # Update the invoice with the new check-in date
    invoice.checkin_date = new_date
    invoice.save()

    messages.success(request, 'WhatsApp postpone message sent successfully and invoice updated.')
    return redirect('employee_invoice_detail', invoice_id=invoice_id)



def employee_postpone_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)

    if request.method == "POST":
        try:
            # Store the original check-in date
            original_checkin_date = invoice.checkin_date
            original_resort_name = invoice.resort_name

            # Update invoice fields
            invoice.customer_id = int(request.POST.get('customer_id'))
            invoice.sales_person_id = int(request.POST.get('sales_person'))
            new_resort_id = int(request.POST.get('resort_name'))
            invoice.resort_name_id = int(request.POST.get('resort_name'))
            invoice.account_name_id = int(request.POST.get('bank_account'))
            invoice.meal_plan_id = int(request.POST.get('meal_plan'))
            invoice.invoice_date = request.POST.get('invoice_date')
            invoice.due_date = request.POST.get('due_date')
            new_checkin_date = request.POST.get('checkin_date')
            invoice.checkin_date = new_checkin_date
            invoice.checkout_date = request.POST.get('checkout_date')
            invoice.mobile = request.POST.get('mobile')
            invoice.checkin_time = request.POST.get('checkin_time')
            invoice.checkout_time = request.POST.get('checkout_time')
            invoice.adults = int(request.POST.get('adults'))
            invoice.children = int(request.POST.get('children'))
            invoice.number_of_nights = int(request.POST.get('number_of_nights'))
            invoice.room_type = request.POST.get('room_type')
            invoice.number_of_rooms = int(request.POST.get('number_of_rooms'))
            invoice.package_price = Decimal(request.POST.get('package_price') or 0)
            invoice.resort_price = Decimal(request.POST.get('resort_price') or 0)
            invoice.total_amount = Decimal(request.POST.get('total_amount') or 0)
            invoice.tax = int(request.POST.get('tax') or 0)
            invoice.recieved_price = Decimal(request.POST.get('recieved_price') or 0)
            invoice.pending_price = Decimal(request.POST.get('pending_price') or 0)
            invoice.profit = Decimal(request.POST.get('profit') or 0)
            invoice.navigo = Decimal(request.POST.get('navigo') or 0)

             # Get the new resort name
            new_resort = Stay.objects.get(id=new_resort_id)
            new_resort_name = new_resort.resort_name if new_resort.id != original_resort_name.id else None

            # Send WhatsApp message with original and new check-in dates, and new resort name if changed
            employee_send_whatsapp_postpone_invoice(
                invoice.id, 
                datetime.strptime(new_checkin_date, '%Y-%m-%d').date(),
                new_resort_name
            )

            
            invoice.save()

            # Send WhatsApp message with original and new check-in dates
            

            messages.success(request, 'Invoice updated successfully and WhatsApp message sent.')
            return redirect('employee_customerview', id=invoice.customer.id)

        except (ValueError, TypeError) as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('employee_postpone_invoice', invoice_id=invoice_id)

    # If it's a GET request, prepare the form
    customers = Customers.objects.all()
    sales_persons = CustomUser.objects.all()
    resorts = Stay.objects.all()
    bank_accounts = BankAccount.objects.all()
    meals = MealPlans.objects.all()

    return render(request, 'EmpPostpone/employee_postpone_invoice.html', {
        'invoice': invoice,
        'customers': customers,
        'sales_persons': sales_persons,
        'resorts': resorts,
        'bank_accounts': bank_accounts,
        'meals': meals,
    })



#----------------------------------------------- Cancel Booking ----------------------------------



def employee_send_whatsapp_cancel_invoice_message(request, invoice_id, cancellation_date):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    customer_name = invoice.customer.customer_display_name
    resort_name = invoice.resort_name.resort_name
    checkin_date = invoice.checkin_date.strftime('%d-%B-%Y')
    cancel_date = cancellation_date.strftime('%d-%B-%Y')
    whatsapp_number = invoice.customer.whatsapp_number
    country_code_whatsapp = invoice.customer.country_code_whatsapp
    
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
        "template_name": "cancel_stay_invoice"
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


def employee_cancelinvoice(request, id):
    invoice = get_object_or_404(Invoice, id=id)
    
    if request.method == "POST":
        try:
            # Update the cancellation date in the existing invoice record
            invoice.cancellation_date = datetime.now().date()

            # Send WhatsApp message
            employee_send_whatsapp_cancel_invoice_message(request, invoice.id, invoice.cancellation_date)
            
            # Save the updated invoice
            invoice.save()
            
            # Add success message
            messages.success(request, 'Invoice cancelled successfully and WhatsApp message sent.')
            
            # Redirect back to customerview with the customer's ID
            return redirect('employee_customerview', id=invoice.customer.id)
        
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('employee_customerview', id=invoice.customer.id)
    
    # If it's not a POST request, render the template with invoice details
    return render(request, 'EmpSales/EmpCustomers/employee_Customers_View.html', {'invoice': invoice})













