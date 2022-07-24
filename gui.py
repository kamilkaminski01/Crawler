import tkinter as tk
from mysql_database import *

bg_colour = '#EAD8D5'
padx = 20
font_label = ('TkMenuFont', 30)
font_status_label = ('TkMenuFont', 20)
font_button = ('TkMenuFont', 15)

def essa():
    partie = get_partie()

def load_frame():
    frame.pack_propagate(False)

    tk.Label(frame, text='PARTIE', bg=bg_colour, fg='white', font=('TkMenuFont', 30)).pack()
    tk.Button(frame, text='Wyszukaj', fg='black', font=('TkMenuFont', 20), cursor='hand2').pack(pady=10)

    tk.Label(frame, text='POSIEDZENIA', bg=bg_colour, fg='white', font=('TkMenuFont', 30)).pack()
    tk.Button(frame, text='Wyszukaj', fg='black', font=('TkMenuFont', 20), cursor='hand2').pack(pady=10)

    tk.Label(frame, text='GŁOSOWANIA', bg=bg_colour, fg='white', font=('TkMenuFont', 30)).pack()
    tk.Button(frame, text='Wyszukaj', fg='black', font=('TkMenuFont', 20), cursor='hand2').pack(pady=10)

    tk.Label(frame, text='POSŁOWIE', bg=bg_colour, fg='white', font=('TkMenuFont', 30)).pack()
    tk.Button(frame, text='Wyszukaj', fg='black', font=('TkMenuFont', 20), cursor='hand2').pack(pady=10)

    tk.Label(frame, text='GŁOSY', bg=bg_colour, fg='white', font=('TkMenuFont', 30)).pack()
    tk.Button(frame, text='Wyszukaj', fg='black', font=('TkMenuFont', 20), cursor='hand2').pack(pady=10)

def load_partie():
    partie_label = tk.Label(root, text='Partie', font=font_label, bg=bg_colour, fg='black')
    partie_label.grid(column=0, row=0, padx=padx, sticky='w')

    partie_wyszukaj_button = tk.Button(root, text='Wyszukaj', font=font_button, cursor='hand2')
    partie_wyszukaj_button.grid(column=1, row=0)

    partie_import_button = tk.Button(root, text='Importuj', font=font_button, cursor='hand2', command=execute_partie())
    partie_import_button.grid(column=2, row=0)

    partie_status_label = tk.Label(root, text='Status:', font=font_status_label, bg=bg_colour, fg='black')
    partie_status_label.grid(column=3, row=0, padx=padx, sticky='e')

    # status_text_box = tk.Text(root, height=1, width=10, padx=20)
    # status_text_box.insert(1.0, 'Essa')
    # status_text_box.grid(column=4, row=0)


def load_poslowie():
    poslowie_label = tk.Label(root, text='Posłowie', font=font_label, bg=bg_colour, fg='black')
    poslowie_label.grid(column=0, row=1, padx=padx, sticky='w')

    poslowie_wyszukaj_button = tk.Button(root, text='Wyszukaj', font=font_button, cursor='hand2')
    poslowie_wyszukaj_button.grid(column=1, row=1)

    poslowie_import_button = tk.Button(root, text='Importuj', font=font_button, cursor='hand2')
    poslowie_import_button.grid(column=2, row=1)

    poslowie_status_label = tk.Label(root, text='Status:', font=font_status_label, bg=bg_colour, fg='black')
    poslowie_status_label.grid(column=3, row=1, padx=padx, sticky='e')

def load_posiedzenia():
    posiedzenia_label = tk.Label(root, text='Posiedzenia', font=font_label, bg=bg_colour, fg='black')
    posiedzenia_label.grid(column=0, row=2, padx=padx, sticky='w')

    posiedzenia_wyszukaj_button = tk.Button(root, text='Wyszukaj', font=font_button, cursor='hand2')
    posiedzenia_wyszukaj_button.grid(column=1, row=2)

    posiedzenia_import_button = tk.Button(root, text='Importuj', font=font_button, cursor='hand2')
    posiedzenia_import_button.grid(column=2, row=2)

    posiedzenia_status_label = tk.Label(root, text='Status:', font=font_status_label, bg=bg_colour, fg='black')
    posiedzenia_status_label.grid(column=3, row=2, padx=padx, sticky='e')

def load_glosowania():
    glosowania_label = tk.Label(root, text='Głosowania', font=font_label, bg=bg_colour, fg='black')
    glosowania_label.grid(column=0, row=3, padx=padx, sticky='w')

    glosowania_wyszukaj_button = tk.Button(root, text='Wyszukaj', font=font_button, cursor='hand2')
    glosowania_wyszukaj_button.grid(column=1, row=3)

    glosowania_import_button = tk.Button(root, text='Importuj', font=font_button, cursor='hand2')
    glosowania_import_button.grid(column=2, row=3)

    glosowania_status_label = tk.Label(root, text='Status:', font=font_status_label, bg=bg_colour, fg='black')
    glosowania_status_label.grid(column=3, row=3, padx=padx, sticky='e')

def load_glosy():
    glosy_label = tk.Label(root, text='Głosy', font=font_label, bg=bg_colour, fg='black')
    glosy_label.grid(column=0, row=4, padx=padx, sticky='w')

    glosy_wyszukaj_button = tk.Button(root, text='Wyszukaj', font=font_button, cursor='hand2')
    glosy_wyszukaj_button.grid(column=1, row=4)

    glosy_import_button = tk.Button(root, text='Importuj', font=font_button, cursor='hand2')
    glosy_import_button.grid(column=2, row=4)

    glosy_status_label = tk.Label(root, text='Status:', font=font_status_label, bg=bg_colour, fg='black')
    glosy_status_label.grid(column=3, row=4, padx=padx, sticky='e')


root = tk.Tk()
canvas = tk.Canvas(root, width=800, height=600, bg=bg_colour)
canvas.grid(columnspan=5, rowspan=6, sticky='nesw')

root.title("Sejm Crawler")
root.eval("tk::PlaceWindow . center")

load_partie()
load_poslowie()
load_posiedzenia()
load_glosowania()
load_glosy()

# frame = tk.Frame(root, width=500, height=600, bg=bg_colour)
# frame.grid(row=0, column=0, sticky='nesw')
# load_frame()

root.mainloop()