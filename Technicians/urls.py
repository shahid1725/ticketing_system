from django.urls import path

from .views import *


urlpatterns=[
    path('tech_base', tech_base, name="tech_base"),
    path('tech_signup', tech_signup, name="tech_signup"),
    path('', tech_signin, name="tech_signin"),
    path('tech_index',tech_index,name="tech_index"),
    path('tech_logout', tech_logout, name="tech_logout"),

    path('tech_ticketlist', tech_ticketlist, name="tech_ticketlist"),
    path('tech_ticketadd', tech_ticketadd, name="tech_ticketadd"),
    path('tech_ticketdetails/<int:id>/', tech_ticket_details, name='tech_ticket_details'),
    # path('lead/edit/<int:id>/', leadedit, name="tech_leadedit"),
    # path('lead/attend/<int:id>/', leadattend, name='tech_leadattend'),
    # path('lead/attend/update/<int:id>/', update_lead_date, name='tech_update_lead_date'),


]