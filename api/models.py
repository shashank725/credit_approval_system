from django.db import models

# Create your models here.


class Customer(models.Model):
    customer_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=10)
    monthly_salary = models.IntegerField()
    approved_limit = models.IntegerField()
    current_debt = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self) -> str:
        return str(self.customer_id)

class Loan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan_id = models.IntegerField()
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    monthly_repayment = models.DecimalField(max_digits=10, decimal_places=2)
    emis_paid_on_time = models.IntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self) -> str:
        return str(self.customer)+" - "+str(self.loan_id)
