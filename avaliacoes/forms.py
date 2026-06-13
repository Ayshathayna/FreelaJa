from django import forms
from .models import AvaliaVaga, AvaliaFreelancer


class AvaliaVagaForm(forms.ModelForm):

    class Meta:
        model = AvaliaVaga

        fields = [  # campos que aparecerão no formulário
            'nota',
            'comentario'
        ]

        widgets = {   # customização dos campos do formulário

            'nota': forms.RadioSelect(   # para exibir as opções como botões de rádio
                choices=[
                    
                    (1, '1'),
                    (2, '2'),
                    (3, '3'),
                    (4, '4'),
                    (5, '5')
                ]
            ),

            'comentario': forms.Textarea(    # para exibir o campo de comentário como uma área de texto
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Conte como foi sua experiência...',
                    'rows': 6  
                }
            )
        }

        labels = {  
            'nota': 'Avaliação',
            'comentario': 'Comentário'
        }
class AvaliaFreelancerForm(forms.ModelForm):

    class Meta:
        model = AvaliaFreelancer

        fields = [  # campos que aparecerão no formulário
            'nota',
            'comentario'
        ]

        widgets = {   # customização dos campos do formulário

            'nota': forms.RadioSelect(   # para exibir as opções como botões de rádio
                choices=[
                    (1, '1'),
                    (2, '2'),
                    (3, '3'),
                    (4, '4'),
                    (5, '5')
                ]
            ),

            'comentario': forms.Textarea(    # para exibir o campo de comentário como uma área de texto
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Conte como foi sua experiência...',
                    'rows': 6  
                }
            )
        }

        labels = {  
            'nota': 'Avaliação',
            'comentario': 'Comentário'
        }