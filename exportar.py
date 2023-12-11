import pandas as pd
import mysql.connector
from mysql.connector import Error

con = mysql.connector.connect(host='127.0.0.1', database='sistema_sgfo', 
                              user='root', password='')

try:
    if con.is_connected():
        db_info = con.get_server_info()
        print('Conectado ao servidor MySQL versão ', db_info)
        cursor = con.cursor()
        cursor.execute("select database();")
        linha = cursor.fetchone()
        print("Conectado ao banco de dados ", linha)

        tabela = pd.read_excel('teste.xlsx')

            
            

              #print(f"{i} - SLA: {sla} - IP: {ip}")

    buscar = """SELECT `idATP`, `osp` FROM `sgfo` WHERE 1 """
    cursor= con.cursor()

    cursor.execute(buscar)
    idATP = []
    osp = []


    linhas = cursor.fetchall()
    print('numeros total de linhas: ', cursor.rowcount)
    total =  cursor.rowcount
    for linha in linhas:
       # print("id",linha[1])
        #print("nome",linha[2])

        idATP.append(linha[0])
        osp.append(linha[1])

    n=0
    for c in range(0,total):
        
        if c < total:
            i = c
            

            tabela.loc[c,"idATP"] = idATP[i] 
            tabela.loc[c,"osp"] = osp[i]


        c+=1
    print(tabela)
    tabela.to_excel('teste.xlsx', index = False)
    


    con.commit()
    cursor.close()

except Error as e:
    print(e)

finally:   
    if con.is_connected():
        cursor.close()
        con.close()
        print("Conexão ao MySQL foi encerrada.")