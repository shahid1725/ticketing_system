from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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


def employee_tripvoucheradd(request):
    if request.method == "POST":
        customer_id = request.POST.get('customer_id')
        sales_person_id = request.POST.get('sales_person')
        account_id = request.POST.get('bank_account')
        meal_plan_id = request.POST.get('meal_plan')
        destination_id = request.POST.get('destination')
        voucher_date = request.POST.get('voucher_date')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        Pickup_location = request.POST.get('Pickup_location')
        drop_location = request.POST.get('drop_location')
        adults = request.POST.get('adults')
        children = request.POST.get('children')

        # Handle decimal fields, converting None or invalid values to Decimal('0.00')
        try:
            package_price = Decimal(request.POST.get('package_price', '0.00'))
        except InvalidOperation:
            package_price = Decimal('0.00')

        try:
            transport_price = Decimal(request.POST.get('transport_price', '0.00'))
        except InvalidOperation:
            transport_price = Decimal('0.00')

        try:
            accomadation_price = Decimal(request.POST.get('accomadation_price', '0.00'))
        except InvalidOperation:
            accomadation_price = Decimal('0.00')

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
            guide_charge = Decimal(request.POST.get('guide_charge', '0.00'))
        except InvalidOperation:
            guide_charge = Decimal('0.00')

        try:
            other_charge = Decimal(request.POST.get('other_charge', '0.00'))
        except InvalidOperation:
            other_charge = Decimal('0.00')

        customer_instance = get_object_or_404(Customers, id=customer_id)
        sales_person = get_object_or_404(CustomUser, id=sales_person_id)
        destination_instance = get_object_or_404(Trip, id=destination_id)
        account_instance = get_object_or_404(BankAccount, id=account_id)
        meal_instance = get_object_or_404(MealPlans, id=meal_plan_id)

        voucher_number = generate_voucher_number()

        TripVoucher.objects.create(
            customer=customer_instance,
            sales_person=sales_person,
            destination=destination_instance,
            account_name=account_instance,
            meal_plan=meal_instance,
            voucher_number=voucher_number,
            voucher_date=voucher_date,
            start_date=start_date,
            end_date=end_date,
            Pickup_location=Pickup_location,
            drop_location=drop_location,
            adults=adults,
            children=children if children else 0,
            package_price=package_price,
            transport_price=transport_price,
            accomadation_price=accomadation_price,
            total_amount=total_amount,
            recieved_price=recieved_price,
            pending_price=pending_price,
            profit=profit,
            guide_charge=guide_charge,
            other_charge=other_charge

        )
        messages.success(request,'Voucher created successfully')
        return redirect('employee_tripvoucher')

    customers = Customers.objects.all()
    sales_persons = CustomUser.objects.all()
    destination = Trip.objects.all()
    bank_accounts = BankAccount.objects.all()
    meals = MealPlans.objects.all()
    return render(request,'EmpSales/EmpTrip_voucher/employee_VoucherAdd.html', {
        'customers': customers,
        'sales_persons': sales_persons,
        'destination': destination,
        'bank_accounts': bank_accounts,
        'meals': meals,
        'next_voucher_number': generate_voucher_number()
    })

def generate_voucher_number():
    last_voucher = TripVoucher.objects.aggregate(Max('id'))
    last_id = last_voucher['id__max']
    if last_id:
        return f'VOC-{last_id + 1:04d}'
    else:
        return 'VOC-0001'

def employee_tripvoucheredit(request,voucher_id):
    voucher = get_object_or_404(TripVoucher, id=voucher_id)

    if request.method == "POST":
        try:
            voucher.customer_id = request.POST.get('customer_id')
            voucher.sales_person_id = request.POST.get('sales_person')
            voucher.destination_id = request.POST.get('destination')
            voucher.account_name_id = request.POST.get('bank_account')
            voucher.meal_plan_id = request.POST.get('meal_plan')
            voucher.voucher_date = request.POST.get('voucher_date')
            voucher.start_date = request.POST.get('start_date')
            voucher.end_date = request.POST.get('end_date')
            voucher.Pickup_location = request.POST.get('Pickup_location')
            voucher.drop_location = request.POST.get('drop_location')
            voucher.adults = request.POST.get('adults')
            voucher.children = request.POST.get('children')

            # Handle decimal fields, converting None or invalid values to Decimal('0.00')
            try:
                voucher.package_price = Decimal(request.POST.get('package_price', '0.00'))
            except InvalidOperation:
                voucher.package_price = Decimal('0.00')
            
            try:
                voucher.transport_price = Decimal(request.POST.get('transport_price', '0.00'))
            except InvalidOperation:
                voucher.transport_price = Decimal('0.00')

            try:
                voucher.accomadation_price = Decimal(request.POST.get('accomadation_price', '0.00'))
            except InvalidOperation:
                voucher.accomadation_price = Decimal('0.00')

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
                voucher.guide_charge = Decimal(request.POST.get('guide_charge', '0.00'))
            except InvalidOperation:
                voucher.guide_charge = Decimal('0.00')

            try:
                voucher.other_charge = Decimal(request.POST.get('other_charge', '0.00'))
            except InvalidOperation:
                voucher.other_charge = Decimal('0.00')

            voucher.save()
            messages.success(request, 'Voucher updated successfully')
        except InvalidOperation:
            messages.error(request, 'Failed to update voucher due to invalid data')

        return redirect('employee_tripvoucher')

    customers = Customers.objects.all()
    sales_persons = CustomUser.objects.all()
    destination = Trip.objects.all()
    bank_accounts = BankAccount.objects.all()
    meals = MealPlans.objects.all()
    return render(request,'EmpSales/EmpTrip_voucher/employee_VoucherEdit.html',{
        'voucher': voucher,
        'customers': customers,
        'sales_persons': sales_persons,
        'destination': destination,
        'bank_accounts': bank_accounts,
        'meals': meals,
    })

def employee_tripvoucherlist(request):
    voucher_list = TripVoucher.objects.all().order_by('-id')
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
    return render(request,'EmpSales/EmpTrip_voucher/employee_VoucherList.html',{'voucher': voucher, 'query': query})

def employee_tripvoucherdetail(request,voucher_id):
    voucher = get_object_or_404(TripVoucher, id=voucher_id)
    context = {
        'voucher': voucher
    }
    return render(request,'EmpSales/EmpTrip_voucher/employee_VoucherDetail.html',context)


@login_required(login_url='admin_loginview')
def employee_tripvoucherdelete(request, voucher_id):
    voucher = get_object_or_404(TripVoucher, id=voucher_id)
    if request.method == "POST":
        voucher.delete()
        messages.success(request, 'Voucher deleted successfully.')
        return redirect('employee_tripvoucher') 
    

@login_required(login_url='admin_loginview')
def employee_trip_voucher_record_payment(request, id):
    voucher = get_object_or_404(TripVoucher, id=id)

    if request.method == 'POST':
        # Retrieve form data
        client_name = request.POST.get('client_name')
        voucher_number = request.POST.get('voucher_number')
        amount_received = request.POST.get('amount_received')
        payment_date = request.POST.get('payment_date')
        payment_mode = request.POST.get('payment_mode')

        # Save payment details to the database (adjust based on your models)
        TripVoucherPayment.objects.create(
            voucher=voucher,
            client_name=client_name,
            voucher_number=voucher_number,
            amount_received=amount_received,
            payment_date=payment_date,
            payment_mode=payment_mode
        )

        # Redirect back to the invoice view or any other desired page
        return redirect('employee_tripvoucherdetail',  voucher_id=id)

    return render(request, 'EmpSales/EmpTrip_voucher/employee_VoucherDetail.html', {'voucher': voucher})


def employee_trip_send_voucher_email(request, voucher_id):
    voucher = get_object_or_404(TripVoucher, id=voucher_id)
    customer_email = voucher.customer.customer_email

    subject = f"Booking for {voucher.customer.full_name} - For {voucher.destination.place_name}"
    voucher_id = voucher.id
    viewcolor_link = f'https://www.sales.navigotrips.com/tripvoucher_emails/{voucher_id}/'
    
    message = f'Dear team, Greetings From Navigo !!! As per the telephonic conversation , Kindly Confirm as follows:'

   
    
    html_message = render_to_string('emailtemplates/tripemailvoucher.html', {'tripvoucher': voucher, 'viewcolor_link': viewcolor_link,'subject': subject,
        'message': message})
    text_message = message

    email = EmailMultiAlternatives(subject, text_message, settings.DEFAULT_FROM_EMAIL, [customer_email])
    email.attach_alternative(html_message, "text/html")
    email.send()

    messages.success(request, 'Email sent successfully.')
    return redirect('employee_tripvoucher')



def employee_trip_voucher_email_template(request,voucher_id):
    voucher = get_object_or_404(TripVoucher, id=voucher_id)
    return render(request,'trip_voucher_email_template.html', {'tripvoucher':voucher})



#------------------------------------------ Wattsapp message --------------------------------------

def send_whatsapp_voucher(customer_display_name, destination, start_date, trip_voucher_id, whatsapp_number,country_code_whatsapp):
    url = "https://live-mt-server.wati.io/329541/api/v1/sendTemplateMessages"
    
    payload = {
        "broadcast_name": "Navigo Trips",
        "receivers": [
            {
                "customParams": [
                    {"name": "name", "value": customer_display_name},
                    {"name": "destination", "value": destination},
                    {"name": "date", "value": start_date},
                    {"name": "inv_link", "value": f"trip_voucher_whatsapp/{trip_voucher_id}/"}
                ],
                "whatsappNumber": country_code_whatsapp + whatsapp_number
            }
        ],
        "template_name": "trip_voucher"
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

def employee_send_whatsapp_voucher_message(request, trip_voucher_id):
    trip_voucher = get_object_or_404(TripVoucher, id=trip_voucher_id)
    
    # Extract necessary data from the trip voucher object
    customer_display_name = trip_voucher.customer.customer_display_name
    destination = trip_voucher.destination.place_name  # Assuming the Trip model has a 'name' field
    start_date = trip_voucher.start_date.strftime('%d-%B-%Y')  # Convert date to string
    whatsapp_number = trip_voucher.customer.whatsapp_number
    country_code_whatsapp = trip_voucher.customer.country_code_whatsapp

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
        messages.error(request, f"Missing required values: {missing_values_str}. All values must be filled to send the WhatsApp voucher message.")
        return redirect('employee_tripvoucher')
    
    # Call the send_whatsapp_voucher function
    send_whatsapp_voucher(customer_display_name, destination, start_date, trip_voucher_id, whatsapp_number,country_code_whatsapp)
    
    messages.success(request, 'WhatsApp voucher message sent successfully.')
    return redirect('employee_tripvoucher')  # Adjust this to your actual trip voucher list view name

def employee_trip_voucher_whatsapp(request, trip_voucher_id):
    trip_voucher = get_object_or_404(TripVoucher, id=trip_voucher_id)
    
    context = {
        'trip_voucher': trip_voucher,
        'package_price': trip_voucher.package_price,
        'total_amount': trip_voucher.total_amount,
        'received_price': trip_voucher.recieved_price,
        'pending_price': trip_voucher.pending_price,
    }
    
    return render(request, 'whatsapp_templates/trip_voucher_whatsapp.html', context)



#---------------------------------------- Postpone whatsapp ------------------------------------


def employee_send_whatsapp_postpone_trip_voucher(voucher_id, new_date, new_destination_name=None):
    voucher = get_object_or_404(TripVoucher, id=voucher_id)
    
    customer_name = voucher.customer.full_name
    original_destination_name = voucher.destination.place_name
    destination_name = new_destination_name if new_destination_name else original_destination_name
    original_date = voucher.start_date.strftime('%d-%B-%Y')
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
                    {"name": "destination", "value": destination_name},
                    {"name": "date", "value": original_date},
                    {"name": "newdate", "value": new_date}
                ],
                "whatsappNumber": country_code_whatsapp + whatsapp_number
            }
        ],
        "template_name": "postpone_voucher_trip"
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





def employee_send_whatsapp_postpone_trip_voucher_message(request,voucher_id):
    voucher = get_object_or_404(TripVoucher, id=voucher_id)

    # Assuming 'new_checkin_date' is posted as 'YYYY-MM-DD'
    new_date_str = request.POST.get('new_start_date')
    new_date = datetime.strptime(new_date_str, '%Y-%m-%d').date()

    missing_fields = {
        'New Start Date': new_date_str,
        'Customer Display Name': voucher.customer.customer_display_name,
        'Destination': voucher.destination.place_name,  # Assuming destination has a 'place_name' field
        'Voucher ID': voucher_id,
    }

    # Identify missing values
    missing_values = [field for field, value in missing_fields.items() if not value]

    if missing_values:
        missing_values_str = ", ".join(missing_values)
        messages.error(request, f"Missing required values: {missing_values_str}. All values must be filled to send the WhatsApp postpone message.")
        return redirect('employee_voucher_detail', voucher_id=voucher_id)
    
    # Call the send_whatsapp_postpone_invoice function
    employee_send_whatsapp_postpone_trip_voucher(voucher_id, new_date)
    
    # Update the invoice with the new check-in date
    voucher.start_date = new_date
    voucher.save()

    messages.success(request, 'WhatsApp postpone message sent successfully and invoice updated.')
    return redirect('employee_voucher_detail', voucher_id=voucher_id)





def employee_postpone_trip_voucher(request, voucher_id):
    voucher = get_object_or_404(TripVoucher, id=voucher_id)

    if request.method == "POST":
        try:
            # Store the original details
            original_start_date = voucher.start_date
            original_destination_name = voucher.destination.place_name

            # Update voucher fields
            voucher.customer_id = int(request.POST.get('customer_id'))
            voucher.sales_person_id = int(request.POST.get('sales_person'))
            new_destination_id = int(request.POST.get('destination'))
            voucher.destination_id = new_destination_id
            voucher.account_name_id = int(request.POST.get('bank_account'))
            voucher.meal_plan_id = int(request.POST.get('meal_plan'))
            voucher.voucher_date = request.POST.get('voucher_date')
            new_start_date = request.POST.get('start_date')
            voucher.start_date = new_start_date
            voucher.end_date = request.POST.get('end_date')
            voucher.Pickup_location = request.POST.get('Pickup_location')
            voucher.drop_location = request.POST.get('drop_location')
            voucher.adults = int(request.POST.get('adults'))
            voucher.children = int(request.POST.get('children'))
            voucher.package_price = Decimal(request.POST.get('package_price') or 0)
            voucher.transport_price = Decimal(request.POST.get('transport_price') or 0)
            voucher.total_amount = Decimal(request.POST.get('total_amount') or 0)
            voucher.recieved_price = Decimal(request.POST.get('recieved_price') or 0)
            voucher.pending_price = Decimal(request.POST.get('pending_price') or 0)
            voucher.profit = Decimal(request.POST.get('profit') or 0)
            voucher.accomadation_price = Decimal(request.POST.get('accomadation_price') or 0)
            voucher.guide_charge = Decimal(request.POST.get('guide_charge') or 0)
            voucher.other_charge = Decimal(request.POST.get('other_charge') or 0)

            # Get the new destination name
            new_destination = Trip.objects.get(id=new_destination_id)
            new_destination_name = new_destination.place_name if new_destination.id != original_destination_name else None

            # Send WhatsApp message with original and new details
            employee_send_whatsapp_postpone_trip_voucher(
                voucher.id, 
                datetime.strptime(new_start_date, '%Y-%m-%d').date(),
                new_destination_name
            )

            voucher.save()

            messages.success(request, 'Voucher updated successfully and WhatsApp message sent.')
            return redirect('employee_customerview', id=voucher.customer.id)

        except (ValueError, TypeError) as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('employee_postpone_voucher', voucher_id=voucher_id)

    # If it's a GET request, prepare the form
    customers = Customers.objects.all()
    sales_persons = CustomUser.objects.all()
    destinations = Trip.objects.all()
    bank_accounts = BankAccount.objects.all()
    meals = MealPlans.objects.all()

    return render(request, 'EmpPostpone/employee_postpone_trip_voucher.html', {
        'voucher': voucher,
        'customers': customers,
        'sales_persons': sales_persons,
        'destinations': destinations,
        'bank_accounts': bank_accounts,
        'meals': meals,
    })



#------------------------------------------- Cancel Voucher ------------------------------------


def employee_send_whatsapp_cancel_trip_voucher_message(request, voucher_id, cancellation_date):
    voucher = get_object_or_404(TripVoucher, id=voucher_id)
    
    customer_name = voucher.customer.customer_display_name
    destination = voucher.destination.place_name
    start_date = voucher.start_date.strftime('%d-%B-%Y')
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
                    {"name": "destination", "value": destination},
                    {"name": "date", "value": start_date},
                    {"name": "canceldate", "value": cancel_date}
                ],
                "whatsappNumber": country_code_whatsapp + whatsapp_number
            }
        ],
        "template_name": "cancel_trip_vouchers"
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



def employee_cancel_trip_voucher(request, id):
    voucher = get_object_or_404(TripVoucher, id=id)
    
    if request.method == "POST":
        try:
            # Update the cancellation date in the existing voucher record
            voucher.cancellation_date = timezone.now().date()

            # Send WhatsApp message
            employee_send_whatsapp_cancel_trip_voucher_message(request, voucher.id, voucher.cancellation_date)
            
            # Save the updated voucher
            voucher.save()
            
            # Add success message
            messages.success(request, 'Trip voucher cancelled successfully and WhatsApp message sent.')
            
            # Redirect back to customer view with the customer's ID
            return redirect('employee_customerview', id=voucher.customer.id)
        
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('employee_customerview', id=voucher.customer.id)
    
    # If it's not a POST request, render the template with voucher details
    return render(request, 'EmpSales/EmpCustomers/employee_Customers_View.html', {'voucher': voucher})