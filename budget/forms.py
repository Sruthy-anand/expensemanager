from django import forms
from budget.models import Expense

class ExpenseForm(forms.ModelForm):

    class Meta:

        model=Expense

        exclude=("created_date",)

        # fields="__all__"

        widgets={

            "title":forms.TextInput(attrs={"class":"form-control"}),
            "amount":forms.NumberInput(attrs={"class":"form-control"}),
            "category":forms.Select(attrs={"class":"form-control form-select"}),
            "user":forms.TextInput(attrs={"class":"form-control"})

        }