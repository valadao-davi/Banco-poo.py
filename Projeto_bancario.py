menu=f"""
      Olá usuário
      Aperte uma tecla para começar:

      [d] -> Depósito
      [s] -> Saque
      [e] -> Extrato
      [nc] -> Nova conta
      [lu] -> Listar usuários
      [nu] -> Novo usuário
      [nc] -> Nova conta
      [q] -> Sair
      """
#Variáveis
usuarios = []
deposito = 0
LIMITE = 500
extrato = []
limite_saques = 3
contas = []
AGENCIA = "001"
#Funções

#Funções do usuário

def criarUsuario(usuarios):
    cpf = input("Primeiramente informe o CPF deste usuário: ")
    usuario = filtrarUsuario(cpf, usuarios)

    if usuario:
        print("Erro! Já há um usuário com este CPF")
        return
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento: ")
    endereco = input("Informe o endereço completo(logradouro, nro - bairro - cidade/sigla estado):")
    usuarios.append({"nome": nome, "cpf": cpf, "data_nascimento": data_nascimento, "endereço": endereco})
    print("Usuário criado com sucesso!")
    return usuarios

def filtrarUsuario(cpf, usuarios):
    usuarioFiltrados = [usuarios for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarioFiltrados[0] if usuarioFiltrados else None

def criarConta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF deste usuário: ")
    usuario = filtrarUsuario(cpf, usuarios)

    if usuario:
        print("Conta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    else: 
        print("Usuário não encontrado")

def listarUsuarios(usuarios):
    print("Usuário nesta lista:")
    for usuario in usuarios:
        print(f"{usuario}...", end=" \n")



#Funções de dinheiro
def exibirExtratos(extrato):
    print(f"Extrato atual: R${deposito}")
    print("Extratos realizados: ")
    for item in extrato:
        print(f"{item}...", end=" \n")

def depositar(deposito, valor, extrato, /):
    if(valor > 0 and type(float(valor))):
        deposito += valor
        extrato.append(f"Depósito realizado de: R$ {deposito}")
        print(f"Depósito atual: {deposito}")
    else:
        print("Erro detectado! insira um depósito válido") 
    return deposito, extrato

   
def sacar(deposito, limite_saques, extrato, /):
    global LIMITE
    if(deposito > 0 and limite_saques > 0):
        saque = float(input("Insira um valor para sacar: "))
        if(saque <= LIMITE):
                deposito = deposito - saque
                extrato.append(f"Saque realizado de: R$ {saque}") 
                limite_saques = limite_saques - 1
                print("Saque realizado com sucesso!")
        elif(saque > deposito):
                print("Não há valor suficiente para sacar!")  
        else:
                print("Valor maior que o limite!")

    elif(limite_saques <= 0):
        print("Limite de saques diários ultrapassado, tente novamente amanhã!")

    else:
        print("Erro, não há deposito para sacar")

    return deposito, extrato, limite_saques

        
def mostrarMenu():
    print(menu)


while True:
    mostrarMenu()
    opcao = input(f"Insira sua opção: ")


    if opcao == "d":
        valor = float(input("Insira um valor para depositar: "))
        deposito, extrato = depositar(deposito, valor, extrato)

    elif opcao == "s":
        deposito, extrato, limite_saques = sacar(deposito, limite_saques, extrato)
        
    elif opcao == "e":
        exibirExtratos(extrato)
    
    elif opcao == "nu":
        usuarios = criarUsuario(usuarios)
    
    elif opcao == "lc":
        listarUsuarios(usuarios)
    
    elif opcao == "nc":
        numero_conta = len(contas) + 1
        conta = criarConta(AGENCIA, numero_conta, usuarios)

        if conta:
            contas.append(conta)
          
    elif opcao == "q":
        print("Encerrando operação...")
        break
    

    else:
        print("Opção inválida, tente uma das opções listadas!")    