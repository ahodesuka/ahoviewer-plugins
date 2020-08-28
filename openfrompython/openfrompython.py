import gi
gi.require_version('Ahoviewer', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Ahoviewer, GObject, Gtk

class PythonHelloPlugin(Ahoviewer.WindowAbstract):

  # This is just an exmaple of using the open_file member function, using a dialog
  # here is obviously redundant because ahoviewer has it's own file chooser dialog.
  # A more practical plugin that uses the WindowAbstract class could be something
  # like a local (or online) manga library, similar to mcomix's library.
  def do_activate(self):
    self.dialog = Gtk.FileChooserDialog(
        title="Please choose a file",
        action=Gtk.FileChooserAction.OPEN)
    self.dialog.add_buttons(
        Gtk.STOCK_CANCEL,
        Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OPEN,
        Gtk.ResponseType.OK)

    response = self.dialog.run()
    if response == Gtk.ResponseType.OK:
      self.open_file(self.dialog.get_filename())

    self.dialog.destroy()

  def do_deactivate(self):
    pass
