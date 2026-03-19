import time

def linha():
    # prints a line with a defined lenght 
    print('-'*30)
def cabecalho(msg):
    # prints a message between two lines
    linha()
    print(msg)
    linha()

def menu(msg,*item):
    #receives and unpack a sequence of words and manage them
    #cabecalho is calling and prints the 'msg'
    #for loop with enumarate method is unpacking, enumarating and printing the items
    # at the end, a variable receive an input with an option and return to the program
    cabecalho(msg)
    for c,i in enumerate(item):
        print(f'{c+1}- {i}')
    linha()

    sua_opcao = int(input('Escolha: '))
    return sua_opcao    


def sacar(saldo,extrato,numero_saques, LIMITE_SAQUES,limite):
    #ask the user a value and makes a wothdraw if it's possible, otherwise give an error message with the reason of the error
    #valor receives the value to the withdraw
    #v1 analizes if the value is less/ equal to the balance(saldo)
    #n1 analizes if the daily saques is less than the daily limit
    #l1 analizes if the value is less/equal to the withdraw limit
    # saldo saves teh balance of the account
    #extrato saves strings messages with each sucessfull withdraw
    # numero_saques saves the withdraws made
    # LIMITE_SAQUES is the sucessfull withdraw limit
    #limite is the amount limit for each withdraw
    # 
    #the if else condition manage all the variable and try to make the operation, at the end, returns the current: saldo, extrato and numero_saques   
    valor = int(input('Valor: '))
    v1 = valor<=saldo
    n1 = numero_saques<LIMITE_SAQUES
    l1 = valor<=limite
    if n1 and v1 and l1:
        saldo -= valor
        extrato += f'Saque: R${valor:.2f}\n'
        print('Saque realizado com sucesso')
        print(numero_saques)
        numero_saques = numero_saques+ 1
        print(numero_saques)
        
    elif v1==False:
        print('Saque inválido. Saldo insuficiente.')
    elif n1 == False:
        print('Sem saques disponíveis hoje')
    else:
        print('Saque não realizado. Valor superior ao limite')
    return saldo, extrato, numero_saques

def deposito(saldo,extrato):
    #ask the user for a value to deposit
    #valor receive the value to deposit
    #if else condition analises if the value is valid and make the transaction or prints an error with the reason
    #at the end returns the current: saldo and extrato
    valor = int(input('Valor: '))
    if valor <=0:
        print('Valor inválido')
    else:
        saldo+= valor
        extrato+= f'Depósito: R${valor:.2f}\n'
        print('Depósito realizado com sucesso')

    return saldo, extrato

def mostrar_extrato(extrato,saldo):
    #prints the balance and transactions of the account
    cabecalho('EXTRATO')
    print(f'Saldo: R${saldo:.2f}')
    print(extrato if extrato else 'Sem movimentações')

LIMITE_SAQUES = 3
numero_saques = int(0)
saldo = 200
extrato = ''
limite = 500


while True:
    #creates a infinit loop
    time.sleep(1)
    escolha = menu('MENU','Saque','Extrato', 'Depósito', 'Sair')
    #calls menu and assign with the return
    time.sleep(1)

    if escolha == 1 :
        #this option executes the function sacar passing the arguments and get uptade values at the end
        saldo, extrato,numero_saques = sacar(saldo,extrato,numero_saques,LIMITE_SAQUES,limite)
        print(numero_saques)
    elif escolha == 2:
        #this option prints the balance by calling mostrar_extrato 
        mostrar_extrato(extrato, saldo)
    elif escolha == 3:
        #this option calls deposit function, passing saldo and extrato and updating them 
        saldo, extrato = deposito(saldo,extrato)
    elif escolha == 4:
        #this option breaks the loop
        break
    else:
        #this option occurs when a different value is atributted
        print('Opção inválida')
    