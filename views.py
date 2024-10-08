from myapp.models import Dreamreal,createAccount,verifiedAccount
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.templatetags.static import static
from django import forms
from .models import Dreamreal
from myapp.forms import LoginForm
import re
from django.urls import reverse
from django.middleware import csrf
import pandas as pd
import datetime
import base64
import mysql.connector
from django.core.cache import cache
show_data='暫無資料'
db_config = {
    'host': 'u3r5w4ayhxzdrw87.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',         # 資料庫伺服器地址 (可以是 IP 或域名)
    'user': 'dhv81sqnky35oozt',     # 資料庫使用者名稱
    'password': 'rrdv8ehsrp8pdzqn', # 資料庫密碼
    'database': 'xltc236odfo1enc9',  # 要使用的資料庫名稱
}
def initialise(request):
    global show_data
    if request.method !='POST':
        form_action_url = reverse('initialise')
        csrf_token = csrf.get_token(request)
        res=f''' <h>click to start</h>
<form action="{form_action_url}"  method="post">
     <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
    <input type="submit" name="start_crawling" value="yes">
</form>'''
        return render(request,'initialise.html',{'res': res})
    else:
        db_config = {
    'host': 'u3r5w4ayhxzdrw87.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',         # 資料庫伺服器地址 (可以是 IP 或域名)
    'user': 'dhv81sqnky35oozt',     # 資料庫使用者名稱
    'password': 'rrdv8ehsrp8pdzqn', # 資料庫密碼
    'database': 'xltc236odfo1enc9',  # 要使用的資料庫名稱
}
        connection = mysql.connector.connect(**db_config)
        cursor=connection.cursor()
        cursor.execute('SELECT * FROM movies_html ORDER BY id DESC LIMIT 1')
        result=cursor.fetchall()
        res=result[0][1]
        final_data=pd.read_html(res)[0]
        show_data=final_data
        return render(request,'initialise.html', {'res': res})
def Taiwan_movies_all(request):
    global show_data , db_config
    if request.method !='POST':
        csrf_token = csrf.get_token(request)
        form_action_url = reverse('Taiwan_movies_all')
        final_data = cache.get('dataframe')
        if final_data is not None:
            from myapp.html_show import html_show
            res=html_show(final_data)
            return render(request,'Taiwan_movie_all.html', {'res': res})
        connection = mysql.connector.connect(**db_config)
        cursor=connection.cursor()
        cursor.execute('SELECT * FROM movies_html ORDER BY id DESC LIMIT 1')
        result=cursor.fetchall()
        res=result[0][1]
        final_data=pd.read_html(res)[0]
        final_data['日期'] = pd.to_datetime(final_data['日期'])
        cache.set('dataframe',final_data, timeout=60*30)
        from myapp.html_show import html_show
        res=html_show(final_data)
        return render(request,'Taiwan_movie_all.html', {'res': res})
    else:
         csrf_token = csrf.get_token(request)
         form_action_url = reverse('Taiwan_movies_all')
         m_select=request.POST['search_movie_name']
         all_data=pd.read_csv('mira_data.csv')
         all_data=all_data[(all_data['中文片名'].str.contains(m_select, na=False)) | (all_data['英文片名'].str.contains(m_select,case=False,na=False))][['中文片名','英文片名','日期','時刻表']].head(10).to_html(classes='table table-striped', index=False)
         all_data=f'''<h>search movie<h>
                    <img src="{image_url}" alt="My Image" width="50" height="50">
                    <form action={form_action_url} method='POST'>
                    <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                    <input type='text' name='search_movie_name'>
                    </form>'''+all_data
         return render(request,'Taiwan_movie_all.html', {'all_data': all_data})
def hello(request):
    if request.method=='POST':
        where_from=request.POST.get('where_from')
        if where_from=='create_account':
            return render(request,'create_account.html')
        elif where_from=='from_create':
            create_e_mail = request.POST.get('create_e_mail')
            create_password_1 = request.POST.get('create_password_1')
            create_password_2 = request.POST.get('create_password_2')
            pattern=re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
            if not re.match(pattern,create_e_mail):
                detail='信箱不正確'
                return render(request,'create_account.html',locals())
            if createAccount.objects.filter(mail=create_e_mail).exists()==False:
                if create_password_2 !=create_password_1 :
                    detail='密碼不一樣'
                    return render(request,'create_account.html',locals())
                createAccount(mail=create_e_mail,password=create_password_2).save()
                res = send_mail("驗證信", "comment tu vas?", "ian27368885@gmail.com", [create_e_mail], html_message=f'<a href="http://127.0.0.1:8000/hello?detail=帳號驗證完成&create_e_mail={create_e_mail}" class="button">點我驗證帳號</a>')
                return HttpResponse(f'{create_e_mail}驗證信已寄出,請查收')
            else:
                 detail='信箱已註冊'
                 return render(request,'create_account.html',locals())
        elif where_from=='from_log_in':
            e_mail = request.POST.get('e_mail')
            password=request.POST.get('password')
            user=verifiedAccount.objects.filter(mail=e_mail)
            for i in user:
                if i.password==password:
                    request.session['logged_in']='logged_in'
                    response=render(request,'sucessfully_logged_in.html')
                    response.set_cookie('e_mail',e_mail)
                    return response
                else:
                     detail='密碼錯誤'
                     return render(request,'hello.html',locals())
            user=createAccount.objects.filter(mail=e_mail)
            for i in user:
                res = send_mail("驗證信", "comment tu vas?", "ian27368885@gmail.com", [e_mail], html_message=f'<a href="http://127.0.0.1:8000/hello?detail=帳號驗證完成&create_e_mail={e_mail}" class="button">點我驗證帳號</a>')
                return HttpResponse(f'{e_mail}驗證信已寄出,請查收')
            detail='無此帳號'
            return render(request,'hello.html',locals())
        elif where_from=='from_log_out':
            e_mail=request.COOKIES.get('e_mail')
            for i in verifiedAccount.objects.filter(mail=e_mail):
                password=i.password
            detail='已登出'
            del request.session['logged_in']
            return render(request,'hello.html',locals())
    else:
        if request.session.get('logged_in') =='logged_in':
            return render(request,'sucessfully_logged_in.html')
        detail=request.GET.get('detail')
        create_e_mail=request.GET.get('create_e_mail')
        if detail==None:
            return render(request,'hello.html')
        users = createAccount.objects.filter(mail=create_e_mail)
        for user in users:
            create_password=user.password
        verifiedAccount(mail=create_e_mail,password=create_password).save()
        return render(request,'hello.html',locals())
    return render(request,'hello.html')


