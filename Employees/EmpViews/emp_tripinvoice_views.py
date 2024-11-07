from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from dashboard.models import *
from django.http import JsonResponse
from django.db.models import Max, Q
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import requests
from django.contrib.auth.decorators import login_required
from decimal import Decimal, InvalidOperation
import datetime
from datetime import datetime


@login_required(login_url='employee_signin')
def employee_tripinvoiceadd(request):
    if request.method == "POST":
        try:
            customer_id = request.POST.get('customer_id')
            sales_person_id = request.POST.get('sales_person')
            account_id = request.POST.get('bank_account')
            meal_plan_id = request.POST.get('meal_plan')
            destination_id = request.POST.get('destination')
            invoice_date = request.POST.get('invoice_date')
            due_date = request.POST.get('due_date')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            Pickup_location = request.POST.get('Pickup_location')
            drop_location = request.POST.get('drop_location')
            adults = request.POST.get('adults')
            children = request.POST.get('children')

            try:
                package_price = Decimal(request.POST.get('package_price', '0.00'))
            except InvalidOperation:
                package_price = Decimal('0.00')

            try:
                transport_price = Decimal(request.POST.get('transport_price', '0.00'))
            except InvalidOperation:
                transport_price = Decimal('0.00')

            try:
                total_amount = Decimal(request.POST.get('total_amount', '0.00'))
            except InvalidOperation:
                total_amount = Decimal('0.00')

            try:
                tax = Decimal(request.POST.get('tax', '0.00'))
            except InvalidOperation:
                tax = Decimal('0.00')

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
                accomadation_price = Decimal(request.POST.get('accomadation_price', '0.00'))
            except InvalidOperation:
                accomadation_price = Decimal('0.00')

            try:
                guide_charge = Decimal(request.POST.get('guide_charge', '0.00'))
            except InvalidOperation:
                guide_charge = Decimal('0.00')

            try:
                other_charge = Decimal(request.POST.get('other_charge', '0.00'))
            except InvalidOperation:
                other_charge = Decimal('0.00')

            customer_instance = get_object_or_404(Customers, id=customer_id)
            sales_person = get_object_or_404(CustomUser, id=sales_person_id)
            account_instance = get_object_or_404(BankAccount, id=account_id)
            meal_instance = get_object_or_404(MealPlans, id=meal_plan_id)
            destination_instance = get_object_or_404(Trip, id=destination_id)

            invoice_number = generate_trip_invoice_number()

            TripInvoice.objects.create(
                customer=customer_instance,
                sales_person=sales_person,
                account_name=account_instance,
                meal_plan=meal_instance,
                destination=destination_instance,
                invoice_number=invoice_number,
                invoice_date=invoice_date,
                due_date=due_date,
                start_date=start_date,
                end_date=end_date,
                Pickup_location=Pickup_location,
                drop_location=drop_location,
                adults=adults,
                children=children if children else 0,
                package_price=package_price,
                transport_price=transport_price,
                total_amount=total_amount,
                tax=tax,
                recieved_price=recieved_price,
                pending_price=pending_price,
                profit=profit,
                accomadation_price=accomadation_price,
                guide_charge=guide_charge,
                other_charge=other_charge

            )
            messages.success(request,'Invoice created successfully')
            return redirect('employee_tripinvoice')
        except InvalidOperation:
            messages.error(request, 'Failed to create invoice due to invalid data')
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {e}')

    customers = Customers.objects.all()
    sales_persons = CustomUser.objects.all()
    bank_accounts = BankAccount.objects.all()
    meals = MealPlans.objects.all()
    destination = Trip.objects.all()

    return render(request, 'EmpSales/EmpTrip_invoice/employee_InvoiceAdd.html', {
        'customers': customers,
        'sales_persons': sales_persons,
        'bank_accounts': bank_accounts,
        'meals': meals,
        'destination': destination,
        'next_invoice_number': generate_trip_invoice_number()
    })

def generate_trip_invoice_number():
    last_invoice = TripInvoice.objects.order_by('-invoice_number').first()
    if last_invoice:
        last_number = int(last_invoice.invoice_number.split('-')[1])
        return f'INV-{last_number + 1:04d}'
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
def employee_tripinvoiceedit(request,invoice_id):
    invoice = get_object_or_404(TripInvoice, id=invoice_id)

    if request.method == "POST":
        try:
        # Update or save the invoice details
            invoice.customer_id = request.POST.get('customer_id')
            invoice.sales_person_id = request.POST.get('sales_person')
            invoice.account_name_id = request.POST.get('bank_account')
            invoice.meal_plan_id = request.POST.get('meal_plan')
            invoice.destination_id = request.POST.get('destination')
            invoice.invoice_date = request.POST.get('invoice_date')
            invoice.due_date = request.POST.get('due_date')
            invoice.start_date = request.POST.get('start_date')
            invoice.end_date = request.POST.get('end_date')
            invoice.Pickup_location = request.POST.get('Pickup_location')
            invoice.drop_location = request.POST.get('drop_location')
            invoice.adults = request.POST.get('adults')
            invoice.children = request.POST.get('children')
            try:
                invoice.package_price = Decimal(request.POST.get('package_price', '0.00'))
            except InvalidOperation:
                invoice.package_price = Decimal('0.00')

            try:
                invoice.transport_price = Decimal(request.POST.get('transport_price', '0.00'))
            except InvalidOperation:
                invoice.transport_price = Decimal('0.00')

            try:
                invoice.accomadation_price = Decimal(request.POST.get('accomadation_price', '0.00'))
            except InvalidOperation:
                invoice.accomadation_price = Decimal('0.00')

            try:
                invoice.total_amount = Decimal(request.POST.get('total_amount', '0.00'))
            except InvalidOperation:
                invoice.total_amount = Decimal('0.00')

            try:
                invoice.tax = Decimal(request.POST.get('tax', '0.00'))
            except InvalidOperation:
                invoice.tax = Decimal('0.00')

            try:
                invoice.recieved_price = Decimal(request.POST.get('recieved_price', '0.00'))
            except InvalidOperation:
                invoice.recieved_price = Decimal('0.00')

            try:
                invoice.pending_price = Decimal(request.POST.get('pending_price', '0.00'))
            except InvalidOperation:
                invoice.pending_price = Decimal('0.00')

            try:
                invoice.profit = Decimal(request.POST.get('profit', '0.00'))
            except InvalidOperation:
                invoice.profit = Decimal('0.00')

            try:
                invoice.guide_charge = Decimal(request.POST.get('guide_charge', '0.00'))
            except InvalidOperation:
                invoice.guide_charge = Decimal('0.00')

            try:
                invoice.other_charge = Decimal(request.POST.get('other_charge', '0.00'))
            except InvalidOperation:
                invoice.other_charge = Decimal('0.00')
            invoice.save()
            messages.success(request,'Invoice updated successfully')

            return redirect('employee_tripinvoice')
        
        except InvalidOperation:
            messages.error(request, 'Failed to update invoice due to invalid data')
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {e}')

    customers = Customers.objects.all()
    sales_persons = CustomUser.objects.all()
    bank_accounts = BankAccount.objects.all()
    meals = MealPlans.objects.all()
    destination = Trip.objects.all()

    return render(request,'EmpSales/EmpTrip_invoice/employee_InvoiceEdit.html',{
        'invoice': invoice,
        'customers': customers,
        'sales_persons': sales_persons,
        'bank_accounts': bank_accounts,
        'meals': meals,
        'destination':destination
    })


@login_required(login_url='employee_signin')
def employee_tripinvoicelist(request):
    invoices_list = TripInvoice.objects.all().order_by('-id')
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
    return render(request,'EmpSales/EmpTrip_invoice/employee_InvoiceList.html',{'invoices': invoices, 'query': query})


@login_required(login_url='employee_signin')
def employee_tripinvoicedetail(request,invoice_id):
    invoice = get_object_or_404(TripInvoice, id=invoice_id)
    context = {
        'invoice': invoice
    }
    return render(request,'EmpSales/EmpTrip_invoice/employee_InvoiceDetail.html',context)


@login_required(login_url='employee_signin')
def employee_tripinvoicedelete(request, invoice_id):
    invoice = get_object_or_404(TripInvoice, id=invoice_id)
    if request.method == "POST":
        invoice.delete()
        messages.success(request, 'Invoice deleted successfully.')
        return redirect('employee_tripinvoice')
    

@login_required(login_url='admin_loginview')
def employee_tripinvoice_record_payment(request, id):
    invoice = get_object_or_404(TripInvoice, id=id)

    if request.method == 'POST':
        # Retrieve form data
        client_name = request.POST.get('client_name')
        invoice_number = request.POST.get('invoice_number')
        amount_received = request.POST.get('amount_received')
        payment_date = request.POST.get('payment_date')
        payment_mode = request.POST.get('payment_mode')

        # Save payment details to the database (adjust based on your models)
        TripInvoicePayment.objects.create(
            invoice=invoice,
            client_name=client_name,
            invoice_number=invoice_number,
            amount_received=amount_received,
            payment_date=payment_date,
            payment_mode=payment_mode
        )

        # Redirect back to the invoice view or any other desired page
        return redirect('employee_tripinvoicedetail', invoice_id=id)

    return render(request, 'EmpSales/EmpTrip_invoice/employee_InvoiceDetail.html', {'invoice': invoice})

#---------------------------------------- trip Invoice Email message -------------------------------------

def employee_tripsend_invoice_email(request, invoice_id):
    invoice = get_object_or_404(TripInvoice, id=invoice_id)
    subject = f"Booking for {invoice.customer.full_name}  - For {invoice.destination.place_name}"
    viewcolor_link = f'https://www.sales.navigotrips.com/tripinvoice_emails/{invoice.id}/'
    message = f'Dear team, Greetings From Navigo! As per the telephonic conversation, kindly confirm the following:'

    html_message = render_to_string('emailtemplates/trip_emailinvoice.html',
                                    {'invoices': invoice, 'viewcolor_link': viewcolor_link, 'subject': subject,
                                     'message': message})
    text_message = message
    customer_email = invoice.customer.customer_email
    email = EmailMultiAlternatives(subject, text_message, settings.DEFAULT_FROM_EMAIL, [customer_email])
    email.attach_alternative(html_message, "text/html")
    email.send()

    # Add success message
    messages.success(request, 'Email sent successfully.')

    # Redirect back to list_invoice view
    return redirect('employee_tripinvoice')


def employee_trip_invoice_email(request, invoice_id):
    invoices = get_object_or_404(TripInvoice, id=invoice_id)
    return render(request, 'tripinvoice_email_template.html', {'invoices': invoices})




#--------------------------------------- Whatssapp Message ---------------------------------------

def send_whatsapps(customer_display_name, destination, start_date, trip_invoice_id, whatsapp_number,country_code_whatsapp):
    url = "https://live-mt-server.wati.io/329541/api/v1/sendTemplateMessages"
    
    payload = {
        "broadcast_name": "Navigo Trips",
        "receivers": [
            {
                "customParams": [
                    {"name": "name", "value": customer_display_name},
                    {"name": "destination", "value": destination},
                    {"name": "date", "value": start_date},
                    {"name": "inv_link", "value": f"trip_invoice_whatsapp/{trip_invoice_id}/"}
                ],
                "whatsappNumber": country_code_whatsapp + whatsapp_number
            }
        ],
        "template_name": "invoice_trip"
    }
    
    headers = {
        "content-type": "text/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI4MTMzMmU2OC0wODRkLTQ1MjMtODU0MS04MWYyMmI5ZWJiMDMiLCJ1bmlxdWVfbmFtZSI6Im5hdmlnb3RyaXBzQGdtYWlsLmNvbSIsIm5hbWVpZCI6Im5hdmlnb3RyaXBzQGdtYWlsLmNvbSIsImVtYWlsIjoibmF2aWdvdHJpcHNAZ21haWwuY29tIiwiYXV0aF90aW1lIjoiMDgvMDIvMjAyNCAwODo0Nzo1NCIsImRiX25hbWUiOiJtdC1wcm9kLVRlbmFudHMiLCJ0ZW5hbnRfaWQiOiIzMjk1NDEiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6IkNsYXJlX0FJIiwiYXVkIjoiQ2xhcmVfQUkifQ.wr78I9zQx18T6PovGICUHJhWWjofegZiGpdpfZlHFz8"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)
    if response.status_code == 200:
        print("WhatsApp message sent successfully.")
    else:
        print(f"Failed to send WhatsApp message. Status Code: {response.status_code}, Response: {response.text}")

def employee_send_whatsapp_invoice_message(request, trip_invoice_id):
    trip_invoice = get_object_or_404(TripInvoice, id=trip_invoice_id)
    
    # Extract necessary data from the trip invoice object
    customer_display_name = trip_invoice.customer.customer_display_name
    destination = trip_invoice.destination.place_name  # Assuming the Trip model has a 'name' field
    start_date = trip_invoice.start_date.strftime('%d-%B-%Y')  # Convert date to string
    whatsapp_number = trip_invoice.customer.whatsapp_number
    country_code_whatsapp = trip_invoice.customer.country_code_whatsapp

    missing_fields = {
        'Customer Display Name': customer_display_name,
        'Destination': destination,
        'Start Date': start_date,
        'WhatsApp Number': whatsapp_number,
        'Country Code for WhatsApp': country_code_whatsapp
    }
    
    # Identify missing values
    missing_values = [field for field, value in missing_fields.items() if not value]
    
    if missing_values:
        missing_values_str = ", ".join(missing_values)
        messages.error(request, f"Missing required values: {missing_values_str}. All values must be filled to send the WhatsApp message.")
        return redirect('employee_tripinvoice')
    
    # Call the send_whatsapps function
    send_whatsapps(customer_display_name, destination, start_date, trip_invoice_id, whatsapp_number,country_code_whatsapp)
    
    messages.success(request, 'WhatsApp message sent successfully.')
    return redirect('employee_tripinvoice')  # Adjust this to your actual trip invoice list view name

def employee_trip_invoice_whatsapp(request, trip_invoice_id):
    trip_invoice = get_object_or_404(TripInvoice, id=trip_invoice_id)
    package_price = trip_invoice.package_price
    tax_percentage = trip_invoice.tax
    
    # Calculate CGST and SGST based on tax percentage and package price
    if tax_percentage == 12:
        cgst_percentage = sgst_percentage = 6
    elif tax_percentage == 18:
        cgst_percentage = sgst_percentage = 9
    else:
        cgst_percentage = sgst_percentage = 0
    
    cgst = (package_price * cgst_percentage) / 100
    sgst = (package_price * sgst_percentage) / 100
    
    return render(request, 'whatsapp_templates/trip_invoice_whatsapp.html', {
        'trip_invoice': trip_invoice,
        'package_price': package_price,
        'cgst': cgst,
        'sgst': sgst
    })





#------------------------------------------postpone Whatsapp message ----------------------------------------

def employee_send_whatsapp_postpone_trip_invoice(invoice_id, new_date, new_destination_name=None):
    invoice = get_object_or_404(TripInvoice, id=invoice_id)
    
    customer_name = invoice.customer.customer_display_name
    original_destination_name = invoice.destination.place_name
    destination_name = new_destination_name if new_destination_name else original_destination_name
    original_date = invoice.start_date.strftime('%d-%B-%Y')
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
                    {"name": "destination", "value": destination_name},
                    {"name": "date", "value": original_date},
                    {"name": "newdate", "value": new_date}
                ],
                "whatsappNumber": country_code_whatsapp + whatsapp_number
            }
        ],
        "template_name": "postpone_invoice_trip"
    }
    headers = {
        "content-type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI4MTMzMmU2OC0wODRkLTQ1MjMtODU0MS04MWYyMmI5ZWJiMDMiLCJ1bmlxdWVfbmFtZSI6Im5hdmlnb3RyaXBzQGdtYWlsLmNvbSIsIm5hbWVpZCI6Im5hdmlnb3RyaXBzQGdtYWlsLmNvbSIsImVtYWlsIjoibmF2aWdvdHJpcHNAZ21haWwuY29tIiwiYXV0aF90aW1lIjoiMDgvMDIvMjAyNCAwODo0Nzo1NCIsImRiX25hbWUiOiJtdC1wcm9kLVRlbmFudHMiLCJ0ZW5hbnRfaWQiOiIzMjk1NDEiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6IkNsYXJlX0FJIiwiYXVkIjoiQ2xhcmVfQUkifQ.wr78I9zQx18T6PovGICUHJhWWjofegZiGpdpfZlHFz8"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        print("WhatsApp message sent successfully.")
    else:
        print(f"Failed to send WhatsApp message. Status Code: {response.status_code}, Response: {response.text}")




def employee_send_whatsapp_postpone_trip_invoice_message(request,invoice_id):
    invoice = get_object_or_404(TripInvoice, id=invoice_id)

    # Assuming 'new_checkin_date' is posted as 'YYYY-MM-DD'
    new_date_str = request.POST.get('new_start_date')
    missing_fields = {
        'New Start Date': new_date_str,
        'Customer Display Name': invoice.customer.customer_display_name,
        'Destination': invoice.destination.place_name,
        'Invoice ID': invoice_id,
    }

    # Identify missing values
    missing_values = [field for field, value in missing_fields.items() if not value]

    if missing_values:
        missing_values_str = ", ".join(missing_values)
        messages.error(request, f"Missing required values: {missing_values_str}. All values must be filled to send the WhatsApp postpone message.")
        return redirect('employee_invoice_detail', invoice_id=invoice_id)
    new_date = datetime.strptime(new_date_str, '%Y-%m-%d').date()
    
    # Call the send_whatsapp_postpone_invoice function
    employee_send_whatsapp_postpone_trip_invoice(invoice_id, new_date)
    
    # Update the invoice with the new check-in date
    invoice.start_date = new_date
    invoice.save()

    messages.success(request, 'WhatsApp postpone message sent successfully and invoice updated.')
    return redirect('employee_invoice_detail', invoice_id=invoice_id)





def employee_postpone_trip_invoice(request, invoice_id):
    invoice = get_object_or_404(TripInvoice, id=invoice_id)

    if request.method == "POST":
        try:
            # Store the original details
            original_start_date = invoice.start_date
            original_destination_name = invoice.destination.place_name

            # Update invoice fields
            invoice.customer_id = int(request.POST.get('customer_id'))
            invoice.sales_person_id = int(request.POST.get('sales_person'))
            new_destination_id = int(request.POST.get('destination'))
            invoice.destination_id = new_destination_id
            invoice.account_name_id = int(request.POST.get('bank_account'))
            invoice.meal_plan_id = int(request.POST.get('meal_plan'))
            invoice.invoice_date = request.POST.get('invoice_date')
            invoice.due_date = request.POST.get('due_date')
            new_start_date = request.POST.get('start_date')
            invoice.start_date = new_start_date
            invoice.end_date = request.POST.get('end_date')
            invoice.Pickup_location = request.POST.get('Pickup_location')
            invoice.drop_location = request.POST.get('drop_location')
            invoice.adults = int(request.POST.get('adults'))
            invoice.children = int(request.POST.get('children'))
            invoice.package_price = Decimal(request.POST.get('package_price') or 0)
            invoice.transport_price = Decimal(request.POST.get('transport_price') or 0)
            invoice.total_amount = Decimal(request.POST.get('total_amount') or 0)
            invoice.tax = int(request.POST.get('tax') or 0)
            invoice.recieved_price = Decimal(request.POST.get('recieved_price') or 0)
            invoice.pending_price = Decimal(request.POST.get('pending_price') or 0)
            invoice.profit = Decimal(request.POST.get('profit') or 0)
            invoice.accomadation_price = Decimal(request.POST.get('accomadation_price') or 0)
            invoice.guide_charge = Decimal(request.POST.get('guide_charge') or 0)
            invoice.other_charge = Decimal(request.POST.get('other_charge') or 0)

            # Get the new destination name
            new_destination = Trip.objects.get(id=new_destination_id)
            new_destination_name = new_destination.place_name if new_destination.id != original_destination_name else None

            # Send WhatsApp message with original and new details
            employee_send_whatsapp_postpone_trip_invoice(
                invoice.id, 
                datetime.strptime(new_start_date, '%Y-%m-%d').date(),
                new_destination_name
            )

            invoice.save()

            messages.success(request, 'Invoice updated successfully and WhatsApp message sent.')
            return redirect('employee_customerview', id=invoice.customer.id)

        except (ValueError, TypeError) as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('employee_postpone_invoice', invoice_id=invoice_id)

    # If it's a GET request, prepare the form
    customers = Customers.objects.all()
    sales_persons = CustomUser.objects.all()
    destinations = Trip.objects.all()
    bank_accounts = BankAccount.objects.all()
    meals = MealPlans.objects.all()

    return render(request, 'EmpPostpone/employee_postpone_trip_invoice.html', {
        'invoice': invoice,
        'customers': customers,
        'sales_persons': sales_persons,
        'destinations': destinations,
        'bank_accounts': bank_accounts,
        'meals': meals,
    })




#----------------------------------------- Cancel Booking --------------------------------------

def employee_send_whatsapp_cancel_trip_invoice_message(request, invoice_id, cancellation_date):
    invoice = get_object_or_404(TripInvoice, id=invoice_id)
    
    customer_name = invoice.customer.customer_display_name
    destination = invoice.destination.place_name
    start_date = invoice.start_date.strftime('%d-%B-%Y')
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
                    {"name": "destination", "value": destination},
                    {"name": "date", "value": start_date},
                    {"name": "canceldate", "value": cancel_date}
                ],
                "whatsappNumber": country_code_whatsapp + whatsapp_number
            }
        ],
        "template_name": "cancel_trip_invoice"
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



def employee_cancel_trip_invoice(request, id):
    invoice = get_object_or_404(TripInvoice, id=id)
    
    if request.method == "POST":
        try:
            # Update the cancellation date in the existing invoice record
            invoice.cancellation_date = datetime.now().date()

            # Send WhatsApp message
            employee_send_whatsapp_cancel_trip_invoice_message(request, invoice.id, invoice.cancellation_date)
            
            # Save the updated invoice
            invoice.save()
            
            # Add success message
            messages.success(request, 'Trip invoice cancelled successfully and WhatsApp message sent.')
            
            # Redirect back to customerview with the customer's ID
            return redirect('employee_customerview', id=invoice.customer.id)
        
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('employee_customerview', id=invoice.customer.id)
    
    # If it's not a POST request, render the template with invoice details
    return render(request, 'EmpSales/Emp_Customers/employee_Customers_View.html', {'invoice': invoice})
    


