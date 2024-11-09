from django.shortcuts import render
from dashboard.models import *
from django.contrib.auth import authenticate,login
from django.contrib import messages, auth
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db.models import Sum
from django.views.generic import CreateView, ListView, UpdateView, TemplateView
from dashboard.forms import *
from django.urls import reverse_lazy
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


    return render(request, 'employee_index.html')



@login_required(login_url='employee_signin')
def employee_ticketlist(request):
    ticket_list=Ticket.objects.exclude(status='Attended').order_by('-id')
    solved_ticket = Ticket.objects.all().filter(status='Attended')
    query = request.GET.get('q')
    if query:
        ticket_list = ticket_list.filter(Q(full_name__icontains=query) | Q(mobile__icontains=query))

    return render(request,'Ticket/employee_ticket_List.html',{'ticket_list':ticket_list, 'query': query,'solved_ticket':solved_ticket})

@login_required(login_url='employee_signin')
def employee_ticket_details(request,id):
    ticket=get_object_or_404(Ticket,id=id)
    return render(request,'Ticket/employee_Ticket_Details.html',{'ticket':ticket})

class EmployeeTicketStatusUpdate(UpdateView):
    template_name = "Ticket/employee_Status_update.html"
    model = Ticket
    form_class = StatusUpdateForm
    pk_url_kwarg = "pk"
    context_object_name = "instance"
    success_url = reverse_lazy("employee_ticketlist")

    def get_object(self, queryset=None):
        title = self.kwargs.get('title')
        return get_object_or_404(Ticket, title=title)

    def form_valid(self, form):
        # Set the attended_by field to the currently logged-in user
        ticket = form.save(commit=False)
        ticket.attended_by = self.request.user
        ticket.save()

        # Add your success message here
        messages.success(self.request, 'Status successfully updated')
        return super().form_valid(form)