from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

@login_required
def payment_page(request):
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        
        if amount:
            try:
                amount = int(amount)
                
                if amount > 0:
                    with transaction.atomic():
                        profile = request.user.customer_profile
                        profile.balance += amount
                        profile.save()
                    
                    messages.success(
                        request, 
                        f'موجودی شما به میزان {amount:,} تومان افزایش یافت.'
                    )
                else:
                    messages.error(request, 'مبلغ باید مثبت باشد.')
                    
            except ValueError:
                messages.error(request, 'مبلغ نامعتبر است.')
        else:
            messages.error(request, 'لطفاً مبلغ را وارد کنید.')
        
        return redirect('accounts:profile')
    
    balance = 0
    if hasattr(request.user, 'customer_profile'):
        balance = request.user.customer_profile.balance
    
    context = {
        'balance': balance,
    }
    
    return render(request, 'payments/payment.html', context)
