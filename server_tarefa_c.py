#server - tarefa c
import socket

HOST    = ''     
PORT    = 5002
s       = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
orig    = (HOST, PORT)
s.bind(orig)
s.listen()

global x

x = 0
while True:
  con, cliente = s.accept()
  print ("\nConectado por .: ", cliente)
  msg = con.recv(1024).decode()
  [comando, numero] = msg.split(";")
  if (comando == "ler"):
    print (msg + "\n")
    msg = str(x)
    con.send(msg.encode())
  else:
    if (comando == "escrever"):
      print (msg + "\n")
      x = int(numero)
  con.close()
