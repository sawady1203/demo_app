from django import forms # Djangoが準備しているforms
from .models import Customer # モデルで定義したDBテーブル
from django.forms.widgets import NumberInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RangeInput(NumberInput):
    input_type = 'range'
    input_oninput = "document.getElementById('output').values=this.value"

class InputForm(forms.ModelForm):
    limit_balance = forms.IntegerField(widget=RangeInput(), min_value=0, max_value=200000)
    bill_amt_1 = forms.IntegerField(widget=RangeInput(), min_value=0, max_value=10000)
    pay_amt_1 = forms.IntegerField(widget=RangeInput(), min_value=0, max_value=10000)
    pay_amt_2 = forms.IntegerField(widget=RangeInput(), min_value=0, max_value=10000)
    pay_amt_3 = forms.IntegerField(widget=RangeInput(), min_value=0, max_value=10000)
    pay_amt_4 = forms.IntegerField(widget=RangeInput(), min_value=0, max_value=10000)
    pay_amt_5 = forms.IntegerField(widget=RangeInput(), min_value=0, max_value=10000)
    pay_amt_6 = forms.IntegerField(widget=RangeInput(), min_value=0, max_value=10000)

    class Meta:
        model = Customer
        exclude = ['id', 'result', 'proba', 'comment', 'registered_date']
        widgets = {
            'last_name' : forms.TextInput(attrs={'placeholder':'last_name'}),
            'first_name' : forms.TextInput(attrs={'placeholder':'first_name'}),
        }

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        help_text='名字を入力'
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        help_text='名前を入力',
    )
    email = forms.EmailField(
        max_length=254, 
        help_text='Required. Inform a valid email address.'
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')