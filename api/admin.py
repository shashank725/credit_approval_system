from django.contrib import admin
from api.models import Customer, Loan

# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["customer_id", "first_name", "last_name"]
    ordering = ["customer_id"]
    # empty_value_display = "-empty-"
    # list_filter = ["age", "monthly_salary"]
    fieldsets = [
        (
            'Persoanl Info',
            {
                "fields": ["customer_id", "first_name", "last_name", "age"],
            },
        ),
        (
            'Contact', {"fields": ["phone_number"]}
        ),
        (
            "Financial :",
            {
                "classes": ["collapse"],
                "fields": ["monthly_salary", "approved_limit", "current_debt"],
            },
        ),
    ]

admin.site.register(Customer, CustomerAdmin)


class LoanAdmin(admin.ModelAdmin):
    list_display = ["customer", "loan_id"]
    ordering = ["id"]

admin.site.register(Loan, LoanAdmin)
