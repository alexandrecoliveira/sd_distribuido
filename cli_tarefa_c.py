#cliente do modelo distribuido - tarefa c
#import socket
from socket import *
import time                                             # time.sleep(1)
import random                                           #usado no for

def ler(dest): 
  servidor = socket(AF_INET, SOCK_STREAM)
  servidor.connect(dest)
  comando = "ler;0"
  print (comando)
  servidor.send(comando.encode())
  res = servidor.recv(1024).decode()
  servidor.close()
  return int(res) 

def escrever(x, dest): 
  servidor = socket(AF_INET, SOCK_STREAM)
  servidor.connect(dest)
  comando = "escrever;" + str(x)
  print (comando)
  servidor.send(comando.encode())
  time.sleep(1)
  servidor.close()

def realizaOperacao(server_d):
  print (server_d)
  for i in range(1, random.randint(1,10) * 5):        
      x = ler(server_d)
      print (x)
      x = x + 1
      escrever(x, server_d)
      print ("Valor de x: ", x)

def quemEstaAi(addr, porta):
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(0.01)                                  # set a timeout of 0.01 sec    
    if not s.connect_ex((addr,porta)):                  # connect_ex retorna 0 se a operação foi bem sucedida #not 0 == 1
        s.send("Hello my friend".encode())
        s.close()                         
        return 1
    else:#print ("não esta rodando:", s)
        s.close()

def buscarNaRede(faixa_ip, lista_ips, porta):
    for ip in range(1,256):                             # 'ping' os enderecos de x.x.x.1 to x.x.x.255
        addr = FAIXA_IP + str(ip)
        if quemEstaAi(addr, porta):
            LISTA_IPS.append(addr)
            time.sleep(1)
            #print ("rodando: ", addr, getfqdn(addr))   # the function 'getfqdn' returns the remote hostname

#main
print ("Inicio")
#servidor de armazenamento
HOST_SERVER = "192.168.50.127" #"127.0.0.1"                               # na apresentacao usar input("Digite o ip do servidor.: ")
PORT_SERVER = 5002          
DEST_SERVER = (HOST_SERVER, PORT_SERVER)
# Criacao do socket e estado de listen
HOST        = ''
PORTA       = 7001
s           = socket(AF_INET, SOCK_STREAM)  
orig        = (HOST, PORTA)
s.bind(orig)
s.listen(2)

MEU_IP      = gethostbyname(gethostname())
FAIXA_IP    = MEU_IP.rsplit(".", 1)[0] + "."            #remove o ultimo numero apos o "." e adiciona a string "." novamente
LISTA_IPS   = []

time.sleep(10)                                          # (tempo para aguardar a entrada dos demais clientes)

buscarNaRede(FAIXA_IP, LISTA_IPS, PORTA)                
print ("Meu IP: ", MEU_IP)
LISTA_DEMAIS_IPS = [ip for ip in LISTA_IPS if ip != MEU_IP]
print ("Demais IPS: ", LISTA_DEMAIS_IPS)

if len(LISTA_IPS) > 1:   
  print ("mais máquinas na rede")
else:                                                   # somente essa maquina está na rede
  realizaOperacao(DEST_SERVER)

print ("Final")
