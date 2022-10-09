import tkinter as tk
from datetime import timedelta
from timeit import default_timer as timer

from database.executes import (execute_deputies, execute_parties,
                               execute_sittings, execute_votes,
                               execute_votings)
from html_scraper import (get_deputies, get_parties, get_sittings, get_votes,
                          get_votings)


def parties_gui(choice):
    global parties
    start = timer()
    if choice == 1:
        parties = get_parties()
        parties_status_label.config(text='Status: partie pobrane', fg='green')
    elif choice == 2:
        execute_parties(parties)
        parties_status_label.config(text='Status: partie dodane do bazy danych', fg='green')
    end = timer()
    duration = str(timedelta(seconds=end - start))[:-7]
    parties_time_label.config(text=f"Czas: {duration}")


def deputies_gui(choice):
    global deputies_dataframe
    start = timer()
    if choice == 1:
        deputies_dataframe = get_deputies()
        deputies_status_label.config(text='Status: posłowie pobrani', fg='green')
    elif choice == 2:
        execute_deputies(deputies_dataframe)
        deputies_status_label.config(text='Status: poslowie dodani do bazy danych', fg='green')
    end = timer()
    duration = str(timedelta(seconds=end - start))[:-7]
    deputies_time_label.config(text=f"Czas: {duration}")


def sittings_gui(choice):
    global sittings_dataframe
    start = timer()
    if choice == 1:
        sittings_dataframe = get_sittings()
        sittings_status_label.config(text='Status: posiedzenia pobrane', fg='green')
    elif choice == 2:
        execute_sittings(sittings_dataframe)
        sittings_status_label.config(text='Status: posiedzenia dodane do bazy danych', fg='green')
    end = timer()
    duration = str(timedelta(seconds=end - start))[:-7]
    sittings_time_label.config(text=f"Czas: {duration}")


def votings_gui(choice):
    global votings_dataframe
    start = timer()
    if choice == 1:
        votings_dataframe = get_votings()
        votings_status_label.config(text='Status: głosowania pobrane', fg='green')
    elif choice == 2:
        execute_votings(votings_dataframe)
        votings_status_label.config(text='Status: głosowania dodane do bazy danych', fg='green')
    end = timer()
    duration = str(timedelta(seconds=end - start))[:-7]
    votings_time_label.config(text=f"Czas: {duration}")


def votes_gui(choice):
    global votes_dataframe
    start = timer()

    id_deputy_from = votes_id_deputy_text_box_from.get()
    id_deputy_to = votes_id_deputy_text_box_to.get()
    id_sitting_from = votes_id_sitting_text_box_from.get()
    id_sitting_to = id_sitting_text_box_to.get()

    if len(id_deputy_from) == 1:
        id_deputy_from = f"00{id_deputy_from}"
    elif len(id_deputy_from) == 2:
        id_deputy_from = f"0{id_deputy_from}"

    if len(id_deputy_to) == 1:
        id_deputy_to = f"00{id_deputy_to}"
    elif len(id_deputy_to) == 2:
        id_deputy_to = f"0{id_deputy_to}"

    if choice == 1:
        votes_dataframe = get_votes(id_deputy_from, id_deputy_to, id_sitting_from, id_sitting_to)
        votes_status_label.config(text='Status: głosy pobrane', fg='green')
    elif choice == 2:
        execute_votes(votes_dataframe)
        votes_status_label.config(text='Status: głosy dodane do bazy danych', fg='green')

    end = timer()
    duration = str(timedelta(seconds=end - start))[:-7]
    votes_time_label.config(text=f"Czas: {duration}")


bg_colour = '#EAD8D5'
padx = 10
font_label = ('TkMenuFont', 30)
font_status_label = ('TkMenuFont', 20)
font_button = ('TkMenuFont', 15)
cursor = 'hand2'


root = tk.Tk()
canvas = tk.Canvas(root, width=800, height=600, bg=bg_colour)
canvas.grid(columnspan=5, rowspan=7, sticky='nesw')

root.title("Gov Crawler")
root.eval("tk::PlaceWindow . center")

# PARTIE
partie_label = tk.Label(root, text='Partie', font=font_label, bg=bg_colour, fg='black')
partie_label.grid(column=0, row=0, padx=padx, sticky='w')

partie_wyszukaj_button = tk.Button(root, text='Wyszukaj', font=font_button, cursor=cursor, command=lambda: parties_gui(1))
partie_wyszukaj_button.grid(column=1, row=0)

partie_import_button = tk.Button(root, text='Importuj', font=font_button, cursor=cursor, command=lambda: parties_gui(2))
partie_import_button.grid(column=2, row=0)

parties_status_label = tk.Label(root, text='Status:', font=font_status_label, bg=bg_colour, fg='black')
parties_status_label.grid(column=3, row=0, padx=padx, sticky='w')

parties_time_label = tk.Label(root, text='Czas: ', font=font_status_label, bg=bg_colour, fg='black')
parties_time_label.grid(column=3, row=0, padx=padx, sticky='ws')

# POSŁOWIE
poslowie_label = tk.Label(root, text='Posłowie', font=font_label, bg=bg_colour, fg='black')
poslowie_label.grid(column=0, row=1, padx=padx, sticky='w')

poslowie_wyszukaj_button = tk.Button(root, text='Wyszukaj', font=font_button, cursor=cursor, command=lambda: deputies_gui(1))
poslowie_wyszukaj_button.grid(column=1, row=1)

poslowie_import_button = tk.Button(root, text='Importuj', font=font_button, cursor=cursor, command=lambda: deputies_gui(2))
poslowie_import_button.grid(column=2, row=1)

deputies_status_label = tk.Label(root, text='Status:', font=font_status_label, bg=bg_colour, fg='black')
deputies_status_label.grid(column=3, row=1, padx=padx, sticky='w')

deputies_time_label = tk.Label(root, text='Czas: ', font=font_status_label, bg=bg_colour, fg='black')
deputies_time_label.grid(column=3, row=1, padx=padx, sticky='ws')

# POSIEDZENIA
posiedzenia_label = tk.Label(root, text='Posiedzenia', font=font_label, bg=bg_colour, fg='black')
posiedzenia_label.grid(column=0, row=2, padx=padx, sticky='w')

posiedzenia_wyszukaj_button = tk.Button(root, text='Wyszukaj', font=font_button, cursor=cursor, command=lambda: sittings_gui(1))
posiedzenia_wyszukaj_button.grid(column=1, row=2)

posiedzenia_import_button = tk.Button(root, text='Importuj', font=font_button, cursor=cursor, command=lambda: sittings_gui(2))
posiedzenia_import_button.grid(column=2, row=2)

sittings_status_label = tk.Label(root, text='Status:', font=font_status_label, bg=bg_colour, fg='black')
sittings_status_label.grid(column=3, row=2, padx=padx, sticky='w')

sittings_time_label = tk.Label(root, text='Czas: ', font=font_status_label, bg=bg_colour, fg='black')
sittings_time_label.grid(column=3, row=2, padx=padx, sticky='ws')

# GŁOSOWANIA
glosowania_label = tk.Label(root, text='Głosowania', font=font_label, bg=bg_colour, fg='black')
glosowania_label.grid(column=0, row=3, padx=padx, sticky='w')

glosowania_wyszukaj_button = tk.Button(root, text='Wyszukaj', font=font_button, cursor=cursor, command=lambda: votings_gui(1))
glosowania_wyszukaj_button.grid(column=1, row=3)

glosowania_import_button = tk.Button(root, text='Importuj', font=font_button, cursor=cursor, command=lambda: votings_gui(2))
glosowania_import_button.grid(column=2, row=3)

votings_status_label = tk.Label(root, text='Status:', font=font_status_label, bg=bg_colour, fg='black')
votings_status_label.grid(column=3, row=3, padx=padx, sticky='w')

votings_time_label = tk.Label(root, text='Czas: ', font=font_status_label, bg=bg_colour, fg='black')
votings_time_label.grid(column=3, row=3, padx=padx, sticky='ws')

# GŁOSY
glosy_label = tk.Label(root, text='Głosy', font=font_label, bg=bg_colour, fg='black')
glosy_label.grid(column=0, row=4, padx=padx, sticky='w')

glosy_wyszukaj_button = tk.Button(root, text='Wyszukaj', font=font_button, cursor=cursor, command=lambda: votes_gui(1))
glosy_wyszukaj_button.grid(column=1, row=4)

glosy_import_button = tk.Button(root, text='Importuj', font=font_button, cursor=cursor, command=lambda: votes_gui(2))
glosy_import_button.grid(column=2, row=4)

votes_status_label = tk.Label(root, text='Status:', font=font_status_label, bg=bg_colour, fg='black')
votes_status_label.grid(column=3, row=4, padx=padx, sticky='w')

votes_time_label = tk.Label(root, text='Czas: ', font=font_status_label, bg=bg_colour, fg='black')
votes_time_label.grid(column=3, row=4, padx=padx, sticky='ws')

glosy_id_posla_label_od = tk.Label(root, text='ID posła od:', font=font_button, bg=bg_colour, fg='black')
glosy_id_posla_label_od.grid(column=1, row=4, sticky='s')
votes_id_deputy_text_box_from = tk.Entry(root, width=9)
votes_id_deputy_text_box_from.grid(column=1, row=5, sticky='n')

glosy_id_posla_label_do = tk.Label(root, text='ID posła do:', font=font_button, bg=bg_colour, fg='black')
glosy_id_posla_label_do.grid(column=2, row=4, sticky='s')
votes_id_deputy_text_box_to = tk.Entry(root, width=9)
votes_id_deputy_text_box_to.grid(column=2, row=5, sticky='n')

glosy_id_posiedzenia_label_od = tk.Label(root, text='ID posiedzenia od:', font=font_button, bg=bg_colour, fg='black')
glosy_id_posiedzenia_label_od.grid(column=1, row=5, sticky='s')
votes_id_sitting_text_box_from = tk.Entry(root, width=12)
votes_id_sitting_text_box_from.grid(column=1, row=6, sticky='n')

glosy_id_posiedzenia_label_do = tk.Label(root, text='ID posiedzenia do:', font=font_button, bg=bg_colour, fg='black')
glosy_id_posiedzenia_label_do.grid(column=2, row=5, sticky='s')
id_sitting_text_box_to = tk.Entry(root, width=12)
id_sitting_text_box_to.grid(column=2, row=6, sticky='n')

root.mainloop()
