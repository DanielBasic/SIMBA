from django import forms
from time import sleep
from .tasks import task_one

class async_form(forms.Form):
    name = forms.CharField(max_length=100)
    
    
    def func_async(self):
        task_one.delay()
        print("terminou")


