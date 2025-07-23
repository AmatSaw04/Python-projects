from tkinter import *
from tkinter import Entry

'''def add(*sumall):
    sum = 0
    for num in sumall:
        sum += num
    return sum

print(add(3,4,5,6,7,7,8,2))'''

'''def calc(n, **kwargs):
    n+= kwargs["add"]
    n*= kwargs["multiply"]
calc(n=2, add= 5, multiply=10)'''
window = Tk()
window.title("My First GUI Program")

my_label = Label(text ="I Am a Label", font=("Arial", 24, "bold"))
#my_label.pack()
my_label.config(text="New text")
my_label.grid(column=0,row=0)

def click():
    my_label.config(text=input.get())

button = Button(text="click me", command=click)
#button.pack()
button.grid(column=2, row=2)
def clicked():
    my_label.config(text="clickoo")
new_butt = Button(text="clit me", command=clicked)
#new_butt.pack()
new_butt.grid(column=0, row=2)

input = Entry(width=100)
#input.pack()
print(input.get())
input.grid(column=4, row=4)



window.mainloop()
