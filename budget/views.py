from django.shortcuts import render,redirect

# Create your views here.
from budget.forms import ExpenseForm,RegistrationForm,SignInForm

from django.contrib import messages

from django.views.generic import View

from budget.models import Expense

from django.db.models import Q

from django.contrib.auth.models import User

from django import forms

from django.contrib.auth import authenticate,login,logout

from budget.decorators import signin_required

from django.utils.decorators import method_decorator

from django.views.decorators.cache import never_cache

decs=[signin_required,never_cache]
@method_decorator(decs,name="dispatch")

class ExpenseCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=ExpenseForm()

        return render(request,"exp_create.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=ExpenseForm(request.POST)

        if form_instance.is_valid():

            form_instance.instance.user=request.user

            form_instance.save()

            messages.success(request,"Package is added successfully")

            return redirect("exp-list")
        
        else:

            messages.error(request,"package created is failed")

            return render(request,"exp_create.html",{"form":form_instance})

decs=[signin_required,never_cache]
@method_decorator(decs,name="dispatch")

class ExpenseListView(View):

    def get(self,request,*args,**kwargs):

        # if not request.user.is_authenticated:
        #     return redirect('signin')

        search_text=request.GET.get("search_text")

        selected_category=request.GET.get("category","all")

        if selected_category == "all":
            
            qs=Expense.objects.filter(user=request.user)

        else:
            qs=Expense.objects.filter(category=selected_category,user=request.user)

        if search_text!=None:

            qs=Expense.objects.filter(user=request.user)

            qs=qs.filter(Q(title__contains=search_text))

        return render(request,"exp_list.html",{"expenses":qs,"selected":selected_category})



decs=[signin_required,never_cache]
@method_decorator(decs,name="dispatch")   
class ExpenseDetailView(View):

    def get(self,request,*args,**kwargs):

        # extract id from url
        id=kwargs.get("pk")

        # fetching expense list with id
        qs=Expense.objects.get(id=id)

        return render(request,"exp_detail.html",{"expense":qs})


decs=[signin_required,never_cache]
@method_decorator(decs,name="dispatch")
    
class ExpenseUpdateView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")
        exp_obj=Expense.objects.get(id=id)
        form_instance=ExpenseForm(instance=exp_obj)

        return render(request,"exp_edit.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        exp_obj=Expense.objects.get(id=id)
        form_instance=ExpenseForm(request.POST,instance=exp_obj)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            Expense.objects.filter(id=id).update(**data)
            
            form_instance.save()

            return redirect("exp-list")
        
        else:

            return render(request,"exp_edit.html",{"form":form_instance})
        


decs=[signin_required,never_cache]
@method_decorator(decs,name="dispatch")

class ExpenseDeleteView(View):

    def get(self,request,*args,**kwargs):

        Expense.objects.get(id=kwargs.get("pk")).delete()

        return redirect("exp-list")
    
from django.db.models import Sum



decs=[signin_required,never_cache]
@method_decorator(decs,name="dispatch")

class ExpenseSummaryView(View):

    def get(self,request,*args,**kwargs):
        
        qs=Expense.objects.filter(user=request.user)

        total_exp_count=qs.count()

        category_summary=qs.values("amount").aggregate(exp_sum=Sum("amount"))
        context={
            "total_exp_count":total_exp_count,
            "category_summary":category_summary,
        }

        return render(request,"exp_summary.html",context)
    

class SignUpView(View):

    template_name="register.html"

    def get(self,request,*args,**kwargs):

        form_instance=RegistrationForm()

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=RegistrationForm(request.POST)
        if form_instance.is_valid():

            data=form_instance.cleaned_data
            User.objects.create_user(**data)

            return redirect("exp-list")

        else:

            return render(request,self.template_name,{"form":form_instance})


class SignInView(View):

    template_name="login.html"

    def get(self,request,*args,**kwargs):

        form_instance=SignInForm()

        return render(request,self.template_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_instance=SignInForm(request.POST)

        if form_instance.is_valid():

            uname=form_instance.cleaned_data.get("username")
            pwd=form_instance.cleaned_data.get("password")

            user_object=authenticate(request,username=uname,password=pwd)

            if user_object:

                login(request,user_object)

                return redirect("exp-list")

            return render(request,self.template_name,{"form":form_instance})



decs=[signin_required,never_cache]
@method_decorator(decs,name="dispatch")

class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)
        return redirect("signin")
    


class DashBoradView(View):

    template_name="dash_board.html"
    def get(self,request,*args,**kwargs):

        return render(request,self.template_name)