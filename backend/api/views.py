import uuid
from api.models import AuthUser
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json,requests
import time
from django.core import serializers
# Create your views here.
from django.middleware.csrf import get_token


def getToken(request):
    token = get_token(request)
    json_dict = {'csrftoken': token}
    return JsonResponse(json_dict, safe=False)

def clearSession(request):
    request.session.clear()
    json_dict = {'errcode': 200, 'errmsg': '退出成功！'}
    return JsonResponse(json_dict, safe=False)

def userLogin(request):
    json_dict = {'errcode': 403, 'errmsg': None}
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        userlist = AuthUser.objects.filter(username=username)
        if len(userlist) == 0:
            json_dict['errcode'] = 101
            json_dict['errmsg'] = '找不到你的用户名！'
        else:
            check_pwd = check_password(password, userlist[0].password)
            if check_pwd:
                json_dict['errcode'] = 200
                json_dict['errmsg'] = '登录成功！'
                request.session['id']=userlist[0].id
                request.session['username']=userlist[0].username
                request.session['staff']=userlist[0].is_superuser
                request.session['superuser']=userlist[0].is_superuser
                request.session['email']=userlist[0].email
                request.session['phone']=userlist[0].phone
            else:
                json_dict['errcode'] = 102
                json_dict['errmsg'] = '用户名或密码错误'
    else:
        json_dict['errmsg'] = '你干嘛，嗨嗨呦!'
    return JsonResponse(json_dict, safe=False)


def userReg(request):
    json_dict = {'errcode': 403, 'errmsg': None}
    strTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    if request.method == 'POST':
        username = request.POST.get('username', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        if username == '' or password == '' or phone == '' or email == '':
            json_dict['errmsg'] = '请填写完整！'
        else:
            userlist = AuthUser.objects.filter(username=username)
            if len(userlist) == 0:
                userlist = AuthUser.objects.filter(email=email)
                if len(userlist) == 0:
                    userlist = AuthUser.objects.filter(phone=phone)
                    if len(userlist) == 0:
                        password = make_password(password)
                        AuthUser.objects.create(
                            username=username,
                            email=email,
                            phone=phone,
                            password=password,
                            is_superuser=0,
                            is_staff=1,
                            is_active=1,
                            date_joined=strTime
                        )
                        json_dict['errcode'] = 200
                        json_dict['errmsg'] = '注册成功！'
                        userlist = AuthUser.objects.filter(username=username)
                        request.session['id']=userlist[0].id
                        request.session['username']=userlist[0].username
                        request.session['staff']=userlist[0].is_superuser
                        request.session['superuser']=userlist[0].is_superuser
                        request.session['email']=userlist[0].email
                        request.session['phone']=userlist[0].phone
                    else:
                        json_dict['errcode'] = 103
                        json_dict['errmsg'] = '手机号已经被注册了'
                else:
                    json_dict['errcode'] = 102
                    json_dict['errmsg'] = '邮箱已经被注册了'
                
            else:
                json_dict['errcode'] = 101
                json_dict['errmsg'] = '用户名已经被注册了！'

    else:
        json_dict['errmsg'] = '你干嘛，嗨嗨呦!'
    return JsonResponse(json_dict, safe=False)

def userStatues(request):
    json_dict = {'errcode': 403, 'errmsg': None , 'user': None}
    try:
        request.session['id']
    except KeyError:
        json_dict['errmsg'] = '你干嘛，嗨嗨呦!'
    else:
        json_dict['errcode'] = 200
        json_dict['errmsg'] = 'succeed!'
        data = [
            {
                'userid':request.session['id'],
                'username':request.session['username'],
                'is_staff':request.session['staff'],
                'email':request.session['email'],
                'phone':request.session['phone'],
                'is_superuser':request.session['superuser']
            }
        ]
        json_dict['user']  = data
    return JsonResponse(json_dict, safe=False)

def adminUserlist(request):
    json_dict = {'errcode': 403, 'errmsg': None , 'user': None}
    try:
        request.session['id']
    except KeyError:
        json_dict['errmsg'] = '你干嘛，嗨嗨呦!'
    else:
        if request.session['superuser'] == 1:
            userlist = AuthUser.objects.all()
            json_data = serializers.serialize('json', userlist) 
            json_data = json.loads(json_data)
            data = []
            for i in range(len(json_data)):
                user_json = {
                    'username':json_data[i]['fields']['username'],
                    'email':json_data[i]['fields']['email'],
                    'phone':json_data[i]['fields']['phone'],
                    'is_superuser':json_data[i]['fields']['is_superuser'],
                }
                data.append(user_json)
            json_dict['errcode'] = 200
            json_dict['errmsg'] = 'succeed!'
            json_dict['user'] = data
        else:
            json_dict['errmsg'] = '你干嘛，嗨嗨呦!'
    return JsonResponse(json_dict, safe=False)

def updatePwd(request):
    json_dict = {'errcode': 403, 'errmsg': None, 'user': None}
    try:
        request.session['id']
    except KeyError:
        json_dict['errmsg'] = '你干嘛，嗨嗨哟!'
    else:
        if request.method == 'POST':
            username = request.session['username']
            user = AuthUser.objects.filter(username=username)
            password = request.POST.get('password', '')
            new_password = request.POST.get('new_password', '')
            confirmed_password = request.POST.get('confirmed_password', '')
            if new_password != '' and confirmed_password != '':
                check = check_password(password, user[0].password)
                if not check:
                    json_dict['errmsg'] = '原密码不正确'
                else:
                    if new_password == confirmed_password:
                        user = AuthUser.objects.get(username=username)
                        user.password = make_password(new_password)
                        user.save()
                        json_dict['errcode'] = '200'
                        json_dict['errmsg'] = '修改成功'
                    else:
                        json_dict['errcode'] = '103'
                        json_dict['errmsg'] = '两次输入的密码不一致'
            else:
                json_dict['errcode'] = '102'
                json_dict['errmsg'] = '密码不能为空'
            return JsonResponse(json_dict, safe=False)

def updateEphone(request):
    json_dict = {'errcode': 403, 'errmsg': None, 'user': None}
    try:
        request.session['id']
    except KeyError:
        json_dict['errmsg'] = '你干嘛，嗨嗨哟!'
    else:
        if request.method == 'POST':
            username = request.session['username']
            user = AuthUser.objects.filter(username=username)
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            new_email = request.POST.get('new_email', '')
            new_phone = request.POST.get('new_phone', '')

            if new_phone != '' and new_email != '':
                if not phone == user[0].phone or not email == user[0].email:
                    json_dict['errmsg'] = '原电话或邮箱错误'
                else:
                        user = AuthUser.objects.get(username=username)
                        user.email = new_email
                        user.phone = new_phone
                        user.save()
                        json_dict['errcode'] = '200'
                        json_dict['errmsg'] = '修改成功'
            else:
                json_dict['errcode'] = '102'
                json_dict['errmsg'] = '电话或邮箱不能为空'
            return JsonResponse(json_dict, safe=False)


import openai
openai.api_base = "https://api.chatanywhere.com.cn/v1"
openai.api_key = "apikey"


def completion(prompt):
    null = None
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
        }
    getUrl = 'https://api.chatanywhere.com.cn/v1/chat/completions'
    getResponse = eval(requests.post(getUrl,headers={"Authorization":"Bearer apikey","Content-Type":"application/json"},data=json.dumps(data)).text)
    return getResponse

def getAnswer(request):
    json_dict = {'errcode':200,'errmsg':'success','answerData':''}
    try:
        request.session['id']
    except KeyError:
        json_dict['errcode'] = 403
        json_dict['errmsg'] = '你干嘛，嗨嗨哟!'
    else:
        null = None
        question = request.GET.get('question',default='')
        if question == '':
            json_dict['errcode'] = 404
            json_dict['errmsg'] = '请输入你的问题'
        else:
            json_dict['answerData'] = completion(question)
    return JsonResponse(json_dict,safe=False)

