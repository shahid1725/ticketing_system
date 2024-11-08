from django.urls import path

from . import views
from .EmpViews.emp_customer_views import *
from .EmpViews.emp_resorts_views import *
from .EmpViews.emp_ownresorts_views import *

from .EmpViews.emp_lead_views import *
from .EmpViews.emp_account_views import *
from .EmpViews.emp_meals_views import *
from .EmpViews.emp_invoice_views import *
from .EmpViews.emp_trip_views import *
from .EmpViews.emp_stay_views import *
from .EmpViews.emp_script_views import *
from .EmpViews.emp_voucher_views import *
from .EmpViews.emp_tag_views import *
from .EmpViews.emp_report_views import *
from .EmpViews.emp_itinerary_views import *
from .EmpViews.emp_guide_views import *
from .EmpViews.emp_tripinvoice_views import *
from .EmpViews.emp_tripvoucher_views import *
from .views import *

urlpatterns=[
    path('employee_base', views.employee_base, name="employee_base"),
    path('', views.employee_signin, name="employee_signin"),
    path('employee_index',views.employee_index,name="employee_index"),
    path('logout', views.employee_logout, name="employee_logout"),

    # path('lead/list', employee_leadlist, name="employee_leadlist"),
    path('lead/add', employee_leadadd, name="employee_leadadd"),
    path('lead/details/<int:id>/', employee_lead_details, name='employee_lead_details'),
    path('lead/edit/<int:id>/', employee_leadedit, name="employee_leadedit"),
    path('lead/attend/<int:id>/', employee_leadattend, name="employee_leadattend"),
    path('lead/attend/update/<int:id>/', employee_update_lead_date, name='employee_update_lead_date'),

    path('ticket/list', employee_ticketlist, name="employee_ticketlist"),
    path('ticket/details/<int:id>/', employee_ticket_details, name='employee_ticket_details'),
    path('ticket/status/<str:title>/', EmployeeTicketStatusUpdate.as_view(), name='employee_ticket_status_update'),



    
    # path('report', views.voucher_report, name="report"),
    path('employee_report', employee_sales_report, name='employee_report'),
    path('employee_voucherreport', employee_voucher_report, name='employee_voucher_report'),
    path('employee/profitreport', employee_profit_report, name='employee_profit_report'),
    path('employee_leadsreport', employee_leads_report, name='employee_leads_report'),
    path('packages', employee_packages, name="employee_packages"),

    
    path('packages/addtrip', employee_tripadd, name="employee_tripadd"),
    path('packages/edittrip/<int:id>/', employee_tripedit, name="employee_tripedit"),
    path('packages/deletetrip/<int:id>/', employee_tripdelete, name='employee_tripdelete'),
    path('send-trip-email/<int:trip_id>/', employee_send_trip_email, name='employee_send_trip_email'),


    path('packages/addstay', employee_stayadd, name="employee_stayadd"),
    path('packages/editstay/<int:stay_id>/', employee_stayedit, name='employee_stayedit'),
    path('packages/staydelete/<int:id>/', employee_staydelete, name='employee_staydelete'),
    path('send-stay-email/<int:stay_id>/', employee_send_stay_email, name='employee_send_stay_email'),

    path('script/addscript', employee_addscript, name='employee_addscript'),
    path('script/updatescript/<int:id>/', employee_editscript, name='employee_editscript'),
    path('script/employee_scriptanswer/<int:id>/', employee_scriptanswer, name='employee_scriptanswer'),

    path('tag/addtag', employee_addtag, name='employee_addtag'),
    path('tag/listtag', employee_taglist, name='employee_taglist'),
    path('delete_tag/<int:tag_id>/', employee_delete_tag, name='employee_delete_tag'),


    path('sales/customers/list', employee_customerlist, name="employee_customerlist"),
    path('sales/customers/view/<int:id>', employee_customerview, name="employee_customerview"),
    path('sales/customers/add', employee_customeradd, name="employee_customeradd"),
    path('sales/customers/edit/<int:customer_id>', employee_customeredit, name="employee_customeredit"),
    path('sales/customers/delete/<int:customer_id>', employee_customerdelete, name="employee_customerdelete"),


    path('sales/resorts/list', employee_resortlist, name="employee_resortlist"),
    path('sales/resorts/add', employee_resortadd, name="employee_resortadd"),
    path('sales/resorts/edit/<int:id>/', employee_resortedit, name="employee_resortedit"),
    path('sales/resorts/delete/<int:id>/', employee_resortdelete, name='employee_resortdelete'),

    path('sales/own_resorts/resorts', employee_ownresortlist, name="employee_ownresortlist"),
    path('sales/own_resorts/add_resorts', employee_ownresortadd, name="employee_ownresortadd"),
    path('sales/own_resorts/edit_resorts/<int:id>/', employee_ownresortedit, name="employee_ownresortedit"),
    path('sales/own_resorts/delete_resorts/<int:id>/', employee_ownresortdelete, name="employee_ownresortdelete"),


    path('sales/account_details/details', employee_accountdetails, name="employee_accountdetails"),
    path('sales/account_details/add_details', employee_accountdetailsadd, name="employee_accountdetailsadd"),
    path('sales/account_details/edit_details/<int:id>', employee_accountdetailsedit, name="employee_accountdetailsedit"),
    path('sales/account_details/delete_details/<int:account_id>', employee_accountdetailsdelete, name="employee_accountdetailsdelete"),

    path('sales/Meal_Plans/meal', employee_meallist, name="employee_meallist"),
    path('sales/Meal_Plans/add_meal', employee_mealadd, name="employee_mealadd"),
    path('sales/Meal_Plans/edit_meal/<int:id>', employee_mealedit, name="employee_mealedit"),
    path('sales/Meal_Plans/delete_meal/<int:meal_id>', employee_mealdelete, name="employee_mealdelete"),



    path('sales/sale_invoice/invoice', employee_saleinvoice, name="employee_saleinvoice"),
    path('sales/sale_invoice/add_invoice', employee_saleinvoiceadd, name="employee_saleinvoiceadd"),
    path('sale_invoice/search_customer/', search_customer, name='search_customer'),
    path('sales/sale_invoice/view_invoice/<int:invoice_id>', employee_saleinvoiceview, name="employee_saleinvoiceview"),
    path('sales/sale_invoice/edit_invoice/<int:invoice_id>', employee_saleinvoiceedit, name="employee_saleinvoiceedit"),
    path('sales/sale_invoice/delete_voucher/<int:invoice_id>', employee_saleinvoicedelete, name="employee_saleinvoicedelete"),
    path('invoice_record_payment/<int:id>/', employee_invoice_record_payment, name='employee_invoice_record_payment'),
    path('send_invoice_email/<int:invoice_id>/', employee_send_invoice_email, name='employee_send_invoice_email'),
    path('invoice_emails/<int:invoice_id>/', invoice_email, name="invoice_emails"),

    path('invoice_whattsapp/<int:invoice_id>/', employee_invoice_whattsapp, name="employee_invoice_whattsapp"),
    path('send_whatsapp/<int:invoice_id>/', employee_send_whatsapp_message, name='employee_send_whatsapp_message'),


    path('invoices/<int:invoice_id>/send-postpone-message/', employee_send_whatsapp_postpone_invoice_message, name='employee_send_postpone_message'),
    path('postpone_invoices/<int:invoice_id>/', employee_postpone_invoice, name='employee_postpone_invoice'),

    path('cancelinvoice/<int:id>/', employee_cancelinvoice, name='employee_cancelinvoice'),

    # If you want a separate URL for sending the WhatsApp message (optional)
    path('send-cancel-invoice-message/<int:invoice_id>/', employee_send_whatsapp_cancel_invoice_message, name='employee_send_cancel_invoice_message'),

    # path('send_whatsapp/<int:invoice_id>/', send_whatsapp_message, name='send_whatsapp_message'),


    path('sales/trip/invoice/list', employee_tripinvoicelist, name="employee_tripinvoice"),
    path('sales/trip/invoice/add', employee_tripinvoiceadd, name="employee_tripinvoiceadd"),
    path('sales/trip/invoice/edit/<int:invoice_id>', employee_tripinvoiceedit, name="employee_tripinvoiceedit"),
    path('sales/trip/invoice/detail/<int:invoice_id>', employee_tripinvoicedetail, name="employee_tripinvoicedetail"),
    path('sales/trip/invoice/delete/<int:invoice_id>', employee_tripinvoicedelete, name="employee_tripinvoicedelete"),
    path('sales/trip/invoice_record_payment/<int:id>/', employee_tripinvoice_record_payment, name='employee_tripinvoice_record_payment'),
    path('sales/tripemail/<int:invoice_id>/', employee_tripsend_invoice_email, name='employee_tripsend_invoice_email'),
    path('tripinvoice_emails/<int:invoice_id>/', employee_trip_invoice_email, name='employee_trip_invoice_emails'),

    path('send_trip_whatsapp/<int:trip_invoice_id>/', employee_send_whatsapp_invoice_message, name='employee_send_trip_whatsapp'),
    path('trip_invoice_whatsapp/<int:trip_invoice_id>/', employee_trip_invoice_whatsapp, name='employee_trip_invoice_whatsapp'),

    path('trip_invoices/<int:invoice_id>/', employee_send_whatsapp_postpone_trip_invoice_message, name='employee_send_whatsapp_postpone_trip_invoice_message'),
    path('postpone_trip_invoices/<int:invoice_id>/', employee_postpone_trip_invoice, name='employee_postpone_trip_invoice'),
    path('cancel_trip_invoice/<int:id>/', employee_cancel_trip_invoice, name='employee_cancel_trip_invoice'),
    path('send-cancel-trip-invoice-message/<int:invoice_id>/', employee_send_whatsapp_cancel_trip_invoice_message, name='employee_send_cancel_trip_invoice_message'),




    path('sales/sale_voucher/voucher', employee_salevoucher, name="employee_salevoucher"),
    path('sales/sale_voucher/add_voucher', employee_salevoucheradd, name="employee_salevoucheradd"),
    path('sales/sale_voucher/view_voucher/<int:voucher_id>', employee_salevoucherview, name="employee_salevoucherview"),
    path('sales/sale_voucher/edit_voucher/<int:voucher_id>', employee_salevoucheredit, name="employee_salevoucheredit"),
    path('sales/sale_voucher/delete_voucher/<int:voucher_id>/', employee_salevoucherdelete, name="employee_salevoucherdelete"),
    path('voucher_record_payment/<int:id>/', employee_voucher_record_payment, name='employee_voucher_record_payment'),
    path('send_voucher_email/<int:voucher_id>/', employee_send_voucher_email, name='employee_send_voucher_email'),
    path('voucher_emails/<int:voucher_id>/', voucher_email_template, name="voucher_email"),

    path('send_voucher_whatsapp/<int:voucher_id>/', employee_send_stay_whatsapp_voucher_message, name='employee_send_stay_whatsapp_voucher_message'),
    path('voucher_whattsapp/<int:voucher_id>/', employee_voucher_whatsapp, name="employee_voucher_whatsapp"),

    path('send_whatsapp_postpone_voucher/<int:voucher_id>/', employee_send_whatsapp_postpone_voucher_message, name='employee_send_whatsapp_postpone_voucher'),
    path('postpone_vouchers/<int:voucher_id>/', employee_postpone_voucher, name='employee_postpone_voucher'),

    path('cancelvoucher/<int:voucher_id>/', employee_cancelvoucher, name='employee_cancelvoucher'),
    # Optional: Add a URL for sending the WhatsApp message separately
    path('send-cancel-voucher-message/<int:voucher_id>/', employee_send_whatsapp_cancel_voucher_message, name='employee_send_cancel_voucher_message'),
    # path('send_voucher_whatsapp/<int:voucher_id>/', send_voucher_whatsapp_message, name='send_voucher_whatsapp_message'),


    path('sales/trip/voucher/list', employee_tripvoucherlist, name="employee_tripvoucher"),
    path('sales/trip/voucher/add', employee_tripvoucheradd, name="employee_tripvoucheradd"),
    path('sales/trip/voucher/edit/<int:voucher_id>', employee_tripvoucheredit, name="employee_tripvoucheredit"),
    path('sales/trip/voucher/detail/<int:voucher_id>', employee_tripvoucherdetail, name="employee_tripvoucherdetail"),
    path('sales/trip/voucher/delete/<int:voucher_id>/', employee_tripvoucherdelete, name="employee_tripvoucherdelete"),
    path('sales/trip/voucher_record_payment/<int:id>/', employee_trip_voucher_record_payment, name='employee_trip_voucher_record_payment'),
    path('send_trip_voucher_email/<int:voucher_id>/', employee_trip_send_voucher_email, name='employee_tripsend_voucher_email'),
    path('tripvoucher_emails/<int:voucher_id>/', employee_trip_voucher_email_template, name="employee_trip_voucher_email"),

    path('send_trip_voucher_whatsapp/<int:trip_voucher_id>/', employee_send_whatsapp_voucher_message, name='employee_send_trip_voucher_whatsapp'),
    path('trip_voucher_whatsapp/<int:trip_voucher_id>/', employee_trip_voucher_whatsapp, name='employee_trip_voucher_whatsapp'),

    path('trip_invoices/<int:invoice_id>/', employee_send_whatsapp_postpone_trip_voucher_message, name='employee_send_whatsapp_postpone_trip_voucher_message'),
    path('trip_vouchers/<int:voucher_id>/', employee_postpone_trip_voucher, name='employee_postpone_trip_voucher'),
    path('cancel-trip-voucher/<int:id>/', employee_cancel_trip_voucher, name='employee_cancel_trip_voucher'),
    path('send-cancel-trip-voucher-message/<int:voucher_id>/', employee_send_whatsapp_cancel_trip_voucher_message, name='employee_send_cancel_trip_voucher_message'),

    #-----itinerary
    path('sales/itinerary/add', employee_itinerary_add, name="employee_additinerary"),
    path('sales/itinerary/edit/<int:pk>/', employee_itinerary_edit, name="employee_edititinerary"),
    path('sales/itinerary/list', employee_itinerary_list, name="employee_listitinerary"),
    path('sales/itinerary/view/<int:pk>/', employee_itinerary_view, name="employee_viewitinerary"),
    path('sales/sale_voucher/itinerary_delete/<int:itinerary_id>/', employee_itinerary_delete, name="employee_itinerary_delete"),
    path('send_itinerary_email/<int:itinerary_id>/', employee_send_itinerary_email, name='employee_send_itinerary_email'),
    path('itinerary_emails/<int:itinerary_id>/', itinerary_email_template, name='itinerary_email_template'),

    path('send_itinerary_whatsapp/<int:itinerary_id>/', employee_send_whatsapp_itinerary_message, name='employee_send_itinerary_whatsapp'),
    path('itinerary_whatsapp/<int:itinerary_id>/', employee_itinerary_whatsapp, name='employee_itinerary_whatsapp'),

    path('sales/guide/add', employee_guide_add, name='employee_guide_add'),
    path('sales/guide/list', employee_guide_list, name='employee_guide_list'),
    path('sales/guide/delete/<int:guide_id>/', employee_guide_delete, name='employee_guide_delete'),




    path('send_stay/<int:stay_id>/', staywhatsapp, name='staywhatsapp'),
    path('employee_send_stay_whatsapp/<int:stay_id>/', employee_send_stay_whatsapp_message, name='employee_send_stay_whatsapp'),



#-------------------------------PostPone Invoice and Voucher -------------------------------------- 

    # path('postpone_invoices/<int:invoice_id>/', employee_postpone_invoice, name='employee_postpone_invoice'),

    # path('postpone_vouchers/<int:voucher_id>/', employee_postpone_voucher, name='employee_postpone_voucher'),


#------------------------------------ Cancel Invoice and Voucher ---------------------------------

    # path('cancelinvoice/<int:id>/', employee_cancelinvoice, name='employee_cancelinvoice'),
    # path('cancelvoucher/<int:id>/', employee_cancelvoucher, name='employee_cancelvoucher'),






    ]