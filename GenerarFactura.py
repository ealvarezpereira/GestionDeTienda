import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from sqlite3 import dbapi2


class GenerarFactura(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Ventana de Facturas")
        