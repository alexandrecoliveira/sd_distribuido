#cliente do modelo distribuido - tarefa c
#https://ashishpython.blogspot.com/2013/11/how-to-show-all-computer-name-in-lan.html

from socket import *
import time                               #time.sleep(1)

def is_up(addr):
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(0.01)                    # set a timeout of 0.01 sec    
    if not s.connect_ex((addr,7001)):     # connect_ex retorna 0 se a operação foi bem sucedida #not 0 == 1
        s.send("Hello my friend\n".encode())
        s.close()                         
        return 1
    else:
        #print ("não esta rodando:", s)
        s.close()

def run(faixa_ip, lista_ips):
    for ip in range(1,256):               # 'ping' os enderecos de x.x.x.1 to x.x.x.255
        addr = FAIXA_IP + str(ip)
        if is_up(addr):
            LISTA_IPS.append(addr)
            time.sleep(1)
            #print ("rodando: ", addr, getfqdn(addr))   # the function 'getfqdn' returns the remote hostname

#main
print ("Inicio")
#servidor de armazenamento
HOST_SERVER = "127.0.0.1"                     #na apresentacao usar input("Digite o ip do servidor.: ")
PORT_SERVER = 5002          
DEST_SERVER = (HOST_SERVER, PORT_SERVER)

#FAIXA_IP = "10.250.208."                   #faixa de ips da nuvem
FAIXA_IP = "192.168.50."
LISTA_IPS = []

run(FAIXA_IP, LISTA_IPS)
print (LISTA_IPS)

print ("Final")
