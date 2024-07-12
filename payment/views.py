from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .utils import incomes_in_one_day, incomes_between_two_dates, calculate_total_discounted_amount
from datetime import date, timedelta
from django.contrib import messages
from course.models import *
from django.db.models import Count, Q, Sum
from users.models import User


# Create your views here.
@login_required 
def income(request):
      user = request.user
      if user.is_staff == True:
            negative_wallet_sum, positive_wallet_sum = Student.get_wallet_sums()
            negative_wallet_students = Student.objects.filter(wallet__lt=0)
            positive_wallet_students = Student.objects.filter(wallet__gt=0)
            total_discount  = calculate_total_discounted_amount
            total_students = Student.objects.all().count()
            all_courses_count = Course.objects.count()
            ended_courses_count = Course.objects.filter(is_ended=True).count()
            ongoing_courses_count = Course.objects.filter(is_ended=False).count()

            receiption_admin_true_count = ReceiptionAdmin.objects.filter(status=True).count()
            receiption_admin_false_count = ReceiptionAdmin.objects.filter(status=False).count()

            registration_data_count = RegistrationData.objects.count()
            teacher_count = User.objects.filter(is_teacher=True).count()
            negative_wallet_count = negative_wallet_students.count()
            positive_wallet_count = positive_wallet_students.count()
            if total_students > 0:
                  negative_wallet_percentage = (negative_wallet_count / total_students) * 100
                  positive_wallet_percentage = (positive_wallet_count / total_students) * 100
            else:
                  negative_wallet_percentage = 0
                  positive_wallet_percentage = 0
            start = date.today()-timedelta(days=30)
            end=date.today()
            incomes_between_dates = incomes_between_two_dates( start, end)
            if request.method == 'POST':
                  start = request.POST['start']
                  end = request.POST['end']
                  incomes_between_dates = incomes_between_two_dates( start, end)

            context = {
                  'incomes_between_dates':incomes_between_dates,
                  'todays_income': incomes_in_one_day(date.today()),
                  'start':str(start),
                  'end':str(end),
                  'total_discount':total_discount,
                  'negative_wallet_sum': negative_wallet_sum,
                  'positive_wallet_sum': positive_wallet_sum,
                  'negative_wallet_students' : negative_wallet_students,
                  'positive_wallet_students' : positive_wallet_students,
                  'total_students' : total_students,
                  'all_courses_count': all_courses_count,
                  'ended_courses_count': ended_courses_count,
                  'ongoing_courses_count': ongoing_courses_count,
                  'receiption_admin_true_count': receiption_admin_true_count,
                  'receiption_admin_false_count': receiption_admin_false_count,
                  'registration_data_count': registration_data_count,
                  'teacher_count': teacher_count,
                  'negative_wallet_percentage': negative_wallet_percentage,
                  'positive_wallet_percentage': positive_wallet_percentage,
            }
            return render(request, "income.html", context)
      else  :
            messages.warning(request, "Siz uchun bu sahifa mavjud emas.")
            return redirect('index')
