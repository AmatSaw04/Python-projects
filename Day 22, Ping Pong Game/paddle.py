from turtle import Turtle, Screen

screen = Screen()

class Paddle(Turtle):

    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.shapesize(stretch_wid=4, stretch_len=1)
        self.color("white")
        self.penup()
        self.goto(position)


    def go_up(self):
        new_y = self.ycor() + 20
        self.goto(self.xcor(), new_y )
    def go_down(self):
        neww_y = self.ycor() - 15
        self.goto(self.xcor(), neww_y)
