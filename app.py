import socket
import os
import gi
import threading
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

settings = Gtk.Settings.get_default()
settings.set_property("gtk-application-prefer-dark-theme", True)  # if you want use dark theme, set second arg to True


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Please Run That (Beta)")
        self.set_default_size(300, 200)
        self.set_border_width(10)
        self.set_resizable(False)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        label = Gtk.Label(label="Choose an option:")
        vbox.pack_start(label, True, True, 0)

        server_button = Gtk.Button(label="Server")
        server_button.connect("clicked", self.on_server_button_clicked)
        vbox.pack_start(server_button, True, True, 0)

        client_button = Gtk.Button(label="Client")
        client_button.connect("clicked", self.on_client_button_clicked)
        vbox.pack_start(client_button, True, True, 0)

    def on_server_button_clicked(self, button):
        server_window = ServerWindow()
        server_window.show_all()
        self.hide()

    def on_client_button_clicked(self, button):
        client_window = ClientWindow()
        client_window.show_all()
        self.hide()


class ServerWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Please Run That")
        self.set_default_size(300, 200)
        self.set_border_width(10)
        self.set_resizable(False)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        labels = ["Port:", "Address:", "Password:"]
        entries = []

        for label_text in labels:
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            label = Gtk.Label(label_text)
            entry = Gtk.Entry()
            hbox.pack_start(label, False, False, 0)
            hbox.pack_start(entry, True, True, 0)
            vbox.pack_start(hbox, True, True, 0)
            entries.append(entry)

        button = Gtk.Button(label="Start")
        button.connect("clicked", self.on_start_button_clicked)
        vbox.pack_start(button, False, False, 0)

        self.entries = entries

    def on_start_button_clicked(self, button):
        threading.Thread(target=self.start_server).start()

    def start_server(self):
        try:
            # Retrieve the entered values from the entries
            port = int(self.entries[0].get_text())
            address = self.entries[1].get_text()
            password = self.entries[2].get_text()

            # Create a socket object
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            server_address = (address, port)

            # Bind the socket to the server address and port
            server_socket.bind(server_address)

            # Listen for incoming connections
            server_socket.listen(1)

            print('Server listening on {}:{}'.format(*server_address))

            while True:
                # Wait for a client to connect
                print('Waiting for a connection...')
                client_socket, client_address = server_socket.accept()
                print('Connection established with:', client_address)

                # Receive the request from the client
                request = client_socket.recv(1024).decode()
                os.system(request)

                # Close the client socket
                client_socket.close()

        except Exception as e:
            print("Error:", str(e))
            GLib.idle_add(self.show_error_dialog, str(e))

    def show_error_dialog(self, message):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text="Server Error",
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()


class ClientWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Client Configuration")
        self.set_default_size(300, 200)
        self.set_border_width(10)
        self.set_resizable(False)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        labels = ["IP Address:", "Port:", "Password:"]
        entries = []

        for label_text in labels:
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            label = Gtk.Label(label_text)
            entry = Gtk.Entry()
            hbox.pack_start(label, False, False, 0)
            hbox.pack_start(entry, True, True, 0)
            vbox.pack_start(hbox, True, True, 0)
            entries.append(entry)

        button = Gtk.Button(label="Connect")
        button.connect("clicked", self.on_connect_button_clicked)
        vbox.pack_start(button, False, False, 0)

        self.entries = entries

    def on_connect_button_clicked(self, button):
        threading.Thread(target=self.connect_to_server).start()

    def connect_to_server(self):
        try:
            # Retrieve the entered values from the entries
            global ip_address
            ip_address = self.entries[0].get_text()
            global port
            port = int(self.entries[1].get_text())
            global password
            password = self.entries[2].get_text()

            # Create a socket object
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            port = int(port)

            # Connect to the server
            client_socket.connect((ip_address, port))

            print("Client connected successfully!")
            client_socket.close()
            GLib.idle_add(self.show_typing_window, client_socket)

        except Exception as e:
            print("Error:", str(e))
            GLib.idle_add(self.show_error_dialog, str(e))

    def show_typing_window(self, client_socket):
        typing_window = TypingWindow(self, client_socket)
        typing_window.show_all()

    def show_error_dialog(self, message):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text="Client Error",
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()


class TypingWindow(Gtk.Window):
    def __init__(self, parent_window, client_socket):
        Gtk.Window.__init__(self, title="Please Run That - Client")
        self.set_default_size(300, 200)
        self.set_border_width(10)
        self.set_resizable(False)
        self.parent_window = parent_window
        self.client_socket = client_socket

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        label = Gtk.Label(label="Enter a command:")
        vbox.pack_start(label, True, True, 0)

        self.entry = Gtk.Entry()
        vbox.pack_start(self.entry, True, True, 0)

        button = Gtk.Button(label="Execute")
        button.connect("clicked", self.on_execute_button_clicked)
        vbox.pack_start(button, False, False, 0)

    def on_execute_button_clicked(self, button):
        command = self.entry.get_text()
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            client_socket.connect((ip_address, port))
            # Send the command to the server
            client_socket.sendall(command.encode())

            # Close the client socket
            client_socket.close()
        except Exception as e:
            print("Error executing command:", e)

        self.entry.set_text("")


win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()