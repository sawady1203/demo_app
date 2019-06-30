from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import InputForm, SignUpForm
import joblib
from datetime import date
import numpy as np
from .models import Customer
from django.contrib.auth.decorators import login_required



# 学習済みモデルの読み込み
# 最初に読み込んだ方が一回で済む
loaded_model = joblib.load('demo_app/demo_model.pkl')

@login_required
def index(request):
    return render(request, 'demo_app/index.html', {})

@login_required
def input_form(request):
    if request.method == "POST":
        form = InputForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('demo_app:result') # /resultへ遷移するように変更
    else:
        form = InputForm()
        return render(request, 'demo_app/input_form.html', {'form':form})

@login_required
def result(request):
    # 最新データを持ってきて推論結果を渡したい
    _data = Customer.objects.order_by('id').reverse().values_list\
        ('limit_balance', 'sex', 'education', 'marriage', 'age', 'pay_0', 'pay_2', 'pay_3', 'pay_4', 'pay_5', 'pay_6', 'bill_amt_1', 'pay_amt_1', 'pay_amt_2', 'pay_amt_3', 'pay_amt_4', 'pay_amt_5', 'pay_amt_6')

    # print(_data)
    # 推論の実行
    x = np.array([_data[0]])
    y = loaded_model.predict(x)
    y_proba = loaded_model.predict_proba(x)
    y, y_proba = y[0], y_proba[0]

    # 結果に基づいてコメントを返す
    if y == 0:
        if y_proba[y] > 75:
            comment = 'この方への貸し出しは危険です'
        else:
            comment = 'この方への貸し出しは用検討です'
    else:
        if y_proba[y] > 75:
            comment = 'この方への貸し出しは全く問題ありません'
        else:
            comment = 'この方への貸し出しは問題ないでしょう'

    # 推論結果をDBに保存
    _customer = Customer.objects.order_by('id').reverse()[0] # Customerの切り出し
    _customer.proba = y_proba[y]
    _customer.result = y
    _customer.comment = comment
    _customer.save() # データを保存

    contexts = {
        'y':y,
        'y_proba':round(y_proba[y], 2),
        'comment': comment,
    }
    return render(request, 'demo_app/result.html', contexts)

@login_required
def history(request):
    if request.method == 'POST':
        print(request)
        print(request.POST)
        d_id = request.POST # POSTされた値を取得
        d_customer = Customer.objects.get(id=d_id['d_id'])
        d_customer.delete() # 顧客データを消去
        customers = Customer.objects.all()
        contexts = {
            'customers': customers
        }
        return render(request, 'demo_app/history.html', contexts)
    else:        
        customers = Customer.objects.all() # 顧客データの取得
        contexts = {
            'customers': customers
        }
        return render(request, 'demo_app/history.html', contexts)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            print('username: ' + username)
            print('raw_password: ' + raw_password)
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('demo_app:index')
    else:
        form = SignUpForm()
    return render(request, 'demo_app/signup.html', {'form': form})