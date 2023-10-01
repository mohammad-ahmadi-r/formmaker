from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.http import HttpResponse
from .models import Token
from django.core.mail import send_mail
import smtplib
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
smtp_server.ehlo()
smtp_server.login(gmail_user, gmail_password)
import smtplib
from django.urls import reverse



def register(request):
    if request.method == "POST":
        '''if User.objects.filter(email=request.POST['email']).exists():
            context = {
                'message': 'This email is already in use'}
            return render(request, 'atent/register.html', context)
        else:'''
        nuser = User.objects.create_user(username = request.POST["username"] , password = request.POST["password"] , email = request.POST["email"])
        token = Token(user_id=User.objects.get(username=nuser.username).id , type=0)
        token.save()
        t = Token.objects.get(user_id=User.objects.get(username=nuser.username).id , type=0)
#        send_mail("Verify yor account" , f"here : <a href = 'http://localhost:8000/auth/verify/{t.id}'></a>" , gmail_user, [nuser.email] ,fail_silently=False)
        try:
            #Create your SMTP session
            smtp = smtplib.SMTP('smtp.gmail.com', 587)

           #Use TLS to add security
            smtp.starttls()

            #User Authentication
            smtp.login(gmail_user,gmail_password)

            #Defining The Message
            message = """From: From Person <"example@gmail.com">
            To: To Person <user@gmail.com>
            Subject: SMTP e-mail test

            http://localhost:8000/auth/verify/{num}
            """

#            message = f'http://localhost:8000/auth/verify/{t.id}'

            #Sending the Email
            smtp.sendmail(gmail_user, nuser.email , message.format(num = t.id))

            #Terminating the session
            smtp.quit()
            context = {'message': "Please check your mailbox to VERIFY your email"}
            return render(request, 'atent/login.html', context)
#            return HttpResponseRedirect(reverse('create'))
        except Exception as ex:
            return HttpResponse("Something went wrong....",ex)
        return HttpResponse("Hello!pls check your email")
    else:
        return render(request ,"atent/register.html")


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        user = authenticate(request , username = request.POST["username"] , password = request.POST["password"])
        if user is not None:
            try:
                Token.objects.get(user_id=user.id , type=0)
                context = {'message': "please check your email to verify your account"}
                return render(request, 'atent/login.html', context)
            except:
                pass
            login(request , user)
            return HttpResponseRedirect(reverse('index'))

        context = {'message': "Invalid Username or Password"}
        return render(request, 'atent/login.html', context)
    else:
        return render(request ,"atent/login.html")
def logout_view(request):
    logout(request)
    return render(request ,"dashbord/index.html")

def verify(request , token):
    try:
        Token.objects.get(id=token).delete()
        context = {'message': "You successfully verified your account! login please"}
        return render(request, 'atent/login.html', context)
    except:
        context = {'message': "Please verify your email"}
        return render(request, 'atent/login.html', context)


def forgot_password(request):

    if request.method == "POST":
        try:
            user = User.objects.get(username=request.POST["username"])
        except:
            try:
                euser = User.objects.get(email=request.POST["username"])
            except:
                return HttpResponse("No such user")
        Token(user_id=user.id, type=1).save()
        t = Token.objects.filter(user_id=user.id, type=1)[::-1][0]
        try:
            smtp = smtplib.SMTP('smtp.gmail.com', 587)
            smtp.starttls()
            smtp.login(gmail_user,gmail_password)
            message = """From: From Person <"example@gmail.com">
            To: To Person <user@gmail.com>
            Subject: SMTP e-mail test

            http://localhost:8000/auth/reset-password/{num}
            """
            smtp.sendmail(gmail_user, user.email , message.format(num = t.id))
            smtp.quit()
            context = {
                'message': "Please check your email for next step."}
            return render(request, 'dashbord/index.html', context)
        except Exception as ex:
            return HttpResponse("Something went wrong....",ex)
    else:
        return render(request, "atent/forgot-password.html")


def reset_password(request, token):
    if request.method == "POST":
        t = Token.objects.get(id=token, type=1)
        user = User.objects.get(id=t.user_id)
        user.set_password(request.POST["password"])
        user.save()
        t.delete()
        return HttpResponse("Password updated successfully")
    else:
        try:
            t = Token.objects.get(id=token, type=1)
            return render(request, "atent/reset-password.html", {
                "username": User.objects.get(id=t.user_id).username
            })
        except:
            return HttpResponse("Sorry, your token not found.")
