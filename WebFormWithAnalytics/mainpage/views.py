from django.shortcuts import render
from decimal import Decimal
from expenses_and_incomes.models import Transaction

def home_view(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')
    current_balance = transactions.first().total_balance if transactions.exists() else Decimal('0.00')

    context = {
        'user': request.user,
        'total_balance': current_balance,
    }
    return render(request, 'main_page.html', context)