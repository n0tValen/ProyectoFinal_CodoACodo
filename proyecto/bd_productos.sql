
CREATE DATABASE IF NOT EXISTS cafeteria;
USE cafeteria; 
CREATE TABLE clientes (
    dni_cliente INT NOT NULL PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    tel VARCHAR(15) NULL
    
  );

CREATE TABLE productos (
    cod_producto INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nom_producto VARCHAR(20) NOT NULL,
    precio FLOAT NOT NULL,
   
);

CREATE TABLE pedidos (
    cod_pedido INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    dni_cliente INT NOT NULL,
    cod_producto INT NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (dni_cliente) REFERENCES clientes (dni_cliente),
    Foreign Key (cod_producto) REFERENCES productos (cod_producto)
);
 
INSERT into clientes(
  dni_cliente,
  nombre,
  tel)
VALUES
  (44665577,'Elena',11558899),
  (48776699,'Clara',11775522),
  (52336699,'Mateo',16889944)
        
SELECT ALL from clientes;

USE cafeteria;
ALTER TABLE productos ADD COLUMN  imagen VARCHAR(40) NOT NULL;
