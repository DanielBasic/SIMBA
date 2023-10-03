from django import forms
from django.contrib.auth.models import User  #importa o modelo Usuario
from django.contrib.auth.forms import UserCreationForm  #importa a criação do usuario


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            # 'first_name',
            # 'last_name',
            'password1',
            'password2',
        ]

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email já está sendo usado por outra conta.')
        return email
        