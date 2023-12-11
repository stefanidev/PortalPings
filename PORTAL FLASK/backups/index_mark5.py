from flask import Flask, render_template, request, redirect, flash
import time
from subprocess import Popen, PIPE
import subprocess
import pandas as pd
from models import Cliente, Cliente_hosp
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'brigadeiro'

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

        query_hosp_ativo = """select count(*) from pings where tipo_cliente = 'HOSPITAIS'
        and situacao = true;"""
        query_hosp_inativo = """select count(*) from pings where tipo_cliente = 'HOSPITAIS'
        and situacao = false;"""
        query_estra_ativo = """select count(*) from pings where tipo_cliente = 'ESTRATÉGICOS' 
        and situacao = true"""
        query_estra_inativo = """select count(*) from pings where tipo_cliente = 'ESTRATÉGICOS' 
        and situacao = false"""

        cursor.execute(query_hosp_ativo)
        linhas = cursor.fetchall()
        for linha in linhas:
            hosp_ativos = int(linha[0])

        cursor.execute(query_hosp_inativo)
        linhas = cursor.fetchall()
        for linha in linhas:
            hosp_inativos = int(linha[0])
            
        cursor.execute(query_estra_ativo)
        linhas = cursor.fetchall()
        for linha in linhas:
            estra_ativos = int(linha[0])

        cursor.execute(query_estra_inativo)
        linhas = cursor.fetchall()
        for linha in linhas:
            estra_inativos = int(linha[0])


        if con.is_connected():
            cursor.close()
            con.close()
            print("Conexão ao MySQL foi encerrada.")
    
    return render_template('index.html', titulo='HOME', 
            cont_ativos=cont_ativos, cont_inativos=cont_inativos, horario=horario,
            hosp_ativos=hosp_ativos, hosp_inativos=hosp_inativos, estra_ativos=estra_ativos,
            estra_inativos=estra_inativos)

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
        
        query_ativos = "select * from pings where tipo_cliente = 'HOSPITAIS' and situacao = true;"

        cursor.execute(query_ativos)

        linhas = cursor.fetchall()

        ativos_hosp = []
        inativos_hosp = []

        for linha in linhas:   
            cliente = Cliente(linha[1], linha[2], linha[3], 
            linha[4], linha[5], linha[6], linha[7] )
            ativos_hosp.append(cliente)
            
        query_inativos = """select * from pings where tipo_cliente = 'HOSPITAIS' 
        and situacao = false order by vezes_off asc;"""  

        cursor.execute(query_inativos)

        linhas = cursor.fetchall()

        for linha in linhas:   
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
    
    
    return render_template('hospitais.html', titulo='HOSPITAIS', 
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
        
        query_ativos = "select * from pings where tipo_cliente = 'ESTRATÉGICOS' and situacao = true;"

        cursor.execute(query_ativos)

        linhas = cursor.fetchall()

        ativos_estra = []
        inativos_estra = []

        for linha in linhas:   
            cliente = Cliente(linha[1], linha[2], linha[3], 
            linha[4], linha[5], linha[6], linha[7] )
            ativos_estra.append(cliente)
            
        query_inativos = """select * from pings where tipo_cliente = 'ESTRATÉGICOS' 
        and situacao = false order by vezes_off asc;"""  

        cursor.execute(query_inativos)

        linhas = cursor.fetchall()

        for linha in linhas:   
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


@app.route('/cadastroDeCliente')
def cadastro_cliente():
    return render_template('cadastro.html', titulo="CADASTRO DE IP")


@app.route('/cadastrando', methods=['POST',])
def cadastrando():
    vantive = request.form['vantive']
    cliente = request.form['cliente']
    cliente = cliente.replace("'", " ")
    ip = request.form['ip']
    ip = ip.replace('/32', '')
    tipo_cliente = request.form['tipo_cliente']
    sla = request.form['sla']

    con = mysql.connector.connect(host='127.0.0.1', database='clientes', 
                              user='root', password='')
    if con.is_connected():
        db_info = con.get_server_info()
        print('Conectado ao servidor MySQL versão ', db_info)
        cursor = con.cursor()
        cursor.execute("select database();")
        linha = cursor.fetchone()
        print("Conectado ao banco de dados ", linha)

        insert = """insert into pings (id_vantive, cliente, ip, tipo_cliente, sla, situacao)
        values('{}', '{}', '{}', '{}', '{}', true);""".format(vantive, cliente, ip, tipo_cliente, sla)

        cursor.execute(insert)
        con.commit()

    if con.is_connected():
        cursor.close()
        con.close()
        print("Conexão ao MySQL foi encerrada.")    

    flash('Cliente {} cadastrado com sucesso!\nVantive: {}\nIP: {}'.format(cliente, vantive, ip))
    return redirect('/cadastroDeCliente')

@app.route('/edit')
def edit():
    con = mysql.connector.connect(host='127.0.0.1', database='clientes', 
                              user='root', password='')
    if con.is_connected():
        db_info = con.get_server_info()
        print('Conectado ao servidor MySQL versão ', db_info)
        cursor = con.cursor()
        cursor.execute("select database();")
        linha = cursor.fetchone()
        print("Conectado ao banco de dados ", linha)

        query = "select id_vantive, cliente, ip, situacao, tipo_cliente, sla, id_programa from pings;"
        
        """Aqui eu precisei colocar o ID_PROGRAMA no lugar de VEZES_OFF no objeto cliente porque o mesmo
        não tem este atributo criado na classe."""

        cursor.execute(query)

        linhas = cursor.fetchall()

        clientes = []
        for linha in linhas:
            cliente = Cliente(linha[0], linha[1], linha[2], linha[3], linha[4],
            linha[5], linha[6])
            clientes.append(cliente)

    if con.is_connected():
        cursor.close()
        con.close()
        print("Conexão ao MySQL foi encerrada.")

    return render_template('editar.html', titulo='Alterar e Excluir', clientes=clientes)


@app.route('/alterar', methods=['GET'],)
def alterar():
    id_programa = request['id_programa']
    con = mysql.connector.connect(host='127.0.0.1', database='clientes', 
                              user='root', password='')
    if con.is_connected():
        db_info = con.get_server_info()
        print('Conectado ao servidor MySQL versão ', db_info)
        cursor = con.cursor()
        cursor.execute("select database();")
        linha = cursor.fetchone()
        print("Conectado ao banco de dados ", linha)

        

    if con.is_connected():
        cursor.close()
        con.close()
        print("Conexão ao MySQL foi encerrada.")

app.run(host='0.0.0.0', debug=False)
