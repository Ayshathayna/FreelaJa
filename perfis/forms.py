from django import forms
from django.contrib.auth.hashers import make_password

from perfis.models import Freelancer, Empresa


class PerfilFreelancerForm(forms.ModelForm):

    email = forms.EmailField()

    nova_senha = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "id": "id_nova_senha"
            }
        )
    )

    confirmar_senha = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "id": "id_confirmar_senha"
            }
        )
    )
    interesses = forms.MultipleChoiceField(
        required=False,
        choices=Freelancer.INTERESSES,
        widget=forms.CheckboxSelectMultiple
    )
    interesses_texto = forms.CharField(
        required=False
    )
    foto = forms.ImageField(
        required=False,
        label="",
        widget=forms.FileInput(
            attrs={
                "id": "id_foto",
                "class": "hidden-input"
            }
        )
    )
    class Meta:

        model = Freelancer

        fields = [
            'foto',
            'nomeCompleto',
            'experiencia'        
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['email'].initial = (
            self.instance.usuario.email
        )

        self.fields['interesses'].initial = (
            self.instance.interesses
        )
    def clean_interesses(self):

        interesses = self.cleaned_data.get(
            'interesses',
            []
        )

        if len(interesses) < 3:

            raise forms.ValidationError(
                'Selecione pelo menos 3 interesses.'
            )

        if len(interesses) > 5:

            raise forms.ValidationError(
                'Selecione no máximo 5 interesses.'
            )

        return interesses
    def save(self, commit=True):

        freelancer = super().save(commit=False)

        freelancer.interesses = self.cleaned_data[ 'interesses'  ]

        usuario = freelancer.usuario

        usuario.email = self.cleaned_data['email']
        usuario.username = self.cleaned_data['email']

        senha = self.cleaned_data.get(
            'nova_senha'
        )

        if senha:

            usuario.password = make_password(
                senha
            )

        if commit:

            usuario.save()
            freelancer.save()

        return freelancer
    

class PerfilEmpresaForm(forms.ModelForm):

    email = forms.EmailField()

    nova_senha = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "id": "id_nova_senha"
            }
        )
    )

    confirmar_senha = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "id": "id_confirmar_senha"
            }
        )
    )

    foto = forms.ImageField(
        required=False,
        label="",
        widget=forms.FileInput(
            attrs={
                "id": "id_foto",
                "class": "hidden-input"
            }
        )
    )

    class Meta:

        model = Empresa

        fields = [
            "foto",
            "nomeFantasia",
            "descricao",
            "site"
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["email"].initial = (
            self.instance.usuario.email
        )

    def save(self, commit=True):

        empresa = super().save(commit=False)

        usuario = empresa.usuario

        usuario.email = self.cleaned_data["email"]
        usuario.username = self.cleaned_data["email"]

        senha = self.cleaned_data.get(
            "nova_senha"
        )

        if senha:

            usuario.password = make_password(
                senha
            )

        if commit:

            usuario.save()
            empresa.save()

        return empresa