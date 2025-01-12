import tkinter as tk
import webbrowser as wb

# Agregamos las url de las playlist
playlists = {
    "playlist 1" : "https://open.spotify.com/track/0RLsjFdrB8S1NQRki5glvP?si=4343a42a0d1d46d5",
    "playlist 2" : "https://open.spotify.com/playlist/21QF7g2vZW6LsFrkoUqJMi?si=9c9dbad2a528402d"
}

def open_playlist(url):
    wb.open(url)

def show_menu_1():
    # Ocultar el menú secundario
    menu_2_frame.pack_forget()
    # Mostrar el segundo menú
    menu_1_frame.pack()

def show_menu_2():
    # Ocultar el menú inicial
    menu_1_frame.pack_forget()
    # Mostrar el segundo menú
    menu_2_frame.pack()

# Configuracion de la ventana principal
root = tk.Tk()
root.title('REGALO DE MI HERMOSA HIJA') # Tengo que entender como funciona esto

# Menú inicial
menu_1_frame = tk.Frame(root)
menu_1_label = tk.Label(menu_1_frame, text="Feliz año mi Juliette Hermosa!", font=("Helvetica", 16))
menu_1_label.pack(pady=10)
menu_1_button = tk.Button(menu_1_frame, text="Ver tus playlists", width=25, command=show_menu_2)
menu_1_button.pack(pady=10)
menu_1_frame.pack()

# Menú secundario con playlists
menu_2_frame = tk.Frame(root)
menu_2_label = tk.Label(menu_2_frame, text="Elige una playlist para abrir:", font=("Helvetica", 14))
menu_2_label.pack(pady=10)

#Crear botones para cada playlist
back_button = tk.Button(menu_2_frame, text="Back", width=30, command=show_menu_1)
back_button.pack(pady=10)
for name, url in playlists.items():
    btn = tk.Button(menu_2_frame, text=name, width=30, command=lambda u=url: open_playlist(u))
    btn.pack(pady=5)


# window = tk.Label(root,text='Feliz año mi Juliette Hermosa!')
# window.pack() # Permite hacer visible el widget

# # Creacion de un boton
# button = tk.Button(root,text='Canciones para tu vida',width=25,command=open_file_playlist)
# button.pack() # Permite hacer visible el boton

root.mainloop() # Esto sirve para mantener activo la ventana
