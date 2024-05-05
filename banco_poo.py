from abc import ABC, abstractmethod
import textwrap

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Sacar(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar_check(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_Transacao(self)


class Depositar(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar_check(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_Transacao(self)

class Historico():
    def __init__(self):
        self._transacoes = []
    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_Transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
            }
        )


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "001"
        self._cliente = cliente
        self.historico = Historico()
    
    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def cliente(self):
        return self._cliente
    
    @property 
    def agencia(self):
        return self._agencia

    @classmethod
    def criar_conta(cls, cliente, numero):
        return cls(numero, cliente)

    def sacar_check(self, valor):
        if(self._saldo > valor):
            print("Saque feito com sucesso...")
            self._saldo -= valor
            return True
        elif(valor <= 0):
            print("Insira um valor válido para saque.")
            return False
        else:
            print("Error! Valor indisponível para sacar....")
            return False
    
    def depositar_check(self, valor):
        if(valor <= 0):
            print("Error! Insira um valor válido para depositar")
            return False
        else:
            print("Deposito feito com sucesso...")
            self._saldo += valor
            return True

class ContaCorrente(Conta):
    def __init__(self,  numero,  cliente,  limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len (
            [transacao for transacao in self._historico.transacoes 
            if transacao["tipo"] == "Saque"]
        )
        
        passou_limite = valor > self._limite
        excedeu_limite = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("Error, limite de saques diários atingidos!")
        elif(passou_limite):
            print("Error, valor emitido maior que o limite!")
        else:
            return super().sacar_check(valor)
        return False
    
    def __str__(self):
        return f"""\
            Agência: \t{self.agencia}
            C/C: \t{self.numero}
            Cliente: \t{self.cliente.nome}
        """
class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self._contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self._nome = nome
        self._cpf = cpf
        self._data_nascimento = data_nascimento

    @property
    def nome(self):
        return self._nome    


def filtrar_clientes(cpf, clientes):
    cliente_filtrado = [cliente for cliente in clientes if cliente._cpf == cpf]
    if cliente_filtrado:
        return cliente_filtrado[0]
    else:

        None

def depositar(clientes, contas):
    cpf = input("Informe o CPF para depositar...")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return
    
    valor = float(input("Informe o valor do depósito:"))
    transacao = Depositar(valor=valor)
    conta = recuperar_conta_cliente(cliente, contas)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes, contas):
    cpf = input("Informe o CPF para depositar...")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return
    
    valor = float(input("Informe o valor do depósito:"))
    transacao = Sacar(valor=valor)
    conta = recuperar_conta_cliente(cliente, contas)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def exibirExtrato(clientes, contas):
    cpf = input("Informe o CPF do cliente")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente=cliente, contas=contas)
    if not conta:
        return
    
    print("Extrato da conta:")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Transações não encontradas"
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}: \n\tR${transacao['valor']:.2f}"

    print(extrato)
    print(f"Saldo:\n\tR$ {conta.saldo:.2f}")
    
def criar_conta(numero_conta, clientes, contas):
    conta_filtrada = [conta for conta in contas if conta._numero == numero_conta]
    if conta_filtrada:
        return print("Conta existente")
    
    cpf = input("Informe o CPF:")
    cliente = filtrar_clientes(cpf, clientes=clientes)
    if not cliente:
        print("Cliente não encontrado!")
        return

    conta = ContaCorrente.criar_conta(cliente, numero_conta)
    contas.append(conta)
    cliente._contas.append(conta)
    print("Conta criada com sucesso!")

def listar_contas(contas):
    for conta in contas:
        print("="*100)
        print(textwrap.dedent(str(conta)))

def recuperar_conta_cliente(cliente, contas):
    if not cliente._contas:
        print("Cliente não possui conta")
        return
    else:
        numero_conta = int(input("Insira o número desta conta cadastrada: "))
        conta_filtrada = [conta for conta in contas if conta._numero == numero_conta]
        if conta_filtrada:
            return conta_filtrada[0]
        else:
            None

def criarCliente(clientes):
    cpf = input("Primeiramente informe o seu CPF:")
    cliente = filtrar_clientes(cpf, clientes)
    if cliente:
        print("Cliente existente!")
        return
    nome = input("Agora informe o nome deste cliente: ")
    endereco = input("Insira o endereço deste cliente: ")
    data_nascimento = input("Sua data de nascimento: ")
    cliente = PessoaFisica(nome=nome, cpf=cpf, endereco=endereco, data_nascimento=data_nascimento)
    clientes.append(cliente)
    print("Cliente criado com sucesso!")
    
def mostrarMenu():
    print(f"""
      Olá usuário
      Aperte uma tecla para começar:

      [d] -> Depósito
      [s] -> Saque
      [e] -> Extrato
      [ncl] -> Novo cliente
      [lu] -> Listar contas
      [nc] -> Nova conta
      [q] -> Sair
      """)

def main():
    clientes = []
    contas = []
    while True:

        if not clientes:
            print("Cadastre um cliente antes de tudo: ")
            criarCliente(clientes=clientes)
            print("Perfeito, vamos agora cadastrar uma conta para este cliente: ")
            numero = int(input("Informe o número da conta: "))
            criar_conta(numero_conta=numero, clientes=clientes, contas=contas)
            
        

        mostrarMenu()
        opcao = input(f"Insira sua opção: ")


        if opcao == "d":
            depositar(clientes=clientes, contas=contas)

        elif opcao == "s":
            sacar(clientes=clientes, contas=contas)
            
        elif opcao == "e":
            exibirExtrato(clientes=clientes,contas=contas)
        
        elif opcao == "lu":
            listar_contas(contas=contas)
        
        elif opcao == "ncl":
            criarCliente(clientes=clientes)
        
        elif opcao == "nc":
           numero = int(input("Informe o número da conta: "))
           criar_conta(numero_conta=numero, clientes=clientes, contas=contas)
            
        elif opcao == "q":
            print("Encerrando operação...")
            break
        

        else:
            print("Opção inválida, tente uma das opções listadas!")    

main()