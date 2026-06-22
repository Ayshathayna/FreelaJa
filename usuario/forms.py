from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from .models import Usuario
from perfis.models import Freelancer, Empresa
from django.contrib.auth.hashers import make_password


class LoginForm(AuthenticationForm):

    username = forms.CharField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Digite seu email'
        })
    )

    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite sua senha',
            'id': 'id_password'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-field'
            })




# *********************************************************************************** FREELANCER

class CadastroFreelancerForm(forms.Form):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Digite seu email'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite sua senha',
            'id': 'id_password_freelancer'
        })
    )

    confirmar_senha = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme sua senha',
            'id': 'id_confirmar_senha_freelancer'
        })
    )

    nomeCompleto = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome completo'
        })
    )

    cpf = forms.CharField(
        max_length=14,
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite somente os números'
        })
    )

    dataNascimento = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date'
        })
    )

    celular = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': '(00) 00000-0000'
        })
    )

    interesses = forms.MultipleChoiceField(
        choices=Freelancer.INTERESSES,
        required=True,
        widget=forms.CheckboxSelectMultiple
    )

    experiencia = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Conte um pouco sobre sua experiência (opcional)'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-field'
            })

    def clean_email(self):
        email = self.cleaned_data['email']

        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Já existe um usuário com este email.'
            )

        return email

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']

        cpf_limpo = ''.join(filter(str.isdigit, cpf))

        if len(cpf_limpo) != 11:
            raise forms.ValidationError(
                'CPF deve possuir 11 números.'
            )

        if Freelancer.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError(
                'CPF já cadastrado.'
            )

        return cpf

    def clean(self):
        cleaned_data = super().clean()

        senha = cleaned_data.get('password')
        confirmar = cleaned_data.get('confirmar_senha')

        if senha and confirmar and senha != confirmar:
            raise forms.ValidationError(
                'As senhas não coincidem.'
            )
        interesses = cleaned_data.get('interesses')

        if interesses:

            if len(interesses) < 3:
                raise forms.ValidationError(
                    'Escolha pelo menos 3 interesses.'
                )

            if len(interesses) > 5:
                raise forms.ValidationError(
                    'Escolha no máximo 5 interesses.'
                )

        return cleaned_data

    def save(self):

        with transaction.atomic():

            usuario = Usuario.objects.create_user(
                username=self.cleaned_data['email'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],
                tipo_usuario='freelancer'
            )

            freelancer = Freelancer.objects.create(
                usuario=usuario,
                nomeCompleto=self.cleaned_data['nomeCompleto'],
                cpf=self.cleaned_data['cpf'],
                dataNascimento=self.cleaned_data['dataNascimento'],
                celular=self.cleaned_data['celular'],
                experiencia=self.cleaned_data['experiencia'],
                interesses=self.cleaned_data['interesses']
            )

        return freelancer


# ************************************************************************  EMPRESA


class CadastroEmpresaForm(forms.Form):

    nomeFantasia = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome fantasia'
        })
    )

    cnpj = forms.CharField(
        max_length=18,
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite somente os números'
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Digite seu email'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite sua senha',
            'id': 'id_password_empresa'
        })
    )

    confirmar_senha = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme sua senha',
            'id': 'id_confirmar_senha_empresa'
        })
    )

   

    site = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'seusite.com.br'
        })
    )

    descricao = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Descreva sua empresa'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-field'
            })

    def clean_email(self):
        email = self.cleaned_data['email']

        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Já existe um usuário com este email.'
            )

        return email

    def clean_cnpj(self):

        cnpj = self.cleaned_data['cnpj']

        cnpj_limpo = ''.join(filter(str.isdigit, cnpj))

        if len(cnpj_limpo) != 14:
            raise forms.ValidationError(
                'CNPJ deve possuir 14 números.'
            )

        if Empresa.objects.filter(cnpj=cnpj).exists():
            raise forms.ValidationError(
                'CNPJ já cadastrado.'
            )

        return cnpj

    def clean(self):
        cleaned_data = super().clean()

        senha = cleaned_data.get('password')
        confirmar = cleaned_data.get('confirmar_senha')

        if senha and confirmar and senha != confirmar:
            raise forms.ValidationError(
                'As senhas não coincidem.'
            )

        return cleaned_data

    def save(self):

        with transaction.atomic():

            usuario = Usuario.objects.create_user(
                username=self.cleaned_data['email'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],
                tipo_usuario='empresa'
            )
            empresa = Empresa.objects.create(
                usuario=usuario,
                nomeFantasia=self.cleaned_data['nomeFantasia'],
                cnpj=self.cleaned_data['cnpj'],
                descricao=self.cleaned_data['descricao'],
                site=self.cleaned_data['site']
            )

        return empresa