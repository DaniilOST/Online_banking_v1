from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, AccountCreateForm, TransferFundsForm
from django.contrib.auth.decorators import login_required
from .utils import convert_currency, get_conversion_rate
from .services import TransferFunds
from .models import Client
from .models import Account
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Вы успешно вошли!')
            return redirect('online_banking:account') 
        else:
            messages.error(request, 'Ошибка входа: неверное имя пользователя или пароль.')

    return render(request, 'online_banking/login.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('online_banking:account')  
        else:
            messages.error(request, 'Ошибка при регистрации. Проверьте введенные данные.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'online_banking/register.html', {'form': form})

def home(request):
    return render(request, 'online_banking/index.html')

@login_required
def account(request):
    return render(request, 'online_banking/account.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли.')
    return redirect('online_banking:home')  

@login_required
def create_account(request):
    try:
        client = request.user.client
    except Client.DoesNotExist:
        messages.error(request, 'Ваш аккаунт не привязан к клиенту. Обратитесь к администратору.')
        return redirect('online_banking:account')

    if request.method == 'POST':
        form = AccountCreateForm(request.POST)
        if form.is_valid():
            try:
                account = form.save(commit=False)
                account.client = client
                account.save()
                form.save_m2m()  
                messages.success(request, 'Счет успешно создан!')
                return redirect('online_banking:account')
            except Exception as e:
                messages.error(request, f'Ошибка при создании счета: {e}')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = AccountCreateForm()

    return render(request, 'online_banking/create_account.html', {'form': form})


@login_required
def transfer_funds(request):
    if request.method == 'POST':
        form = TransferFundsForm(request.POST)
        if form.is_valid():
            from_account = form.cleaned_data['from_account']
            to_account = form.cleaned_data['to_account']
            amount = form.cleaned_data['amount']
            
            try:
                from_account = Account.objects.get(account_number=from_account.account_number)
                to_account = Account.objects.get(account_number=to_account.account_number)
                print("Счета найдены:", from_account, to_account)  
            except Account.DoesNotExist:
                messages.error(request, 'Указанный счет не найден.')
                return redirect('online_banking:transfer_funds')

            from_currency = from_account.currencies.first()
            to_currency = to_account.currencies.first()
            if from_currency != to_currency:
                amount = convert_currency(amount, from_currency, to_currency)

            try:
                TransferFunds(from_account.id, to_account.id, amount, from_currency.name, to_currency.name)
                messages.success(request, 'Перевод выполнен успешно.')
            except ValueError as e:
                messages.error(request, f'Ошибка при переводе: {str(e)}')

            return redirect('online_banking:account')
        else:
            print("Форма невалидна:", form.errors) 
            messages.error(request, 'Ошибка при заполнении формы.')
    else:
        form = TransferFundsForm()
    return render(request, 'online_banking/transfer_funds.html', {'form': form})
