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
def pacientes():
	cursor = mysql.get_db().cursor()
	cursor.execute("SELECT * FROM paciente") #Muestra los pacientes desde la BD
	paciente_=cursor.fetchall()
	return render_template("plantilla.html", pacientes=paciente_)
	#en la plantilla leo los datos 

'''
@app.route('/vacunas') #Listado de vacunas
def vacunas():
	cursor = mysql.get_db().cursor()
	cursor.execute("SELECT * FROM paciente") #Muestra los pacientes desde la BD
	paciente_=cursor.fetchall()
	return render_template("plantilla.html", pacientes=paciente_)
'''
if __name__ == "__main__":
	app.run(debug=True)



