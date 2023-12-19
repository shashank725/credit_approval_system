from api.models import Customer, Loan
import datetime

def check_loan_eligibility(customer_id, loan_amount, interest_rate, tenure, customer):
    monthly_salary = customer.monthly_salary
    sum_of_all_current_EMIs = 0
    totel_emi_paid_on_time = 0
    total_number_of_past_loans = 0
    current_year_total_payment = 0
    today_date = datetime.datetime.now().date()
    sum_of_current_loans_of_customer = 0
    loans = customer.loan_set.all()
    for loan in loans:
        monthly_repayment = int(loan.monthly_repayment)
        if loan.end_date > today_date:
            sum_of_all_current_EMIs += monthly_repayment
            sum_of_current_loans_of_customer += loan.loan_amount
        # Past Loans paid on time & No of loans taken in past (i & ii)
        if loan.end_date < today_date:
            emi_paid_on_time = loan.emis_paid_on_time / loan.tenure   # Eg:2/4
            totel_emi_paid_on_time += emi_paid_on_time
            total_number_of_past_loans += 1
        # Loan activity in current year (iii)
        if int(today_date.strftime("%Y")) < int(loan.end_date.strftime("%Y")):
            total_emi_payment = int(today_date.strftime("%m")) * monthly_repayment
            current_year_total_payment += total_emi_payment
        if int(today_date.strftime("%Y")) == int(loan.end_date.strftime("%Y")):
            if int(today_date.strftime("%m")) > int(loan.end_date.strftime("%m")):
                current_year_total_payment = int(today_date.strftime("%m")) * monthly_repayment
            else:
                current_year_total_payment = int(loan.end_date.strftime("%m")) * monthly_repayment
    # Assigning a credit score
    if len(loans) == 0:
        credit_score = 50                            # Did not take any loans till now
    else:
        credit_score = 0
        past_loans_paid_on_time=loans_taken_in_the_past=loan_activity_in_current_year=loan_approved_volume = 0
        if total_number_of_past_loans != 0:
            # i. Past Loans paid on time
            past_loans_paid_on_time = totel_emi_paid_on_time / total_number_of_past_loans   # <=1
            # ii. No of loans taken in past
            if total_number_of_past_loans <= 3:                                             
                loans_taken_in_the_past = 1                                                 # <=1
            elif total_number_of_past_loans <= 6:
                loans_taken_in_the_past = 0.7
            elif total_number_of_past_loans <= 15:
                loans_taken_in_the_past = 0.5
            else:
                loans_taken_in_the_past = 0.2
        # iii. Loan activity in current year
        if current_year_total_payment != 0:
            if current_year_total_payment <= monthly_salary:
                loan_activity_in_current_year = 1                                           # <=1
            elif current_year_total_payment <= monthly_salary+(monthly_salary*0.25):
                loan_activity_in_current_year = 0.7
            elif current_year_total_payment <= monthly_salary+(monthly_salary*0.5):
                loan_activity_in_current_year = 0.5
            else:
                loan_activity_in_current_year = 0.2
        # iv. Loan approved volume
        if len(loans) <= 3:
            loan_approved_volume = 1                                                        # <=1
        elif len(loans) <= 6:
            loan_approved_volume = 0.7
        elif len(loans) <= 15:
            loan_approved_volume = 0.5
        else:
            loan_approved_volume = 0.2
        no_of_factors = 0
        factors = [past_loans_paid_on_time, loans_taken_in_the_past, loan_activity_in_current_year, loan_approved_volume]
        # for count, factor in enumerate(factors, start=1):
        for factor in factors:
            if factor is not None and factor != 0:
                no_of_factors += 1
                credit_score += factor
        credit_score = (credit_score / no_of_factors) * 100
    # v. If sum of current loans of customer > approved limit of customer , credit score = 0
    if sum_of_current_loans_of_customer >= customer.approved_limit:
        credit_score = 0
    print("Credit Score=",credit_score)
    # Loan slabs
    corrected_interest_rate = interest_rate
    if credit_score >= 50:
        approval = True
    elif 50 > credit_score >= 30:
        if interest_rate >= 12:
            approval = True
        else:
            approval = False
            corrected_interest_rate = 12.00
    elif 30 > credit_score >= 10:
        if interest_rate >= 16:
            approval = True
        else:
            approval = False
            corrected_interest_rate = 16.00
    else:
        approval = False
        corrected_interest_rate = None
    print("Current EMIs:",sum_of_all_current_EMIs,"Sal/2:",(monthly_salary/2))
    if sum_of_all_current_EMIs >= (monthly_salary/2):
        approval = False
        corrected_interest_rate = None
    # monthly_installment = float(round((loan_amount * corrected_interest_rate)/tenure, 2))
    if corrected_interest_rate != None:
        monthly_installment = f"{(loan_amount * corrected_interest_rate)/tenure:.2f}"
    else:
        monthly_installment = None
    return {
        "customer_id": customer_id,
        "approval": approval,
        "interest_rate": interest_rate,
        "corrected_interest_rate": corrected_interest_rate,
        "tenure": tenure,
        "monthly_installment": monthly_installment
    }