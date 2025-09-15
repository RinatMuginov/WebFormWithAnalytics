from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Category, Transaction
from decimal import Decimal


def expenses_and_incomes(request):
    if request.method == 'POST':
        # 🔹 Проверка: удаление транзакции
        delete_id = request.POST.get('delete_transaction_id')
        if delete_id:
            try:
                transaction = Transaction.objects.get(pk=delete_id, user=request.user)
                transaction.delete()

                # 🔹 Пересчёт баланса после удаления
                transactions = Transaction.objects.filter(user=request.user).order_by('created_at')
                balance = Decimal('0.00')
                for tr in transactions:
                    if tr.transaction_type == 'income':
                        balance += tr.amount
                    else:
                        balance -= tr.amount
                    tr.total_balance = balance
                    tr.save()

                messages.success(request, 'Транзакция удалена!')
            except Transaction.DoesNotExist:
                messages.error(request, 'Транзакция не найдена')
            return redirect('expenses_and_incomes')

        # 🔹 Добавление транзакции
        amount = request.POST.get('amount')
        category_id = request.POST.get('category')
        comment = request.POST.get('comment', '')
        ctype = request.POST.get('ctype')

        try:
            amount = Decimal(amount)
        except Exception:
            messages.error(request, 'Введите корректную сумму')
            return redirect('expenses_and_incomes')

        last_transaction = Transaction.objects.filter(user=request.user).order_by('-created_at').first()
        current_balance = last_transaction.total_balance if last_transaction else Decimal('0.00')

        if ctype == 'income':
            current_balance += amount
        else:
            current_balance -= amount

        try:
            category = Category.objects.get(pk=category_id, type=ctype)
        except Category.DoesNotExist:
            messages.error(request, 'Неверная категория')
            return redirect('expenses_and_incomes')

        Transaction.objects.create(
            user=request.user,
            category=category,
            amount=amount,
            comment=comment,
            transaction_type=ctype,
            total_balance=current_balance
        )
        messages.success(request, 'Операция добавлена!')
        return redirect('expenses_and_incomes')

    # 🔹 Данные для отображения
    income_categories = Category.objects.filter(type='income')
    expense_categories = Category.objects.filter(type='expense')
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')

    if transactions.exists():
        current_balance = transactions.first().total_balance
    else:
        current_balance = Decimal('0.00')

    print("DEBUG BALANCE:", current_balance)

    return render(request, 'expenses_and_incomes.html', {
        'income_categories': income_categories,
        'expense_categories': expense_categories,
        'transactions': transactions,
        'total_balance': current_balance,
    })
