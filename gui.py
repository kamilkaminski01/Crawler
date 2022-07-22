import tkinter as tk

bg_colour = '#C3B7B4'

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

root = tk.Tk()
canvas = tk.Canvas(root, width=600, height=300)
canvas.grid(columnspan=3)

root.title("Sejm Crawler")
# root.eval("tk::PlaceWindow . center")

frame = tk.Frame(root, width=500, height=600, bg=bg_colour)

frame.grid(row=0, column=0, sticky='nesw')
# load_frame()

root.mainloop()