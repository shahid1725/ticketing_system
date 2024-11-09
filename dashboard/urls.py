from django.urls import path
from . import views





from .views import *



urlpatterns=[
    path('', views.AdminLogin.as_view(), name='adminlogin'),
    path('signout', views.adminsignout, name='adminsignout'),
    path('index',views.index,name="index"),
    path('base', views.base, name="base"),
    path('reset_password/<int:user_id>/', views.reset_password, name='reset_password'),

    path('ticket/list', ticketlist, name="ticketlist"),
    path('ticket/details/<int:id>/', ticket_details, name='ticket_details'),
    path('ticket/status/<str:title>/', TicketStatusUpdate.as_view(), name='ticket_status_update'),

    path('tech/list', tech_list, name="tech_list"),


    path('employee/list', views.employeelist, name="employeelist"),
    path('employee/add', views.employeeadd, name="employeeadd"),
    path('employee/delete/<int:id>/', views.employee_delete, name='employee_delete'),
    # path('employee/signin', views.employee_signin, name="employee_signin"),
    # path('employee/dashboard', views.employee_dashboard, name="employee_dashboard"),


]
