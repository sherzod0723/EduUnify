from django import forms
from .models import Dif_students, Expenses

class DifStudentsForm(forms.ModelForm):
    class Meta:
        model = Dif_students
        fields = ['student', 'course', 'dif_summ', 'teacher_money', 'general_payment']


class ExpensesForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = ['name', 'about', 'summ']