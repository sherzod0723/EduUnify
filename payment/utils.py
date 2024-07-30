from .models import AddCashToWallet, PayToCourse, Course, Discounted_students, Dif_students, Expenses
from django.utils.dateparse import parse_date
from django.http import HttpResponseBadRequest


def incomes_in_one_day(date):
      total_income = 0
      expected_income = 0
      
      payments =  AddCashToWallet.objects.filter(date = date) 
      pay_to_courses = PayToCourse.objects.filter(date=date)
      
      for i in payments:
            total_income += i.summ

      for i in pay_to_courses:
            expected_income += i.transfer_summ      


      context = {
            'total_income':total_income,
            'expected_income':expected_income,
            'wage_of_teachers': expected_income/2,
            'payments':payments,
            'pay_to_courses':pay_to_courses,
      }   
      return context      

def incomes_between_two_dates(start, end):
      total_income = 0
      expected_income = 0
      payments = AddCashToWallet.objects.filter(date__gte=start, date__lte=end).order_by('date')
      pay_to_courses = PayToCourse.objects.filter(date__gte=start, date__lte=end).order_by('date')
      for i in payments:
            total_income += i.summ
      for i in pay_to_courses:
            expected_income += i.transfer_summ     
      context = {
            'total_income':total_income,
            'expected_income':expected_income,
            'wage_of_teachers': expected_income/2,
            'payments':payments,
            'pay_to_courses':pay_to_courses, 
      } 
 
      return context



def income_of_teacher_between_dates(request, start, end):
    teacher = request.user
    income = 0
    courses = Course.objects.filter(teacher=teacher)

    # Ensure start and end are strings
    if not isinstance(start, str) or not isinstance(end, str):
        return HttpResponseBadRequest("Invalid date format")

    start_date = parse_date(start)
    end_date = parse_date(end)

    if start_date is None or end_date is None:
        return HttpResponseBadRequest("Invalid date format")

    pay_to_courses = PayToCourse.objects.filter(course__in=courses, date__gte=start_date, date__lte=end_date).order_by('date')

    for i in pay_to_courses:
        try:
            dif_student = Dif_students.objects.get(student=i.student, course=i.course)
            transfer_amount = dif_student.teacher_money
        except Dif_students.DoesNotExist:
            transfer_amount = i.transfer_summ / 2  # Or any default logic you have for non-Dif_students cases

        income += transfer_amount
    return {'income': income, 'pay_to_courses': pay_to_courses}

def calculate_total_discounted_amount():
    total_discount = 0
    for discount in Discounted_students.objects.all():
        total_discount += discount.discount_summ
    return float(total_discount)


def calculate_total_expenses():
    total_expenses = 0
    for expense in Expenses.objects.all():
        total_expenses += expense.summ
    return float(total_expenses)

def calculate_fresh_income():
    total_income = 0

    pay_to_courses = PayToCourse.objects.all()

    for payment in pay_to_courses:
        try:
            dif_student = Dif_students.objects.get(student=payment.student, course=payment.course)
            income = dif_student.dif_summ - dif_student.teacher_money
        except Dif_students.DoesNotExist:
            income = payment.transfer_summ - (payment.transfer_summ / 2)

        total_income += income

    total_discounted_amount = calculate_total_discounted_amount()
    total_expenses = calculate_total_expenses()
    fresh_income = total_income - total_discounted_amount - total_expenses

    return float(fresh_income)


