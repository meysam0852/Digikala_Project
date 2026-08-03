from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('products:landing')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'خوش آمدید {user.username}')
            return redirect('products:landing')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('products:landing')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'خوش آمدید {user.username}')
                return redirect('products:landing')
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
        else:
            form = LoginForm()

        return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'از حساب کاربری خود خارج شدید.')
    return redirect('products:landing')

@login_required
def profile_view(request):
    user = request.user
    is_seller = hasattr(user, 'seller_profile')
    customer_profile = user.customer_profile
    context = {
        'user': user,
        'is_seller': is_seller,
        'customer_profile': customer_profile,
    }
    return render(request, 'accounts/profile.html', context)

