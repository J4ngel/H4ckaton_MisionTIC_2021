

$(document).ready(function() {
    const filter_Clientes = document.getElementById("tablaClientes_filter");
    const filter_Productos = document.getElementById("tablaProductos_filter");
    const filter_Empleados = document.getElementById("tablaEmpleados_filter");
    var tablaClientes = $('#tablaClientes').DataTable();
    var tablaProductos = $('#tablaProductos').DataTable();
    var tablaEmpleados = $('#tablaEmpleados').DataTable();

    if (filter_Clientes)
    {
        
        filter_Clientes.style.display = 'None';
        
    }
    
    if (filter_Productos)
    {
        filter_Productos.style.display = 'None';
    } 
    
    if (filter_Empleados)
    {
        filter_Empleados.style.display = 'None';
    }

    const input = document.querySelector('#input-search');
    input.addEventListener('keyup', (event) =>{
        tablaProductos.search(input.value).draw();
    });
  });