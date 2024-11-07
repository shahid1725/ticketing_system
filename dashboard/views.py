from django.contrib import messages, auth
from django.contrib.auth import authenticate,login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from dashboard.models import *
from openpyxl import Workbook
import openpyxl
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth import get_user_model, login
from .forms import *
from django.views.generic import CreateView, ListView, UpdateView, TemplateView
# Create your views here.


User = get_user_model()  # This will point to your CustomUser model

# Admin Login View
class AdminLogin(TemplateView):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        context = {"form": form}
        return render(request, "SignIn.html", context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_superuser:
                login(request, user)
                # request.session[settings.ADMIN_SESSION_COOKIE_NAME] = True
                # request.session.pop(settings.CUSTOMER_SESSION_COOKIE_NAME, None)
                return redirect("index")
            else:
                form.add_error(None, "Incorrect username or password")
        return render(request, 'SignIn.html')


# Admin Logout View
def adminsignout(request):
    logout(request)
    request.session.pop(settings.ADMIN_SESSION_COOKIE_NAME, None)
    return redirect("adminlogin")




@login_required(login_url='admin_loginview')
def index(request):
    today = timezone.now().date()
    first_day_this_month = today.replace(day=1)
    last_month = first_day_this_month - relativedelta(months=1)

    # vouchers_this_month = Voucher.objects.filter(voucher_date__gte=first_day_this_month).count()
    # vouchers_last_month = Voucher.objects.filter(voucher_date__gte=last_month, voucher_date__lt=first_day_this_month).count()

    # # Calculate percentage change
    # if vouchers_last_month > 0:
    #     voucher_percentage_change = ((vouchers_this_month - vouchers_last_month) / vouchers_last_month) * 100
    # else:
    #     voucher_percentage_change = 100 if vouchers_this_month > 0 else 0

    
    # invoices_this_month = Invoice.objects.filter(invoice_date__gte=first_day_this_month).count()
    # invoices_last_month = Invoice.objects.filter(invoice_date__gte=last_month, invoice_date__lt=first_day_this_month).count()

    # # Calculate percentage change
    # if invoices_last_month > 0:
    #     invoice_percentage_change = ((invoices_this_month - invoices_last_month) / invoices_last_month) * 100
    # else:
    #     invoice_percentage_change = 100 if invoices_this_month > 0 else 0


    # leads_this_month = Leads.objects.filter(lead_date__gte=first_day_this_month).count()
    # leads_last_month = Leads.objects.filter(lead_date__gte=last_month, lead_date__lt=first_day_this_month).count()

    # # Calculate percentage change
    # if leads_last_month > 0:
    #     leads_percentage_change = ((leads_this_month - leads_last_month) / leads_last_month) * 100
    # else:
    #     leads_percentage_change = 100 if leads_this_month > 0 else 0

    
    # customers_this_month = Customers.objects.filter(id__gte=1).count()
    # customers_last_month = Customers.objects.filter(id__gte=1).exclude(id__in=Customers.objects.filter(id__gte=1).order_by('-id')[:customers_this_month]).count()

    # # Calculate percentage change
    # if customers_last_month > 0:
    #     customers_percentage_change = ((customers_this_month - customers_last_month) / customers_last_month) * 100
    # else:
    #     customers_percentage_change = 100 if customers_this_month > 0 else 0

    
    # bookings_this_month = Invoice.objects.filter(invoice_date__gte=first_day_this_month).count()
    # bookings_last_month = Invoice.objects.filter(invoice_date__gte=last_month, invoice_date__lt=first_day_this_month).count()

    # # Calculate percentage change
    # if bookings_last_month > 0:
    #     bookings_percentage_change = ((bookings_this_month - bookings_last_month) / bookings_last_month) * 100
    # else:
    #     bookings_percentage_change = 100 if bookings_this_month > 0 else 0

    # profit_this_month = Invoice.objects.filter(invoice_date__gte=first_day_this_month).aggregate(Sum('profit'))['profit__sum'] or 0
    # profit_last_month = Invoice.objects.filter(invoice_date__gte=last_month, invoice_date__lt=first_day_this_month).aggregate(Sum('profit'))['profit__sum'] or 0

    # # Calculate total profit
    # total_profit = Invoice.objects.aggregate(Sum('profit'))['profit__sum'] or 0

    # # Calculate percentage change
    # if profit_last_month > 0:
    #     profit_percentage_change = ((profit_this_month - profit_last_month) / profit_last_month) * 100
    # else:
    #     profit_percentage_change = 100 if profit_this_month > 0 else 0


    def get_percentage_change(current, previous):
        if previous > 0:
            return ((current - previous) / previous) * 100
        return 100 if current > 0 else 0

    # Fetch counts and calculate percentage changes
    # def get_model_stats(model, date_field):
    #     current_month_count = model.objects.filter(**{f"{date_field}__gte": first_day_this_month}).count()
    #     last_month_count = model.objects.filter(**{f"{date_field}__gte": last_month, f"{date_field}__lt": first_day_this_month}).count()
    #     percentage_change = get_percentage_change(current_month_count, last_month_count)
    #     return current_month_count, percentage_change
    #
    # vouchers_this_month, voucher_percentage_change = get_model_stats(Voucher, 'voucher_date')
    # invoices_this_month, invoice_percentage_change = get_model_stats(Invoice, 'invoice_date')
    # leads_this_month, leads_percentage_change = get_model_stats(Leads, 'lead_date')
    #
    # customers_this_month = Customers.objects.filter(id__gte=1).count()
    # customers_last_month = Customers.objects.filter(id__gte=1).exclude(id__in=Customers.objects.filter(id__gte=1).order_by('-id')[:customers_this_month]).count()
    # customers_percentage_change = get_percentage_change(customers_this_month, customers_last_month)
    #
    # bookings_this_month, bookings_percentage_change = get_model_stats(Invoice, 'invoice_date')
    #
    # profit_this_month = Invoice.objects.filter(invoice_date__gte=first_day_this_month).aggregate(Sum('profit'))['profit__sum'] or 0
    # profit_last_month = Invoice.objects.filter(invoice_date__gte=last_month, invoice_date__lt=first_day_this_month).aggregate(Sum('profit'))['profit__sum'] or 0
    # total_profit = Invoice.objects.aggregate(Sum('profit'))['profit__sum'] or 0
    # profit_percentage_change = get_percentage_change(profit_this_month, profit_last_month)
    #
    #
    # bookings_count = Invoice.objects.count()
    # vouchers_count = Voucher.objects.count()  # Get the total count of Voucher instances
    # invoices_count = Invoice.objects.count()
    # customers_count = Customers.objects.count()
    # leads_count = Leads.objects.count()
    # recent_customers = Customers.objects.order_by('-id')[:2]
    # recent_leads = Leads.objects.order_by('-id')[:2]
    # upcoming_bookings = Invoice.objects.order_by('-id')[:4]
    # document_type = request.GET.get('document_type', 'Invoice')  # Default to Invoice
    #
    # if document_type == 'Invoice':
    #     recent_invoices = Invoice.objects.order_by('-id')[:2]
    #     recent_vouchers = []  # Empty queryset for vouchers
    # else:
    #     recent_vouchers = Voucher.objects.order_by('-id')[:2]
    #     recent_invoices = []  # Empty queryset for invoices
    return render(request, 'tech_index.html')
   

def base(request):
    return render(request,'base.html')

@login_required(login_url='admin_loginview')
def employeelist(request):
    users_list=CustomUser.objects.filter(is_superuser=False,is_staff=False).order_by('-id')

    paginator=Paginator(users_list, 10)
    page_number=request.GET.get('page')
    try:
        user=paginator.page(page_number)
    except PageNotAnInteger:
        user=paginator.page(1)
    except EmptyPage:
        user=paginator.page(paginator.num_pages)

    has_user= paginator.count > 0
    return render(request,'Employee/Employee_List.html',{'user':user, 'has_user': has_user})

@login_required(login_url='admin_loginview')
def employeeadd(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        date_joined = request.POST.get('date_joined')
        date_of_birth = request.POST.get('date_of_birth')
        email = request.POST.get('email')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        position = request.POST.get('position')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'User with this username already exists')
            return render(request, 'Employee/Employee_Add.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'User with this email already exists')
            return render(request, 'Employee/Employee_Add.html')

        if CustomUser.objects.filter(mobile=mobile).exists():
            messages.error(request, 'User with this mobile number already exists')
            return render(request, 'Employee/Employee_Add.html')

        if password !=password2:
            messages.error(request,'Passwords do not match')
            return render(request,'Employee/Employee_Add.html')

        if len(mobile) < 10:
            messages.error(request,'Mobile number should not be less than 10 digits')
            return render(request, 'Employee/Employee_Add.html')

        try:
            CustomUser.objects.create_user(username=username,date_joined=date_joined,date_of_birth=date_of_birth,
                                           email=email,address=address,mobile=mobile,password=password,
                                           position=position)
            messages.success(request,'Account created successfully')
            return redirect('employeelist')

        except IntegrityError:
            messages.error(request,'User with this username or email or mobile number already exists')
            return render(request,'Employee/Employee_Add.html')

        except Exception as e:
            messages.error(request,f'An error occurred: {str(e)}')
            return render(request,'Employee/Employee_Add.html')

    return render(request,'Employee/Employee_Add.html')


# def employee_signin(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(username=username, password=password)
#         if user and not user.is_superuser:
#             login(request,user)
#             return redirect('employee_dashboard')
#         else:
#             messages.error(request, 'Invalid username or password')

#     return render(request, 'Employee/Employee_signin.html')

@login_required(login_url='admin_loginview')
def employee_delete(request,id):
    employee=get_object_or_404(CustomUser,id=id)
    employee.delete()
    messages.success(request,'Employee deleted successfully')
    return redirect('employeelist')

@login_required(login_url='admin_loginview')
def reset_password(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            user.set_password(new_password)
            user.save()

            messages.success(request, 'Password reset successfully')
            return redirect('employeelist')
        else:
            messages.error(request, 'Passwords do not match')

    return render(request, 'reset_password.html', {'user': user})

def staywhatsapp(request, stay_id):
    stay = get_object_or_404(Stay, id=stay_id)
    context = {
        'stay': stay
    }
    return render(request, 'whatsapp_templates/stay_whattsapp.html', context)
    

# def employee_dashboard(request):
#     return render(request,'Employee/Employee_dashboard.html')
 
# def voucher_report(request):
#     employees = CustomUser.objects.exclude(username='admin')
#     resorts = Resorts.objects.all()

#     selected_employee = None
#     selected_resort = None
#     start_date = None
#     end_date = None
#     employee_views_report = False  # Default value for the checkbox

#     if request.method == 'POST':
#         start_date = request.POST.get('start_date')
#         end_date = request.POST.get('end_date')
#         selected_employee = request.POST.get('selected_employee')
#         selected_resort = request.POST.get('selected_resort')
#         employee_views_report = 'employee_views_report' in request.POST

#     filters = {}
#     if start_date and end_date:
#         filters['voucher_date__range'] = [start_date, end_date]

#     if employee_views_report and selected_employee:
#         filters['sales_person__username'] = selected_employee

#     if selected_resort:
#         filters['resort_name__id'] = selected_resort

#     data = Voucher.objects.filter(**filters).order_by('voucher_date')

#     # Pagination
#     paginator = Paginator(data, 200)  # Show 200 vouchers per page

#     page_number = request.GET.get('page')
#     try:
#         data = paginator.page(page_number)
#     except PageNotAnInteger:
#         data = paginator.page(1)
#     except EmptyPage:
#         data = paginator.page(paginator.num_pages)

#     if 'export_excel' in request.POST:
#         workbook = Workbook()
#         worksheet = workbook.active

#         headers = [
#             '#', 'Date', 'Voucher No', 'Customer', 'Mobile Number', 'Resort Name', 'Profit', 'Price Quoted',
#             'Received', 'Pending', 'Sales Person', 'Account Details',
#         ]
#         worksheet.append(headers)

#         column_widths = [5, 15, 15, 30, 15, 30, 20, 15, 20, 15, 15, 30]
#         for i, width in enumerate(column_widths, start=1):
#             worksheet.column_dimensions[openpyxl.utils.get_column_letter(i)].width = width

#         for idx, d in enumerate(data, start=1):
#             received_price = float(d.received_price) if isinstance(d.received_price, str) else d.received_price
#             pending_price = float(d.pending_price) if isinstance(d.pending_price, str) else d.pending_price
#             account_name = str(d.account_name) if d.account_name else ""
#             profit = f"{d.profit:.0f}" if d.profit else ""
#             resort_name = str(d.resort_name) if d.resort_name else ""
#             row = [
#                 idx, d.voucher_date, d.voucher_number,
#                 f"{d.customer.salutation}. {d.customer.first_name}", d.customer.mobile, resort_name, profit,
#                 f"{d.total_amount:.0f}", f"{received_price:.0f}",
#                 f"{pending_price:.0f}", d.sales_person.username,
#                 account_name,
#             ]
#             worksheet.append(row)

#         response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#         response['Content-Disposition'] = 'attachment; filename=voucher_report.xlsx'
#         workbook.save(response)
#         return response

#     return render(request, 'Report/Report.html', {
#         'data': data,
#         'employees': employees,
#         'selected_employee': selected_employee,
#         'resorts': resorts,
#         'selected_resort': selected_resort,
#         'start_date': start_date,
#         'end_date': end_date,
#         'employee_views_report': employee_views_report,
#     })


# sneha---------------------------------------------->




# resortlist------------------------------------------------
# def resortlist(request):
#     return render(request,'Sales/Resorts/Resorts_List.html')

# def resortadd(request):
#     return render(request,'Sales/Resorts/Resorts_Add.html')

# def resortedit(request):
#     return render(request,'Sales/Resorts/Resorts_Edit.html')


# #ownresort---------------------------------------------------
# def ownresortlist(request):
#     return render(request,'Sales/Own_Resort/Own_resort_list.html')

# def ownresortadd(request):
#     return render(request,'Sales/Own_Resort/Own_Resort_Add.html')

# def ownresortedit(request):
#     return render(request,'Sales/Own_Resort/Own_Resort_Edit.html')


# #accountDetails-----------------------------------------------
# def accountdetails(request):
#     return render(request,'Sales/Account_Details/Account_Details_list.html')

# def accountdetailsadd(request):
#     return render(request,'Sales/Account_Details/Account_Details_Add.html')

# def accountdetailsedit(request):
#     return render(request,'Sales/Account_Details/Account_Details_Edit.html')


# #meal_list------------------------------------------------------->
# def meallist(request):
#     return render(request,'Sales/Meal_Plans/Meal_List.html')

# def mealadd(request):
#     return render(request,'Sales/Meal_Plans/Meal_Add.html')

# def mealedit(request):
#     return render(request,'Sales/Meal_Plans/Meal_Edit.html')



# #invoice------------------------------------------------------------>
# def saleinvoice(request):
#     return render(request,'Sales/Sale_invoice/Sale_invoice.html')

# def saleinvoiceadd(request):
#     return render(request,'Sales/Sale_invoice/Sale_invoice_add.html')

# def saleinvoiceview(request):
#     return render(request,'Sales/Sale_invoice/Sale_invoice_view.html')

# def saleinvoiceedit(request):
#     return render(request,'Sales/Sale_invoice/Sale_invoice_edit.html')


# #voucher----------------------------------------------------------->
# def salevoucher(request):
#     return render(request,'Sales/Sale_voucher/Sale_voucher.html')

# def salevoucheradd(request):
#     return render(request,'Sales/Sale_voucher/Sale_voucher_add.html')

# def salevoucherview(request):
#     return render(request,'Sales/Sale_voucher/Sale_voucher_view.html')

# def salevoucheredit(request):
#     return render(request,'Sales/Sale_voucher/Sale_voucher_edit.html')

# #------------------------------------------
# def invoiceemail(request):
#     return render(request,'EWtemplate/InvoiceEmail.html')

# def voucheremail(request):
#     return render(request,'EWtemplate/VoucherEmail.html')


# def itineraryemail(request):
#     return render(request,'emailtemplates/emailItenary.html')


# def itineraryemailtemplate(request):
#     return render(request,'itinerary_email.html')


def Settings(request):
    return render(request,'settings/settings.html')











