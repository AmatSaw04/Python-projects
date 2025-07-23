from tkinter import *

window = Tk()


label1 = Label(text="Miles", font=("Arial", 14))
label1.grid(row=2, column=8)

label2 = Label(text="Km", font=("Arial", 14))
label2.grid(row=4, column=8)

label3 = Label(text="is equal to", font=("Arial", 14))
label3.grid(row=3, column=2)


def calculate_miles_to_km():
    x = float(entry.get())
    y = x*1.609
    label4 = Label(text=f"{y}", font=("Arial", 14))
    label4.grid(row=4, column=5)



entry = Entry(width=10)
entry.grid(row=2, column=5)
print(entry.get())



window.title("Mile to Kilo converter")
new_butt = Button(text="Calculate", command=calculate_miles_to_km)
new_butt.grid(row=5, column=5)




mainloop()