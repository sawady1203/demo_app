from django.shortcuts import render, redirect
from .forms import InputForm

from sklearn.externals import joblib
import numpy as np
from .models import Customer

# 学習済みモデルの読み込み
# 最初に読み込んだ方が一回で済む
loaded_model = joblib.load('demo_app/demo_model.pkl')


# Create your views here.
def index(request):
    return render(request, 'demo_app/index.html', {})

def input_form(request):
    if request.method == "POST":
        form = InputForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('demo_app:index') # /resultへ遷移するように変更
    else:
        form = InputForm()
        return render(request, 'demo_app/input_form.html', {'form':form})

def result(request):
    # 最新データを持ってきて推論結果を渡したい
    _data = Customer.objects.order_by('id').reverse().values_list\
        ('limit_balance', 'sex', 'education', 'marriage', 'age', 'pay_0', 'pay_2', 'pay_3', 'pay_4', 'pay_5', 'pay_6', 'bill_amt_1', 'pay_amt_1', 'pay_amt_2', 'pay_amt_3', 'pay_amt_4', 'pay_amt_5', 'pay_amt_6')

    print(_data)
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
    contexts = {
        'y':y,
        'y_proba':round(y_proba[y], 2),
        'comment': comment,
    }
    return render(request, 'demo_app/result.html', contexts)