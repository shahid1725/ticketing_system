from django.urls import path
from . import views
from .Views.customer_views import *
from .Views.resorts_views import *
from .Views.ownresorts_views import *

from .Views.lead_views import *
from .Views.account_views import *
from .Views.meals_views import *
from .Views.invoice_views import *
from .Views.trip_views import *
from .Views.stay_views import *
from .Views.script_views import *
from .Views.voucher_views import *
from .Views.tag_views import *
from .Views.report_views import *
from .Views.itinerary_views import *
from .Views.guide_views import *
from .Views.tripinvoice_views import *
from .Views.tripvoucher_views import *
from .views import *



urlpatterns=[
    path('', views.AdminLogin.as_view(), name='adminlogin'),
    path('signout', views.adminsignout, name='adminsignout'),
    path('index',views.index,name="index"),
    path('base', views.base, name="base"),
    path('reset_password/<int:user_id>/', views.reset_password, name='reset_password'),


    path('lead/list', leadlist, name="leadlist"),
    path('lead/add', leadadd, name="leadadd"),
    # path('lead/details/<int:id>/', lead_details, name='lead_details'),
    path('lead/edit/<int:id>/', leadedit, name="leadedit"),
    path('lead/attend/<int:id>/', leadattend, name='leadattend'),
    path('lead/attend/update/<int:id>/', update_lead_date, name='update_lead_date'),

    path('ticket/list', ticketlist, name="ticketlist"),
    path('ticket/details/<int:id>/', ticket_details, name='ticket_details'),
    path('ticket/status/<str:title>/', TicketStatusUpdate.as_view(), name='ticket_status_update'),

    path('tech/list', tech_list, name="tech_list"),



















    path('employee/list', views.employeelist, name="employeelist"),
    path('employee/add', views.employeeadd, name="employeeadd"),
    path('employee/delete/<int:id>/', views.employee_delete, name='employee_delete'),
    # path('employee/signin', views.employee_signin, name="employee_signin"),
    # path('employee/dashboard', views.employee_dashboard, name="employee_dashboard"),

    # path('report', views.voucher_report, name="report"),
    path('report', sales_report, name='report'),
    path('voucherreport', voucher_report, name='voucher_report'),
    path('leadsreport', leads_report, name='leads_report'),
    path('profitreport', profit_report, name='profit_report'),
    path('packages', packages, name="packages"),
    path('packages/addtrip', tripadd, name="tripadd"),
    path('packages/edittrip/<int:id>/', tripedit, name="tripedit"),
    path('packages/deletetrip/<int:id>/', tripdelete, name='tripdelete'),
    path('send-trip-email/<int:trip_id>/', send_trip_email, name='send_trip_email'),
    path('send_stay_whatsapp/<int:stay_id>/', send_stay_whatsapp_message, name='send_stay_whatsapp'),
    path('packages/addstay', stayadd, name="stayadd"),
    path('packages/editstay/<int:stay_id>/', stayedit, name='stayedit'),
    path('packages/staydelete/<int:id>/', staydelete, name='staydelete'),
    path('send-stay-email/<int:stay_id>/', send_stay_email, name='send_stay_email'),

    path('script/addscript', addscript, name='addscript'),
    path('script/updatescript/<int:id>/', editscript, name='editscript'),
    path('script/scriptanswer/<int:id>/', scriptanswer, name='scriptanswer'),

    path('tag/addtag', addtag, name='addtag'),
    path('tag/listtag', taglist, name='taglist'),
    path('delete_tag/<int:tag_id>/', delete_tag, name='delete_tag'),

    path('sales/customers/list', customerlist, name="customerlist"),
    path('sales/customers/view/<int:id>', customerview, name="customerview"),
    path('sales/customers/add', customeradd, name="customeradd"),
    path('sales/customers/edit/<int:customer_id>', customeredit, name="customeredit"),
    path('sales/customers/delete/<int:customer_id>', customerdelete, name="customerdelete"),

    path('sales/resorts/list', resortlist, name="resortlist"),
    path('sales/resorts/add', resortadd, name="resortadd"),
    path('sales/resorts/edit/<int:id>/', resortedit, name="resortedit"),
    path('sales/resorts/delete/<int:id>/', resortdelete, name='resortdelete'),

    path('sales/own_resorts/resorts', ownresortlist, name="ownresortlist"),
    path('sales/own_resorts/add_resorts', ownresortadd, name="ownresortadd"),
    path('sales/own_resorts/edit_resorts/<int:id>/', ownresortedit, name="ownresortedit"),
    path('sales/own_resorts/delete_resorts/<int:id>/', ownresortdelete, name="ownresortdelete"),


    path('sales/account_details/details', accountdetails, name="accountdetails"),
    path('sales/account_details/add_details', accountdetailsadd, name="accountdetailsadd"),
    path('sales/account_details/edit_details/<int:id>', accountdetailsedit, name="accountdetailsedit"),
    path('sales/account_details/delete_details/<int:account_id>', accountdetailsdelete, name="accountdetailsdelete"),

    path('sales/Meal_Plans/meal', meallist, name="meallist"),
    path('sales/Meal_Plans/add_meal', mealadd, name="mealadd"),
    path('sales/Meal_Plans/edit_meal/<int:id>', mealedit, name="mealedit"),
    path('sales/Meal_Plans/delete_meal/<int:meal_id>', mealdelete, name="mealdelete"),



    path('sales/sale_invoice/invoice', saleinvoice, name="saleinvoice"),
    path('sales/sale_invoice/add_invoice', saleinvoiceadd, name="saleinvoiceadd"),
    path('sale_invoice/search_customer/', search_customer, name='search_customer'),
    path('sales/sale_invoice/view_invoice/<int:invoice_id>', saleinvoiceview, name="saleinvoiceview"),
    path('sales/sale_invoice/edit_invoice/<int:invoice_id>', saleinvoiceedit, name="saleinvoiceedit"),
    path('sales/sale_invoice/delete_voucher/<int:invoice_id>', saleinvoicedelete, name="saleinvoicedelete"),
    path('invoice_record_payment/<int:id>/', invoice_record_payment, name='invoice_record_payment'),
    path('send_invoice_email/<int:invoice_id>/', send_invoice_email, name='send_invoice_email'),
    path('invoice_emails/<int:invoice_id>/', invoice_email, name="invoice_emails"),

    path('invoice_whattsapp/<int:invoice_id>/', invoice_whattsapp, name="invoice_whattsapp"),
    path('send_whatsapp/<int:invoice_id>/', send_whatsapp_message, name='send_whatsapp_message'),
    
    
    path('sales/trip/invoice/list', tripinvoicelist, name="tripinvoice"),
    path('sales/trip/invoice/add', tripinvoiceadd, name="tripinvoiceadd"),
    path('sales/trip/invoice/edit/<int:invoice_id>', tripinvoiceedit, name="tripinvoiceedit"),
    path('sales/trip/invoice/detail/<int:invoice_id>', tripinvoicedetail, name="tripinvoicedetail"),
    path('sales/trip/invoice/delete/<int:invoice_id>', tripinvoicedelete, name="tripinvoicedelete"),
    path('sales/trip/invoice_record_payment/<int:id>/', tripinvoice_record_payment, name='tripinvoice_record_payment'),
    path('sales/tripemail/<int:invoice_id>/', tripsend_invoice_email, name='tripsend_invoice_email'),
    path('tripinvoice_emails/<int:invoice_id>/', trip_invoice_email, name='trip_invoice_emails'),
    path('send_trip_whatsapp/<int:trip_invoice_id>/', send_whatsapp_invoice_message, name='send_trip_whatsapp'),
    path('trip_invoice_whatsapp/<int:trip_invoice_id>/',trip_invoice_whatsapp, name='trip_invoice_whatsapp'),
    path('trip_invoices/<int:invoice_id>/', send_whatsapp_postpone_trip_invoice_message, name='send_whatsapp_postpone_trip_invoice_message'),
    path('postpone_trip_invoices/<int:invoice_id>/', postpone_trip_invoice, name='postpone_trip_invoice'),
    path('cancel_trip_invoice/<int:id>/', cancel_trip_invoice, name='cancel_trip_invoice'),
    path('send-cancel-trip-invoice-message/<int:invoice_id>/', send_whatsapp_cancel_trip_invoice_message, name='send_cancel_trip_invoice_message'),
    
    path('sales/trip/voucher/list', tripvoucherlist, name="tripvoucher"),
    path('sales/trip/voucher/add', tripvoucheradd, name="tripvoucheradd"),
    path('sales/trip/voucher/edit/<int:voucher_id>', tripvoucheredit, name="tripvoucheredit"),
    path('sales/trip/voucher/detail/<int:voucher_id>', tripvoucherdetail, name="tripvoucherdetail"),
    path('sales/trip/voucher/delete/<int:voucher_id>/', tripvoucherdelete, name="tripvoucherdelete"),
    path('sales/trip/voucher_record_payment/<int:id>/', trip_voucher_record_payment, name='trip_voucher_record_payment'),
    path('send_trip_voucher_email/<int:voucher_id>/', trip_send_voucher_email, name='tripsend_voucher_email'),
    path('tripvoucher_emails/<int:voucher_id>/', trip_voucher_email_template, name="trip_voucher_email"),
    path('send_trip_voucher_whatsapp/<int:trip_voucher_id>/', send_whatsapp_voucher_message, name='send_trip_voucher_whatsapp'),
    path('trip_voucher_whatsapp/<int:trip_voucher_id>/', trip_voucher_whatsapp, name='trip_voucher_whatsapp'),
    path('trip_invoices/<int:invoice_id>/', send_whatsapp_postpone_trip_voucher_message, name='send_whatsapp_postpone_trip_voucher_message'),
    path('trip_vouchers/<int:voucher_id>/', postpone_trip_voucher, name='postpone_trip_voucher'),
    path('cancel-trip-voucher/<int:id>/', cancel_trip_voucher, name='cancel_trip_voucher'),
    path('send-cancel-trip-voucher-message/<int:voucher_id>/', send_whatsapp_cancel_trip_voucher_message, name='send_cancel_trip_voucher_message'),



    path('sales/sale_voucher/voucher', salevoucher, name="salevoucher"),
    path('sales/sale_voucher/add_voucher', salevoucheradd, name="salevoucheradd"),
    path('sales/sale_voucher/view_voucher/<int:voucher_id>', salevoucherview, name="salevoucherview"),
    path('sales/sale_voucher/edit_voucher/<int:voucher_id>', salevoucheredit, name="salevoucheredit"),
    path('sales/sale_voucher/delete_voucher/<int:voucher_id>/', salevoucherdelete, name="salevoucherdelete"),
    path('voucher_record_payment/<int:id>/', voucher_record_payment, name='voucher_record_payment'),
    path('send_voucher_email/<int:voucher_id>/', send_voucher_email, name='send_voucher_email'),
    path('voucher_emails/<int:voucher_id>/', voucher_email_template, name="voucher_email"),
    path('send_voucher_whatsapp/<int:voucher_id>/', send_stay_whatsapp_voucher_message, name='send_stay_whatsapp_voucher_message'),
    path('voucher_whattsapp/<int:voucher_id>/', voucher_whatsapp, name="voucher_whatsapp"),
    
    #-----itinerary
    path('sales/itinerary/add', itinerary_add, name="additinerary"),
    path('sales/itinerary/edit/<int:pk>/', itinerary_edit, name="edititinerary"),
    path('sales/itinerary/list', itinerary_list, name="listitinerary"),
    path('sales/itinerary/view/<int:pk>/', itinerary_view, name="viewitinerary"),
    path('sales/sale_voucher/itinerary_delete/<int:itinerary_id>/', itinerary_delete, name="itinerary_delete"),
    path('send_itinerary_email/<int:itinerary_id>/', send_itinerary_email, name='send_itinerary_email'),
    path('itinerary_emails/<int:itinerary_id>/', itinerary_email_template, name='itinerary_email_template'),
    path('send_itinerary_whatsapp/<int:itinerary_id>/', send_whatsapp_itinerary_message, name='send_itinerary_whatsapp'),
    path('itinerary_whatsapp/<int:itinerary_id>/', itinerary_whatsapp, name='itinerary_whatsapp'),

    path('guide/add', guide_add, name='guide_add'),
    path('guide/list', guide_list, name='guide_list'),
    path('gudie/delete/<int:guide_id>/', guide_delete, name='guide_delete'),


    # path('email/invoice/download',views.invoiceemail,name='invoiceemail'),
    # path('email/voucher/download',views.voucheremail,name='voucheremail'),
    # path('email/itenary/download',views.itineraryemail,name='itineraryemail'),
    # path('itenaryemail', itineraryemailtemplate,name='itineraryemailtemplate'),

#-------------------------------PostPone Invoice and Voucher -------------------------------------- 
    # path('invoices/<int:invoice_id>/postpone/', postpone_invoice, name='postpone_invoice'),
    path('invoices/<int:invoice_id>/send-postpone-message/', send_whatsapp_postpone_invoice_message, name='send_postpone_message'),
    path('postpone_invoices/<int:invoice_id>/', postpone_invoice, name='postpone_invoice'),

    path('cancelinvoice/<int:id>/', cancelinvoice, name='cancelinvoice'),

    # If you want a separate URL for sending the WhatsApp message (optional)
    path('send-cancel-invoice-message/<int:invoice_id>/', send_whatsapp_cancel_invoice_message, name='send_cancel_invoice_message'),


    
    path('send_whatsapp_postpone_voucher/<int:voucher_id>/', send_whatsapp_postpone_voucher_message, name='send_whatsapp_postpone_voucher'),
    path('postpone_vouchers/<int:voucher_id>/', postpone_voucher, name='postpone_voucher'),

    path('cancelvoucher/<int:voucher_id>/', cancelvoucher, name='cancelvoucher'),
    # Optional: Add a URL for sending the WhatsApp message separately
    path('send-cancel-voucher-message/<int:voucher_id>/', send_whatsapp_cancel_voucher_message, name='send_cancel_voucher_message'),



]
