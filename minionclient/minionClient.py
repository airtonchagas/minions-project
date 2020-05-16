
import requests
import json
import hashlib
import platform
import cpuinfo
import psutil


def postInfMinion(disconnect):
    ativo = 1
    if(disconnect == True):
        ativo = 0
        

    url = "http://127.0.0.1:8000/postInfMinion/"
    headers = {'Content-Type': 'application/json'}

    payload = {
        'nome': platform.node(),
        'so_nome': platform.system(),
        'so_inf': platform.platform(),
        'cpu_modelo': cpuinfo.get_cpu_info()['brand'],
        'cpu_perc': str(psutil.cpu_percent()) + " %",
        'mem_total': str(round(psutil.virtual_memory().total / 1024/1024/1024)) + " GB",
        'mem_dispon': str(round(psutil.virtual_memory().available / 1024/1024/1024)) + " GB",
        'mem_usada': str(round(psutil.virtual_memory().used / 1024/1024/1024)) + " GB",
        'mem_livre': str(round(psutil.virtual_memory().free / 1024/1024/1024)) + " GB",
        'mem_perc': str(psutil.virtual_memory().percent) + " %",
        'disc_total': str(round(psutil.disk_usage('/').total / 1024/1024/1024)) + " GB",
        'disc_usado': str(round(psutil.disk_usage('/').used / 1024/1024/1024)) + " GB",
        'disc_livre': str(round(psutil.disk_usage('/').free / 1024/1024/1024)) + " GB",
        'disc_perc': str(psutil.disk_usage('/').percent) + " %",
        'ativo': ativo
    }

    resposta = requests.post(url, data=json.dumps(payload), headers=headers)
    contantResp = json.loads(resposta.content.decode('utf-8'))
    print(contantResp['msg'])


def buscaContentApi():

    url = "http://127.0.0.1:8000/wordList/"
    headers = {'Content-Type': 'application/json'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return response.status_code


def testarHash(hash, wordList):

    url = "http://127.0.0.1:8000/postResult/"
    headers = {'content-type': 'application/json'}
    payload = {
        'name': platform.node(),
        'msg': 'Senha Não encontrada!'
    }

    for senha in wordList:
        hashSenha = hashlib.md5(senha.encode('utf-8')).hexdigest()
        if (hashSenha == hash):
            payload['msg'] = 'senha encotrada: ' + senha + " >> " + hashSenha
            print(payload['msg'])
            break

    resposta = requests.post(url, data=json.dumps(payload), headers=headers)
    contantResp = json.loads(resposta.content.decode('utf-8'))
    print(contantResp['msg'])


if __name__ == '__main__':
    #content = buscaContentApi()
    #testarHash(content["hash"], content["wordList"])
    disconnect = False
    postInfMinion(disconnect)
