menu="""
      Olá usuário
     
      Aperte uma tecla para começar:

      [d] -> Depósito
      [s] -> Saque
      [e] -> Extrato
      [q] -> Sair
      """

deposito = 0
LIMITE = 500
extrato = [""]
limite_saques = 3


while True:

    opcao = input(f"{menu}")


    if opcao == "d":
        valor = float(input("Insira um valor para depositar: "))
        if(valor > 0 and type(float(valor))):
            deposito = deposito + valor
            extrato.append(f"Depósito realizado de: R$ {deposito}") 
            print(f"Depósito atual: {deposito}")

    elif opcao == "s":
        if(deposito > 0 and limite_saques > 0):
            saque = float(input("Insira um valor para sacar: "))
            if(saque <= LIMITE):
                deposito = deposito - saque
                extrato.append(f"Saque realizado de: R$ {saque}") 
                limite_saques = limite_saques - 1
                print("Saque realizado com sucesso!")
            elif(saque < deposito):
                print("Não há valor suficiente para sacar!")  
            else:
                print("Valor maior que o limite!")

        elif(limite_saques <= 0):
            print("Limite de saques diários ultrapassado, tente novamente amanhã!")

        else:
            print("Erro, não há deposito para sacar")    
        
    elif opcao == "e":
        print("Extratos realizados: ")
        for item in extrato:
            print(f"\n{item}...", end=" ")

    elif opcao == "q":
        print("Encerrando operação...")
        break

    else:
        print("Opção inválida, tente uma das opções listadas!")    