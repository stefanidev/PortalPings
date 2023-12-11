from flask import Flask, render_template, request, redirect
import time
from subprocess import Popen, PIPE
import subprocess
import pandas as pd
from models import Cliente, Cliente_hosp

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
                cliente = Cliente(empresa, ip, situacao)
                lista_inativos.append(cliente)

            else:                    ## se estiver pegando
                situacao = "OK"
                cliente = Cliente(empresa, ip, situacao)
                lista_ativos.append(cliente)

            print('Cliente {}/{}'.format(i, quant))
    return render_template('lista.html', titulo='Relatório', clientes_inativos=lista_inativos, 
    clientes_ativos=lista_ativos)



@app.route('/hospitais')
def teste():
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

            print("Essa é a resposta {}\n\n".format(resposta_hosp.returncode))

            resposta_hosp = str(subprocess.run('ping {} -n 1'.format(ip_hosp), stdout=PIPE))
            if("encontrar o host" in resposta_hosp):
                print('IP {} inválido'.format(ip_hosp))
            
            elif("Esgotado o tempo limite" in resposta_hosp):
                print("Esgotado o tempo limite")
                print(resposta_hosp)
    
            else:
                print(resposta_hosp)
                indi_recebido = resposta_hosp.find("Recebidos")
                recebido = resposta_hosp[indi_recebido + 12: indi_recebido + 13]
                recebido = recebido.strip()
                recebido = int(recebido)
                
                indi_perdido = resposta_hosp.find("Perdidos")
                perdido = resposta_hosp[indi_perdido + 10: indi_perdido + 12]
                perdido = perdido.strip()
                perdido = int(perdido)
                

                indi_perda_por = resposta_hosp.find("%")
                perda_por = resposta_hosp[indi_perda_por - 2 : indi_perda_por]
                perda_por = perda_por.strip()
                perda_por = str(perda_por)
                print("Esse é o perda por: {}".format(perda_por))
                if(recebido == 0 or perdido > 0): ## se não estiver pegando
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


app.run(host='0.0.0.0', debug=False)
