from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import User
import time
import random
from django.http import JsonResponse
import os
from django.contrib.auth import logout
from django.conf import settings

def main(request):
    username = request.session.get('username','未登录')
    usertoken = request.session.get('token')
    MemberRank = request.session.get('MemberRank',' ')
    MemberBlance = request.session.get('MemberBlance', '0')
    MemberIntegral = request.session.get('MemberIntegral', '0')
    loginstatus = request.session.get('loginstatus')

    if loginstatus==True:
        LoginViewstatus = '已登录'
        LoginOrLogout = '注销'    # 判断登录状态的文字，用于在main.html中显示
        flag = 0                 # 判断登录状态的数字，用于在main.html中做判断
    else:
        LoginViewstatus = '未登录'
        LoginOrLogout = '登录'
        flag = 1
    return render(request,'main.html',{'username':username, 'MemberRank':MemberRank,
                                       'MemberBlance':MemberBlance, 'MemberIntegral':MemberIntegral,
                                       'LoginViewstatus': LoginViewstatus,'LoginOrLogout': LoginOrLogout, 'flag':flag})

#验证码
def verifycode(request):
    from PIL import Image, ImageDraw, ImageFont
    import random
    #图片背景颜色
    bgcolor = (random.randrange(20,100),random.randrange(20,100),random.randrange(20,100))
    width = 80
    height = 34
    #创建画面对象
    im = Image.new('RGB',(width,height),bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0,100):
        xy = (random.randrange(0,width),random.randrange(0,height))
        fill = (random.randrange(0,255),255,random.randrange(0,255))
        draw.point(xy,fill=fill)
    #定义验证码备选值
    str='1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    #随机取其中4个值作为验证码
    rand_str = ''
    for i in range(0,4):
        rand_str += str[random.randrange(0,len(str))]
    #构造字体对象
    font = ImageFont.truetype(r'C:\Windows\Fonts\AdobeArabic-Bold.otf',30)
    #构造字体颜色
    fontcolor1 = (255,random.randrange(0,255),random.randrange(0,255))
    fontcolor2 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor3 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor4 = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((8, 2), rand_str[0], font=font, fill=fontcolor1)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor2)
    draw.text((40, 2), rand_str[2], font=font, fill=fontcolor3)
    draw.text((58, 2), rand_str[3], font=font, fill=fontcolor4)
    #释放画笔
    del draw
    #将随机生成的验证码存入session中
    request.session['verify'] = rand_str
    #内存文件操作
    import io

    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型png
    im.save(buf,'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片PNG
    return HttpResponse(buf.getvalue(),'image/png')

def regist(request):
   if request.method == 'POST':
        userphone = request.POST.get('userPhone')
        userpasswd = request.POST.get('userPass')

        verifycode1 = request.POST.get('verifycode').upper()
        verifycode2 = request.session.get('verify').upper()

        if len(str(userphone)) != 11 or\
           len(str(userpasswd)) < 6 or len(str(userpasswd))>16 or\
           verifycode1 != verifycode2:
           request.session['flag_VerifycodeIsRight'] = 1

           flag_VerifycodeIsRight = request.session.get('flag_VerifycodeIsRight', '0')
           print(flag_VerifycodeIsRight)
           return render(request,'regist.html',{'flag_VerifycodeIsRight':flag_VerifycodeIsRight})
        else:
            userrank = '黄金会员'
            userblance = 0
            userintergral = 0
            usercoupon = '无'
            userexpenses_record = '无'
            userloginstatus = True
            usertoken = str(time.time() + random.randrange(1,10000))

            user = User.createuser(userphone, userpasswd,userrank,userblance,
                                  userintergral, usercoupon,userexpenses_record,
                                   userloginstatus,usertoken )
            user.save()

            request.session['username'] = userphone
            request.session['token'] = usertoken
            request.session['loginstatus'] = user.userLoginStatus

            return redirect('/')
   else:
       return render(request, 'regist.html')
   print(flag_VerifycodeIsRight)
   return render(request,'regist.html',{'flag_VerifycodeIsRight':flag_VerifycodeIsRight})

def checkuserid(request):
    userid = request.POST.get('userid')

    try:
        user = User.objects.get(userPhone=userid)
        return JsonResponse({'data': '该用户已被注册', 'status': 'error'})
    except User.DoesNotExist as e:
        return JsonResponse({'data': 'ok', 'status': 'success'})

#注销
def quit(request):
    username = request.session.get('username', '登录')
    user = User.objects.get(userPhone=username)
    user.userLoginStatus = False
    request.session['loginstatus'] = user.userLoginStatus
    logout(request)
    print(user.userLoginStatus)
    return redirect('/')

#登录
from .forms import LoginForm
def login(request):
    if request.method == 'POST':
        f = LoginForm(request.POST)
        if f.is_valid():

            nameid = f.cleaned_data['userphone']
            passwd = f.cleaned_data['passwd']
            '''
            try:
                user = User.objects.get(userPhone=nameid)
                if user.userpasswd != passwd:
                    return redirect('/login/')
            except user.DoesNotExist as e:
                return redirect('/login/')
            '''
            user = User.objects.filter(userPhone=nameid, userpasswd = passwd)
            if user:
                user = User.objects.get(userPhone=nameid)
                user.userToken = time.time() + random.randrange(1,10000)
                user.userLoginStatus = True
                user.save()

                request.session['username'] = user.userPhone
                request.session['MemberRank'] = user.userRank
                request.session['MemberBlance'] = user.userBlance
                request.session['MemberIntegral'] = user.userIntegral
                request.session['loginstatus'] = user.userLoginStatus
                request.session['token'] = user.userToken
                print(user.userLoginStatus)

                return redirect('/')

            else:
                #传值——判断用户或密码是否正确，用于显示错误信息
                request.session['flag_userDoesNotExist'] = 1
                return redirect('/login/')
        else:
            return render(request, 'login.html', {'form': f, 'error':f.errors})
    else:
        f = LoginForm()
    flag_userDoesNotExist = request.session.get('flag_userDoesNotExist',0)
    print(flag_userDoesNotExist)
    return render(request,'login.html', {'form':f, 'flag_userDoesNotExist':flag_userDoesNotExist})

#忘记密码
def forgetpassword(request):

    if request.method == 'POST':
        userphone = request.POST.get('REuserPhone')
        userpasswd = request.POST.get('REuserPass')

        if len(str(userphone)) != 11 or \
                len(str(userpasswd)) < 6 or len(str(userpasswd)) > 16 :
            return render(request, 'forgetpassword.html')
        else:
            user = User.objects.get(userPhone = userphone)
            user.userpasswd = userpasswd
            user.userToken = str(time.time() + random.randrange(1, 10000))
            user.save()
            return redirect('/login/')

        return render(request, 'forgetpassword.html')
    else:
        return render(request, 'forgetpassword.html')

    return render(request, 'forgetpassword.html')

def forget_checkuserid(request):
    userid = request.POST.get('userid')

    try:
        user = User.objects.get(userPhone=userid)
        return JsonResponse({'data': 'ok', 'status': 'success'})
    except User.DoesNotExist as e:
        return JsonResponse({'data': '该用户未被注册', 'status': 'error'})