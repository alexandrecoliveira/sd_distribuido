#cliente do modelo distribuido - tarefa c
#import socket
from socket import *
import time                                                 
import random                                               #usado no for

def ler(dest): 
  servidor = socket(AF_INET, SOCK_STREAM)
  servidor.connect(dest)
  comando = "ler;0"
  servidor.send(comando.encode())
  res = servidor.recv(1024).decode()
  servidor.close()
  return int(res) 

def escrever(x, dest): 
  servidor = socket(AF_INET, SOCK_STREAM)
  servidor.connect(dest)
  comando = "escrever;" + str(x)
  servidor.send(comando.encode())
  time.sleep(1)
  servidor.close()

def realizaOperacao(server_d):
  for i in range(1, random.randint(1,10) * 5):        
      x = ler(server_d)
      x = x + 1
      escrever(x, server_d)
      print ("Valor de x: ", x)

def removerIpDoEleito(lista_demais_ips, ip):
  lista_demais_ips.remove(ip)
  return 1

def informarFimOperacao(lista_demais_ips, porta):
  print("Informando fim aos demais ...\n")
  for ip in lista_demais_ips:
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(0.01)                                  
    s.connect_ex((ip,porta))                            
    s.send("fim".encode())
    time.sleep(1)


def informarMinhaEleicao(lista_demais_ips, meu_ip, porta):
  print("Informando eleicao aos demais...\n")
  for ip in lista_demais_ips:
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(0.01)                                  
    s.connect_ex((ip,porta))                  
    comando = "eleito;" + meu_ip
    s.send(comando.encode());
    time.sleep(1)
  
def maiorIp(lista_ips, ip):
  return (lista_ips[-1] == ip)                              # se o ip atual for igual ao ultimo entao eh o maior

def quemEstaAi(addr, porta):
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(0.01)                                      # set a timeout of 0.01 sec    
    if not s.connect_ex((addr,porta)):                      # connect_ex retorna 0 se a operação foi bem sucedida #not 0 == 1
        #s.send("Hello my friend".encode())
        s.close()                         
        return 1
    else:#print ("não esta rodando:", s)
        s.close()

def buscarNaRede(faixa_ip, lista_ips, porta):
    for ip in range(1,256):                                 # 'ping' os enderecos de x.x.x.1 to x.x.x.255
        addr = FAIXA_IP + str(ip)
        if quemEstaAi(addr, porta):
            LISTA_IPS.append(addr)
            time.sleep(1)
            #print ("rodando: ", addr, getfqdn(addr))       # the function 'getfqdn' returns the remote hostname


#main
print ("Inicio")
#servidor de armazenamento
HOST_SERVER = "192.168.50.127" #"127.0.0.1"                 # na apresentacao usar input("Digite o ip do servidor.: ")
PORT_SERVER = 5002          
DEST_SERVER = (HOST_SERVER, PORT_SERVER)
# Criacao do socket e estado de listen
HOST        = ''
PORTA       = 7001
s           = socket(AF_INET, SOCK_STREAM)  
orig        = (HOST, PORTA)
s.bind(orig)
s.listen()
#definicao de ips
MEU_IP      = gethostbyname(gethostname())
FAIXA_IP    = MEU_IP.rsplit(".", 1)[0] + "."                #remove o ultimo numero apos o "." e adiciona a string "." novamente
LISTA_IPS   = []

time.sleep(10)                                              # (tempo para aguardar a entrada dos demais clientes)

buscarNaRede(FAIXA_IP, LISTA_IPS, PORTA)                
LISTA_DEMAIS_IPS = [ip for ip in LISTA_IPS if ip != MEU_IP]

print ("Meu IP: ", MEU_IP)
print ("Demais IPS: ", LISTA_DEMAIS_IPS)

if maiorIp(LISTA_IPS, MEU_IP):
  print ("Minha vez\n")
  informarMinhaEleicao(LISTA_DEMAIS_IPS, MEU_IP, PORTA)
  realizaOperacao(DEST_SERVER)
  informarFimOperacao(LISTA_DEMAIS_IPS, PORTA)
  print ("Finalizei, saindo da eleicao...\n")
else:
  while not maiorIp(LISTA_IPS, MEU_IP):
    print ("Nao eh a minha vez\n")
    while True:   #funcionamento do servidor
      con, cliente = s.accept()
      while True:                                           # aguaarda receber mensagem no formato eleito;ip
        msgEleicao = con.recv(1024).decode()                
        if (msgEleicao.startswith("eleito")):
          break
      [eleito, ip_eleito] = msgEleicao.split(";")
      print ("O eleito foi: ", ip_eleito)
      removerIpDoEleito(LISTA_DEMAIS_IPS, ip_eleito)
      while True:                                           # Laço que serve para aguardar o comando "fim"
        msgDeFim = con.recv(1024).decode()
        if (msgFim.startswith("fim")):
          print (ip, " finalizou ...\n")
          break
    #con.close()

print ("Final")
