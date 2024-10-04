from django.shortcuts import render,redirect

# Create your views here.
from budget.forms import ExpenseForm

from django.contrib import messages

from django.views.generic import View

from budget.models import Expense

class ExpenseCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=ExpenseForm()

        return render(request,"exp_create.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=ExpenseForm(request.POST)

        if form_instance.is_valid():

            form_instance.save()

            messages.success(request,"Package is added successfully")

            return redirect("exp-add")
        
        else:

            messages.error(request,"package created is failed")

            return render(request,"exp_create.html",{"form":form_instance})

class ExpenseListView(View):

    def get(self,request,*args,**kwargs):

        qs=Expense.objects.all()

        return render(request,"exp_list.html",{"expenses":qs})
    
class ExpenseDetailView(View):

    def get(self,request,*args,**kwargs):

        # extract id from url
        id=kwargs.get("pk")

        # fetching expense list with id
        qs=Expense.objects.get(id=id)

        return render(request,"exp_detail.html",{"expense":qs})