##del modulo flask importamos la clase Flask y los métodos jsonify y request
from flask import Flask, jsonify, request
from flask_cors import CORS 
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
##creamos el objeto app de la clase Flask
app= Flask(__name__)
##el modulo cors es para que nos permita acceder desde el frontend al backend
CORS(app)
##configuramos la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymsql://root:030115@localhost/cafeteria'
##none
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
#creamos el objeto db de la clase SQLAlquemy
data_base= SQLAlchemy(app)
#creamos el objeto ma de de la clase Marshmallow
ma= Marshmallow(app)

##programa principal    
if __name__=='__main__':
    ##ejecuta el servidor Flask en el puerto 5000
    app.run(debug=True, port=5000)

#Definimos la tabla correspondiente a nuestra base de datos
class Clientes(data_base.Model): ##la clase Clientes hereda de db.Model
    ##definimos los campos de la tabla
    dni_cliente= data_base.Column(data_base.Integer(), primary_key= True)
    nombre= data_base.Column(data_base.String(40))
    tel= data_base.Column(data_base.String(15))
    fecha_nac= data_base.Column(data_base.Date())
     
    #creamos el constructor de la clase 
    def __init__ (self, dni_cliente, nombre, tel, fecha_nac):
        self.dni_cliente= dni_cliente
        self.nombre= nombre
        self.tel= tel
        self.fecha_nac= fecha_nac
        
with app.app_context():
    #aqui creamos todas las tablas
    data_base.create_all()

class ClientesSchema(ma.Schema):
    class Meta:
        fields= ('dni_ciente', 'nombre', 'tel', 'fecha_nac')

#El objeto producto_schema es para traer un producto
clientes_schema= ClientesSchema()
##El objeto productos_schema es para traer multiples registros de producto
clientes_schema= ClientesSchema(many= True)

##creamos los endpoint o rutas (json)
@app.route('/clientes', methods= ['GET'])

def get_Clientes():
    ##el metodo query.all() lo hereda de data_base.Model
    all_clients= Clientes.query.all()
    ##el metodo dump() lo hereda de ma.Schema y trae todos los registros de la tabla
    result= clientes_schema.dump(all_clients)
    ##retorna un JSON de todos los registros de la tabla
    return jsonify(result)
    
@app.route('/clientes/<dni>',methods=['GET'])
def get_cliente(dni):
   cliente= Clientes.query.get(dni)
   ##nos retorna el JSON de un cliente recibido como parametro
   return clientes_schema.jsonify(cliente)
    
@app.route('/clientes/<dni>',methods= ['DELETE'])
def delete_cliente(dni):
    cliente= Clientes.query.get(dni)
    data_base.session.delete(cliente)
    data_base.session.commit()
    ##nos devuelve un JSON con el registro eliminado
    return clientes_schema.jsonify(cliente)

@app.route('/clientes', methods= ['POST']) 
def create_cliente():
    ##request.json contiene el json que envio el pedido
    dni_cliente= request.json['dni_cliente']
    nombre= request.json['nombre']
    tel= request.json['tel']
    fecha_nac= request.json['fecha_nac']
    new_cliente= Clientes(dni_cliente, nombre, tel, fecha_nac)
    data_base.session.add(new_cliente)
    data_base.session.commit()
    return clientes_schema.jsonify(new_cliente)

##creamos una ruta o endpoint    
@app.route('/clientes/<dni>', methods= ['PUT'])
def update_producto(dni):
    cliente= Clientes.query.get(dni)
    cliente.dni_cliente= request.json['nombre']
    cliente.nombre=request.json['nombre']
    cliente.tel= request.json['tel']
    cliente.fecha_nac= request.json['fecha_nac']
    data_base.session.commit()
    return clientes_schema.jsonify(cliente)

#Definimos la tabla correspondiente a nuestra base de datos

class Pedidos(data_base.Model):
    cod_pedido= data_base.Column(data_base.String(10), primary_key= True)
    dni_cliente= data_base.Column(data_base.Integer(), primary_key= True)  
    nro_pedido= data_base.Column(data_base.Integer(), primary_key= True)  
    fecha= data_base.Column(data_base.Date())

    def __init__ (self, cod_pedido, dni_cliente, nro_pedido, fecha):
        self.cod_pedido= cod_pedido
        self.dni_cliente= dni_cliente
        self.nro_pedido= nro_pedido
        self.fecha= fecha

with app.app_context():
    data_base.create_all()

class PedidosSchema(ma.Schema):
    class Meta:
        fields= ('cod_pedido', 'dni_cliente', 'nro_pedido', 'fecha')

pedidos_schema= PedidosSchema()
pedidos_schema= PedidosSchema(many= True) 

@app.route('/pedidos', methods= ['GET'])

def get_Pedidos():
    all_orders= Pedidos.query.all()
    result= pedidos_schema.dump(all_orders)
    return jsonify(result)
    
@app.route('/pedidos/<cod_pedido>',methods=['GET'])

def get_pedido(cod_pedido):
    pedido= Pedidos.query.get(cod_pedido)
    return pedidos_schema.jsonify(pedido)
    
@app.route('/pedidos/<cod_pedido>',methods=['DELETE'])

def delete_pedido(cod_pedido):
    pedido= Pedidos.query.get(cod_pedido)
    data_base.session.delete(pedido)
    data_base.session.commit()
    return pedidos_schema.jsonify(pedido)
    
@app.route('/pedidos', methods=['POST']) 
    
def create_pedido():
    cod_pedido= request.json['cod_pedido']
    dni_cliente= request.json['dni_cliente']
    nro_pedido= request.json['nro_pedido']
    fecha= request.json['fecha']
    new_pedido= Pedidos(cod_pedido, dni_cliente, nro_pedido, fecha)
    data_base.session.add(new_pedido)
    data_base.session.commit()
    return pedidos_schema.jsonify(new_pedido)
    
@app.route('/pedidos/<cod_pedido>' ,methods=['PUT'])
    
def update_pedido(cod_pedido):
    pedido= Pedidos.query.get(cod_pedido)
    pedido.cod_pedido= request.jseon['cod_pedido']
    pedido.dni_cliente= request.json['dni_cliente']
    pedido.nro_pedido= request.json['nro_pedido']
    pedido.fecha= request.json['fecha']
    data_base.session.commit()
    return pedidos_schema.jsonify(pedido)   

#Definimos la tabla correspondiente a nuestra base de datos

class Productos(data_base.Model):
    cod_pedido= data_base.Column(data_base.Integer(), primary_key= True)
    nombre= data_base.Column(data_base.String(40))
    precio= data_base.Column(data_base.Integer())
    
    def __init__ (self, cod_pedido, nombre, precio):
        self.cod_pedido= cod_pedido
        self.nombre= nombre
        self.precio= precio
    
with app.app_context():
    data_base.create_all()

class ProductosSchema(ma.Schema):
    class Meta: 
        fields= ('cod_pedido', 'nombre', 'precio', 'stock')

productos_schema= ProductosSchema()
productos_schema= ProductosSchema(many=True)  

@app.route('/productos', methods= ['GET'])

def get_Productos():
    all_products= Productos.query.all()
    result= productos_schema.dump(all_products)
    return jsonify(result)
    
@app.route('/productos/<cod_pedido>',methods=['GET'])

def get_producto(cod_pedido):
    producto= Productos.query.get(cod_pedido)
    return productos_schema.jsonify(producto)
    
@app.route('/productos/<cod_pedido>',methods=['DELETE'])
    
def delete_producto(cod_pedido):
    producto= Productos.query.get(cod_pedido)
    data_base.session.delete(producto)
    data_base.session.commit()
    return productos_schema.jsonify(producto)
    
@app.route('/productos', methods=['POST']) 

def create_producto():
    cod_pedido= request.json['cod_pedido']
    nombre= request.json['nombre']
    precio= request.json['precio']
    new_producto= Productos(cod_pedido, nombre, precio)
    data_base.session.add(new_producto)
    data_base.session.commit()
    return productos_schema.jsonify(new_producto)
    
@app.route('/productos/<cod_pedido>' ,methods=['PUT'])
    
def update_producto(cod_pedido):
    producto= Productos.query.get(cod_pedido)
    producto.cod_pedido= request.jseon['cod_pedido']
    producto.nombre=request.json['nombre']
    producto.precio=request.json['precio']
    data_base.session.commit()
    return productos_schema.jsonify(producto)

    


