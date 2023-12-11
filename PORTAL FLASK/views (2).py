from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from main import app, db
from models import Excluidos, Pings, Horarios, Usuarios, Dados
from flask_googlecharts import PieChart
import subprocess
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import pytz

@app.route('/teste')
def teste():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    resposta = request.args.getlist('resposta', None)
    return render_template('teste.html', titulo='Testes', resposta=resposta, permissao=session['permissao'])

@app.route('/ajuda')
def ajuda():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    resposta = request.args.getlist('resposta', None)
    return render_template('ajuda.html', titulo='Ajuda', resposta=resposta, permissao=session['permissao'])


@app.route('/pingar', methods=['POST',])
def pingar():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    id_vantive = request.form['id_vantive']
    ip = request.form['ip']
    # Adiciona o campo "id_vantive"
    processo = subprocess.Popen('ping {}'.format(ip), stdout=subprocess.PIPE, text=True)
    linhas = processo.stdout.readlines()
    respostas = []
    resposta = []
    for linha in linhas:
        respostas.append(linha)
       
    for linha in respostas:
        linha = str(linha).replace("\n", "")
        resposta.append(linha)
    print(resposta)
    
    # Adiciona o registro na tabela Dados
    if 'usuario_logado' in session:
        usuario = session['usuario_logado']
        nome = session['nome']
    novo_dado = Dados(ip=ip, id_vantive=id_vantive, usuario=usuario, nome=nome)  # Adiciona os dados no bds
    db.session.add(novo_dado)
    db.session.commit()

    return redirect(url_for('teste', resposta=resposta))



@app.route('/')
def login():
    session['usuario_logado'] = None
    return render_template('login.html', titulo='Login')

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('login'))



@app.route('/autenticar', methods=['POST',])
def autenticar():
    re = request.form['re']
    usuario = Usuarios.query.filter_by(re=re).first()
    if(usuario):
        if(usuario.senha == request.form['senha']):
            session['usuario_logado'] = usuario.re
            session['permissao'] = usuario.permissao
            session['nome'] = usuario.nome 
            return redirect(url_for('teste'))
        else:
            flash('RE ou senha incorretos. Tente novamente.')
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
    

@app.route('/cadastroDeUsuario')
def cadastro_usuario():
    if(session['permissao'] != 'administrador'):
        return redirect(url_for('listar'))
    usuarios = Usuarios.query.order_by(Usuarios.id_usuario)
    return render_template('cad_usuarios.html', titulo='Cadastro Usuário', permissao=session['permissao'], usuarios=usuarios)

@app.route('/cadastrando_usuario', methods=['POST'])
def cadastrando_usuario():
    if(session['permissao'] != 'administrador'):
        return redirect(url_for('listar'))
    nome = request.form['nome']
    re = str(request.form['re'])
    senha = str(request.form['senha'])
    permissao = request.form['permissao']
    
    usuario = Usuarios(nome=nome, re=re, senha=senha, permissao=permissao)
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('cadastro_usuario'))

@app.route('/delete_usuario', methods=['POST', 'GET'])
def delete_usuario():
    if(session['permissao'] != 'administrador'):
        return redirect(url_for('listar'))
    re = request.args['re']
    Usuarios.query.filter_by(re=re).delete()
    db.session.commit()
    return redirect(url_for('cadastro_usuario'))
