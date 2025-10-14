"""
Application: Typing Speed Test
Author: Istvan Godeny
Date: 27/06/2025
License: MIT License
"""

import turtle

## ======================================== Variables ===================================================
# Paddle
paddle_width = 1
paddle_length = 8

# Ball speed
ball_dx = 5
ball_dy = 5

# Brick grid and dimensions, 1 unit = 20 pixel
bricks_per_line = 10
number_of_bricks_row = 3
brick_length = 2
brick_height = 1
bricks_x = 0
bricks_y = 0

# Score
score = 0
lives = 5

## ======================================== Functions ===================================================
## Paddle controllers
# Paddle move left
def move_left():
    x = paddle.xcor()
    if x > -window.canvwidth + (window.canvwidth*0.015*13):
        paddle.backward(20)


# Paddle move right
def move_right():
    x = paddle.xcor()
    if x < window.canvwidth - (window.canvwidth * 0.015 * 13):
        paddle.forward(20)

## Ball controllers
# Ball movement
def ball_move():
    x = ball.xcor() + ball_dx
    y = ball.ycor() + ball_dy

    ball.goto(x, y)
    window.ontimer(ball_move, 10)

    ## Check collisions
    # Wall collision check
    wall_collision()
    # Paddle collision check
    paddle_collision()
    # Brick collision check
    brick_collision()


# Ball reset
def ball_reset():
    global ball_dx, ball_dy

    ball.goto(0, -150)

    ball_dx = 5
    ball_dy = 5


## Collision detectors
# Wall collision detector
def wall_collision():
    global ball_dx, ball_dy, lives

    # Walls
    max_x = window.canvwidth
    max_y = window.canvheight

    # Ball actual position
    x = ball.xcor()
    y = ball.ycor()

    # Check for the left or the right wall
    if x > max_x - 20 or x < -max_x + 15:
        ball_dx *= -1

    # Check for the top
    if y > max_y -10:
        ball_dy *= -1

    # The bottom wall
    if y < -max_y:

        # The ball fell, reset and restart form the origin
        ball_dx = 0
        ball_dy = 0

        ball_reset()

        lives -= 1
        lives_display()
        if lives == 0:
            ball.goto(0, 0)
            ball_dx = 0
            ball_dy = 0
            paddle.goto(0, -window.canvheight + 30)
            message_lost_all_lives.goto(0, -150)
            message_lost_all_lives.write(f"You lost all of your lives!\nGame Over!!\nYour Score: {score} and you left {lives} Lives.",
                                       font=("Arial", 25, "bold"), align="center")

            new_game_btn.showturtle()
            new_game_btn_text.shapesize(stretch_len=new_game_btn.shapesize()[1],
                                        stretch_wid=new_game_btn.shapesize()[0] * 0.9)
            new_game_btn_text.write("New Game", align="center", font=("Arial", 20, "bold"))

            exit_btn.showturtle()
            exit_btn_text.shapesize(stretch_len=exit_btn.shapesize()[1],
                                    stretch_wid=exit_btn.shapesize()[0] * 0.9)
            exit_btn_text.write("Exit", align="center", font=("Arial", 20, "bold"))

            return


# Paddle collision detector
def paddle_collision():
    global ball_dx, ball_dy

    paddle_xcor = paddle.xcor()
    paddle_ycor = paddle.ycor()

    ball_xcor = ball.xcor()
    ball_ycor = ball.ycor()

    if ball_dy < 0 and abs(ball_ycor - paddle_ycor) <= 20:
        if abs(ball_xcor - paddle_xcor) < 0.9 * ((20 * paddle_length) / 2):
            ball_dy *= -1
            ball.sety(paddle_ycor + 10)


# Brick collision detector
def brick_collision():
    global ball_dx, ball_dy, score, lives
    for hit_brick in bricks:
        if ball.distance(hit_brick) < 20:
            if hit_brick in bricks:
                hit_brick.hideturtle()
                bricks.remove(hit_brick)

                score += 1
                score_display()

                # Check if we broke all bricks
                if len(bricks) == 0:
                    if lives < 5:
                        lives += 1
                        lives_display()

                    ball.goto(0, 0)
                    ball_dx = 0
                    ball_dy = 0

                    paddle.goto(0, -window.canvheight + 30)

                    message_clean_bricks.goto(0, -150)
                    message_clean_bricks.write(f"All bricks destroyed!\nCongratulations!\nYour Score: {score} and you left {lives} Lives.",
                                               font=("Arial", 25, "bold"), align="center")

                    new_game_btn.showturtle()
                    new_game_btn_text.shapesize(stretch_len=new_game_btn.shapesize()[1],
                                                stretch_wid=new_game_btn.shapesize()[0] * 0.9)
                    new_game_btn_text.write("New Game", align="center", font=("Arial", 20, "bold"))

                    exit_btn.showturtle()
                    exit_btn_text.shapesize(stretch_len=exit_btn.shapesize()[1],
                                                stretch_wid=exit_btn.shapesize()[0] * 0.9)
                    exit_btn_text.write("Exit", align="center", font=("Arial", 20, "bold"))
                    return

                else:
                    ball_dy *= -1
                    return


## Score and Lives display
# Score display
def score_display():
    score_writer.clear()
    score_writer.write(f"Score: {score}", font=("Arial", 20, "bold"))


# Lives display
def lives_display():
    lives_writer.clear()
    lives_writer.write(f"Lives: {lives}", font=("Arial", 20, "bold"))


## Button controllers
# New Game
def new_game(x, y):
    global score, lives, bricks_x, bricks_y

    if new_game_btn_text.xcor() - round((new_game_btn_text.shapesize()[1] * 20) / 2) <= x <= new_game_btn_text.xcor() + round(
            (new_game_btn_text.shapesize()[1] * 20) / 2) and new_game_btn_text.ycor() - round(
        (new_game_btn_text.shapesize()[0] * 20) / 2) <= y <= new_game_btn_text.ycor() + round((new_game_btn_text.shapesize()[0] * 20) / 2):
        # print("pressed")
        score = 0
        score_display()
        lives = lives
        lives_display()

        message_clean_bricks.clear()
        message_lost_all_lives.clear()

        new_game_btn.hideturtle()
        new_game_btn_text.clear()
        new_game_btn_text.shapesize(stretch_len=1/20, stretch_wid=1/20)

        exit_btn.hideturtle()
        exit_btn_text.clear()
        exit_btn_text.shapesize(stretch_len=1 / 20, stretch_wid=1 / 20)

        for remain_brick in bricks:
            remain_brick.hideturtle()

        bricks.clear()
        create_bricks()

        paddle.goto(0, -window.canvheight + 30)
        ball.goto(0, -150)
        ball_reset()


# Create Bricks
def create_bricks():
    global bricks_x, bricks_y
    bricks_y = window.canvheight - 70
    for _ in range(number_of_bricks_row):
        bricks_x = -window.canvwidth + bricks_distance
        for _ in range(bricks_per_line):
            brick = turtle.Turtle()
            brick.shape("square")
            brick.shapesize(stretch_wid=brick_height, stretch_len=brick_length)
            brick.color("blue")
            brick.penup()
            brick.goto(bricks_x, bricks_y)
            bricks.append(brick)
            bricks_x += bricks_distance
        bricks_y -= 40


# Exit
def exit_game(x, y):
    if exit_btn_text.xcor() - round(
            (exit_btn_text.shapesize()[1] * 20) / 2) <= x <= exit_btn_text.xcor() + round(
            (exit_btn_text.shapesize()[1] * 20) / 2) and exit_btn_text.ycor() - round(
        (exit_btn_text.shapesize()[0] * 20) / 2) <= y <= exit_btn_text.ycor() + round(
        (exit_btn_text.shapesize()[0] * 20) / 2):
        window.clear()
        window.bye()




## ======================================== Window ===================================================
# Create the app window
window = turtle.Screen()
window.title("Breakout")
window.bgcolor("grey")
window.setup(width=800, height=600)
window.cv._rootwindow.resizable(False, False)

## Elements
# Buttons
# New Game
new_game_btn = turtle.Turtle()
new_game_btn.penup()
new_game_btn.hideturtle()
new_game_btn.shape("square")
new_game_btn.goto(-70, window.canvheight -25)
new_game_btn.shapesize(stretch_wid=2, stretch_len=6)
new_game_btn.color("black", "grey")

new_game_btn_text = turtle.Turtle()
new_game_btn_text.penup()
new_game_btn_text.hideturtle()
new_game_btn_text.shapesize(stretch_len=1/20, stretch_wid=1/20)
new_game_btn_text.goto(new_game_btn.xcor(), new_game_btn.ycor() - 10)
new_game_btn_text.color("black")

# Exit Button
exit_btn = turtle.Turtle()
exit_btn.penup()
exit_btn.hideturtle()
exit_btn.shape("square")
exit_btn.goto(70, window.canvheight -25)
exit_btn.shapesize(stretch_wid=2, stretch_len=6)
exit_btn.color("black", "grey")

exit_btn_text = turtle.Turtle()
exit_btn_text.penup()
exit_btn_text.hideturtle()
exit_btn_text.shapesize(stretch_len=1/20, stretch_wid=1/20)
exit_btn_text.goto(exit_btn.xcor(), exit_btn.ycor() - 10)
exit_btn_text.color("black")

# Messages
message_clean_bricks = turtle.Turtle()
message_clean_bricks.penup()
message_clean_bricks.hideturtle()

message_lost_all_lives = turtle.Turtle()
message_lost_all_lives.penup()
message_lost_all_lives.hideturtle()

# Score
score_writer = turtle.Turtle()
score_writer.penup()
score_writer.hideturtle()
score_writer.goto(-window.canvwidth + 100, window.canvheight - 30)
score_writer.write(f"Score: {score}", font=("Arial", 20, "bold"))

# Lives
lives_writer = turtle.Turtle()
lives_writer.penup()
lives_writer.hideturtle()
lives_writer.goto(window.canvwidth - 200, window.canvheight - 30)
lives_writer.write(f"Lives: {lives}", font=("Arial", 20, "bold"))

# Create the paddle
paddle = turtle.Turtle()
paddle.shape("square")
paddle.shapesize(stretch_wid=paddle_width, stretch_len=paddle_length)
paddle.penup()
paddle.goto(0, -window.canvheight + 30)

# Ball
ball = turtle.Turtle()
ball.shape("circle")
ball.shapesize(stretch_len=1, stretch_wid=1)
ball.penup()
ball.goto(0,-150)

# Bricks
bricks = []
bricks_distance = round(window.canvwidth / (bricks_per_line+1)*2)
create_bricks()


# This call starts the game
ball_move()
#Paddle move Left
window.onkeypress(move_left, "Left")
# Paddle move right
window.onkeypress(move_right, "Right")
# New Game Event
window.onclick(new_game, 1, add=True)
# Exit Game Event
window.onclick(exit_game, 1, add=True)

window.listen()

window.mainloop()
