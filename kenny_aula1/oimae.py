## print() para printar

## declarar variaveis basta nomear da seguinte maneira:
## nome_da_variavel = tipo_da_variavel_

##x = 2
##print(x)
##x = 'oi mae'
##print(x)
##oi = [1,2,3,'oi']
## print(oi)

## for elemento in oi:
##    print(elemento)

## for i in range(4):
##    if type(oi[i]) == type(1):
##        print('inteiro')
  ##  elif type(oi[i]) == type('s'):
##        print('string')


##try:
##string    x = 1/0

## rd.randint(4)

import random as rd

balas = int(input())
slots = int(input())
resposta = 'sim'

if balas == slots:
    print('Voce morreu')
    exit()



while resposta == 'sim':

    aleatorioslots = rd.randint(0, slots) + 1

    if aleatorioslots/slots > balas/slots:
        print('Voce sobreviveeeeuu!!! HURUU')
        print('Quuer tentar novamente?')
        print('sim ou nao')
        resposta = input()
        slots = slots - 1

    else:
        print('VOCE MORREEEEUUU')
        exit()