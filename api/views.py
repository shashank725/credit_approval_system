from django.shortcuts import render
from django.http.response import JsonResponse
from celery.result import AsyncResult
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
from dateutil.relativedelta import relativedelta

from credit_approval_system.celery import celery_app
from api.tasks import ingest_data
from api.models import Customer, Loan
from api.serializers import CustomerSerializer, LoanApprovalSerializer, LoanDetailSerializer, CustomerDetailSerializer
from api.check_loan_eligibility import check_loan_eligibility

# Create your views here.

def import_data(request, task_id=None):
    if not task_id:
        task = ingest_data.delay()
        result = AsyncResult(task.id, app=celery_app)
        return JsonResponse({'Uploading to DB':f'{task.id} = {result.status}'})
    else:
        result = AsyncResult(task_id)
        return JsonResponse({task_id:str(result.status)})


@api_view(['POST'])
def register_customer(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        approved_limit = round(36 * serializer.validated_data['monthly_salary'] / 100000) * 100000
        serializer.validated_data['approved_limit'] = approved_limit
        customer = serializer.save()
        customer.save()           #We have used 'save' method in models.py, that why we are using it
        response_data = {
            'customer_id': customer.customer_id,
            'name': f'{customer.first_name} {customer.last_name}',
            'age': customer.age,
            'monthly_income': customer.monthly_salary,
            'approved_limit': approved_limit,
            'phone_number': int(customer.phone_number),
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def check_eligibility(request):
    serializer = LoanApprovalSerializer(data=request.data)
    if serializer.is_valid():
        customer_id = serializer.validated_data['customer_id']
        loan_amount = serializer.validated_data['loan_amount']
        interest_rate = serializer.validated_data['interest_rate']
        tenure = serializer.validated_data['tenure']
        try:
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return Response({customer_id: "Customer does not exists"},
                             status=status.HTTP_404_NOT_FOUND)
        response_data = check_loan_eligibility(customer_id, loan_amount, interest_rate, tenure, customer)
        return Response(response_data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class create_loan(APIView):
    def post(elf, request, format=None):
        serializer = LoanApprovalSerializer(data=request.data)
        if serializer.is_valid():
            customer_id = serializer.validated_data['customer_id']
            loan_amount = serializer.validated_data['loan_amount']
            interest_rate = serializer.validated_data['interest_rate']
            tenure = serializer.validated_data['tenure']
            try:
                customer = Customer.objects.get(customer_id=customer_id)
            except Customer.DoesNotExist:
                return Response({customer_id: "Customer does not exists"},
                                status=status.HTTP_404_NOT_FOUND)
            response = check_loan_eligibility(customer_id, loan_amount, interest_rate, tenure, customer)
            if response["approval"] == True:
                loan = Loan.objects.create(
                    customer=customer,
                    loan_amount=loan_amount,
                    tenure=response["tenure"],
                    interest_rate=response["interest_rate"],
                    monthly_repayment=response["monthly_installment"],
                    start_date=datetime.datetime.now().date(),
                    end_date=datetime.datetime.now().date()+relativedelta(months=tenure)
                    )
                loan.save()           #We have used 'save' method in models.py, that why we are using it
                message = None
                status_code = status.HTTP_201_CREATED
            else:
                status_code = status.HTTP_202_ACCEPTED
                loan = {"id": None}
                if response["corrected_interest_rate"] is not None:
                    print(response["corrected_interest_rate"])
                    message = f'Loan available at {response["corrected_interest_rate"]}% interest_rate'
                else:
                    message = f'Sorry, cannot avail this amount of loan'
            print(f'Loan available at {response["corrected_interest_rate"]}% interest_rate')
            response_data = {
                "loan_id": loan.id,
                "customer_id": customer_id,
                "loan_approved": response["approval"],
                "message": message,
                "monthly_installment": response["monthly_installment"]
            }
            return Response(response_data, status=status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def view_loan(request, loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        loan_serializer = LoanDetailSerializer(loan)
        customer_serializer = CustomerDetailSerializer(loan.customer)
        response_data = {
            'loan_id': loan_serializer.data['loan_id'],
            'customer': customer_serializer.data,
            'loan_amount': loan_serializer.data['loan_amount'],
            'interest_rate': loan_serializer.data['interest_rate'],
            'monthly_installment': loan_serializer.data['monthly_repayment'],
            'tenure': loan_serializer.data['tenure'],
        }
        return Response(response_data, status=status.HTTP_202_ACCEPTED)
    except Loan.DoesNotExist:
        return Response({'error': 'Loan not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def view_loans_by_customer(request, customer_id):
    loans = Loan.objects.filter(customer__id=customer_id)
    serializer = LoanDetailSerializer(loans, many=True)
    if len(serializer.data) == 0:
        return Response({"detail": "No Loan Found"}, status=status.HTTP_200_OK)
    for loan_data in serializer.data:
        loan = Loan.objects.get(customer__id=customer_id,loan_id=loan_data['loan_id'])
        repayments_left = loan.tenure - loan.emis_paid_on_time
        loan_data['repayments_left'] = repayments_left
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
