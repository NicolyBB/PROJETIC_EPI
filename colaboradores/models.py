from django.db import models

class Colaborador(models.Model):

    nome_completo = models.CharField(max_length=150)
    
    # Define um campo 'matricula'.
    # models.CharField armazena o matricula como texto.
    #   - unique=True: [IMPORTANTE] Garante que não possam existir dois colaboradores 
    #     com o mesmo matricula no banco de dados. O banco aplicará uma restrição UNIQUE.
    matricula = models.CharField(unique=True)
    
    # Define um campo 'funcao'.
    # models.CharField para armazenar a função/cargo do colaborador.
    funcao = models.CharField(max_length=50)

    # [BOA PRÁTICA] Define uma lista de tuplas para as opções do campo 'status'.
    # Cada tupla contém: (valor_armazenado_no_banco, valor_exibido_para_usuario).
    # Isso melhora a consistência e facilita a manutenção.
    STATUS_CHOICES = [
        ('Ativo', 'Ativo'),
        ('Inativo', 'Inativo'),
    ]
    # Define um campo 'status'.
    # models.CharField para armazenar o status.
    #   - max_length=10: Tamanho suficiente para 'Ativo' ou 'Inativo'.
    #   - choices=STATUS_CHOICES: Vincula este campo às opções definidas acima. 
    #     No Django Admin e em ModelForms, isso renderizará um campo <select> automaticamente.
    #   - default='Ativo': Define o valor padrão para este campo se nenhum valor for 
    #     fornecido ao criar um novo Colaborador.
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Ativo')

    # Define um campo 'data_cadastro'.
    # models.DateTimeField armazena data e hora.
    #   - auto_now_add=True: [IMPORTANTE] Faz com que o Django preencha automaticamente 
    #     este campo com a data e hora exatas do momento em que o objeto Colaborador 
    #     é CRIADO pela primeira vez. O campo não será atualizado depois.
    data_cadastro = models.DateTimeField(auto_now_add=True)

    # [BOA PRÁTICA] Define o método especial '__str__'.
    # Este método retorna uma representação em string "legível" do objeto Colaborador.
    # É o que o Django Admin (e outras partes do Django) usa para exibir o objeto.
    # Aqui, ele retorna o nome completo do colaborador.
    def __str__(self):
        return self.nome_completo