import turtle
import random
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 20
BULLET_SPEED = 20
ALIEN_SPEED_X = 10
ALIEN_MOVE_INTERVAL = 100
ALIEN_DROP_INTERVAL = 1000
ALIEN_ROWS = 4
ALIEN_COLS = 8
ALIEN_X_GAP = 60
ALIEN_Y_GAP = 50
BARRIER_COUNT = 4
BARRIER_WIDTH = 6
BARRIER_HEIGHT = 4
BLOCK_SIZE = 10

wn = turtle.Screen()
wn.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
wn.title("Space Invaders - Turtle")
wn.bgcolor("black")
wn.tracer(0)

score = 0
game_over_flag = False
alien_wave_size = 1

score_pen = turtle.Turtle()
score_pen.hideturtle()
score_pen.penup()
score_pen.color("white")
score_pen.goto(-SCREEN_WIDTH//2 + 10, SCREEN_HEIGHT//2 - 40)
score_pen.write("Score: 0", align="left", font=("Courier", 16, "normal"))

message_pen = turtle.Turtle()
message_pen.hideturtle()
message_pen.penup()
message_pen.color("white")
message_pen.goto(0, 0)

def show_message(text):
    message_pen.clear()
    message_pen.write(text, align="center", font=("Courier", 18, "bold"))

player = turtle.Turtle()
player.shape("triangle")
player.color("cyan")
player.penup()
player.goto(0, -SCREEN_HEIGHT//2 + 60)
player.setheading(90)

player_bullets = []

def fire_bullet():
    if game_over_flag:
        return
    if len(player_bullets) >= 3:
        return
    b = turtle.Turtle()
    b.shape("circle")
    b.shapesize(0.4, 0.4)
    b.color("yellow")
    b.penup()
    b.goto(player.xcor(), player.ycor() + 20)
    b.setheading(90)
    player_bullets.append(b)

aliens = []
alien_direction = 1

def create_aliens():
    aliens.clear()
    start_x = -((ALIEN_COLS - 1) * ALIEN_X_GAP) / 2
    start_y = SCREEN_HEIGHT//2 - 120
    colors = ["red", "orange", "green", "white"]
    for row in range(ALIEN_ROWS):
        for col in range(ALIEN_COLS):
            a = turtle.Turtle()
            a.shape("square")
            a.shapesize(1.4, 1.4)
            a.color(colors[row % len(colors)])
            a.penup()
            x = start_x + col * ALIEN_X_GAP
            y = start_y - row * ALIEN_Y_GAP
            a.goto(x, y)
            aliens.append(a)

barrier_blocks = []
def create_barriers():
    barrier_blocks.clear()
    left = -SCREEN_WIDTH//2 + 120
    gap = (SCREEN_WIDTH - 240) / (BARRIER_COUNT - 1)
    base_y = -SCREEN_HEIGHT//2 + 140
    for b in range(BARRIER_COUNT):
        bx = left + b * gap
        for row in range(BARRIER_HEIGHT):
            for col in range(BARRIER_WIDTH):
                block = turtle.Turtle()
                block.shape("square")
                block.shapesize(BLOCK_SIZE/20, BLOCK_SIZE/20)
                block.color("darkgreen")
                block.penup()
                x = bx + (col - BARRIER_WIDTH//2) * (BLOCK_SIZE + 1)
                y = base_y + row * (BLOCK_SIZE + 1)
                block.goto(x, y)
                barrier_blocks.append(block)

def is_collision(t1, t2, threshold=20):
    return t1.distance(t2) < threshold

def check_game_over():
    global game_over_flag
    for a in aliens:
        if a.ycor() <= player.ycor() + 20:
            game_over_flag = True
            show_message("GAME OVER - Press 'r' to restart")
            return True
    return False

def increase_difficulty():
    global alien_wave_size
    if game_over_flag:
        return
    alien_wave_size += 1
    # print(f"Aliens are now firing {alien_wave_size} bullets!") # Optional: for testing
    wn.ontimer(increase_difficulty, 2000)

def move_aliens_step():
    global alien_direction
    if game_over_flag:
        return
    edge_hit = False
    for a in aliens:
        if not a.isvisible():
            continue
        a.setx(a.xcor() + ALIEN_SPEED_X * alien_direction)
        if a.xcor() > SCREEN_WIDTH//2 - 40 or a.xcor() < -SCREEN_WIDTH//2 + 40:
            edge_hit = True
    if edge_hit:
        alien_direction *= -1
        for a in aliens:
            if a.isvisible():
                a.setx(a.xcor() + ALIEN_SPEED_X * alien_direction)
    wn.update()
    wn.ontimer(move_aliens_step, ALIEN_MOVE_INTERVAL)


def move_left():
    if game_over_flag:
        return
    x = player.xcor() - PLAYER_SPEED
    min_x = -SCREEN_WIDTH//2 + 20
    if x < min_x:
        x = min_x
    player.setx(x)

def move_right():
    if game_over_flag:
        return
    x = player.xcor() + PLAYER_SPEED
    max_x = SCREEN_WIDTH//2 - 20
    if x > max_x:
        x = max_x
    player.setx(x)

def update_bullets():
    global score, game_over_flag
    if game_over_flag:
        return
    for b in player_bullets[:]:
        b.sety(b.ycor() + BULLET_SPEED)
        if b.ycor() > SCREEN_HEIGHT//2:
            try:
                b.hideturtle()
                player_bullets.remove(b)
            except ValueError:
                pass
            continue
        for a in aliens:
            if a.isvisible() and is_collision(b, a, threshold=20):
                a.hideturtle()
                try:
                    b.hideturtle()
                    player_bullets.remove(b)
                except ValueError:
                    pass
                score += 10
                score_pen.clear()
                score_pen.write(f"Score: {score}", align="left", font=("Courier", 16, "normal"))
                break
        else:
            for blk in barrier_blocks:
                if blk.isvisible() and is_collision(b, blk, threshold=12):
                    try:
                        b.hideturtle()
                        player_bullets.remove(b)
                    except ValueError:
                        pass
                    blk.hideturtle()
                    try:
                        barrier_blocks.remove(blk)
                    except ValueError:
                        pass
                    break
    if all(not a.isvisible() for a in aliens):
        game_over_flag = True
        show_message("YOU WIN! Press 'r' to restart")
    wn.update()
    wn.ontimer(update_bullets, 30)

alien_bullets = []
def alien_fire():
    if game_over_flag:
        return
    visible_aliens = [a for a in aliens if a.isvisible()]
    if visible_aliens:
        for _ in range(alien_wave_size):
            shooter = random.choice(visible_aliens)
            b = turtle.Turtle()
            b.shape("circle")
            b.shapesize(0.45, 0.45)
            b.color("red")
            b.penup()
            b.goto(shooter.xcor(), shooter.ycor() - 15)
            b.setheading(270)
            alien_bullets.append(b)
    wn.ontimer(alien_fire, random.randint(800, 1800))

def update_alien_bullets():
    global game_over_flag
    if game_over_flag:
        return
    for b in alien_bullets[:]:
        b.sety(b.ycor() - BULLET_SPEED*0.6)
        if b.ycor() < -SCREEN_HEIGHT//2:
            try:
                b.hideturtle()
                alien_bullets.remove(b)
            except ValueError:
                pass
            continue
        if is_collision(b, player, threshold=18):
            b.hideturtle()
            try:
                alien_bullets.remove(b)
            except ValueError:
                pass
            game_over_flag = True
            show_message("YOU WERE HIT! GAME OVER - Press 'r' to restart")
            return
        for blk in barrier_blocks:
            if blk.isvisible() and is_collision(b, blk, threshold=12):
                b.hideturtle()
                try:
                    alien_bullets.remove(b)
                except ValueError:
                    pass
                blk.hideturtle()
                try:
                    barrier_blocks.remove(blk)
                except ValueError:
                    pass
                break
    wn.update()
    wn.ontimer(update_alien_bullets, 30)

def reset_game():
    global score, game_over_flag, alien_direction, alien_wave_size
    # clear objects
    for b in player_bullets[:]:
        try:
            b.hideturtle()
            player_bullets.remove(b)
        except ValueError:
            pass
    for b in alien_bullets[:]:
        try:
            b.hideturtle()
            alien_bullets.remove(b)
        except ValueError:
            pass
    for a in aliens[:]:
        try:
            a.hideturtle()
            aliens.remove(a)
        except ValueError:
            pass
    for blk in barrier_blocks[:]:
        try:
            blk.hideturtle()
            barrier_blocks.remove(blk)
        except ValueError:
            pass
    score = 0
    score_pen.clear()
    score_pen.write("Score: 0", align="left", font=("Courier", 16, "normal"))
    message_pen.clear()
    game_over_flag = False
    alien_direction = 1
    alien_wave_size = 1
    player.goto(0, -SCREEN_HEIGHT//2 + 60)
    create_aliens()
    create_barriers()
    wn.update()
    wn.ontimer(move_aliens_step, ALIEN_MOVE_INTERVAL)
    wn.ontimer(update_bullets, 30)
    wn.ontimer(alien_fire, random.randint(600, 1300))
    wn.ontimer(update_alien_bullets, 30)
    wn.ontimer(increase_difficulty, 2000)
wn.listen()
wn.onkeypress(move_left, "Left")
wn.onkeypress(move_right, "Right")
wn.onkeypress(fire_bullet, "space")
wn.onkeypress(reset_game, "r")

create_aliens()
create_barriers()
wn.ontimer(move_aliens_step, ALIEN_MOVE_INTERVAL)
wn.ontimer(update_bullets, 30)
wn.ontimer(alien_fire, random.randint(600, 1300))
wn.ontimer(update_alien_bullets, 30)
wn.ontimer(increase_difficulty, 2000)
show_message("Press Left / Right to move, Space to shoot")

try:
    while True:
        wn.update()
        time.sleep(0.01)
except turtle.Terminator:
    pass