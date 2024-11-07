from django.shortcuts import render
from dashboard.models import *
from django.contrib.auth import authenticate,login
from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db.models import Sum

# Create your views here.

def employee_base(request):
    return render(request,'employee_base.html')

def employee_signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user and not user.is_superuser:
            login(request,user)
            return redirect('employee_index')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'auth/Employee_signin.html')


def employee_logout(request):
    return redirect("employee_signin")


@login_required(login_url='employee_signin')
def employee_index(request):

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
        last_month_count = model.objects.filter(**{f"{date_field}__gte": last_month, f"{date_field}__lt": first_day_this_month}).count()
        percentage_change = get_percentage_change(current_month_count, last_month_count)
        return current_month_count, percentage_change

    vouchers_this_month, voucher_percentage_change = get_model_stats(Voucher, 'voucher_date')
    invoices_this_month, invoice_percentage_change = get_model_stats(Invoice, 'invoice_date')
    leads_this_month, leads_percentage_change = get_model_stats(Leads, 'lead_date')

    customers_this_month = Customers.objects.filter(id__gte=1).count()
    customers_last_month = Customers.objects.filter(id__gte=1).exclude(id__in=Customers.objects.filter(id__gte=1).order_by('-id')[:customers_this_month]).count()
    customers_percentage_change = get_percentage_change(customers_this_month, customers_last_month)

    bookings_this_month, bookings_percentage_change = get_model_stats(Invoice, 'invoice_date')

    profit_this_month = Invoice.objects.filter(invoice_date__gte=first_day_this_month).aggregate(Sum('profit'))['profit__sum'] or 0
    profit_last_month = Invoice.objects.filter(invoice_date__gte=last_month, invoice_date__lt=first_day_this_month).aggregate(Sum('profit'))['profit__sum'] or 0
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
    return render(request, 'employee_index.html', {'bookings_count': bookings_count, 'vouchers_count': vouchers_count, 'invoices_count':invoices_count, 'customers_count':customers_count, 'leads_count':leads_count, 'recent_customers':recent_customers, 'recent_leads':recent_leads, 'recent_invoices': recent_invoices,
        'recent_vouchers': recent_vouchers,
        'document_type': document_type, 'upcoming_bookings':upcoming_bookings,'voucher_percentage_change': round(voucher_percentage_change, 2),'invoice_percentage_change': round(invoice_percentage_change, 2),'leads_percentage_change': round(leads_percentage_change, 2),'customers_percentage_change': round(customers_percentage_change, 2),'bookings_percentage_change': round(bookings_percentage_change, 2),
        'total_profit': total_profit,
        'profit_percentage_change': round(profit_percentage_change, 2)  })



def employee_invoiceemail(request):
    return render(request,'EWtemplate/employee_InvoiceEmail.html')

def employee_voucheremail(request):
    return render(request,'EWtemplate/employee_VoucherEmail.html')