from django import forms
from django.contrib.auth.forms import AuthenticationForm
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
            'placeholder': 'Digite sua senha'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-field'
            })




# ==================================================
# FREELANCER
# ==================================================

class CadastroFreelancerForm(forms.Form):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Digite seu email'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite sua senha',
            'id': 'id_password'
        })
    )

    confirmar_senha = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme sua senha',
            'id': 'id_confirmar_senha'
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
            'placeholder': '000.000.000-00'
        })
    )

    area_atuacao = forms.ChoiceField(
        choices=Freelancer.AREAS
    )

    experiencia = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Conte um pouco sobre sua experiência'
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

        return cleaned_data

    def save(self):

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
            experiencia=self.cleaned_data['experiencia'],
            area_atuacao=self.cleaned_data['area_atuacao']
        )

        return freelancer


# ==================================================
# EMPRESA
# ==================================================

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
            'placeholder': '00.000.000/0000-00'
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
            'id': 'id_confirmar_empresa'
        })
    )

    telefone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '(00) 99999-9999'
        })
    )

    site = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://seusite.com.br'
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
            telefone=self.cleaned_data['telefone'],
            site=self.cleaned_data['site']
        )

        return empresa