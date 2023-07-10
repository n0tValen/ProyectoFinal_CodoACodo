
# del modulo flask importamos la clase Flask y los métodos jsonify y request
from flask import jsonify, request, Flask
from flask import render_template
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

# creamos el objeto app de la clase Flask
app = Flask(__name__)

# programa principal
if __name__ == '__main__':
    # ejecuta el servidor Flask en el puerto 5000
    app.run(port=3000,debug=True)

# el modulo cors es para que nos permita acceder desde el frontend al backend
CORS(app)
# configuramos la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymsql://root:030115@localhost/cafeteria'
# none
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# creamos el objeto db de la clase SQLAlquemy
db = SQLAlchemy(app)
# creamos el objeto ma de de la clase Marshmallow
ma = Marshmallow(app)

# Definimos las tablas correspondientes a nuestra base de datos y creamos el constructor de la clase para cada tabla


class Clientes(db.Model):  # la clase Clientes hereda de db.Model
    # definimos los campos de la tabla
    dni_cliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30))
    tel = db.Column(db.String(15))

    def __init__(self, dni_cliente, nombre, tel):
        self.dni_cliente = dni_cliente
        self.nombre = nombre
        self.tel = tel

class Pedidos(db.Model):
     cod_pedido = db.Column(db.Integer, primary_key=True)
     dni_cliente = db.Column(db.Integer, foreign_key=True)
     cod_producto = db.Column(db.Integer, foreign_key=True)
     fecha = db.Column(db.Integer)

     def __init__(self, cod_pedido, dni_cliente, cod_producto, fecha):
         self.cod_pedido = cod_pedido
         self.dni_cliente = dni_cliente
         self.cod_producto = cod_producto
         self.fecha = fecha

class Productos(db.Model):
    cod_pedido = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(40))
    precio = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    imagen = db.Column(db.String(40))

    def __init__(self, cod_pedido, nombre, precio,stock,imagen):
        self.cod_pedido = cod_pedido
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.imagen = imagen


# CREACION DE TODAS LAS TABLAS (CLIENTES, PEDIDOS, PRODUCTOS)
with app.app_context():
    db.create_all()

# DEFINIMOS LOS CAMPOS DE LA TABLA
# CLIENTES
class ClienteSchema(ma.Schema):
    class Meta:
        fields = ('dni_cliente', 'nombre', 'tel')


# El objeto cliente_schema es para traer un SOLO cliente
cliente_schema = ClienteSchema()
# El objeto clientes_schema es para traer MULTIPLES registros de clientes
clientes_schema = ClienteSchema(many=True)

# PEDIDOS
class PedidoSchema(ma.Schema):
   class Meta:
      fields = ('cod_pedido','dni_cliente','cod_producto','fecha')
 
pedido_schema = PedidoSchema()
pedidos_schema = PedidoSchema(many=True)

# PRODUCTOS
class ProductoSchema(ma.Schema):
   class Meta:
       fields = ('cod_pedido','nombre','precio', 'stock', 'imagen')

producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)

# ENDPOINTS / RUTAS (JSON)
@app.route('/')
def indenx():
    return 'servidor en pie :))'

# CLIENTES

@app.route('/clientes', methods=['GET'])
def get_clientes():
    all_clientes = Clientes.query.all() # el metodo query.all() lo hereda de db.Model
    result= clientes_schema.dump(all_clientes)#el metodo dump() lo hereda de ma.Schema y trae todos los registros de la tabla
    return jsonify(result) # retorna un JSON de todos los registros de la tabla

@app.route('/clientes', methods=['POST'])
def create_cliente():
    #request.json contiene el json que envio el pedido
    nombre = request.json['nombre']
    tel = request.json['tel']
    dni_cliente = request.json['dni_cliente'] 
    new_cliente = Clientes(nombre, tel,dni_cliente)
    db.session.add(new_cliente)
    db.session.commit()
    return clientes_schema.jsonify(new_cliente)

@app.route('/clientes/<dni>', methods=['GET'])
def get_cliente(dni):
    cliente = Clientes.query.get(dni)
    #nos retorna el JSON de un cliente recibido como parametro
    return clientes_schema.jsonify(cliente)


@app.route('/clientes/<dni>', methods=['DELETE'])
def delete_cliente(dni):
    cliente = Clientes.query.get(dni)
    db.session.delete(cliente)
    db.session.commit()
# nos devuelve un JSON con el registro eliminado
    return clientes_schema.jsonify(cliente)

@app.route('/clientes/<dni>', methods=['PUT'])
def update_producto(dni):
    cliente = Clientes.query.get(dni)
    cliente.dni_cliente = request.json['dni_cliente']
    cliente.nombre = request.json['nombre']
    cliente.tel = request.json['tel']
    db.session.commit()
    return clientes_schema.jsonify(cliente)

#PEDIDOS

@app.route('/pedidos', methods=['GET'])
def get_Pedidos():
    all_orders = Pedidos.query.all()
    result = pedidos_schema.dump(all_orders)
    return jsonify(result)


@app.route('/pedidos/<cod_pedido>', methods=['GET'])
def get_pedido(cod_pedido):
    pedido = Pedidos.query.get(cod_pedido)
    return pedidos_schema.jsonify(pedido)


@app.route('/pedidos/<cod_pedido>', methods=['DELETE'])
def delete_pedido(cod_pedido):
    pedido = Pedidos.query.get(cod_pedido)
    db.session.delete(pedido)
    db.session.commit()
    return pedidos_schema.jsonify(pedido)


@app.route('/pedidos', methods=['POST'])
def create_pedido():
    cod_pedido = request.json['cod_pedido']
    dni_cliente = request.json['dni_cliente']
    nro_pedido = request.json['nro_pedido']
    fecha = request.json['fecha']
    new_pedido = Pedidos(cod_pedido, dni_cliente, nro_pedido, fecha)
    db.session.add(new_pedido)
    db.session.commit()
    return pedidos_schema.jsonify(new_pedido)


@app.route('/pedidos/<cod_pedido>', methods=['PUT'])
def update_pedido(cod_pedido):
    pedido = Pedidos.query.get(cod_pedido)
    pedido.cod_pedido = request.jseon['cod_pedido']
    pedido.dni_cliente = request.json['dni_cliente']
    pedido.nro_pedido = request.json['nro_pedido']
    pedido.fecha = request.json['fecha']
    db.session.commit()
    return pedidos_schema.jsonify(pedido)

#PRODUCTOS

@app.route('/productos', methods=['GET'])
def get_Productos():
    all_products = Productos.query.all()
    result = productos_schema.dump(all_products)
    return jsonify(result)


@app.route('/productos/<cod_pedido>', methods=['GET'])
def get_producto(cod_pedido):
    producto = Productos.query.get(cod_pedido)
    return productos_schema.jsonify(producto)


@app.route('/productos/<cod_pedido>', methods=['DELETE'])
def delete_producto(cod_pedido):
    producto = Productos.query.get(cod_pedido)
    db.session.delete(producto)
    db.session.commit()
    return productos_schema.jsonify(producto)


@app.route('/productos', methods=['POST'])
def create_producto():
    cod_pedido = request.json['cod_pedido']
    nombre = request.json['nombre']
    precio = request.json['precio']
    stock = request.json['stock']
    imagen = request.json['imagen']
    new_producto = Productos(cod_pedido, nombre, precio,stock,imagen)
    db.session.add(new_producto)
    db.session.commit()
    return productos_schema.jsonify(new_producto)


@app.route('/productos/<cod_pedido>', methods=['PUT'])
def update_producto(cod_pedido):
    producto = Productos.query.get(cod_pedido)
    producto.cod_pedido = request.jseon['cod_pedido']
    producto.nombre = request.json['nombre']
    producto.precio = request.json['precio']
    producto.stock = request.json['stock']
    producto.imagen = request.json['imagen']
    db.session.commit()
    return productos_schema.jsonify(producto)
