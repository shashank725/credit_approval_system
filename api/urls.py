from django.urls import path
from api.views import import_data, register_customer, check_eligibility, create_loan, view_loan, view_loans_by_customer


urlpatterns = [
    path('import_data/', import_data, name="import_data"),
    path('import_data/<str:task_id>/', import_data, name="task_status"),
    path('register/', register_customer, name="register"),
    path('check-eligibility/', check_eligibility, name="check-eligibility"),
    path('create-loan/', create_loan.as_view(), name="create-loan"),
    path('view-loan/<str:loan_id>/',  view_loan, name="view-loan"),
    path('view_loans/<str:customer_id>/', view_loans_by_customer, name="view_loans")
]