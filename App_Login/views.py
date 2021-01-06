from django.shortcuts import render,HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from App_Login.forms import RegistrationForm,ProfileForm
from django.contrib import messages
from App_Login.models import Profile,User

#custom mail
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import render_to_string
#activate
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator 
from .token import account_activation_token
from django.shortcuts import redirect
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# Create your views here.
def RegistrationView(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('App_Login:profile', ))
    else:
        form=RegistrationForm()
        if request.method=='POST':
            form=RegistrationForm(request.POST)
            if form.is_valid():
                user=form.save(commit=False)
                print(user)
                user.is_active=False 
                user.save()
                current_site=get_current_site(request)
                x=user
                print("user pk")
                print(user.pk)
                subject="Account Activation!"
                uid=urlsafe_base64_encode(force_bytes(user.pk))
                # token=(user)
                # print(token)
                # uid=
                print(uid)
                token=account_activation_token.make_token(user)
                
                print(token)
                # uid=urlsafe_base64_encode(force_bytes(user))
                message=render_to_string('activate.html',{
                    'user':user ,
                    'domain': current_site.domain,
                    'uid': uid,
                    'token':token,
                })
                email=EmailMessage(subject,message,to=[x])
                email.send()
                # login(request,user)
                # messages=messages(request,"Registration Successful")
                messages.success(request,"Registration Successful")
                messages.success(request,"Successfully email sent!")
                return HttpResponseRedirect(reverse('App_Login:profile', ))
            
    dict={'form':form}
    return render(request, 'App_Login/registration.html', context=dict)

def activate(request,uidbd64,token):
    try:
        uid=urlsafe_base64_decode(uidbd64).decode()
        user=User.objects.get(pk=uid)
        print(user)
        print(account_activation_token.check_token(user, token))
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    if user is not None and account_activation_token.check_token(user, token):
        user=request.user
        user.is_active=True
        # user.save()
        messages.success(request,"your account is activated.you can login now")
        return redirect('App_Login:login')
    else:
        messages.success(request,"invalid user")
        return redirect('App_Login:login')
    # return redirect('App_Login:login')

def LoginView(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('App_Login:profile', ))
    else:
        form=AuthenticationForm()
        if request.method=='POST':
            form=AuthenticationForm(data=request.POST)
            if form.is_valid():
                username=form.cleaned_data.get('username')
                password=form.cleaned_data.get('password')
                user=authenticate(username=username,password=password)
                if user is not None:
                    login(request,user)
                    messages.info(request,"Login Successfull")
                    return HttpResponseRedirect(reverse('App_Shop:home', ))
            
    dict={'form':form}
    return render(request, 'App_Login/login.html', context=dict)

@login_required
def LogoutView(request):
    logout(request)
    messages.warning(request,"Loged out user")
    return HttpResponseRedirect(reverse('App_Login:login', ))

@login_required
def ProfileView(request):
    current_user=Profile.objects.get(user=request.user)
    form=ProfileForm(instance=current_user)
    if request.method=='POST':
        form=ProfileForm(request.POST,instance=current_user)
        if form.is_valid():
            form.save()
            messages.success(request,"Profile Updated!")
            return HttpResponseRedirect(reverse('App_Login:profile', ))
    dict={'form':form}
    return render(request, 'App_Login/change_profile.html', context=dict)
    
            



    
    

