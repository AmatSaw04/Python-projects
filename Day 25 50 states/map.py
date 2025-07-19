from turtle import Turtle
import pandas as pd

data = pd.read_csv("50_states.csv")


class Map(Turtle):
    def __init__(self):
        super().__init__()
        self.write()
