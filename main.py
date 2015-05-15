# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template
import urllib2
import urllib
import dropbox
import json
import requests
import apiGitBox

app = Flask(__name__)

class Repositorio:
    def __init__(self):
        self.lista_repos = []
        self.lista_urls = []
        self.lista_ids = []
        self.lista_desc = []
    def getListaRepos(self):
        return self.lista_repos
    def getListaUrls(self):
        return self.lista_urls
    def getListaIds(self):
        return self.lista_ids
    def getListaDescs(self):
        return self.lista_desc   


@app.route('/')
def main():
	return render_template('index.html')

@app.route('/index/')
def index():
	return render_template('index.html')

@app.route('/buscar_usuario/')
def buscar_usuario():
	return render_template('buscar_usuario.html')
	
@app.route('/autores/')
def pagina_autores():
	return render_template('autores.html')

@app.route('/download-repo/<string:owner_github>/<string:repo_github>/<string:compress_format>/', methods=['GET'])
def descargar_repositorio(owner_github, repo_github, compress_format):
    apiGitBox.download_repo(owner_github, repo_github, compress_format)
    return render_template('exito_subida.html', error='exito', mensaje='Se ha realizado con exito la subida del repositorio a DropBox.')

@app.route('/userinfo-to-dropbox/<string:owner_github>/', methods=['GET'])
def descargar_usuario(owner_github):
    apiGitBox.get_userinfo(owner_github)
    return render_template('exito_subida.html', error='exito', mensaje='Se ha realizado con exito la subida los datos del usuario a DropBox.')

@app.route('/commits-to-dropbox/<string:owner_github>/<string:repo_github>/', methods=['GET'])
def descargar_commits(owner_github, repo_github):
    apiGitBox.get_commitsinfo(owner_github, repo_github)
    return render_template('exito_subida.html', error='exito', mensaje='Se ha realizado con exito la subida de los commits a DropBox.')

@app.errorhandler(404)
def not_found(error):
    return render_template('exito_subida.html', error='error', mensaje='Error 404. La consulta realizada no ha obtenido resultados.')

@app.route('/usuario/<string:owner_github>/', methods=['GET'])
def get_userinfo(owner_github):

    data = apiGitBox.get_user(owner_github)

    avatar = data['avatar_url']
    bio = data['bio']
    blog = data['blog']
    company = data['company']
    created_at = data['created_at']
    email = data['email']
    events_url = data['events_url']
    followers = data['followers']
    followers_url = data['followers_url']
    following = data['following']
    following_url = data['following_url']
    gists_url = data['gists_url']
    gravatar_id = data['gravatar_id']
    hireable = data['hireable']
    html_url = data['html_url']
    ide = data['id']
    location = data['location']
    login = data['login']
    name = data['name']
    organizations_url = data['organizations_url']
    public_gists = data['public_gists']
    public_repos = data['public_repos']
    received_events_url = data['received_events_url']
    repos_url = data['repos_url']
    site_admin = data['site_admin']
    starred_url = data['starred_url']
    subscriptions_url = data['subscriptions_url']
    typeu = data['type']
    updated_at = data['updated_at']
    url = data['url']

    #Cargar los repositorios del usuario
    data = apiGitBox.get_user_repos(owner_github)
    
    lista_repos = []
    n = 0;
    r = Repositorio()
    for dato in data:
        r.getListaRepos().append(dato['name'])
        r.getListaUrls().append(dato['html_url'])
        r.getListaIds().append(dato['id'])
        r.getListaDescs().append(dato['description'])
        n += 1

    return render_template('info_usuario.html', avatar=avatar, bio=bio, blog=blog, company=company, created_at=created_at, email=email, followers=followers, following=following, html_url=html_url, location=location, login=login, name=name, public_gists=public_gists, public_repos=public_repos, updated_at=updated_at, clase=r, n=n)


@app.route('/dropbox/')
def pagina_dropbox():
    usuario = apiGitBox.get_dropboxinfo()
    carpeta = apiGitBox.get_dropboxfolder()
    return render_template('dropbox.html', usuario=usuario, carpeta=carpeta, exito=0)

def pagina_dropbox_exito(mensaje):
    usuario = apiGitBox.get_dropboxinfo()
    carpeta = apiGitBox.get_dropboxfolder()
    return render_template('dropbox.html', usuario=usuario, carpeta=carpeta, exito=mensaje)

@app.route('/download_file/<string:file_path>/')
def descargar_archivo(file_path):
    apiGitBox.download_file(file_path)
    return pagina_dropbox_exito('Archivo descargado exitosamente.')

@app.route('/erase_file/<string:file_path>/')
def borrar_archivo(file_path):
    apiGitBox.erase_file(file_path)
    return pagina_dropbox_exito('Archivo eliminado exitosamente.')



if __name__ == '__main__':
    app.run(debug=True)
