from abc import ABC, abstractmethod
from datetime import datetime
import time

class Cliente:
    #Cria um objeto cliente com atributos endereco e contas

    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    #recebe os objetos conta e transacao e realiza o método registrar da Classe Transacao
    def realizar_transacao(self,conta, transacao):
        transacao.registrar(conta)

    #Recebe um objeto conta e o adiciona à lista contas
    def adicionar_conta(self,conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    #Cria um objeto Pessoa Fisica, tambem objeto da classe Cliente
    #Herda os atributos da classe Cliente e recebe nome, data_nascimento e cpf
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento 
        self.cpf = cpf
        



class Conta:
    #Cria um objeto Conta com atributos declarados internamente: _saldo,  _agencia, _historico, e atributos declarados externamente:  _numero e_cliente 
    def __init__(self, cliente, numero):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    #Método de classe que gera um cliente e retorna um cliente e número de conta 
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)
    
    #cria uma propriedade pública do atributo privado: _saldo
    @property
    def saldo(self):
        return self._saldo
    
    #cria uma propriedade pública do atributo privado: _numero
    @property
    def numero(self):
        return self._numero
    
    #cria uma propriedade pública do atributo privado: _agencia
    @property
    def agencia(self):
        return self._agencia
    
    #cria uma propriedade pública do atributo privado: _cliente
    @property
    def cliente(self):
        return self._cliente
    
    #cria uma propriedade pública do atributo privado:_historico
    @property
    def historico(self):
        return self._historico

    #Recebe um parâmetro, faz verificações internas, e em caso de True: retorna um valor True, do contrário, retorn False
    def sacar(self, valor):
        saldo = self.saldo
        saldo_insuficiente = saldo<valor
        if saldo_insuficiente:
            print('Saldo infuciciente ')
            
        elif valor>0:
            print('saque bem sucedido' )
            self._saldo-= valor
            return True
        else:
            print('Opção inválida')
        return False
        
    #Recebe um parâmetro, faz verificações internas, e em caso de True: retorna um valor True, do contrário, retorn False
    def depositar(self,valor):
        if valor>0:
            self._saldo += valor
            print('Depósito bem sucedido')
            
        else:
            print('Valor inválido')
            return False
        return True
        
    #Retorna um valor string para a representação dos atributos agencia, numero e cliente
    def __repr__(self):
        return f'''{'Agencia':<10}: {self.agencia:>20}
{'C/C':<10}: {self.numero:>20}
{'Titular':<10}: {self.cliente.nome:>20}
        '''
        


class ContaCorrente(Conta):
    #Cria um objeto conta corrente, filha de conta
    #recebe atributos limite e limite_saques, com valor já preenchidoo, mas com possibilidade de acesso externo para atualização
    def __init__(self, numero, cliente , limite = 500, limite_saques = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    #Recebe um atributo, faz verificação no número de transações do tipo: class <Saque>.__name__ registrada na lista de transações
    #Faz verificaçoes quanto ao limite de valor no saque
    #Quando dentro dos parâmetros, retorna para a função Pai, do contrario retorna False

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
        print(numero_saques)
        acima_limite = self.limite<valor
        acima_tentativa = numero_saques>self.limite_saques
        if acima_limite:
            print('Saque inválido. Acima do valor limite permitido.')
        
        elif acima_tentativa:
            print('Saque inválido. Acima do numero de saques permitido' )
            
            
        else:
            return super().sacar(valor)
        return False

    def __repr__(self):
        return super().__repr__()

class Historico:
    #Cria um objeto histórico com atributo _transacoes
    def __init__(self):
        self._transacoes = []

    #Cria um atributo público para manipular o atributo: _transacoes
    @property
    def transacoes(self):
        return self._transacoes

    #Recebe um objeto transacao e adiciona informações do tipo, valor e data dessa transacao
    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        })


class Transacao(ABC):
    #Cria uma interface com os abstractmethods valor e registrar
    @property
    @abstractmethod
    def valor(self):
        pass


    @abstractmethod
    def registrar(self,conta):
        pass

class Saque(Transacao):
    #Cria um objeto que recebe um atributo, e herda métodos da interface Transacao
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    #Implementa o método registrar
    #Recebe um objeto conta, e executa conta.sacar da classe conta, tendo como retorno um bool
    #Em caso de True: adiciona um registro da transacao no historico da conta, pelo metodo da classe Historico
    def registrar(self,conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    #Cria um objeto que recebe um atributo, e herda métodos da interface Transacao
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    #Implementa o método registrar
    #Recebe um objeto conta, e executa conta.depositar da classe conta, tendo como retorno um bool
    #Em caso de True: adiciona um registro da transacao no historico da conta, pelo metodo da classe Historico
    def registrar(self,conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


#Recebe cpf e clientes
#cria um filtro do cliente dentro da lista clientes, através do cpf, retorna o cliente ou um None
def filtrar_cliente(cpf,clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

#recebe um objeto cliente, e verifica a existência de contas, na inexistência dessa, retorna sem resultado
#Na existência de contas, retorna a primeira conta encontrada 
def recuperar_conta(cliente):
    if not cliente.contas:
        return
    
    return cliente.contas[0]


#recebe uma lista clientes
#solicita um cpf e verifica a existência do cpf na lista de objetos em clientes
#Caso o cpf não exista, solicita nome, data_nascimento e endereco, e cria um objeto cliente da classe PessoaFisica com os atributos solicitados
#Por fim, adiciona o objeto na lista clientes
def criar_cliente(clientes):
    cabecalho('CADASTRAR CLIENTE')
    cpf = input('Informe o CPF[somente números]: ').strip()
    cliente = filtrar_cliente(cpf,clientes)
    if cliente:
        print('Cliente já cadastrado')
        return
    nome = input("Informe o nome completo: ").lower().strip()
    data_nascimento = input("Informe a data de nascimento [dd-mm-aaaa]: ").strip()
    endereco = input('Informe o endereco [logradouro, nro - bairro -cidade/sigla estado]: ').strip()
    cliente = PessoaFisica(nome=nome,data_nascimento=data_nascimento,cpf=cpf,endereco=endereco)
    clientes.append(cliente)


#recebe a lista clientes
#solicita cpf e verifica a existência na lista clientes
#na existência, solicita o valor e faz a verificação de conta
#Se a conta existir, usa o método cliente.realizar_trasacao da classe Cliente, informando os objetos conta e transacao
#caso não haja cliente ou conta, retorna para o código principal
def deposito(clientes):
    cabecalho('REALIZAR DEPÓSITO')
    cpf = input('Informe o CPF[somente números]: ').strip()
    cliente = filtrar_cliente(cpf,clientes)
    if not cliente:
        print('Cliente não cadastrado, impossível fazer depósitos.')
        return
    
    valor = float(input('Informe o valor do depósito: '))
    transacao = Deposito(valor)

    conta = recuperar_conta(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)


#recebe a lista clientes
#solicita cpf e verifica a existência na lista clientes
#na existência, solicita o valor e faz a verificação de conta
#Se a conta existir, usa o método cliente.realizar_trasacao da classe Cliente, informando os objetos conta e transacao
#caso não haja cliente ou conta, retorna para o código principal
def sacar(clientes):
    cabecalho('REALIZAR SAQUE')
    cpf = input('Informe o CPF[somente números]: ').strip()

    cliente = filtrar_cliente(cpf,clientes)
    if not cliente:
        print('Cliente não cadastrado, impossível fazer depósitos.')
        return
    
    valor = float(input('Informe o valor do saque: '))
    transacao = Saque(valor)

    conta = recuperar_conta(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)



#recebe a lista clientes
#solicita cpf e verifica a existência na lista clientes
#na existência, solicita o valor e faz a verificação de conta
#Se a conta existir, usa o método conta.historico.transacoes para acessar a lista de transacoes do objeto histórico no objeto conta, e retorna os armazena em extrato, caso não hajam registros, retorna uma mensagem do sistema
#Na inexistência de cliente ou conta, retorna ao programa principal
def mostrar_extrato(clientes):
    cpf = input("CPF: ")
    cliente = filtrar_cliente(cpf,clientes)
    if not cliente:
        return
    conta = recuperar_conta(cliente)
    if not conta:
        
        return
    

    cabecalho(f'{'EXTRATO':<10} {'DATA':>10}')
    transacoes = conta.historico.transacoes
    
    extrato =""
    if not transacoes:
        extrato = "Não foram realizadas movimentações"
    for transacao in transacoes:
        extrato +=f'{transacao["tipo"]}\nR${transacao['valor']:.2f}\t\t{transacao['data']}\n'
    print(extrato)
    print(f'Saldo:\t\t{f"R${conta.saldo:.2f}":>28}')
    lin(50)



#Recebe numero_conta, clientes e contas
#solicita um cpf e verifica a existência do cpf na lista de objetos em clientes, na inexistência, retorna uma mensagem de erro
#Existndo um cliente, cria um objeto conta através do classmehtod mova_conta em ContaCorrente
#adiciona a nova conta na lista contas, e na lista contas presente no objeto cliente
def criar_contas(numero_conta, clientes, contas):
    cabecalho('NOVA CONTA')
    cpf = input('Informe o CPF[somente números]: ').strip()
    cliente = filtrar_cliente(cpf,clientes)
    if not cliente:
        print('Cliente não encontrado. Impossível criar conta')
        return
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)





#recebe a lista de contas e exibe cada objeto na tela
# Os objetos saem dispostos conforme a representação __repr__ da classe conta     
def listar_contas(contas):
    cabecalho('LISTA DE CONTAS')
    for conta in contas:
        lin(30)
        print(conta)

#Exibe uma linha com tamanho n
def lin(n):
    print('-'*n)

#Exibe um cabecalho com uma mensagem: msg entre duas linhas com tamanho 50
def cabecalho(msg):
    lin(50)
    print(msg.center(50))
    lin(50)

#Recebe o valor msg para ser a mensagem principal, e desempacota *items
#Exibe msg com a chamada de cabecalho
#Exibe os itens desempacotados com um contador através de enumerate
#pede uma entrada do tipo int, e retorna esse valor para o programa principal 
def menu(msg,*items):
    cabecalho(msg)
    for c,i in enumerate(items):
        print(f"{c} - {i}")

    sua_escolha = int(input('Sua escolha:\t'))
    return sua_escolha


#listas para o funcionamento interno do código
clientes = []
contas = []


#Execução principal
while True:
    #Executa uma função de espera de 1 segundo para o ínicio do loop
    time.sleep(1)

    #Executa a função menu, tendo o primeiro valor como msg, e o restante é empacotado
    #a variávels escolha recebe o valor retornado pela função
    escolha = menu('MENU', 'SAIR', 'DEPOSITAR', 'SACAR', 'EXTRATO', 'NOVO USUÁRIO', 'NOVA CONTA', 'LISTAR CONTAS')
    time.sleep(1)

    #condicional para a execução de cada função conforme a entrada digitada pelo usuário
    if escolha ==0:
        break

    elif escolha == 1:
        deposito(clientes)
    
    elif escolha == 2:
        sacar(clientes)

    elif escolha==3:
        mostrar_extrato(clientes)

    elif escolha == 4:
        criar_cliente(clientes)

    elif escolha == 5:
        numero_conta = len(contas)+1
        criar_contas(numero_conta,clientes, contas)

    elif escolha == 6:
        listar_contas(contas)

    else:
        print('Opção inválida. ')