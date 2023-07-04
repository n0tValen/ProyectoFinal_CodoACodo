#del modulo flask importar la clase Flask y los metodos jsonify,request
from flask import Flask ,jsonify ,request, render_template
#del modulo flask_cors importar CORS, se usa en una api rest, permite conectar desde el frontend a una api
from flask_cors import CORS
#modulos para el manejo de la base de datos
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__) #crea el objeto app de la clase Flask
CORS(app) #Modulo cors para que me permita acceder desde el frontend al backend

#ejecutar el servidor

#configuro la base de datos, con el nombre de usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:030115valen@localhost/postulantes'
#URI de la db. Driver de la DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False 

db = SQLAlchemy(app)  #crea el objecto db de la clase SQLAlchemy
ma = Marshmallow(app)  #crea el objeto ma de la clase Marshmallow

@app.route('/postulantes/')
#definir la tabla
class Postulantes(db.Model):   #clase Postulantes hereda de db.Model
    #Define campos de la tabla
    id= db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(100))
    mail= db.Column(db.String(200))
    imagen=db.Column(db.String(400))
    def __init__(self,nombre,mail,imagen):
        #crea el constructor de la clase
        self.nombre=nombre
        #no hace falta el id pq mysql lo crea sola por ser 'auto_incremento'
        self.mail=mail
        self.imagen=imagen

with app.app_context():
    db.create_all() #aca crea todas las tablas

class PostulantesSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','mail','imagen')

#el objecto postulante_schema es para traer un postulante
postulante_schema = PostulantesSchema()
#el objecto postulantes_schema es para traer múltiples registros de postulante
postulantes_schema = PostulantesSchema(many=True)

#crea las rutas para postulante

@app.route('/postulantes', methods=['GET'])
def get_postulante():
    all_postulantes = Postulantes.query.all()
    return postulantes_schema.jsonify(all_postulantes)

@app.route('/postulantes', methods=['POST'])
def create_postulante():
    nombre = request.json['nombre']
    mail = request.json['email']
    imagen = request.json['imagen']

    new_postulante=Postulantes(nombre,mail,imagen)
    db.session.add(new_postulante)
    db.session.commit()
    return postulante_schema.jsonify(new_postulante)

@app.route('/postulantes/id',methods=['GET'])
def get_postulante(id):
    postulante = Postulantes.query.get(id)
    return postulante_schema.jsonify(postulante)