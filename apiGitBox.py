# -*- coding: utf-8 -*-

from flask import Flask, jsonify
import urllib2
import dropbox
import json
import requests
import os

##Keys de Dropbox
app_key_dropbox = '5n1kdyjscee75nf'
app_secret_dropbox = 'gwro8d6vafi2feq'
accessToken = '4-vfoE-ELS0AAAAAAAAF6_oW2DBJnW7hWWkjukaAHXCxrrCxaauXpUjej1qJuGIH'
client = dropbox.client.DropboxClient(accessToken)

### Keys de GitHub
app_id_github = '246703917863a48df5fb'
app_secret_github = 'fe01ae79e1b65f5b669e144f9b4f9f569e976210'

app = Flask(__name__)

## ************************************************************************************
## GITHUB *****************************************************************************

# Obtiene la información de un usuario de GitHub y lo guarda en Dropbox
@app.route('/userinfo-to-dropbox/<string:owner_github>/', methods=['GET'])
def get_userinfo(owner_github):
    
    respo = urllib2.urlopen('https://api.github.com/users/'+owner_github+'?client_id='+app_id_github+'&client_secret='+app_secret_github)
    data = json.load(respo)
    with open("info", "w") as outfile:
        json.dump({'data': data}, outfile)
        
    f = open('info', 'rb')
    nom = '/'+owner_github+'_info.json'
    response = client.put_file(nom, f)
    return jsonify({'data': data})

@app.route('/userinfo-txt-to-dropbox/<string:owner_github>/', methods=['GET'])
def get_userinfo_txt(owner_github):
    textos = ['Id', 'Nombre', 'Login', 'Biografia', 'Email', 'Blog', 'Compañia', 'Url HTML', 'Fecha creación', 'Fecha actualización', 'Localización', 'Seguidores', 'Siguiendo', 'Gists públicos', 'Repositorios públicos', 'Gravatar ID', 'Hireable', 'Tipo', 'Administrador sitio', 'Url avatar', 'Url eventos', 'Url seguidores', 'Url siguiendo', 'Url gists', 'Url organización', 'Url eventos recibidos', 'Url repositorios', 'Url starred', 'Url suscriptores', 'Url']
    indices = ['id', 'name', 'login', 'bio', 'email', 'blog', 'company', 'html_url', 'created_at', 'updated_at', 'location', 'followers', 'following', 'public_gists', 'public_repos', 'gravatar_id', 'hireable', 'type', 'site_admin', 'avatar_url', 'events_url', 'followers_url', 'following_url', 'gists_url', 'organizations_url', 'received_events_url', 'repos_url', 'starred_url', 'subscriptions_url', 'url']
    
    respo = urllib2.urlopen('https://api.github.com/users/'+owner_github+'?client_id='+app_id_github+'&client_secret='+app_secret_github)
    data = json.load(respo)
    with open("info", "w") as outfile:
        outfile.write('Información del usuario\n')
        for i in range(30):
            outfile.write(textos[i]+': '+str(data[indices[i]])+'\n')

    f = open('info', 'rb')
    nom = '/'+owner_github+'_info.txt'
    client.put_file(nom, f)
    return jsonify({'data': data})


# Obtiene la información de un usuario, pero no guarda los datos en dropbox
@app.route('/userinfo/<string:owner_github>/', methods=['GET'])
def get_user(owner_github):
    respo = urllib2.urlopen('https://api.github.com/users/'+owner_github+'?client_id='+app_id_github+'&client_secret='+app_secret_github)
    return json.load(respo)


# Obtiene la información de los repositorios de un usuario
@app.route('/user_repos/<string:owner_github>/repos')
def get_user_repos(owner_github):
    respo = urllib2.urlopen('https://api.github.com/users/'+owner_github+'/repos?client_id='+app_id_github+'&client_secret='+app_secret_github)
    return json.load(respo)
    

# Obtiene los commits de un repositorio y los guarda en DropBox
@app.route('/commits-to-dropbox/<string:owner_github>/<string:repo_github>', methods=['GET'])
def get_commitsinfo(owner_github, repo_github):
    
    respo = urllib2.urlopen('https://api.github.com/repos/'+owner_github+'/'+repo_github+'/commits?client_id='+app_id_github+'&client_secret='+app_secret_github)
    data = json.load(respo)
    with open("commits", "w") as outfile:
        json.dump({'data': data}, outfile)
        
    f = open('commits', 'rb')
    nom = '/'+repo_github+'_'+owner_github+'_commits.json'
    response = client.put_file(nom, f)
    return jsonify({'data': data})
    

# Obtiene los archivos de un repositorio, los comprime en zip y los guarda en DropBox
@app.route('/download-repo/<string:owner_github>/<string:repo_github>/<string:compress_format>', methods=['GET'])
def download_repo(owner_github, repo_github, compress_format):

    respo = urllib2.urlopen('https://api.github.com/repos/'+owner_github+'/'+repo_github+'/'+compress_format+'?client_id='+app_id_github+'&client_secret='+app_secret_github)
    zipcontent= respo.read()
    with open("log.zip", 'w') as outfile:
        outfile.write(zipcontent)
    f = open('log.zip', 'rb')
    nom = '/'+repo_github+'_'+owner_github+'.zip'
    response = client.put_file(nom, f)
    return response

## ************************************************************************************
## DROPBOX ****************************************************************************

# Obtiene la información de un usuario de dropbox
@app.route('/dropbox/', methods=['GET'])
def get_dropboxinfo():
    return client.account_info()

# obtiene la información de la carpeta de la aplicación
@app.route('/dropbox_metadata/', methods=['GET'])
def get_dropboxfolder():
    return client.metadata('/')

# Descarga un archivo al directorio del usuario
@app.route('/download_file/<string:file_path>/', methods=['GET'])
def download_file(file_path):
    f, metadata = client.get_file_and_metadata(file_path)
    out = open(file_path, 'wb')
    out.write(f.read())
    out.close()
    os.system('mv '+file_path+' ~')

@app.route('/erase_file/<string:file_path>/', methods=['GET'])
def erase_file(file_path):
    client.file_delete(file_path)
    

# Manejo de error si metemos una dirección no válida
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)

