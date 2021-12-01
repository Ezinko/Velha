from socket import *
serverName = "127.0.0.1"
serverPort = 26123

tabelaVelha = [" "," "," "," "," "," "," "," "," "]
jogo = True
player = None
bot = None

def TabEx():
    print("Para jogar você deve escolher a posição onde quer colocar X ou O")
    print()
    print(" 1 | 2 | 3 ")
    print("-----------")
    print(" 4 | 5 | 6 ")
    print("-----------")
    print(" 7 | 8 | 9 ")
    print()
    
def ExibeTabuleiro():
    print()
    print(" {} | {} | {} ".format(tabelaVelha[0], tabelaVelha[1], tabelaVelha[2]))
    print("-----------")
    print(" {} | {} | {} ".format(tabelaVelha[3], tabelaVelha[4], tabelaVelha[5]))
    print("-----------")
    print(" {} | {} | {} ".format(tabelaVelha[6], tabelaVelha[7], tabelaVelha[8]))
    print()

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
escolhaPrimeiro = input("Você quer ser o primeiro? (y/n) ")
while (escolhaPrimeiro != "y" and escolhaPrimeiro != "n" and escolhaPrimeiro != "Y" and escolhaPrimeiro != "N"):
    if (escolhaPrimeiro == "exit"):
        jogo = False
        break
    escolhaPrimeiro = input("Você deve escolher somente entre y ou n: ")
clientSocket.send(bytes(escolhaPrimeiro, "utf-8"))

if (escolhaPrimeiro == "y" or escolhaPrimeiro == "Y"):
    player = "X"
    bot = "O"
elif (escolhaPrimeiro =="n" or escolhaPrimeiro == "N"):
    player = "O"
    bot = "X"
    botJogada = clientSocket.recv(1024)
    jogadaRecebida = int.from_bytes(botJogada, "big")
    tabelaVelha[jogadaRecebida] = bot
    ExibeTabuleiro()

TabEx()
while (jogo == True):
    escolhaJogador = int(input("Escolha o número da posição que deseja jogar: "))
    while (escolhaJogador-1 < 0 or escolhaJogador-1 > 8):
        escolhaJogador = int(input("Deve ser digitado um número entre 1 e 9: "))

    while (tabelaVelha[escolhaJogador-1] == "X" or tabelaVelha[escolhaJogador-1] == "O"):
        escolhaJogador = int(input("Essa posição já foi escolhida, escolha outra: "))
        while (escolhaJogador-1 < 0 or escolhaJogador-1 > 8):
            escolhaJogador = int(input("Deve ser digitado um número entre 1 e 9: "))
    enviarServer = escolhaJogador.to_bytes((escolhaJogador.bit_length() + 7) // 8, "big")
    clientSocket.send(bytes(enviarServer))

    if (escolhaJogador == "exit"):
        jogo = False
        clientSocket.send(bytes(jogo, "utf-8"))
    
    respostaTabela = clientSocket.recv(1024)
    jogadaRecebida = int.from_bytes(respostaTabela, "big")
    if (tabelaVelha[jogadaRecebida-1] == " "):
        tabelaVelha[jogadaRecebida-1] = player
    
    botJogada = clientSocket.recv(1024)
    jogadaRecebida = int.from_bytes(botJogada, "big")
    if (tabelaVelha[jogadaRecebida] == " "):
        tabelaVelha[jogadaRecebida] = bot

    ExibeTabuleiro()

    fim = clientSocket.recv(1024)
    finalJogo = int.from_bytes(fim, "big")
    if (finalJogo == 2):
        decisao = "Você venceu, parabéns!"
        print(decisao)
        fina = input("Aperte enter para finalizar")
        jogo = False
    elif (finalJogo == 3):
        decisao = "Você perdeu!"
        print(decisao)
        fina = input("Aperte enter para finalizar")
        jogo = False
    elif (finalJogo == 4):
        decisao = "Deu velha!"
        print(decisao)
        fina = input("Aperte enter para finalizar")
        jogo = False
clientSocket.close()