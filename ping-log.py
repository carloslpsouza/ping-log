import subprocess
import json
import os
import atexit
from time import sleep
from datetime import datetime
from assinatura import imprimeAssinatura

with open('config.json') as config_file:
    config_data = json.load(config_file)

intervalo = config_data['intervalo']
prefixo = config_data['prefixo_log']
diretorio = config_data['diretorio-log']

arquivos = os.listdir(diretorio)

def le_arquivo(nome_arquivo, dir=""):
    nome_arquivo = dir + nome_arquivo
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
    return linhas


def escreve_arquivo(nome_arquivo, conteudo):
    nome_arquivo = diretorio + nome_arquivo
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.writelines(conteudo)


def atualiza_arquivo(nome_arquivo, conteudo):
    nome_arquivo = diretorio + nome_arquivo
    with open(nome_arquivo, 'a') as arquivo:
        arquivo.writelines(conteudo)


def limparTerminal():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux, macOS
        os.system('clear')


def ping(host):
    try:
        with open(os.devnull, 'w') as devnull:
            if subprocess.call(['ping', '-n', '1',  '-w', '1', host], stdout=devnull, stderr=devnull) == 0:
                return True
    except subprocess.CalledProcessError:
        pass
    return False


def verificar_ips(arq_offline, arq_ips):
    if not os.path.isfile(os.path.join(diretorio, arq_offline)):
        escreve_arquivo(arq_offline, ['Start in: ' + str(datetime.now()) + '\n'])
        print(1)

    ips_offline = le_arquivo(arq_offline, diretorio)
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


def gera_nome_arquivo_log():
    data = datetime.now().strftime('%Y-%m-%d')
    for arquivo in arquivos:
        if not str(data) == arquivo[-14:-4]:
            return f'{prefixo}{data}.txt'
    return f'{prefixo}{data}.txt'

def finalizar_programa(arq_offline):
    if arq_offline is not None:
        atualiza_arquivo(arq_offline, ['Finish in: ' + str(datetime.now()) + '\n'])

def main():
    arq_ips = 'ips'
    arq_offline = gera_nome_arquivo_log()

    atexit.register(finalizar_programa, arq_offline)

    if not os.path.isfile(os.path.join(diretorio, arq_offline)):
        escreve_arquivo(arq_offline, ['Start in: ' + str(datetime.now()) + '\n'])
    else:
        atualiza_arquivo(arq_offline, ['Start again in: ' + str(datetime.now()) + '\n'])

    try:
        while True:
            verificar_ips(arq_offline, arq_ips)
            sleep(intervalo)
    except KeyboardInterrupt:
        if arq_offline is not None:
            finalizar_programa(arq_offline)
        raise

if __name__ == '__main__':
    print('Running...')
    imprimeAssinatura()
    main()
