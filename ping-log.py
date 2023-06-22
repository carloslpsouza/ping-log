import subprocess
import json
import os
from time import sleep
from datetime import datetime

with open('config.json') as config_file:
    config_data = json.load(config_file)

intervalo = config_data['intervalo']
prefixo = config_data['prefixo_log']

def le_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
    return linhas

def escreve_arquivo(nome_arquivo, conteudo):
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.writelines(conteudo)

def limparTerminal():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux, macOS
        os.system('clear')

def imprimeAssinatura():
    print(60*"=")
    print ("| Ping Log                                                 |")
    print(60*"=")
    print ("| Desenvolvido por: Carlos Souza                           |")
    print ("| Email: carlosp.souza@gmail.com                           |")
    print ("| Linkedin: https://www.linkedin.com/in/carloslpsouza/     |")
    print(60*"=")

def ping(host):
    try:
        with open(os.devnull, 'w') as devnull:
            if subprocess.call(['ping', '-n', '1', host], stdout=devnull, stderr=devnull) == 0:
                return True
    except subprocess.CalledProcessError:
        pass
    return False

def verificar_ips(arq_offline, arq_ips):
    ips_offline = le_arquivo(arq_offline)
    ips = le_arquivo(arq_ips)

    ips_offline_novos = []
    for ip in ips:
        if not ping(ip.strip()):
            data = datetime.now()
            ips_offline_novos.append(str(data) + ' - ' + ip)
            limparTerminal()
            imprimeAssinatura()
            print('Dispositivo fora de rede! ' + str(data) + ' - ' + ip)
    
    conteudo = ips_offline + ips_offline_novos
    escreve_arquivo(arq_offline, conteudo)

def main():
    data = datetime.now().strftime('%Y-%m-%d')
    arq_offline = f'{prefixo}{data}.txt'
    arq_ips = 'ips'

    if not os.path.isfile(arq_offline):
        escreve_arquivo(arq_offline, [])

    while True:
        verificar_ips(arq_offline, arq_ips)
        sleep(intervalo)

if __name__ == '__main__':
    print('Running...')
    imprimeAssinatura()
    main()
