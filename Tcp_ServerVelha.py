from socket import *
import random
serverPort = 26123
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(5) # o argumento “listen” diz à biblioteca de soquetes que queremos enfileirar no máximo 5 requisições de conexão (normalmente o máximo) antes de recusar começar a recusar conexões externas. Caso o resto do código esteja escrito corretamente, isso deverá ser o suficiente.
print ("TCP Server\n")

def final(x, y):
    if (y[0] == x and y[1] == x and y[2] == x):
        return True
    if (y[3] == x and y[4] == x and y[5] == x):
        return True
    if (y[6] == x and y[7] == x and y[8] == x):
        return True
    if (y[0] == x and y[4] == x and y[8] == x):
        return True
    if (y[2] == x and y[4] == x and y[6] == x):
        return True
    if (y[0] == x and y[3] == x and y[6] == x):
        return True
    if (y[1] == x and y[4] == x and y[7] == x):
        return True
    if (y[2] == x and y[5] == x and y[8] == x):
        return True
    

def velha(z):
    x = 0
    o = 0
    for i in range(9):
        if (z[i] == "X"):
            x+=1
        elif (z[i] == "O"):
            o+=1
    if (x == 5 or o == 5):
        return True

tabelaVelha = ["","","","","","","","",""]
jogo = True
player = None
bot = None
numero = None
fimDeJogo = 1

connectionSocket, addr = serverSocket.accept()
escolhaPrimeiro = connectionSocket.recv(65000)
recebidoClient = str(escolhaPrimeiro,"utf-8")
if(recebidoClient == "exit"):
    jogo = False
elif (recebidoClient == "y" or recebidoClient == "Y"):
    bot = "O"
    player = "X"
elif (recebidoClient == "n" or recebidoClient == "N"):
    bot = "X"
    player = "O"
    numero = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8])
    tabelaVelha[numero] = bot
    jogaBot = numero.to_bytes((numero.bit_length() + 7) // 8, "big")
    connectionSocket.send(bytes(jogaBot))
    
while (jogo == True):
    escolhaJogador = connectionSocket.recv(65000)
    jogadaRecebida = int.from_bytes(escolhaJogador, "big")
    
    if (jogadaRecebida == False):
        jogo = False
        
    if (tabelaVelha[jogadaRecebida-1] != "X" or tabelaVelha[jogadaRecebida-1] != "O"):
        tabelaVelha[jogadaRecebida-1] = player
        enviarClient = jogadaRecebida.to_bytes((jogadaRecebida.bit_length() + 7) // 8, "big")
        connectionSocket.send(bytes(enviarClient))
    
    numero = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8])
    if not (velha(tabelaVelha)):
        while (tabelaVelha[numero] == "X" or tabelaVelha[numero] == "O"):
            numero = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8])
    if (velha(tabelaVelha)):
        fimDeJogo = 4

    if (fimDeJogo == 1):
        tabelaVelha[numero] = bot
        jogaBot = numero.to_bytes((numero.bit_length() + 7) // 8, "big")
        connectionSocket.send(bytes(jogaBot))

    if (final(player, tabelaVelha)):
        fimDeJogo = 2
    elif (final(bot, tabelaVelha)):
        fimDeJogo = 3

    print(fimDeJogo)

    fim = fimDeJogo.to_bytes((fimDeJogo.bit_length() + 7) // 8, "big")
    connectionSocket.send(bytes(fim))
    
    print(tabelaVelha)

connectionSocket.close()