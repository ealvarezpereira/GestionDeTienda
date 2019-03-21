import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from sqlite3 import dbapi2


class VentanaCompras(Gtk.Window):

    """
    Clase VentanaCompras en la que los clientes pueden comprar artículos

    Métodos de la clase:

    __init__ -> Constructor de la clase
    on_amount_edited -> Método que cambia el valor al campo "Cantidad" de los productos en el TreeView
    on_boComprar_clicked -> Método que añade la compra del cliente a la base de datos.
    """

    def __init__(self, nCliente):

        """
        Constructor que genera la interfaz del apartado de compras
        :param nCliente: Número de cliente que ha iniciado sesión recibido de la clase Login
        """
        Gtk.Window.__init__(self, title="Ventana de Compras")

        self.cajaProductos = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        """
        Iniciamos la conexión a la base de datos.
        :param bbdd: Parámetro que conecta a la base de datos
        :param cursor: Cursor con el que recibimos datos de la base de datos.
        Seleccionamos todos los datos de la tabla productos
        """

        self.bbdd = dbapi2.connect("TiendaInformatica.db")
        self.cursor = self.bbdd.cursor()
        self.cursor.execute("select * from productos")

        """
        Creamos un modelo al que le pasamos los tipos de valores de cada dato de la tabla
        :param modelo: Lista que recibe los datos de la tabla para añadirlo al TreeView
        """
        self.modelo = Gtk.ListStore(int, str, int, int)

        """
        Rellenamos el modelo recorriendo el cursor con un for
        """
        for rellenarModelo in self.cursor:
            codigo = rellenarModelo[0]
            nombre = rellenarModelo[1]
            precio = rellenarModelo[3]
            self.modelo.append([codigo, nombre, precio, 1])

        """
        :param vista: TreeView que contendrá los productos
        :param celdaText: CellRendererText que recibirá los valores
        :param columnaCodigo: columna del TreeView que contiene el codigo
        :param columnaNombre: columna del TreeView que contiene el nombre
        :param columnaPrecio: columna del TreeView que contiene el precio
        :param columnaCantidad: columna del TreeView que contiene la cantidad.
        """
        self.vista = Gtk.TreeView()

        celdaText = Gtk.CellRendererText()
        columnaCodigo = Gtk.TreeViewColumn('Codigo', celdaText, text=0)
        self.vista.append_column(columnaCodigo)

        celdaText2 = Gtk.CellRendererText(xalign=1)
        columnaNombre = Gtk.TreeViewColumn('Nombre', celdaText2, text=1)
        self.vista.append_column(columnaNombre)

        celdaText3 = Gtk.CellRendererText(xalign=1)
        columnaPrecio = Gtk.TreeViewColumn('Precio', celdaText3, text=2)
        self.vista.append_column(columnaPrecio)

        """
        renderer_spin: Es un SpinButton que lo que hace es poder sumar +1 o restar -1 la cantidad.
        Se le establece la propiedrad adjustement.
        """

        renderer_spin = Gtk.CellRendererSpin()
        renderer_spin.connect("edited", self.on_amount_edited)
        renderer_spin.set_property("editable", True)

        adjustment = Gtk.Adjustment(0, 0, 100, 1, 10, 0)
        renderer_spin.set_property("adjustment", adjustment)

        columnaCantidad = Gtk.TreeViewColumn('Cantidad', renderer_spin, text=3)
        self.vista.append_column(columnaCantidad)

        self.vista.set_model(self.modelo)

        """
        Hacemos que la variable nCliente pase a ser variable self de la clase
        """
        self.codcli = nCliente
        boComprar = Gtk.Button("Comprar")
        boComprar.connect('clicked', self.on_boComprar_clicked)

        self.cajaProductos.pack_start(self.vista, True, True, 0)
        self.cajaProductos.pack_start(boComprar, True, True, 0)
        self.add(self.cajaProductos)
        self.show_all()

    def on_amount_edited(self, widget, path, value):
        """
        Método que establece la cantidad en el TreeView cuando la cambias
        :param widget: Componente en sí
        :param path: Puntero en el que está situado el cursor
        :param value: Valor que recibe del SpinButton
        :return: None
        A ese componente del modelo se le asigna el valor que hemos editado
        """
        self.modelo[path][3] = int(value)

    def on_boComprar_clicked(self, boton):
        """
        Método que introduce lo que quieres comprar en la base de datos, en la tabla "factura"
        :param boton: Parametro que recibe el metodo
        :return: None

        Establecemos la conexion con la base de datos, creamos el puntero e introducimos el valor en la tabla
        """
        self.bbdd = dbapi2.connect("TiendaInformatica.db")
        self.cursor = self.bbdd.cursor()

        seleccion = self.vista.get_selection()

        self.modelo, puntero = seleccion.get_selected()

        # Si no hay ningún puntero seleccionado que no haga nada, si lo hay que lo meta en la tabla.
        if puntero is not None:
            codpr = self.modelo[puntero][0]
            cantidad = self.modelo[puntero][3]
            self.cursor.execute("insert into factura values(?,?,?)", (self.codcli, codpr, cantidad))
            self.bbdd.commit()
