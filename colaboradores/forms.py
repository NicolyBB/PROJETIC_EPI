# Importa o módulo 'forms' do Django
from django import forms
# Importa o modelo 'Colaborador'
from .models import Colaborador

# Define o formulário com base no modelo
class ColaboradorForm(forms.ModelForm):
    
    # A classe interna 'Meta' diz ao Django como o formulário deve funcionar
    class Meta:
        # 1. ASSOCIAR AO MODELO
        model = Colaborador
        
        # 2. DEFINIR OS CAMPOS (com 'matricula' em vez de 'cpf')
        fields = ['nome_completo', 'matricula', 'funcao', 'status']

        # 3. DEFINIR OS ATRIBUTOS HTML (Widgets)
        #    (Este é o jeito mais limpo de fazer o que você tinha no __init__)
        widgets = {
            'nome_completo': forms.TextInput(attrs={
                'id': 'nome_completo', # É melhor usar o nome do campo como ID
                'placeholder': 'Digite o nome completo',
                'class': 'form-control' # (Se você estivesse usando Bootstrap)
            }),
            'matricula': forms.TextInput(attrs={
                'id': 'matricula', 
                'placeholder': 'Digite a matrícula (apenas números)',
                'inputmode': 'numeric' # Ajuda em teclados de celular
            }),
            'funcao': forms.TextInput(attrs={
                'id': 'funcao', 
                'placeholder': 'Selecione ou digite a função', 
                'list': 'lista-funcoes' # Para autocompletar
            }),
            'status': forms.Select(attrs={
                'id': 'status'
            }),
        }

    # 4. MÉTODO DE VALIDAÇÃO PERSONALIZADA PARA A MATRÍCULA
    #    (Este método é executado automaticamente pelo form.is_valid())
    def clean_matricula(self):
        # Pega o dado "cru" do campo matricula
        matricula = self.cleaned_data.get('matricula')
        
        # Validação 1: Garante que sejam APENAS números (sem limite de tamanho)
        if not matricula.isdigit():
            # Se falhar, envia este erro para o formulário
            raise forms.ValidationError("A matrícula deve conter apenas números.")

        # Validação 2: Verifica se a matrícula já existe no banco
        # 'self.instance' é o objeto que está sendo editado (ou None se for novo)
        queryset = Colaborador.objects.filter(matricula=matricula)
        
        # Se estamos editando (self.instance.pk existe), excluímos o 
        # próprio colaborador da busca por duplicatas
        if self.instance and self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
            
        # Se, mesmo assim, a busca encontrou alguém...
        if queryset.exists():
            # Envia este erro
            raise forms.ValidationError("ERRO: Esta matrícula já está cadastrada.")

        # Se passou em tudo, retorna o valor limpo (só números)
        return matricula