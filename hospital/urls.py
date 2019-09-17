from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.index, name="index"),
    path('staff/dashboard/', v.staff_dashboard, name="staff-dashboard"),
    path('admin/dashboard/', v.admin_dashboard, name="admin-dashboard"),
    path('payment-made/', v.payment_made, name="payment-made"),
    path('receipts/', v.full_receipts, name="receipts"),
    path('print-receipt/<uuid:uid>/', v.print_receipt, name="receipts"),
    path('transactions/', v.full_transactions, name="transactions"),
    path('make-payment/', v.make_payment, name="make-payment"),
    path('stats/', v.stats_api, name="stats"),
    path('api/login/', v.login_api, name="login-api"),
    path('api/admin-login/', v.login_admin_api, name="login-admin-api"),
    path('api/receipts/', v.receipts_api, name="receipts-api"),
    path('api/transactions/', v.transactions_api, name="transactions-api"),
    path('api/confirm-patient/', v.confirm_patient_api, name="confirm-patient-api"),
    path('api/invoice-data/', v.invoice_data_api, name="invoice-data-api"),
    path('api/process-invoice/', v.process_invoice_api, name="process-invoice-api"),
    path('api/receipts/pay/', v.pay_receipts_api, name="pay-receipts-api"),
    path('dashboard/', v.dashboard, name="dashboard"),
    path('accounts/logout/', v.logout, name="logout"),
    path('staff/issue-invoice/', v.issue_invoice, name="issue-invoice"),
]
