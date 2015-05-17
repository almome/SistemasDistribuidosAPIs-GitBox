# -*- coding: utf-8 -*-

# Grado en Ingeniería informática
# Sistemas Distribuidos
# Curso 2014/2015
# Autores:
#   José Carlos Solís Lojo
#   Alejandro Rosado Pérez
#   Alexandra Morón Méndez
#   Juan Manuel Hidalgo Navarro

# Descripción fichero:
#   Aplicación web que prueba las funcionalidades de la api GitHub 
#   y presenta las diferentes plantillas según la navegación del usuario.

from flask import Flask, jsonify, render_template
import urllib2
import dropbox
import json
import requests
import apiGitBox

app = Flask(__name__)


# Clase de apoyo para facilitar la presentación de información en la web.
# Contiene la lista de nombres de repositorios de un usuario, sus urls, ids
# y descripciones.
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

####___________________________***_PÁGINAS_PRINCIPALES_***__________________________####

# Redirige a la portada de la aplicación web.
@app.route('/')
def main():
	return render_template('index.html')

# Redirige también a la portada de la aplicación web. Se permiten ambas opciones.
@app.route('/index/')
def index():
	return render_template('index.html')

# Al hacer clic en la pestaña "GitHub", redirige a la página buscar_usuario.html.
@app.route('/buscar_usuario/')
def buscar_usuario():
	return render_template('buscar_usuario.html')

# Al hacer clic en la pestaña "Autores", redirige a la página autores.html
@app.route('/autores/')
def pagina_autores():
	return render_template('autores.html')

# Al hacer clic en la pestaña "DropBox", se hacen llamadas a la api para obtener la información
# y archivos del usuario. Posteriormente se redirige a la página dropbox.html.
@app.route('/dropbox/')
def pagina_dropbox():
    usuario = apiGitBox.get_dropboxinfo()
    carpeta = apiGitBox.get_dropboxfolder()
    return render_template('dropbox.html', usuario=usuario, carpeta=carpeta, exito=0)


####___________________________***_PESTAÑA_GITHUB_***__________________________####

# Obtiene la información del usuario y sus repositorios.
# Se redirige a la página info_usuario.html con la información para mostrar.
@app.route('/usuario/<string:owner_github>/', methods=['GET'])
def get_userinfo(owner_github):
    
    # Utilizamos un bloque try por si el usuario no existe
    try:
        # Cargar la información del usuario
        usuario = apiGitBox.get_user(owner_github)
        # Cargar los repositorios del usuario
        repositorios = apiGitBox.get_user_repos(owner_github)
    
        n = 0; # n será el número de repositorios del usuario
        r = Repositorio()
        # Guardamos en r la información de todos los repositorio del usuario
        for dato in repositorios:
            r.getListaRepos().append(dato['name'])
            r.getListaUrls().append(dato['html_url'])
            r.getListaIds().append(dato['id'])
            r.getListaDescs().append(dato['description'])
            n += 1

        # Mostramos la página con la información del usuario y sus repositorios
        return render_template('info_usuario.html', data=usuario, clase=r, n=n)

    except urllib2.HTTPError as e:  # Si el usuario no existe
        # Mostramos mensaje de error
        return render_template('exito_subida.html', error='error', mensaje='El usuario introducido no ha obtenido resultados.')

# Exporta el contenido de un repositorio en formato zip a nuestra carpeta de DropBox
@app.route('/download-repo/<string:owner_github>/<string:repo_github>/<string:compress_format>/', methods=['GET'])
def descargar_repositorio(owner_github, repo_github, compress_format):
    apiGitBox.download_repo(owner_github, repo_github, compress_format)
    return render_template('exito_subida.html', error='exito', mensaje='Se ha realizado con exito la subida del repositorio a DropBox.')

# Exporta la información del usuario en formato json a nuestra carpeta de DropBox
@app.route('/userinfo-to-dropbox/<string:owner_github>/', methods=['GET'])
def descargar_usuario_json(owner_github):
    apiGitBox.get_userinfo(owner_github)
    return render_template('exito_subida.html', error='exito', mensaje='Se ha realizado con exito la subida los datos del usuario a DropBox.')

# Exporta la información del usuario en formato txt a nuestra carpeta de DropBox
@app.route('/userinfo-txt-to-dropbox/<string:owner_github>/', methods=['GET'])
def descargar_usuario_txt(owner_github):
    apiGitBox.get_userinfo_txt(owner_github)
    return render_template('exito_subida.html', error='exito', mensaje='Se ha realizado con exito la subida los datos del usuario a DropBox.')

# Exporta la información de los commits de un repositorio en formato json a nuestra carpeta de DropBox
@app.route('/commits-to-dropbox/<string:owner_github>/<string:repo_github>/', methods=['GET'])
def descargar_commits(owner_github, repo_github):
    apiGitBox.get_commitsinfo(owner_github, repo_github)
    return render_template('exito_subida.html', error='exito', mensaje='Se ha realizado con exito la subida de los commits a DropBox.')


####___________________________***_PESTAÑA_DROPBOX_***__________________________####

# Descarga un archivo de nuestra carpeta de dropbox al directorio del usuario.
@app.route('/download_file/<string:file_path>/')
def descargar_archivo(file_path):
    apiGitBox.download_file(file_path)
    return pagina_dropbox_exito('Archivo descargado exitosamente.')

# Elimina un archivo de nuestra carpeta de dropbox 
@app.route('/erase_file/<string:file_path>/')
def borrar_archivo(file_path):
    apiGitBox.erase_file(file_path)
    return pagina_dropbox_exito('Archivo eliminado exitosamente.')

# Función auxiliar que redirige a la pestaña de dropbox, pero que muestra un mensaje de exito o error.
def pagina_dropbox_exito(mensaje):
    usuario = apiGitBox.get_dropboxinfo()
    carpeta = apiGitBox.get_dropboxfolder()
    return render_template('dropbox.html', usuario=usuario, carpeta=carpeta, exito=mensaje)


#_____________________________***_MANEJO DE ERRORES_***_______________________________#

# Al introducir una dirección no válida se redirige a la pagina de errores.
@app.errorhandler(404)
def not_found(error):
    return render_template('exito_subida.html', error='error', mensaje='Error 404. La consulta realizada no ha obtenido resultados.')

# Main aplicación
if __name__ == '__main__':
    app.run(debug=True)
