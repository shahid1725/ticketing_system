from itertools import chain

from django.shortcuts import render,redirect,get_object_or_404
from dashboard.models import Customers
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

@login_required(login_url='employee_signin')
def employee_customerlist(request):
    query = request.GET.get('q')
    customers_list = Customers.objects.all().order_by('-id')
    if query:
        customers_list = customers_list.filter(
            Q(full_name__icontains=query) | Q(contact_number__icontains=query)
            
        )
    paginator = Paginator(customers_list, 10)  # Show 7 customers per page

    page_number = request.GET.get('page')
    try:
        customers = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        customers = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        customers = paginator.page(paginator.num_pages)

    has_customers = paginator.count > 0
        
    return render(request,'EmpSales/EmpCustomers/employee_Customers_List.html', {'customers':customers,'has_customers':has_customers, 'query': query})


@login_required(login_url='employee_signin')
def employee_customerview(request,id):
    customer = get_object_or_404(Customers, id=id)
    total_billed_amount = Invoice.objects.filter(customer=customer).aggregate(Sum('total_amount'))['total_amount__sum']
    invoices = Invoice.objects.filter(customer=customer)
    paid_amount = invoices.aggregate(Sum('recieved_price'))['recieved_price__sum']
    pending_amount = invoices.aggregate(Sum('pending_price'))['pending_price__sum']
    latest_due_date = invoices.latest('due_date').due_date if invoices.exists() else None


    latest_invoice = invoices.latest('invoice_number') if invoices.exists() else None
    latest_invoice_number = latest_invoice.invoice_number if latest_invoice else None
    latest_voucher = Voucher.objects.filter(customer=customer).latest('voucher_number') if Voucher.objects.filter(customer=customer).exists() else None
    latest_voucher_number = latest_voucher.voucher_number if latest_voucher else None

    latest_trip_invoice = TripInvoice.objects.filter(customer=customer).latest('invoice_number') if TripInvoice.objects.filter(customer=customer).exists() else None
    latest_trip_invoice_number = latest_trip_invoice.invoice_number if latest_trip_invoice else None

    latest_trip_voucher = TripVoucher.objects.filter(customer=customer).latest('voucher_number') if TripVoucher.objects.filter(customer=customer).exists() else None
    latest_trip_voucher_number = latest_trip_voucher.voucher_number if latest_trip_voucher else None

    zero_pending_invoices = invoices.filter(pending_price=0)
    zero_pending_vouchers = Voucher.objects.filter(customer=customer, pending_price=0)

    combined_list = sorted(
        chain(zero_pending_invoices, zero_pending_vouchers),
        key=lambda x: (
            x.invoice_date if isinstance(x, Invoice) else x.voucher_date,
            x.pk,  # Primary key ensures latest added is first if dates are the same
        ),
        reverse=True  # Sort by date in descending order (latest first)
    )

    latest_invoice_and_voucher = {
        'latest_invoice': latest_invoice,
        'latest_voucher': latest_voucher,
        'latest_trip_invoice': latest_trip_invoice,
        'latest_trip_voucher': latest_trip_voucher,
    }
    context ={
        'customer': customer,
        'total_billed_amount': total_billed_amount,
        'paid_amount': paid_amount,
        'pending_amount': pending_amount,
        'latest_due_date': latest_due_date,
        'latest_invoice_number': latest_invoice_number,
        'latest_voucher_number': latest_voucher_number,
        'latest_trip_invoice_number': latest_trip_invoice_number,
        'latest_trip_voucher_number': latest_trip_voucher_number,
        'latest_invoice_and_voucher': latest_invoice_and_voucher,
        'combined_list': combined_list
    }
    return render(request,'EmpSales/EmpCustomers/employee_Customers_View.html',context)

@login_required(login_url='employee_signin')
def employee_customeradd(request):
    if request.method == 'POST':
        customer_type = request.POST.get('customer_type')
        salutation = request.POST.get('salutation')
        full_name = request.POST.get('full_name')
        customer_display_name = request.POST.get('customer_display_name')
        contact_number = request.POST.get('contact_number')
        whatsapp_number = request.POST.get('whatsapp_number')
        country_code_mobile = request.POST.get('country_code_mobile')
        country_code_whatsapp = request.POST.get('country_code_whatsapp')
        same_as_whatsapp = request.POST.get('same_as_whatsapp')
        customer_email = request.POST.get('customer_email')

        if same_as_whatsapp:
            whatsapp_number = contact_number
            country_code_whatsapp = country_code_mobile

        if Customers.objects.filter(contact_number=contact_number).exists():
            messages.error(request,'A customer with this contact number already exists')
            return render(request,'EmpSales/EmpCustomers/employee_Customers_Add.html')
        
        if customer_email and Customers.objects.filter(customer_email=customer_email).exists():
            messages.error(request,'A customer with this email already exists')
            return render(request,'EmpSales/EmpCustomers/employee_Customers_Add.html')
        
        if len(contact_number) < 10:
            messages.error(request,'Contact number must be at least 10 numbers long')
            return render(request,'EmpSales/EmpCustomers/employee_Customers_Add.html')


        customer = Customers.objects.create(
            customer_type=customer_type,
            salutation = salutation,
            full_name = full_name,
            customer_display_name = customer_display_name,
            contact_number = contact_number,
            whatsapp_number=whatsapp_number,
            country_code_mobile=country_code_mobile,
            country_code_whatsapp=country_code_whatsapp,
            customer_email = customer_email
        
        )
        messages.success(request,'Customer created successfully')
        return redirect('employee_customerlist')

    return render(request,'EmpSales/EmpCustomers/employee_Customers_Add.html')


@login_required(login_url='employee_signin')
def employee_customeredit(request, customer_id):
    customer = get_object_or_404(Customers, id=customer_id)

    if request.method == 'POST':
        customer.customer_type = request.POST.get('customer_type')
        customer.salutation = request.POST.get('salutation')
        customer.full_name = request.POST.get('full_name')
        customer.customer_display_name = request.POST.get('customer_display_name')
        customer.contact_number = request.POST.get('contact_number')
        customer.country_code_mobile = request.POST.get('country_code_mobile')
        customer.whatsapp_number = request.POST.get('whatsapp_number').replace(" ", "")
        customer.country_code_whatsapp = request.POST.get('country_code_whatsapp')
        same_as_whatsapp = request.POST.get('same_as_whatsapp') == 'on'
        customer.customer_email = request.POST.get('customer_email')

        if same_as_whatsapp:
            customer.whatsapp_number = customer.contact_number
            customer.country_code_whatsapp = customer.country_code_mobile


        if Customers.objects.filter(contact_number=customer.contact_number).exclude(id=customer.id).exists():
            messages.error(request,'A customer with this contact number already exists')
            return render(request,'EmpSales/EmpCustomers/employee_Customers_Edit.html',{'customer':customer})
        
        if customer.customer_email and Customers.objects.filter(customer_email=customer.customer_email).exclude(id=customer.id).exists():
            messages.error(request,'A customer with this email already exists')
            return render(request,'EmpSales/EmpCustomers/employee_Customers_Edit.html',{'customer':customer})
        
        if len(customer.contact_number) < 10:
            messages.error(request,'Contact number must be at least 10 numbers long')
            return render(request,'EmpSales/EmpCustomers/employee_Customers_Edit.html')
        
        customer.save()
        messages.success(request,'Customer details updated successfully')
        return redirect('employee_customerlist')

    return render(request,'EmpSales/EmpCustomers/employee_Customers_Edit.html',{'customer': customer})


@login_required(login_url='employee_signin')
def employee_customerdelete(request,customer_id):
    customer = get_object_or_404(Customers,id=customer_id)

    if request.method == 'POST':
        customer.delete()
        messages.success(request,'Customer deleted successfully')
        return redirect('employee_customerlist')
