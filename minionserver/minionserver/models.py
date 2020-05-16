from django.db import models
from django.http import JsonResponse
from django.shortcuts import render, redirect
import json
import sqlite3


# Create your models here.

# variaveis globais
linhaAnt = 1
limLinha = 5000000        # 5 milhões de palavras para cada minion
limLinhaAtual = limLinha

# Processa e retorna a wordlist para cada minion


def getWordList(self):
    linha = 1
    WORD_LIST = "minionserver/wordlist.txt"
    data = {
        'hash': "582d9abdeed1764cc463fcb44d0f51fe",
        'wordList': []
    }

    with open(WORD_LIST, 'r', errors='ignore') as f:
        for senhaLinha in f:
            global linhaAnt
            global limLinhaAtual
            if (linha >= linhaAnt):
                if(linha <= limLinhaAtual):
                    data['wordList'].append(senhaLinha.rstrip())
                    linha += 1
                else:
                    linhaAnt = linha
                    limLinhaAtual += limLinha
                    return JsonResponse(data, safe=False)
            else:
                linha += 1

# Recebe o resultado de cada minion


def postResult(request):
    if request.method == "POST":
        postData = json.loads(request.body.decode('utf-8'))
        print("Mensagem: "+postData['msg'])
        return JsonResponse({'success': True, 'msg': "Resultado recebido com sucesso"}, safe=False)
    return JsonResponse({'success': False, 'msg': "Erro, resultado não recebido"}, safe=False)

# Recebe a info de cada minion


def postInfMinion(request):
    if request.method == "POST":
        dados = json.loads(request.body.decode('utf-8'))
        print("Info receb. do Minion: "+dados['nome'])

        conn = sqlite3.connect('minionserver/db.sqlite3')

        listMinion = buscaListMinion(conn)

        if(dados['nome'] in listMinion):
            updateInfMinion(conn, dados)
        else:
            insertInfMinion(conn, dados)
        conn.close()
        return JsonResponse({'success': True, 'msg': "Info recebidas com sucesso"}, safe=False)
    return JsonResponse({'success': False, 'msg': "Erro, info não recebidas"}, safe=False)

# Busca os minion cadastrados no database


def buscaListMinion(conn):
    # lendo os dados
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nome FROM MINION;
    """)
    minionDB = cursor.fetchall()
    i = 0
    listMinion = []
    for row in minionDB:
        listMinion.append(row[0])
        i += 1
    return listMinion

# insere info do Minion no database


def insertInfMinion(conn, dados):
    cursor = conn.cursor()

    # inserindo dados na tabela
    insert = """INSERT INTO 
                MINION (    nome, 
                            so_nome,
                            so_inf,
                            cpu_modelo,
                            cpu_perc,
                            mem_total,
                            mem_dispon,
                            mem_usada,
                            mem_livre,
                            mem_perc,
                            disc_total,
                            disc_usado,
                            disc_livre,
                            disc_perc,
                            data
                        )
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,datetime('now','localtime'),1);"""

    cursor.execute(insert, [
        dados['nome'],
        dados['so_nome'],
        dados['so_inf'],
        dados['cpu_modelo'],
        dados['cpu_perc'],
        dados['mem_total'],
        dados['mem_dispon'],
        dados['mem_usada'],
        dados['mem_livre'],
        dados['mem_perc'],
        dados['disc_total'],
        dados['disc_usado'],
        dados['disc_livre'],
        dados['disc_perc']
    ])
    conn.commit()

# atualiza info do Minion no database


def updateInfMinion(conn, dados):
    cursor = conn.cursor()

    # alterando os dados da tabela
    update = """UPDATE
                    MINION
                SET 
                    so_nome = ?, 
                    so_inf = ?,
                    cpu_modelo = ?, 
                    cpu_perc = ?,
                    mem_total = ?,
                    mem_dispon = ?,
                    mem_usada = ?,
                    mem_livre = ?,
                    mem_perc = ?,
                    disc_total = ?,
                    disc_usado = ?,
                    disc_livre = ?,
                    disc_perc  = ?,
                    data = datetime('now','localtime'),
                    ativo = ?

                WHERE 
                    nome = ?
                """

    cursor.execute(update, [
        dados['so_nome'],
        dados['so_inf'],
        dados['cpu_modelo'],
        dados['cpu_perc'],
        dados['mem_total'],
        dados['mem_dispon'],
        dados['mem_usada'],
        dados['mem_livre'],
        dados['mem_perc'],
        dados['disc_total'],
        dados['disc_usado'],
        dados['disc_livre'],
        dados['disc_perc'],
        dados['ativo'],
        dados['nome']
    ])
    conn.commit()
