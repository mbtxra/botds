from datetime import datetime
import os, inspect

# Endereco no qual vai ser salvo os dados
CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
enderecoJogos = f'{CURRENTDIR}/arquivos/jogos.txt'
enderecoNotificacoes = f'{CURRENTDIR}/arquivos/notificacoes.txt'

def salvarDadosNotificacaoLista(jogos, notificacoes):
    if(existe_arquivo(enderecoNotificacoes)):
        arq = open(enderecoNotificacoes, 'a', encoding="utf-8")
    else:
        arq = open(enderecoNotificacoes, 'w', encoding="utf-8")
    for j in jogos:
        notificacoes.append({
            "titulo": j['titulo'],
            "dataInicioOferta": j['dataInicioOferta'],
            "dataFinalOferta": j['dataFinalOferta']
        })
        arq.write(f"{j['titulo']};{j['dataInicioOferta']};{j['dataFinalOferta']}\n")
    arq.close()

def salvarDadosNotificacao(j):
    if(existe_arquivo(enderecoNotificacoes)):
        arq = open(enderecoNotificacoes, 'a', encoding="utf-8")
    else:
        arq = open(enderecoNotificacoes, 'w', encoding="utf-8")
    arq.write(f"{j['titulo']};{j['dataInicioOferta']};{j['dataFinalOferta']}\n")
    arq.close()

def salvarDados(jogos):
    if(existe_arquivo(enderecoJogos)):
        arq = open(enderecoJogos, 'a')
    else:
        arq = open(enderecoJogos, 'w')
    for j in jogos:
        arq.write(f"{j['titulo']};{j['dataInicioOferta']};{j['dataFinalOferta']};{j['precoOriginal']};{j['precoDesconto']};{j['urlParaDownload']};{j['descricaoJogo']};{j['imagemJogo']}\n")
    arq.close()

def buscarDadosNotificacoesCadastrados():
    notificacoes = []
    if existe_arquivo(enderecoNotificacoes):
        arq = open(enderecoNotificacoes, 'r')
        for linha in arq:
            valores = linha.replace("\n", "").split(";")
            notificacoes.append({
                "titulo": valores[0],
                "dataInicioOferta": valores[1],
                "dataFinalOferta": valores[2]
            })
    return notificacoes

def buscarDadosJogosCadastrados():
    jogos = []
    if existe_arquivo(enderecoJogos):
        arq = open(enderecoJogos, 'r')
        for linha in arq:
            valores = linha.replace("\n", "").split(";")
            jogos.append({
                "titulo": valores[0],
                "dataInicioOferta": valores[1],
                "dataFinalOferta": valores[2],
                "precoOriginal": valores[3],
                "precoDesconto": valores[4],
                "urlParaDownload": valores[5],
                "descricaoJogo": valores[6],
                "imagemJogo": valores[7]
            })
    return jogos

# Verificar a existencia de um arquivo
def existe_arquivo(nome):
    import os
    if os.path.exists(nome):
        return True
    else:
        return False