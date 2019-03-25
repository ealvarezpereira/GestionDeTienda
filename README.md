# GestionDeTienda
Proyecto de la tercera evaluación de Desarrollo de Interfaces

Esta es una pequeña guía de uso de la aplicación.

1. Cuando inicias la aplicación Te lleva a una ventana con un login

Los usuarios son:

- Administrador -> Usuario para acceder a la parte de administración

- 1001 -> Usuario cliente para acceder a la parte de compras

También puedes crear un nuevo cliente en el boton "Registrar Usuario"

2. Ventanas de Administración / Compras:

- En la ventana compras seleccionas un producto del TreeView, el apartado de cantidad es un SpinButton editable.
Una vez terminas de seleccionar los productos si pulsas en "finalizar pedido" generas una factura simple.

- En la ventana de administración hay 3 botones.
  - El boton de gestionar usuarios permite crear usuarios, y mostrar los que hay en la base de datos.
  - El boton de gestionar productos permite crear productos, y mostrar los que hay en la base de datos.
  (Los dos permiten borrar productos/usuarios de la base.)
  - El boton de generar factura te permite generar una factura detallada del usuario que haya realizado alguna compra.
