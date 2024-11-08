from django.contrib import messages, auth
from django.contrib.auth import authenticate,login,logout
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
from django.urls import reverse_lazy
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
    return redirect("adminlogin")





def index(request):
    tickets = Ticket.objects.order_by('created_at')[:1]
    notification = Ticket.objects.filter(status__in=['OPEN', 'IN_PROGRESS']).order_by('-created_at')


    today = timezone.now().date()
    first_day_this_month = today.replace(day=1)
    last_month = first_day_this_month - relativedelta(months=1)


    def get_percentage_change(current, previous):
        if previous > 0:
            return ((current - previous) / previous) * 100
        return 100 if current > 0 else 0


    return render(request, 'index.html',{'tickets':tickets,'notification':notification})
   

def base(request):
    return render(request,'base.html')


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





def employee_delete(request,id):
    employee=get_object_or_404(CustomUser,id=id)
    employee.delete()
    messages.success(request,'Employee deleted successfully')
    return redirect('employeelist')


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






#----------------------------------------------------TICKETS----------------------------------------------------



@login_required(login_url='admin_loginview')
def ticketlist(request):
    ticketlist=Ticket.objects.exclude(status='Attended').order_by('-id')
    solved_ticket = Ticket.objects.all().filter(status='Attended')
    query = request.GET.get('q')
    if query:
        lead_list = ticketlist.filter(Q(full_name__icontains=query) | Q(mobile__icontains=query))

    paginator=Paginator(ticketlist, 10)
    page_number=request.GET.get('page')
    try:
        ticket=paginator.page(page_number)
    except PageNotAnInteger:
        ticket=paginator.page(1)
    except EmptyPage:
        ticket=paginator.page(paginator.num_pages)




    has_ticket=paginator.count > 0

    return render(request,'Ticket/Ticket_List.html',{'ticket':ticket, 'has_ticket': has_ticket, 'query': query,'solved_ticket':solved_ticket})



@login_required(login_url='admin_loginview')
def ticket_details(request,id):
    ticket=get_object_or_404(Ticket,id=id)
    return render(request,'Ticket/Ticket_Details.html',{'ticket':ticket})




class TicketStatusUpdate(UpdateView):
    template_name = "Ticket/Status_update.html"
    model = Ticket
    form_class = StatusUpdateForm
    pk_url_kwarg = "pk"
    context_object_name = "instance"
    success_url = reverse_lazy("ticketlist")

    def get_object(self, queryset=None):
        title = self.kwargs.get('title')
        return get_object_or_404(Ticket, title=title)

    def form_valid(self, form):
        # Add your success message here
        messages.success(self.request, 'Status successfully Updated')
        return super().form_valid(form)



def tech_list(request):
    tech_list=User.objects.filter(is_superuser=False).order_by('-id')

    return render(request,'Tech/Tech_List.html',{'tech_list':tech_list})
