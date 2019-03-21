import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from RegistrarUsuario import RegistrarUsuario
from VentanaAdmin import VentanaAdmin
from VentanaCompras import VentanaCompras
from sqlite3 import dbapi2


class VentanaPrincipal(Gtk.Window):
    """
    Clase VentanaPrincipal donde el usuario se identifica.

    Métodos de la clase:

    __init__ -> Constructor de la clase
    on_boRegistrarse_clicked -> Boton para registrar cliente
    on_boLogin_clicked -> Boton para iniciar sesión
    """

    def __init__(self):
        """
        Método que crea la interfaz del login.

        Componentes:
        :param cajaComponentes: Caja que contiene todos los componentes
        :param lblUsuario: Etiqueta usuario
        :param txtUsuario: Entrada de texto para introducir el usuario
        :param boRegistrarse: Boton para registrar usuario
        :param boLogin: Boton para iniciar sesion
        :param grid: componente que da forma de visualizacion
        """
        Gtk.Window.__init__(self, title="Proyecto de clase")

        cajaComponentes = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        lblUsuario = Gtk.Label("Usuario:")

        self.txtUsuario = Gtk.Entry()

        boRegistrarse = Gtk.Button("Registrarse")
        boLogin = Gtk.Button("Login")

        boRegistrarse.connect("clicked", self.on_boRegistrarse_clicked)
        boLogin.connect("clicked", self.on_boLogin_clicked)

        grid = Gtk.Grid()
        grid.set_column_spacing(20)
        grid.set_row_spacing(20)

        grid.attach(lblUsuario, 0, 0, 1, 1)

        grid.attach(self.txtUsuario, 1, 0, 1, 1)

        grid.attach_next_to(boLogin, lblUsuario, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(boRegistrarse, boLogin, Gtk.PositionType.RIGHT, 1, 2)

        cajaComponentes.add(grid)

        self.connect("destroy", Gtk.main_quit)
        self.add(cajaComponentes)
        self.show_all()

    def on_boRegistrarse_clicked(self, boton):
        """

        :param boton: Parametro que recibe el metodo
        :return: None

        Llama a la clase que registra un usuario
        """
        RegistrarUsuario()

    def on_boLogin_clicked(self, boton):
        """

        :param boton: Parametro que recibe el metodo
        :return: None

        Si el usuario que recibe el TextEntry es "Administrador" llama a la clase VentanaAdmin() que administra
        la parte del administrador.

        Por el contrario comprueba si el usuario está en la base de datos y si es así loguea, si no cambia el color
        del texto del Entry a rojo y muestra que el usuario es incorrecto
        """

        if self.txtUsuario.get_text() == "Administrador":
            VentanaAdmin()
        else:
            self.bbdd = dbapi2.connect("TiendaInformatica.db")
            self.cursor = self.bbdd.cursor()
            self.cursor.execute("select numc from clientes where numc = ?", [self.txtUsuario.get_text()])

            valor = self.cursor.fetchone()
            # Valor recibe el resultado del cursor, si no recibe nada es que no existe el usuario en la base de datos.
            if valor is None:
                COLOR_INVALID = Gdk.color_parse('#de1212')
                self.txtUsuario.modify_fg(Gtk.StateFlags.NORMAL, COLOR_INVALID)
                print("Usuario Incorrecto")
            else:
                numc = valor[0]
                VentanaCompras(numc)


if __name__ == "__main__":
    VentanaPrincipal()
Gtk.main()
