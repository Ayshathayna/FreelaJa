from django import forms
from .models import Vaga
from datetime import date


class VagaForm(forms.ModelForm):

    class Meta:
        model = Vaga

        fields = [  # campos do formulário
            'imagem',
            'titulo',
            'descricao',
            'quantidadeVagas',
            'dataEvento',
            'horarioInicio',
            'horarioFim',
            'endereco',
            'remuneracao',
            'status'
        ]
        widgets = {   #widgets para estilizar os campos do formulário
            'titulo': forms.TextInput(
                attrs={
                    'class': 'form-input',
                    'placeholder': 'Título da vaga',
                    'required': True
                }
            ),

            'descricao': forms.Textarea(
                attrs={
                    'class': 'form-input',
                    'rows': 5,
                    'placeholder': 'Descrição da vaga',
                    'required': True

                }
            ),

            'quantidadeVagas': forms.NumberInput(
                attrs={
                    'class': 'form-input',
                    'required': True
                }
            ),

            'dataEvento': forms.DateInput(
                attrs={
                    'class': 'form-input',
                    'type': 'date',
                    'required': True
                }
            ),

            'horarioInicio': forms.TimeInput(
                attrs={
                    'class': 'form-input',
                    'type': 'time',
                    'required': True
                }
            ),

            'horarioFim': forms.TimeInput(
                attrs={
                    'class': 'form-input',
                    'type': 'time',
                    'required': True
                }
            ),

            'endereco': forms.TextInput(
                attrs={
                    'class': 'form-input',
                    'placeholder': 'Endereço',
                    'required': True
                }
            ),

            'remuneracao': forms.NumberInput(
                attrs={
                    'class': 'form-input',
                    'step': '0.01',
                    'required': True
                }
            ),

            'status': forms.Select(
                attrs={
                    'class': 'form-input',
                    'required': True
                }
            ),
        }
        
    def clean(self): #método clean() é usado para validar os dados do formulário. Ele é chamado automaticamente quando o formulário é submetido e permite que você adicione validações personalizadas para os campos do formulário.

        cleanedData = super().clean()  #chama o método clean() da classe pai (forms.ModelForm) para garantir que as validações padrão sejam executadas antes de adicionar as validações personalizadas.

        inicio = cleanedData.get('horarioInicio')
        fim = cleanedData.get('horarioFim')
        dataEvento = cleanedData.get('dataEvento')
        qtd = cleanedData.get('quantidadeVagas')
        remuneracao = cleanedData.get('remuneracao')


        if inicio and fim:  #verifica se os campos de horário de início e fim foram preenchidos. Compara os horários para garantir que o horário de fim seja maior que o horário de início. 

            if fim <= inicio:

                raise forms.ValidationError(
                    "Horário final não pode ser anterior ao horário inicial."
                )

        if dataEvento: #verifica se o campo de data do evento foi preenchido. Compara a data do evento com a data atual para garantir que a data do evento não seja anterior à data atual. 

            if dataEvento < date.today():

                raise forms.ValidationError(
                    "A data do evento não pode ser anterior a hoje."
                )

        if qtd:

            if qtd < 0:

                raise forms.ValidationError(
                    "Quantidade de candidatos deve ser maior que zero."
                )

        if remuneracao:

            if remuneracao < 0:

                raise forms.ValidationError(
                    "Informe uma remuneração válida."
                )

        return cleanedData
    
