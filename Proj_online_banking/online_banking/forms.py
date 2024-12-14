from django import forms
from django.contrib.auth.models import User
from .models import Account, Client

class CustomUserCreationForm(forms.ModelForm):
    client_name = forms.CharField(max_length=100, required=True, help_text='Введите ваше имя.')
    client_email = forms.EmailField(max_length=254, required=True, help_text='Введите ваш email.')
    client_phone = forms.CharField(max_length=20, required=True, help_text='Введите ваш телефон.')
    client_address = forms.CharField(max_length=255, required=True, help_text='Введите ваш адрес.')

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'client_name', 'client_email', 'client_phone', 'client_address', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            Client.objects.create(
                user=user,
                client_name=self.cleaned_data['client_name'],
                client_email=self.cleaned_data['client_email'],
                client_phone=self.cleaned_data['client_phone'],
                client_address=self.cleaned_data['client_address']
            )
        return user


class AccountCreateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_type', 'currencies']
        widgets = {
            'currencies': forms.CheckboxSelectMultiple
        }

    def save(self, commit=True, client=None):
        # Автогенерация account_number
        import random
        account_number = f'ACC{random.randint(10000, 99999)}'
        
        instance = super().save(commit=False)
        instance.account_number = account_number
        
        if client:
            instance.client = client
        
        if commit:
            instance.save()
            self.save_m2m()
        
        return instance

class TransferFundsForm(forms.Form):
    from_account = forms.ModelChoiceField(queryset=Account.objects.all(), label="Со счета")
    to_account = forms.ModelChoiceField(queryset=Account.objects.all(), label="На счет")
    amount = forms.DecimalField(max_digits=15, decimal_places=2, label="Сумма", min_value=0.01)
