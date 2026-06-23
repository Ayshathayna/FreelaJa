from django import forms
from .models import Vaga
from datetime import date


class VagaForm(forms.ModelForm):
    DETALHES = [
        ("experiencia", "Experiência"),
        ("sem_experiencia", "Sem experiência"),
        ("comunicacao", "Comunicação"),
        ("lideranca", "Liderança"),
        ("atendimento_publico", "Atendimento ao público"),
        ("trabalho_equipe", "Trabalho em equipe"),
        ("disponibilidade_noturna", "Disponibilidade noturna"),
        ("freelancer", "Freelancer"),
        ("temporario", "Temporário"),
        ("presencial", "Presencial"),
        ("home_office", "Home Office"),
    ]

    detalhes = forms.MultipleChoiceField(
        choices=DETALHES,
        required=True,
        widget=forms.CheckboxSelectMultiple
    )
    detalhes_custom = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

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
            'latitude',
            'longitude',
            'remuneracao',
            'status',
            'categoria'
        ]
        widgets = {   #widgets para estilizar os campos do formulário
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'imagem': forms.FileInput(
                attrs={
                    "id": "id_foto",
                    "class": "hidden-input"
                }
            ),
                
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
            'categoria': forms.Select(
                attrs={
                    'class': 'form-input',
                    'required': True
                }
            )
            
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
        detalhes = cleanedData.get('detalhes')
        detalhes_custom = cleanedData.get('detalhes_custom')

        # parse custom list (separado por vírgula)
        custom_list = []
        if detalhes_custom:
            custom_list = [d.strip() for d in detalhes_custom.split(',') if d.strip()]

        # validações: no máximo 3 custom; total (selecionados + custom) entre 1 e 3
        if len(custom_list) > 3:
            raise forms.ValidationError("Você pode cadastrar no máximo 3 detalhes personalizados.")

        total = (len(detalhes) if detalhes else 0) + len(custom_list)
        if total > 3:
            raise forms.ValidationError("Selecione no máximo 3 detalhes no total (incluindo personalizados).")
        if total < 1:
            raise forms.ValidationError("Selecione pelo menos 1 detalhe.")

        return cleanedData

    def __init__(self, *args, **kwargs):
        # preenche valores iniciais para edição a partir de instancia.vaga.detalhes
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        if instance:
            detalhes_atual = instance.detalhes or []
            padrao_keys = dict(self.DETALHES).keys()
            selecionados = [d for d in detalhes_atual if d in padrao_keys]
            custom = [d for d in detalhes_atual if d not in padrao_keys]
            if selecionados:
                self.initial['detalhes'] = selecionados
            if custom:
                self.initial['detalhes_custom'] = ', '.join(custom)

    def save(self, commit=True):
        instance = super().save(commit=False)
        detalhes_selecionados = self.cleaned_data.get('detalhes') or []
        detalhes_custom = self.cleaned_data.get('detalhes_custom') or ''
        custom_list = [d.strip() for d in detalhes_custom.split(',') if d.strip()]
        instance.detalhes = list(detalhes_selecionados) + custom_list
        if commit:
            instance.save()
        return instance
    
