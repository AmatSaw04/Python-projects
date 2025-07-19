import csv
from os import write

import pandas
import pandas as pd
import turtle

'''with open("weather_data.csv") as data_file:
    data = csv.reader(data_file)
    temp = []
    for row in data:
        if row[1] != "temp":
            temp.append(row[1])

        print(temp)'''

'''data = pd.read_csv("weather_data.csv")

data_dict = data.to_dict()
temp_list = data["temp"].to_list()
max_val = data["temp"].max()
for temperature in data["temp"]:
    temperature = (temperature * (9/5)) + 32
    print(temperature)'''

'''data = pd.read_csv("2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv")

grey_color = len(data[data["Primary Fur Color"] == "Gray"])
red_color = len([data["Primary Fur Color"] == "Cinnamon"])
black_color = len(data[data["Primary Fur Color"] == "Black"])
data_dict = {
    "Fur Color": ["grey", "red", "black"],
    "Count": [grey_color, red_color, black_color]
}
df = pandas.DataFrame(data_dict)
print(df)
df.to_csv("Fur color count")'''

screen = turtle.Screen()
screen.title("US states")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)
data = pd.read_csv("50_states.csv")

all_states = data.state.to_list()
answer_state = screen.textinput(title="Guess US states", prompt="What's another state")
guessed_state = []


while len(guessed_state) < 50:
    answer_state = screen.textinput(title=f"{len(guessed_state)}/50 states guessed", prompt="What's another state").title()

    missing_states = [state for state in all_states if state not in guessed_state]
    if answer_state == "Exit":
        new_data = pd.DataFrame(missing_states)
        new_data.to_csv("missed state")
        break
    if answer_state in all_states:
        guessed_state.append(answer_state)
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        state_data = data[data.state == answer_state]
        t.goto(state_data.x.item(), state_data.y.item())
        t.write(answer_state)










turtle.mainloop()