from django.shortcuts import render
from .forms import InputForm

# Create your views here.
def index(request):
    return render(request, 'demo_app/index.html', {})

def input_form(request):
    form = InputForm()
    contexts = {
        'form':form
    }
    return render(request, 'demo_app/input_form.html', contexts)