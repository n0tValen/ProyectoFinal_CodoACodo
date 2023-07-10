function guardar() {
    let nom = document.getElementById("nombre").value
    let tel = parseFloat(document.getElementById("tel").value)
    let dni = parseInt(document.getElementById("dni_cliente").value)
    let f = parseInt(document.getElementById("fecha").value)
    let cod_pd = parseInt(document.getElementById("cod_pedido").value)
    let product = document.getElementById("nom_producto").value
    let precio = parseFloat(document.getElementById("precio").value)
    let cant = parseInt(document.getElementById("stock").value)
    let cod_pp = parseInt(document.getElementById("cod_producto").value)
    let img = document.getElementById("imagen").value
    


    let pedido = {
        nombre: nom,
        tel:tel,
        dni_cliente:dni,
        fecha:f,
        cod_pedido:cod_pd,
        nom_producto:product,
        precio: precio,
        stock: cant,
        cod_producto:cod_pp,
        imagen: img
    }
    let url = "http://127.0.0.1:3000/clientes"
    var options = {
        body: JSON.stringify(pedido),
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
    }
    fetch(url, options)
        .then(function () {
            console.log("creado")
            alert("Grabado")
            // Devuelve el href (URL) de la página actual
            window.location.href = "./producto.html";  
            // Handle response we get from the API
        })
        .catch(err => {
            //this.errored = true
            alert("Error al grabar" )
            console.error(err);
        })
}
