import random
from linecache import updatecache
from random import choice
from tkinter import *
import pyperclip
import json
from tkinter import messagebox

FONT_NAME = "Courier"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    my_pass = []

    my_pass.extend(random.sample(letters, 4))
    my_pass.extend(random.sample(numbers, 4))
    my_pass.extend(random.sample(symbols, 4))

    random.shuffle(my_pass)
    a = "".join(my_pass)

    password_entry.insert(0, a)
    pyperclip.copy(a)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website =website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website)==0 or len(email)==0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")


    else:

        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email} "

                                                              f"\nPassword: {password} \nIs it ok to save?")

        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)


            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)

            else:
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)


            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)

def find_pass():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found")
    else:
        if website in data:
            mail = data[website]["mail"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"email: {mail}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Not Found", message=f"No details of {website} found")






# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

website_label = Label(text="Website:")
website_label.grid(row=2, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=3, column=0)
password_label = Label(text="Password:")
password_label.grid(row=4, column=0)

canvas = Canvas(width=200, height=200)
photo = PhotoImage(file="logo.png")
canvas.create_image(100,100, image=photo)
#timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

website_entry = Entry(width=21)
website_entry.grid(row=2, column=1)
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=3, column=1, columnspan=2)
email_entry.insert(0, "amatyasawant@gmail.com")
password_entry = Entry(width=20)
password_entry.grid(row=4, column=1)

generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=4, column=2)
add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=5, column=1, columnspan=2)
search_button = Button(text="Search", width=36, command=find_pass)
search_button.grid(row=2, column=3)


window.mainloop()