import tkinter as tk
from PIL import ImageTk
import sqlite3
from numpy import random

bg_color = "#3d6466"

def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def fetch_db():
    #create connection
    connection = sqlite3.connect(r"C:\Users\tugra\OneDrive\Desktop\fun\random_recipe_picker\data\recipes.db")
    cursor = connection.cursor()
    #get the titles of the recipes
    cursor.execute("SELECT * FROM sqlite_schema WHERE type='table';")
    all_tables = cursor.fetchall()
    #create a random integer in order to randomize the recipes
    idx  = random.randint(0,  len(all_tables)-1)

    table_name = all_tables[idx][1]
    cursor.execute("SELECT * FROM " + table_name + ";")
    table_records = cursor.fetchall()

    connection.close()
    return table_name, table_records


def pre_process(table_name, table_records):
    
    #format the title to have spaces and remove the number at the end
    title = table_name[:-6]
    title = "".join([char if char.islower() else " " + char for char in title])
    
    ingredients = []
    #format the ingredients
    for i in table_records:
        name = i[1]
        qty = i[2]
        unit = i[3]

        ingredients.append(qty + " " + unit + " of " + name)
    
    return title, ingredients



def load_frame1():
    clear_widgets(frame2)
    frame1.tkraise()
    #stops from children from changing  frame1
    frame1.pack_propagate(False)

    #frame1 widgets
    #logo widget
    logo_img = ImageTk.PhotoImage(file=r"C:\Users\tugra\OneDrive\Desktop\fun\random_recipe_picker\assets\RRecipe_logo.png")
    logo_widget = tk.Label(frame1, image=logo_img, bg=bg_color)
    logo_widget.image = logo_img
    logo_widget.pack()


    #instructions widget
    tk.Label(
        frame1,
        text="ready for ur random recipe?",
        bg=bg_color,
        fg="white",
        font=("TkMenuFont", 14),
        ).pack()

    #button 
    tk.Button(
        frame1,
        text="SHUFFLE",
        font=("TkHeadingFont", 20),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        command=lambda:load_frame2()
        ).pack(pady=20)


def load_frame2():
    clear_widgets(frame1)
    frame2.tkraise()
    table_name, table_records = fetch_db()
    title, ingredients = pre_process(table_name, table_records)

    #logo widget
    logo_img = ImageTk.PhotoImage(file=r"C:\Users\tugra\OneDrive\Desktop\fun\random_recipe_picker\assets\RRecipe_logo_bottom.png")
    logo_widget = tk.Label(frame2, image=logo_img, bg=bg_color)
    logo_widget.image = logo_img
    logo_widget.pack()

    #title
    tk.Label(
        frame2,
        text=title,
        bg=bg_color,
        fg="white",
        font=("TkHeadingFont", 20),
        ).pack()

    #ingredients
    for i in ingredients:
        tk.Label(
            frame2,
            text=i,
            bg="#28393a",
            fg="white",
            font=("TkMenuFont", 12),
            ).pack(fill="both", padx=20)

    #button 
    tk.Button(
        frame2,
        text="BACK",
        font=("TkHeadingFont", 18),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        command=lambda:load_frame1()
        ).pack(pady=20)


# initialize app
root = tk.Tk()
root.title("Recipe Picker")

# place the window at the center of the screen
root.eval("tk::PlaceWindow . center")

#create frame
frame1 = tk.Frame(root, width=500,  height=600, bg=bg_color)
frame2 = tk.Frame(root, bg=bg_color)

for frame in(frame1, frame2):
    frame.grid(row=0, column=0, sticky="nesw")

load_frame1()

# run app
root.mainloop()