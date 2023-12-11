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
    con = mysql.connector.connect(host='127.0.0.1', database='clientes', 
                              user='root', password='')
    if con.is_connected():
        db_info = con.get_server_info()
        print('Conectado ao servidor MySQL versão ', db_info)
        cursor = con.cursor()
        cursor.execute("select database();")
        linha = cursor.fetchone()
        print("Conectado ao banco de dados ", linha)
        
        query = "Select * from pings;"

        cursor.execute(query)

        linhas = cursor.fetchall()

        ativos_hosp = []
        inativos_hosp = []

        for linha in linhas:
            situacao = linha[4]
            if(situacao):    
                cliente = Cliente(linha[1], linha[2], linha[3], 
                linha[4], linha[5], linha[6], linha[7] )
                ativos_hosp.append(cliente)
            else: 
                cliente = Cliente(linha[1], linha[2], linha[3], 
                linha[4], linha[5], linha[6], linha[7] )
                inativos_hosp.append(cliente)

        cont_ativos = len(ativos_hosp)
        cont_inativos = len(inativos_hosp)

        query_hora = "SELECT * FROM horarios;"

        cursor.execute(query_hora)

        horas = cursor.fetchall()

        for hora in horas:
            horario = hora[0]
            continue

        if con.is_connected():
            cursor.close()
            con.close()
            print("Conexão ao MySQL foi encerrada.")
    
    return render_template('index.html', titulo='MONITORAMENTOS', 
            cont_ativos=cont_ativos, cont_inativos=cont_inativos, horario=horario)



@app.route('/hospitais')
def hospitais():
    con = mysql.connector.connect(host='127.0.0.1', database='clientes', 
                              user='root', password='')
    if con.is_connected():
        db_info = con.get_server_info()
        print('Conectado ao servidor MySQL versão ', db_info)
        cursor = con.cursor()
        cursor.execute("select database();")
        linha = cursor.fetchone()
        print("Conectado ao banco de dados ", linha)
        
        query = "Select * from pings where tipo_cliente = 'HOSPITAIS';"

        cursor.execute(query)

        linhas = cursor.fetchall()

        ativos_hosp = []
        inativos_hosp = []

        for linha in linhas:
            situacao = linha[4]
            if(situacao):    
                cliente = Cliente(linha[1], linha[2], linha[3], 
                linha[4], linha[5], linha[6], linha[7] )
                ativos_hosp.append(cliente)
            else: 
                cliente = Cliente(linha[1], linha[2], linha[3], 
                linha[4], linha[5], linha[6], linha[7] )
                inativos_hosp.append(cliente)

        cont_ativos = len(ativos_hosp)
        cont_inativos = len(inativos_hosp)

        query_hora = "SELECT * FROM horarios;"

        cursor.execute(query_hora)

        horas = cursor.fetchall()

        for hora in horas:
            horario = hora[0]
            continue
    
        if con.is_connected():
            cursor.close()
            con.close()
            print("Conexão ao MySQL foi encerrada.")
    
    
    return render_template('hospitais.html', titulo='MONITORAMENTO DE HOSPITAIS', 
    ativos_hosp=ativos_hosp, inativos_hosp=inativos_hosp, 
    cont_ativos=cont_ativos, cont_inativos=cont_inativos, horario=horario)


@app.route('/estrategicos')
def estrategicos():
    con = mysql.connector.connect(host='127.0.0.1', database='clientes', 
                              user='root', password='')
    if con.is_connected():
        db_info = con.get_server_info()
        print('Conectado ao servidor MySQL versão ', db_info)
        cursor = con.cursor()
        cursor.execute("select database();")
        linha = cursor.fetchone()
        print("Conectado ao banco de dados ", linha)
        
        query = "Select * from pings where tipo_cliente = 'ESTRATÉGICOS';"

        cursor.execute(query)

        linhas = cursor.fetchall()

        ativos_estra = []
        inativos_estra = []

        for linha in linhas:
            situacao = linha[4]
            if(situacao):    
                cliente = Cliente(linha[1], linha[2], linha[3], 
                linha[4], linha[5], linha[6], linha[7] )
                ativos_estra.append(cliente)
            else: 
                cliente = Cliente(linha[1], linha[2], linha[3], 
                linha[4], linha[5], linha[6], linha[7] )
                inativos_estra.append(cliente)

        cont_ativos = len(ativos_estra)
        cont_inativos = len(inativos_estra)

        query_hora = "SELECT * FROM horarios;"

        cursor.execute(query_hora)

        horas = cursor.fetchall()

        for hora in horas:
            horario = hora[0]
            continue

        if con.is_connected():
            cursor.close()
            con.close()
            print("Conexão ao MySQL foi encerrada.")

    return render_template('estrategicos.html', titulo="ESTRATÉGICOS", ativos_estra=ativos_estra,
    inativos_estra=inativos_estra, cont_ativos=cont_ativos, cont_inativos=cont_inativos, horario=horario)

app.run(host='0.0.0.0', debug=False)
