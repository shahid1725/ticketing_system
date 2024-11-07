from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from dashboard.models import  Customers, CustomUser
from django.db.models import Max,Q
from decimal import Decimal, InvalidOperation
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages
from django.conf import settings
import requests

@login_required(login_url='admin_loginview')
def employee_itinerary_add(request):
    if request.method == "POST":
        is_per_head = request.POST.get('is_per_head') == '1'
        customer_id = request.POST.get('customer_id')
        itinerary_number = request.POST.get('itinerary_number')
        itinerary_date = request.POST.get('itinerary_date')
        guide_type = request.POST.get('guide_type')
        sales_person_id = request.POST.get('sales_person')
        destination = request.POST.get('destination')
        visiting_place1 = request.POST.get('visiting_place1')
        visiting_place2 = request.POST.get('visiting_place2')
        visiting_place3 = request.POST.get('visiting_place3')
        visiting_place4 = request.POST.get('visiting_place4')
        visiting_place5 = request.POST.get('visiting_place5')
        visiting_place6 = request.POST.get('visiting_place6')
        visiting_place7 = request.POST.get('visiting_place7')
        visiting_place8 = request.POST.get('visiting_place8')
        visiting_place9 = request.POST.get('visiting_place9')
        visiting_place10 = request.POST.get('visiting_place10')
        visiting_place11 = request.POST.get('visiting_place11')
        visiting_place12 = request.POST.get('visiting_place12')
        visiting_place13 = request.POST.get('visiting_place13')
        visiting_place14 = request.POST.get('visiting_place14')
        visiting_place15 = request.POST.get('visiting_place15')
        visiting_place16 = request.POST.get('visiting_place16')
        visiting_place17 = request.POST.get('visiting_place17')
        visiting_place18 = request.POST.get('visiting_place18')
        visiting_place19 = request.POST.get('visiting_place19')
        visiting_place20 = request.POST.get('visiting_place20')
        number_of_days = request.POST.get('number_of_days')
        number_of_nights = request.POST.get('number_of_nights')
        adults = request.POST.get('adults')
        children = request.POST.get('children')
        transportation_mode = request.POST.get('transportation_mode')
        vehicle_type = request.POST.get('vehicle_type')
        pick_up_location = request.POST.get('pick_up_location')
        start_date = request.POST.get('start_date')
        drop_location = request.POST.get('drop_location')
        end_date = request.POST.get('end_date')
        accommodation = request.POST.get('accommodation')
        number_of_rooms = request.POST.get('number_of_rooms')
        breakfast = request.POST.get('breakfast')
        lunch = request.POST.get('lunch')
        dinner = request.POST.get('dinner')
        extra_activities1 = request.POST.get('extra_activities1')
        extra_activities2 = request.POST.get('extra_activities2')
        extra_activities3 = request.POST.get('extra_activities3')
        extra_activities4 = request.POST.get('extra_activities4')
        extra_activities5 = request.POST.get('extra_activities5')
        personal_expenses = request.POST.get('personal_expenses')
        extra_meals_ordered = request.POST.get('extra_meals_ordered')
        # expense_per_person = request.POST.get('expense_per_person')
        # person_count = request.POST.get('person_count')
        # expense_per_child = request.POST.get('expense_per_child')
        # child_count = request.POST.get('child_count')
        # total_expense = request.POST.get('total_expense')


        if is_per_head:
            expense_per_person = request.POST.get('expense_per_person')
            person_count = request.POST.get('person_count')
            expense_per_child = request.POST.get('expense_per_child')
            child_count = request.POST.get('child_count')
            total_expense = request.POST.get('total_expense')
            total = total_expense  # Set total to the calculated total_expense
        else:
            total = request.POST.get('total')
            expense_per_person = None
            person_count = None
            expense_per_child = None
            child_count = None
            total_expense = None

        customer_instance = get_object_or_404(Customers, id=customer_id)
        sales_person = get_object_or_404(CustomUser, id=sales_person_id)
        

        itinerary = Itinerary.objects.create(
            customer=customer_instance,
            sales_person=sales_person,
            guide_type=guide_type,
            itinerary_number=itinerary_number,
            itinerary_date=itinerary_date,
            destination=destination,
            visiting_place1=visiting_place1,
            visiting_place2=visiting_place2,
            visiting_place3=visiting_place3,
            visiting_place4=visiting_place4,
            visiting_place5=visiting_place5,
            visiting_place6=visiting_place6,
            visiting_place7=visiting_place7,
            visiting_place8=visiting_place8,
            visiting_place9=visiting_place9,
            visiting_place10=visiting_place10,
            visiting_place11=visiting_place11,
            visiting_place12=visiting_place12,
            visiting_place13=visiting_place13,
            visiting_place14=visiting_place14,
            visiting_place15=visiting_place15,
            visiting_place16=visiting_place16,
            visiting_place17=visiting_place17,
            visiting_place18=visiting_place18,
            visiting_place19=visiting_place19,
            visiting_place20=visiting_place20,
            number_of_days=number_of_days,
            number_of_nights=number_of_nights,
            adults=adults,
            children=children if children else 0,
            transportation_mode=transportation_mode,
            vehicle_type=vehicle_type,
            pick_up_location=pick_up_location,
            start_date = start_date,
            drop_location=drop_location,
            end_date=end_date,
            accommodation=accommodation,
            number_of_rooms=number_of_rooms,
            breakfast=breakfast,
            lunch=lunch,
            dinner=dinner,
            extra_activities1=extra_activities1,
            extra_activities2=extra_activities2,
            extra_activities3=extra_activities3,
            extra_activities4=extra_activities4,
            extra_activities5=extra_activities5,
            personal_expenses=personal_expenses,
            extra_meals_ordered=extra_meals_ordered,
            expense_per_person=expense_per_person,
            person_count=person_count,
            expense_per_child=expense_per_child,
            child_count=child_count,
            total_expense=total_expense,
            total=total,
            is_per_head=is_per_head
        )

      #   # Handle dynamic visiting places
      #   for i in range(1, 6):
      #       place = request.POST.get(f'visiting_place{i}')
      #       if place:
      #           setattr(itinerary, f'visiting_place{i}', place)

      #   # Handle dynamic extra activities
      #   for i in range(1, 6):
      #       activity = request.POST.get(f'extra_activities{i}')
      #       if activity:
      #           setattr(itinerary, f'extra_activities{i}', activity)

        itinerary.save()

        messages.success(request, 'Itinerary created successfully')
        return redirect('employee_listitinerary')

    customers = Customers.objects.all()
    sales_persons = CustomUser.objects.all()
    guides = Guide.objects.all()

    return render(request, 'EmpSales/EmpItinerary/employee_Itinerary_add.html', {
        'customers': customers,
        'sales_persons': sales_persons,
        
        'next_itinerary_number': generate_itinerary_number(),
        'transportation_choices': Itinerary.TRANSPORTATION_CHOICES,
        'vehicle_choices': Itinerary.VEHICLE_CHOICES,
        'guide_choices': Itinerary.Guide_CHOICES,
    })

def generate_itinerary_number():
    last_itinerary = Itinerary.objects.aggregate(Max('id'))
    last_id = last_itinerary['id__max']
    if last_id:
        return f'ITN-{last_id + 1:04d}'
    else:
        return 'ITN-0001'

@login_required(login_url='admin_loginview')
def employee_itinerary_list(request):
    query = request.GET.get('q')
    if query:
        itineraries = Itinerary.objects.filter(
            Q(itinerary_number__icontains=query) | Q(customer__full_name__icontains=query)
        )
    else:
        itineraries = Itinerary.objects.all().order_by('-id')
    
    return render(request, 'EmpSales/EmpItinerary/employee_Itinerary_list.html', {'itineraries': itineraries, 'query': query})

def employee_itinerary_edit(request, pk):
    itinerary = get_object_or_404(Itinerary, pk=pk)

    if request.method == "POST":
        try:
            itinerary.customer_id = request.POST.get('customer_id')
            itinerary.itinerary_date = request.POST.get('itinerary_date')
            itinerary.sales_person_id = request.POST.get('sales_person')
            itinerary.guide_type = request.POST.get('guide_type')
            itinerary.destination = request.POST.get('destination')

            # Dynamic visiting places
            for i in range(1, 21):
                setattr(itinerary, f'visiting_place{i}', request.POST.get(f'visiting_place{i}', ''))

            itinerary.number_of_days = request.POST.get('number_of_days')
            itinerary.number_of_nights = request.POST.get('number_of_nights')
            itinerary.adults = request.POST.get('adults')
            itinerary.children = request.POST.get('children')
            itinerary.transportation_mode = request.POST.get('transportation_mode')
            itinerary.vehicle_type = request.POST.get('vehicle_type')

            itinerary.pick_up_location = request.POST.get('pick_up_location')
            itinerary.start_date = request.POST.get('start_date')
            itinerary.drop_location = request.POST.get('drop_location')
            itinerary.end_date = request.POST.get('end_date')
            itinerary.accommodation = request.POST.get('accommodation')
            itinerary.number_of_rooms = request.POST.get('number_of_rooms')
            itinerary.breakfast = request.POST.get('breakfast')
            itinerary.lunch = request.POST.get('lunch')
            itinerary.dinner = request.POST.get('dinner')
            

            itinerary.is_per_head = request.POST.get('is_per_head') == 'on'
            
            if itinerary.is_per_head:
                itinerary.expense_per_person = Decimal(request.POST.get('expense_per_person', '0.00') or '0.00')
                itinerary.person_count = request.POST.get('person_count')
                itinerary.expense_per_child = Decimal(request.POST.get('expense_per_child', '0.00') or '0.00')
                itinerary.child_count = request.POST.get('child_count')
                itinerary.total_expense = Decimal(request.POST.get('total_expense', '0.00') or '0.00')
                itinerary.total = itinerary.total_expense
            else:
                itinerary.total = Decimal(request.POST.get('total', '0.00') or '0.00')
                itinerary.expense_per_person = None
                itinerary.person_count = None
                itinerary.expense_per_child = None
                itinerary.child_count = None
                itinerary.total_expense = None

            # Dynamic extra activities
            for i in range(1, 6):
                setattr(itinerary, f'extra_activities{i}', request.POST.get(f'extra_activities{i}', ''))

            # Handle decimal fields
            # try:
            #     itinerary.personal_expenses = Decimal(request.POST.get('personal_expenses', '0.00'))
            # except InvalidOperation:
            #     itinerary.personal_expenses = Decimal('0.00')

            itinerary.extra_meals_ordered = request.POST.get('extra_meals_ordered', '')

            # try:
            #     itinerary.expense_per_person = Decimal(request.POST.get('expense_per_person', '0.00'))
            # except InvalidOperation:
            #     itinerary.expense_per_person = Decimal('0.00')

            # try:
            #     itinerary.expense_per_child = Decimal(request.POST.get('expense_per_child', '0.00'))
            # except InvalidOperation:
            #     itinerary.expense_per_child = Decimal('0.00')

            # try:
            #     itinerary.total_expense = Decimal(request.POST.get('total_expense', '0.00'))
            # except InvalidOperation:
            #     itinerary.total_expense = Decimal('0.00')

            itinerary.save()
            messages.success(request, 'Itinerary updated successfully')
        except InvalidOperation:
            messages.error(request, 'Failed to update itinerary due to invalid data')

        return redirect('employee_listitinerary')

    customers = Customers.objects.all()
    sales_persons = CustomUser.objects.all()
    
    return render(request, 'EmpSales/EmpItinerary/employee_Itinerary_edit.html', {
        'itinerary': itinerary,
        'customers': customers,
        'sales_persons': sales_persons,
        
        'transportation_choices': Itinerary.TRANSPORTATION_CHOICES,
        'vehicle_choices': Itinerary.VEHICLE_CHOICES,
        'guide_choices': Itinerary.Guide_CHOICES,
    })

@login_required(login_url='admin_loginview')
def employee_itinerary_view(request, pk):
    itinerary = get_object_or_404(Itinerary, pk=pk)
    return render(request, 'EmpSales/EmpItinerary/employee_Itinerary_view.html', {'itinerary': itinerary})


@login_required(login_url='admin_loginview')
def employee_itinerary_delete(request, itinerary_id):
    itinerary = get_object_or_404(Itinerary, id=itinerary_id)
    if request.method == "POST":
        itinerary.delete()
        messages.success(request, 'itinerary deleted successfully.')
        return redirect('employee_listitinerary')  # Adjust this redirect to your actual voucher list view name
    

def employee_send_itinerary_email(request, itinerary_id):
    itinerary = get_object_or_404(Itinerary, id=itinerary_id)
    customer_email = itinerary.customer.customer_email

    subject = f"Booking Details for {itinerary.customer.full_name} - Itinerary {itinerary.itinerary_number}"
    itinerary_id = itinerary.id
    itinerary_link = f'https://www.sales.navigotrips.com/itinerary_emails/{itinerary_id}/'

    message = f'Dear {itinerary.customer.salutation}. {itinerary.customer.customer_display_name}, Greetings From Navigo !!! Please find your itinerary details below:'

    html_message = render_to_string('emailtemplates/emailitinerary.html', {'itinerary': itinerary, 'itinerary_link': itinerary_link, 'subject': subject, 'message': message})
    text_message = message

    email = EmailMultiAlternatives(subject, text_message, settings.DEFAULT_FROM_EMAIL, [customer_email])
    email.attach_alternative(html_message, "text/html")
    email.send()

    messages.success(request, 'Email sent successfully.')
    return redirect('employee_listitinerary')

def itinerary_email_template(request, itinerary_id):
    itinerary = get_object_or_404(Itinerary, id=itinerary_id)
    return render(request, 'itinerary_email_template.html', {'itinerary': itinerary})




#------------------------------------------- whatsapp message -------------------------------------



def employee_send_whatsapp_itinerary(customer_display_name, destination, start_date, itinerary_id, contact_number):
    url = "https://live-mt-server.wati.io/329541/api/v1/sendTemplateMessages"
    
    payload = {
        "broadcast_name": "Navigo Trips",
        "receivers": [
            {
                "customParams": [
                    {"name": "name", "value": customer_display_name},
                    {"name": "destination", "value": destination},
                    {"name": "date", "value": start_date},
                    {"name": "inv_link", "value": f"itinerary_whatsapp/{itinerary_id}/"}
                ],
                "whatsappNumber": "91" + contact_number
            }
        ],
        "template_name": "itinerary_trips"
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

def employee_send_whatsapp_itinerary_message(request, itinerary_id):
    itinerary = get_object_or_404(Itinerary, id=itinerary_id)
    
    # Extract necessary data from the itinerary object
    customer_display_name = itinerary.customer.customer_display_name
    destination = itinerary.destination
    if itinerary.start_date:
        start_date = itinerary.start_date.strftime('%d-%B-%Y')  # Convert date to string
    else:
        start_date = "Not Available"  # Or handle this case as needed
    contact_number = itinerary.customer.contact_number
    
    # Call the send_whatsapp_itinerary function
    employee_send_whatsapp_itinerary(customer_display_name, destination, start_date, itinerary_id, contact_number)
    
    messages.success(request, 'WhatsApp itinerary message sent successfully.')
    return redirect('employee_listitinerary')  # Adjust this to your actual itinerary list view name

def employee_itinerary_whatsapp(request, itinerary_id):
    itinerary = get_object_or_404(Itinerary, id=itinerary_id)
    
    context = {
        'itinerary': itinerary,
        'visiting_places': itinerary.get_visiting_places(),
        'extra_activities': itinerary.get_extra_activities(),
    }
    
    return render(request, 'whatsapp_templates/itinerary_whatsapp.html', context)
    



