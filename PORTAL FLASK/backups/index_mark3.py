from flask import Flask, render_template, request, redirect
import time
from subprocess import Popen, PIPE
import subprocess
import pandas as pd
from models import Cliente, Cliente_hosp
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

@app.route('/')
def index():
    arquivo = pd.read_excel('pings.xlsx')

    quant = arquivo['IP'].count()

    lista_inativos = []
    lista_ativos = []

    for i in range(0, quant):
        empresa = arquivo['CLIENTE'][i]
        ip = arquivo['IP'][i]
        id_vant = arquivo['DESIGNADO'] [i]

        resposta = str(subprocess.run('ping {} -n 1'.format(ip), stdout=PIPE))
        
        if("encontrar o host" in resposta):
            print('IP inválido')
        else:
            resposta_dolar = resposta.replace('Recebidos', '$')
            resposta_hash = resposta.replace('Perdidos', '#')

            cont = 0
            for letra in resposta_dolar:
                cont+=1
                if(letra == "$"):
                    indi_inicio = cont + 3
                    indi_final  = indi_inicio + 1
                    recebidos = str(resposta_dolar[indi_inicio:indi_final])
                    recebidos = recebidos.strip()
                    recebidos = int(recebidos)

            cont = 0    
            for letra in resposta_hash:
                cont+=1 
                if(letra == "#"):
                    indi_inicio = cont + 3
                    indi_final = indi_inicio + 1
                    perdidos = str(resposta_hash[indi_inicio:indi_final])
                    perdidos = perdidos.strip()
                    perdidos = int(perdidos)

            cont = 0    
            for letra in resposta:
                cont+=1 
                if(letra == "%"):
                    indi_inicio = cont - 2
                    indi_final = indi_inicio + 1
                    perda_porc = str(resposta[indi_inicio:indi_final])
                    perda_porc = perda_porc.strip()
                    perda_porc = int(perda_porc)

            if(recebidos == 0 or perda_porc > 0): ## se não estiver pegando
                situacao = "Verificar"
                cliente = Cliente(empresa, id_vant, ip, situacao)
                lista_inativos.append(cliente)

            else:                    ## se estiver pegando
                situacao = "OK"
                cliente = Cliente(empresa, id_vant, ip, situacao)
                lista_ativos.append(cliente)

            print('Cliente {}/{}'.format(i, quant))
    return render_template('lista.html', titulo='Relatório', clientes_inativos=lista_inativos, 
    clientes_ativos=lista_ativos)



@app.route('/hospitais')
def hospitais():
    hospitais = pd.read_excel('hospitais.xlsx')

    quant_hosp = hospitais['LP 13'].count()

    hospitais_ativos = []
    hospitais_inativos = [] 
    for h in range(0, quant_hosp):
        ip_hosp = str(hospitais['IP_LOOPBACK'][h])
        ip_hosp = ip_hosp.replace('/32', "")
    
        if(ip_hosp != "-" and ip_hosp != None):
            lp_hosp = hospitais['LP 13'][h]
            id_vantive = hospitais['Vantive'][h]
            cliente_hosp = hospitais['Cliente Nome'][h]

            resposta_hosp = subprocess.run('ping {} -n 1'.format(ip_hosp))

            if(resposta_hosp.returncode != 0): ## se não estiver pegando
                situacao = "Verificar"
                cliente_hosp = Cliente_hosp(ip_hosp, cliente_hosp, lp_hosp, id_vantive, situacao)
                hospitais_inativos.append(cliente_hosp)

            else:                    ## se estiver pegando
                situacao = "OK"
                cliente_hosp = Cliente_hosp(ip_hosp, cliente_hosp, lp_hosp, id_vantive, situacao)
                hospitais_ativos.append(cliente_hosp)

            print('Cliente {}/{}'.format(h, quant_hosp))
            inativos = len(hospitais_inativos)
            ativos = len(hospitais_ativos)
            print("Recebidos: {}".format(ativos))
            print("Perdidos: {}".format(inativos))

    inativos = len(hospitais_inativos)
    ativos = len(hospitais_ativos)
    
    return render_template('hospitais.html', titulo='MONITORAMENTO DE HOSPITAIS', 
    hospitais_ativos=hospitais_ativos, hospitais_inativos=hospitais_inativos, 
    ativos=ativos, inativos=inativos)


@app.route('/teste')
def teste():
    con = mysql.connector.connect(host='127.0.0.1', database='clientes', 
                                  user='root', password='')
    if con.is_connected():
        db_info = con.get_server_info()
        print('Conectado ao servidor MySQL versão ', db_info)
        cursor = con.cursor()
        cursor.execute("select database();")
        linha = cursor.fetchone()
        print("Conectado ao banco de dados ", linha)
        
        query = "Select * from pings where id_programa = 1;"

        cursor.execute(query)

        linhas = cursor.fetchall()
        clientes = []
        for linha in linhas:
            cliente = Cliente(linha[1], linha[2], linha[3], 
            linha[4], linha[5], linha[6], linha[7] )
            clientes.append(cliente)
        if con.is_connected():
            cursor.close()
            con.close()
            print("Conexão ao MySQL foi encerrada.")

    return render_template('teste.html', clientes=clientes)

app.run(host='0.0.0.0', debug=False)
