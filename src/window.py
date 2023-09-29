# window.py
#
# Copyright 2023 Youpie
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GdkPixbuf
from PIL import Image

@Gtk.Template(resource_path='/org/gnome/Example/window.ui')
class FolderIconWindow(Adw.ApplicationWindow):
    select_1_id = Gtk.Template.Child()
    final = Gtk.Template.Child()

    __gtype_name__ = 'FolderIconWindow'

    label = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.make_action("select_folder",self.open_file_dialog)
        self.make_action("select_icon",self.open_file_dialog)
        self.make_action("generate",self.generate_image)

    def make_action(self, action, func):
        install_action = Gio.SimpleAction(name=action)
        install_action.connect("activate", func)
        self.add_action(install_action)

    def open_file_dialog(self, action, _):
        print(action)

    def generate_image(self, action, _):
        print("activated")
        img1 = Image.open(r"/home/youpie/Projects/Folder-icon/Pictures/folder.png")

        # Opening the secondary image (overlay image)
        img2 = Image.open(r"/home/youpie/Projects/Folder-icon/Pictures/test.jpg").convert("RGBA")
        img2.thumbnail((500,500))
        # Pasting img2 image on top of img1
        # starting at coordinates (0, 0)
        img1.paste(img2, (262,400), mask = img2)

        # Displaying the image
        img1.show()
        #image = Image.open("/home/youpie/Projects/Folder-icon/Pictures/folder.png")
        #image = image.convert('RGBA')
        pixbuf = GdkPixbuf.Pixbuf.new_from_data(
            img1.tobytes(),
            GdkPixbuf.Colorspace.RGB,
            True,
            8,
            img1.width,
            img1.height,
            img1.width * 4  # 3 bytes per pixel (RGB)
        )
        gtk_image = Gtk.Image.new_from_pixbuf(pixbuf)
        self.final.set_property('paintable', gtk_image.get_paintable())
