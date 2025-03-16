from django.shortcuts import render,redirect
from .models import registration as register
from .forms import *
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as user_login
from django.contrib.auth import logout as log_out
from store.models import product as Product
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
# Create your views here.

def registration(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            con_password = form.cleaned_data['con_password']

            username = email.split("@")[0]

            user = register.objects.create_user(firstname=firstname,lastname=lastname,email=email,phone=phone,username=username,password=password)
            user.save()
            messages.success(request,"You have Register Success,please cheak out your email.")

            try:
                email_subject = "Please Active your Email"
                current_side = get_current_site(request)

                context = {
                    'user':user,
                    'domain':current_side,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':default_token_generator.make_token(user),
                }
                message = render_to_string('account/verification.html',context)
                send_email = EmailMessage(email_subject,message,to=[email])
                send_email.content_subtype = "html"
                send_email.send()
            except Exception as e:
                print("Error while sending email:",e)

            return redirect(f'/account/login/?command=verification&email='+email)
        
        else:
            return redirect('registration')
        
    else:
        form = RegisterForm()

    context = {
        'form':form,
    }
    return render(request,'account/registration.html',context)

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request,email=email,password=password)

            if user is not None:
                user_login(request,user)
                next_url = request.GET.get('next','index')
                messages.success(request,"you have login success.")
                return redirect(next_url)
            else:
                messages.error(request,"Wrong Email And Password.")
                return redirect('login')

    form = LoginForm()
    return render(request,'account/login.html',{'form':form})

def verification(request,uid64,token):
    try:
        userid = urlsafe_base64_decode(uid64).decode()
        user = register._default_manager.get(id=userid)
        tokens = default_token_generator.check_token(user,token)
    except:
        user = None

    if user is not None and tokens:
        user.is_active = True
        user.save()
        messages.success(request,"Your account has been activated successfully! Please log in.")
        return redirect('login')
    else:
        messages.error(request,"Invalid activation link! Please register again.")
        return redirect('registration')
    
def logout(request):
    log_out(request)
    messages.success(request,"You have logout successfully.")
    return redirect('login')

def Contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('Contact')
    else:
        form = ContactForm()

    context = {
        'form': form,
        'support_email': 'yash@gmail.com',
    }
    return render(request,'account/contact.html',context)

@login_required(login_url='login')
def my_products(request):
    products = Product.objects.filter(seller=request.user)
    return render(request,'account/my_product.html',{'products':products})

@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request,'account/profile.html',{'form':form})

@login_required(login_url='login')  # Make sure login URL is correct
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']
            
            user = request.user  # This should be your `registration` instance

            # Verify current password
            if not user.check_password(current_password):
                form.add_error('current_password', 'Current password is incorrect.')
            else:
                # Set and save new password
                user.set_password(new_password)
                user.save()

                # Keep user logged in after password change
                update_session_auth_hash(request, user)

                messages.success(request, 'Password changed successfully!')
                return redirect('profile')  # Redirect to profile or dashboard
    else:
        form = CustomPasswordChangeForm()

    return render(request, 'account/change_password.html', {'form': form})