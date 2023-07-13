
# del modulo flask importamos la clase Flask y los métodos jsonify y request
from flask import jsonify, request, Flask
from flask import render_template
from flaskext.mysql import MySQL
# creamos el objeto app de la clase Flask
app = Flask(__name__)

# configuramos la base de datos, con el nombre el usuario y la clave
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymsql://root:root@localhost/empleados'
# none
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# creamos el objeto db de la clase SQLAlquemy

# Definimos las tablas correspondientes a nuestra base de datos y creamos el constructor de la clase para cada tabla


# ENDPOINTS / RUTAS (JSON)
@app.route('/')
def index():
    return 'servidor en pie!! :))'
# programa principal
if __name__ == '__main__':
    # ejecuta el servidor Flask en el puerto 5000
    app.run(port=5000,debug=True)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_BD']='empleados'
mysql.init_app(app)







