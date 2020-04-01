Pre-requisitos:
	Base de datos MySQL: https://dev.mysql.com/downloads/installer/
	Heidi: https://www.heidisql.com/download.php
	Cmder: https://cmder.net/
	Python 3.8.2: https://www.python.org/downloads/windows/
	Pip: https://www.liquidweb.com/kb/install-pip-windows/
	SublimeText u otro editor de texto: https://www.sublimetext.com/

Instalación:
	Descargar el repositorio con la app: https://github.com/sebasquez/vacunatorio
	Ejecutar el SQL vacunas.sql en Heidi (archivo se encuentra en vacunatorio/) para crear y poblar la base de datos
	Ejecutar en cmder pip install -r requeriments.txt para descargar los paquetes necesarios para que funcione la app
	Si el usuario de la base de datos tiene clave, descomentar la línea 18 en vacunas.py : app.config['MYSQL_DATABASE_PASSWORD'] = 'pass'
	colocando la password correspondiente
	Ejecutar en cmder vacunas.py desde la carpeta en que se guardó la app para montar en localhost la aplicación


