import os
import json
from datetime import datetime

with open('config.json') as config_file:
    config_data = json.load(config_file)

prefixo = config_data['prefixo_log']
diretorio = config_data['diretorio-log']


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


def trata_diretorio():
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
    arquivos = os.listdir(diretorio)
    return arquivos

def gera_novo_arquivo(novo):
  escreve_arquivo(
            novo, ['Start in: ' + str(datetime.now()) + '\n'])
  pass

def gera_nome_arquivo_log():
    data = datetime.now().strftime('%Y-%m-%d')
    arquivos = trata_diretorio()
    if len(arquivos) > 0:
        for arquivo in arquivos:
            if str(data) == arquivo[-14:-4]:
              return str(arquivo)

    gera_novo_arquivo(f'{prefixo}{data}.txt')
    nome_arquivo = f'{prefixo}{data}.txt'
    return nome_arquivo