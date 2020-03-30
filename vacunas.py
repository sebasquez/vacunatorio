import requests
import json
from flask import Flask, render_template, jsonify, request
from flaskext.mysql import MySQL
import pymysql
import pymysql.cursors

#pip install -r requeriments.txt
app = Flask(__name__)
app.config["MYSQL_DATABASE_USER"] = "root"    #Usuario de la BD
app.config["MYSQL_DATABASE_DB"]  = "vacunatorio" #Nombre de mi base de datos para conectarme
app.config['MYSQL_DATABASE_PASSWORD'] = '1508' #la clave de mi usuario, en vacunas.sql está mi código de la bd
mysql = MySQL(app)

mysql.connect_args["autocommit"] = True #Guardar cambios en la BD de forma automatica
mysql.connect_args["cursorclass"] = pymysql.cursors.DictCursor #Transforma las tuplas a diccionarios en los cursores 	


@app.route('/')#Pagina inicio donde estan listados los pacientes
def inicio():
	#dejar esta pagina como el menú inicial
	#en la plantilla leo los datos 
	return render_template("index.html")


@app.route('/addVacuna') #Listado de vacunas
def vacunarPaciente():
	cursor = mysql.get_db().cursor()
	cursor.execute("SELECT * FROM paciente") #Muestra los pacientes desde la BD
	paciente=cursor.fetchall()
	cursor_vacuna = mysql.get_db().cursor()
	
	cursor_vacuna.execute("SELECT * FROM vacuna") #Muestra los pacientes desde la BD
	vacuna=cursor_vacuna.fetchall()

	return render_template("addVacuna.html",pacientes=paciente,vacunas=vacuna)

if __name__ == "__main__":
	app.run(debug=True)



