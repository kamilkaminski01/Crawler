import tkinter as tk
from mysql_database import *

bg_colour = '#EAD8D5'
padx = 20
font_label = ('TkMenuFont', 30)
font_status_label = ('TkMenuFont', 20)
font_button = ('TkMenuFont', 15)

root = tk.Tk()
canvas = tk.Canvas(root, width=800, height=600, bg=bg_colour)
canvas.grid(columnspan=5, rowspan=6, sticky='nesw')

root.title("Sejm Crawler")
root.eval("tk::PlaceWindow . center")

# Partie status label
partie_status_label = tk.Label(root, text='Status:', font=font_status_label, bg=bg_colour, fg='black')
partie_status_label.grid(column=3, row=0, padx=padx, sticky='e')

# Posiedzenia status label
posiedzenia_status_label = tk.Label(root, text='Status:', font=font_status_label, bg=bg_colour, fg='black')
posiedzenia_status_label.grid(column=3, row=2, padx=padx, sticky='e')

# Posłowie status label
poslowie_status_label = tk.Label(root, text='Status:', font=font_status_label, bg=bg_colour, fg='black')
poslowie_status_label.grid(column=3, row=1, padx=padx, sticky='e')

# Głosowania status label
glosowania_status_label = tk.Label(root, text='Status:', font=font_status_label, bg=bg_colour, fg='black')
glosowania_status_label.grid(column=3, row=3, padx=padx, sticky='e')

# Głosy status label
glosy_status_label = tk.Label(root, text='Status:', font=font_status_label, bg=bg_colour, fg='black')
glosy_status_label.grid(column=3, row=4, padx=padx, sticky='e')


def partia_gui(choice):
    global partie
    if choice == 1:
        partie = get_partie()
        partie_status_label.config(text='Status: partie pobrane')
    elif choice == 2: execute_partie(partie)

def posiedzenia_gui(choice):
    global posiedzenia_dataframe
    if choice == 1:
        posiedzenia_dataframe = get_posiedzenia()
        posiedzenia_status_label.config(text='Status: posiedzenia pobrane')
    elif choice == 2: execute_posiedzenia(posiedzenia_dataframe)

def poslowie_gui(choice):
    global poslowie_dataframe
    if choice == 1:
        poslowie_dataframe = get_poslowie()
        poslowie_status_label.config(text='Status: posłowie pobrani')
    elif choice == 2: execute_poslowie(poslowie_dataframe)

def glosowania_gui(choice):
    global glosowania_dataframe
    if choice == 1:
        glosowania_dataframe = get_glosowania()
        glosowania_status_label.config(text='Status: głosowania pobrane')
    elif choice == 2: execute_glosowania(glosowania_dataframe)

def glosy_gui(choice):
    global glosy_dataframe
    if choice == 1:
        glosy_dataframe = get_glosy()
        glosy_status_label.config(text='Status: głosy pobrane')
    elif choice == 2: execute_glosy(glosy_dataframe)


def load_partie():
    partie_label = tk.Label(root, text='Partie', font=font_label, bg=bg_colour, fg='black')
    partie_label.grid(column=0, row=0, padx=padx, sticky='w')

    partie_wyszukaj_button = tk.Button(root, text='Wyszukaj', font=font_button, cursor='hand2', command=lambda: partia_gui(1))
    partie_wyszukaj_button.grid(column=1, row=0)

    partie_import_button = tk.Button(root, text='Importuj', font=font_button, cursor='hand2', command=lambda: partia_gui(2))
    partie_import_button.grid(column=2, row=0)

def load_poslowie():
    poslowie_label = tk.Label(root, text='Posłowie', font=font_label, bg=bg_colour, fg='black')
    poslowie_label.grid(column=0, row=1, padx=padx, sticky='w')

    poslowie_wyszukaj_button = tk.Button(root, text='Wyszukaj', font=font_button, cursor='hand2', command=lambda: poslowie_gui(1))
    poslowie_wyszukaj_button.grid(column=1, row=1)

    poslowie_import_button = tk.Button(root, text='Importuj', font=font_button, cursor='hand2', command=lambda: poslowie_gui(2))
    poslowie_import_button.grid(column=2, row=1)

def load_posiedzenia():
    posiedzenia_label = tk.Label(root, text='Posiedzenia', font=font_label, bg=bg_colour, fg='black')
    posiedzenia_label.grid(column=0, row=2, padx=padx, sticky='w')

    posiedzenia_wyszukaj_button = tk.Button(root, text='Wyszukaj', font=font_button, cursor='hand2', command=lambda: posiedzenia_gui(1))
    posiedzenia_wyszukaj_button.grid(column=1, row=2)

    posiedzenia_import_button = tk.Button(root, text='Importuj', font=font_button, cursor='hand2', command=lambda: posiedzenia_gui(2))
    posiedzenia_import_button.grid(column=2, row=2)

def load_glosowania():
    glosowania_label = tk.Label(root, text='Głosowania', font=font_label, bg=bg_colour, fg='black')
    glosowania_label.grid(column=0, row=3, padx=padx, sticky='w')

    glosowania_wyszukaj_button = tk.Button(root, text='Wyszukaj', font=font_button, cursor='hand2', command=lambda: glosowania_gui(1))
    glosowania_wyszukaj_button.grid(column=1, row=3)

    glosowania_import_button = tk.Button(root, text='Importuj', font=font_button, cursor='hand2', command=lambda: glosowania_gui(2))
    glosowania_import_button.grid(column=2, row=3)

def load_glosy():
    glosy_label = tk.Label(root, text='Głosy', font=font_label, bg=bg_colour, fg='black')
    glosy_label.grid(column=0, row=4, padx=padx, sticky='w')

    glosy_wyszukaj_button = tk.Button(root, text='Wyszukaj', font=font_button, cursor='hand2', command=lambda: glosy_gui(1))
    glosy_wyszukaj_button.grid(column=1, row=4)

    glosy_import_button = tk.Button(root, text='Importuj', font=font_button, cursor='hand2', command=lambda: glosy_gui(2))
    glosy_import_button.grid(column=2, row=4)

load_partie()
load_poslowie()
load_posiedzenia()
load_glosowania()
load_glosy()

root.mainloop()