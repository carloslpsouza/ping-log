from time import sleep
from datetime import datetime, date
import os, platform
data = str(datetime.now())
arq_offline = data[0:9] + '.txt'
arq_ips = 'ips'
if os.path.isfile(arq_offline): #Verifica se o arquivo existe e apaga se existir
    #os.remove(arq_offline)
    pass
else:
    f = open(arq_offline, 'x')
    f.close()

def configuracoes():
    pass

global slp
cfgs = open('config', 'r').readline()
    
    
def ping(host):
    global resposta
    global encontrado
    if platform.system().lower() == 'windows':
        ping_str = " -n 1 -w 1"
    else:
        ping_str =" -c 1"

    resposta = os.system("ping" + ping_str + " " + host)
    def leArquivo():
        global lines
        f = open(arq_offline, 'r')
        lines = f.readlines()
        f.close()
    if resposta == 1: #quando esta off
        leArquivo()
        encontrado = 0
        for x in lines:
            if x == host:
                encontrado = 1
                break

        f = open(arq_offline, 'a')
        if encontrado != 1:
            timestp = datetime.now()
            f.write(str(timestp) +' - '+ str(host) + '\n')
        f.close()

    else: #quando esta on
        leArquivo()
        f = open(arq_offline, 'w')
        for x in lines:
            if x != host:
                f.write(x)
        f.close()
    
    #return resposta == 0

list_ips = open(arq_ips, 'r')
for x in list_ips:
    ping(x)
list_ips.close()

while True:
    list_ips = open(arq_ips, 'r')
    for x in list_ips:
        ping(x)
    list_ips.close()
    #print(resposta)
    sleep(int(cfgs))