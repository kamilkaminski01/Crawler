import tkinter as tk
from mysql_database import *

def partie_gui(choice):
    global partie
    if choice == 1:
        partie = get_partie()
        partie_status_label.config(text='Status: partie pobrane', fg='green')
    elif choice == 2:
        execute_partie(partie)
        partie_status_label.config(text='Status: partie dodane do bazy danych', fg='green')

def posiedzenia_gui(choice):
    global posiedzenia_dataframe
    if choice == 1:
        posiedzenia_dataframe = get_posiedzenia()
        posiedzenia_status_label.config(text='Status: posiedzenia pobrane', fg='green')
    elif choice == 2:
        execute_posiedzenia(posiedzenia_dataframe)
        posiedzenia_status_label.config(text='Status: posiedzenia dodane do bazy danych', fg='green')

def poslowie_gui(choice):
    global poslowie_dataframe
    if choice == 1:
        poslowie_dataframe = get_poslowie()
        poslowie_status_label.config(text='Status: posłowie pobrani', fg='green')
    elif choice == 2:
        execute_poslowie(poslowie_dataframe)
        poslowie_status_label.config(text='Status: poslowie dodani do bazy danych', fg='green')

def glosowania_gui(choice):
    global glosowania_dataframe
    if choice == 1:
        glosowania_dataframe = get_glosowania()
        glosowania_status_label.config(text='Status: głosowania pobrane', fg='green')
    elif choice == 2:
        execute_glosowania(glosowania_dataframe)
        glosowania_status_label.config(text='Status: głosowania dodane do bazy danych', fg='green')

def glosy_gui(choice):
    global glosy_dataframe

    id_posla_od = glosy_id_posla_text_box_od.get()
    id_posla_do = glosy_id_posla_text_box_do.get()

    id_pos_od = glosy_id_posiedzenia_text_box_od.get()
    id_pos_do = glosy_id_posiedzenia_text_box_do.get()

    if len(id_posla_od) == 1: id_posla_od = '00'+id_posla_od
    elif len(id_posla_od) == 2: id_posla_od = '0'+id_posla_od

    if len(id_posla_do) == 1: id_posla_do = '00'+id_posla_do
    elif len(id_posla_do) == 2: id_posla_do = '0'+id_posla_do

    if choice == 1:
        glosy_dataframe = get_glosy(id_posla_od, id_posla_do, id_pos_od, id_pos_do)
        glosy_status_label.config(text='Status: głosy pobrane', fg='green')
    elif choice == 2:
        execute_glosy(glosy_dataframe)
        glosy_status_label.config(text='Status: głosy dodane do bazy danych', fg='green')


bg_colour = '#EAD8D5'
padx = 10
font_label = ('TkMenuFont', 30)
font_status_label = ('TkMenuFont', 20)
font_button = ('TkMenuFont', 15)


root = tk.Tk()
canvas = tk.Canvas(root, width=800, height=600, bg=bg_colour)
canvas.grid(columnspan=5, rowspan=7, sticky='nesw')

root.title("Sejm Crawler")
root.eval("tk::PlaceWindow . center")

# PARTIE
partie_label = tk.Label(root, text='Partie', font=font_label, bg=bg_colour, fg='black')
partie_label.grid(column=0, row=0, padx=padx, sticky='w')

partie_wyszukaj_button = tk.Button(root, text='Wyszukaj', font=font_button, cursor='hand2', command=lambda: partie_gui(1))
partie_wyszukaj_button.grid(column=1, row=0)

partie_import_button = tk.Button(root, text='Importuj', font=font_button, cursor='hand2', command=lambda: partie_gui(2))
partie_import_button.grid(column=2, row=0)

partie_status_label = tk.Label(root, text='Status:', font=font_status_label, bg=bg_colour, fg='black')
partie_status_label.grid(column=3, row=0, padx=padx, sticky='w')

# POSŁOWIE
poslowie_label = tk.Label(root, text='Posłowie', font=font_label, bg=bg_colour, fg='black')
poslowie_label.grid(column=0, row=1, padx=padx, sticky='w')

poslowie_wyszukaj_button = tk.Button(root, text='Wyszukaj', font=font_button, cursor='hand2', command=lambda: poslowie_gui(1))
poslowie_wyszukaj_button.grid(column=1, row=1)

poslowie_import_button = tk.Button(root, text='Importuj', font=font_button, cursor='hand2', command=lambda: poslowie_gui(2))
poslowie_import_button.grid(column=2, row=1)

poslowie_status_label = tk.Label(root, text='Status:', font=font_status_label, bg=bg_colour, fg='black')
poslowie_status_label.grid(column=3, row=1, padx=padx, sticky='w')

# POSIEDZENIA
posiedzenia_label = tk.Label(root, text='Posiedzenia', font=font_label, bg=bg_colour, fg='black')
posiedzenia_label.grid(column=0, row=2, padx=padx, sticky='w')

posiedzenia_wyszukaj_button = tk.Button(root, text='Wyszukaj', font=font_button, cursor='hand2', command=lambda: posiedzenia_gui(1))
posiedzenia_wyszukaj_button.grid(column=1, row=2)

posiedzenia_import_button = tk.Button(root, text='Importuj', font=font_button, cursor='hand2', command=lambda: posiedzenia_gui(2))
posiedzenia_import_button.grid(column=2, row=2)

posiedzenia_status_label = tk.Label(root, text='Status:', font=font_status_label, bg=bg_colour, fg='black')
posiedzenia_status_label.grid(column=3, row=2, padx=padx, sticky='w')

# GŁOSOWANIA
glosowania_label = tk.Label(root, text='Głosowania', font=font_label, bg=bg_colour, fg='black')
glosowania_label.grid(column=0, row=3, padx=padx, sticky='w')

glosowania_wyszukaj_button = tk.Button(root, text='Wyszukaj', font=font_button, cursor='hand2', command=lambda: glosowania_gui(1))
glosowania_wyszukaj_button.grid(column=1, row=3)

glosowania_import_button = tk.Button(root, text='Importuj', font=font_button, cursor='hand2', command=lambda: glosowania_gui(2))
glosowania_import_button.grid(column=2, row=3)

glosowania_status_label = tk.Label(root, text='Status:', font=font_status_label, bg=bg_colour, fg='black')
glosowania_status_label.grid(column=3, row=3, padx=padx, sticky='w')

# GŁOSY
glosy_label = tk.Label(root, text='Głosy', font=font_label, bg=bg_colour, fg='black')
glosy_label.grid(column=0, row=4, padx=padx, sticky='w')

glosy_wyszukaj_button = tk.Button(root, text='Wyszukaj', font=font_button, cursor='hand2', command=lambda: glosy_gui(1))
glosy_wyszukaj_button.grid(column=1, row=4)

glosy_import_button = tk.Button(root, text='Importuj', font=font_button, cursor='hand2', command=lambda: glosy_gui(2))
glosy_import_button.grid(column=2, row=4)

glosy_status_label = tk.Label(root, text='Status:', font=font_status_label, bg=bg_colour, fg='black')
glosy_status_label.grid(column=3, row=4, padx=padx, sticky='w')

glosy_id_posla_label_od = tk.Label(root, text='ID posła od:', font=('TkMenuFont', 15), bg=bg_colour)
glosy_id_posla_label_od.grid(column=1, row=4, sticky='s')
glosy_id_posla_text_box_od = tk.Entry(root, width=9)
glosy_id_posla_text_box_od.grid(column=1, row=5, sticky='n')

glosy_id_posla_label_do = tk.Label(root, text='ID posła do:', font=('TkMenuFont', 15), bg=bg_colour)
glosy_id_posla_label_do.grid(column=2, row=4, sticky='s')
glosy_id_posla_text_box_do = tk.Entry(root, width=9)
glosy_id_posla_text_box_do.grid(column=2, row=5, sticky='n')

glosy_id_posiedzenia_label_od = tk.Label(root, text='ID posiedzenia od:', font=('TkMenuFont', 15), bg=bg_colour)
glosy_id_posiedzenia_label_od.grid(column=1, row=5, sticky='s')
glosy_id_posiedzenia_text_box_od = tk.Entry(root, width=12)
glosy_id_posiedzenia_text_box_od.grid(column=1, row=6, sticky='n')

glosy_id_posiedzenia_label_do = tk.Label(root, text='ID posiedzenia do:', font=('TkMenuFont', 15), bg=bg_colour)
glosy_id_posiedzenia_label_do.grid(column=2, row=5, sticky='s')
glosy_id_posiedzenia_text_box_do = tk.Entry(root, width=12)
glosy_id_posiedzenia_text_box_do.grid(column=2, row=6, sticky='n')

root.mainloop()