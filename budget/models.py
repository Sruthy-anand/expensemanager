from django.db import models
from django.contrib.auth.models import User



class Expense(models.Model):

    title=models.CharField(max_length=200)

    amount=models.IntegerField()

    created_date=models.DateTimeField(auto_now_add=True)

    category_choices=(
        ("food","food"),
        ("travel","travel"),
        ("health","health"),
        ("other","other")
    )

    category=models.CharField(max_length=200,choices=category_choices,default="other")
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    
    def __str__(self) -> str:

        return self.title
    