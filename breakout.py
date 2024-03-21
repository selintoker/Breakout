"""
File: breakout.py
-----------------
This program implements the game Breakout!  The user controls a paddle
moving horizontally with the mouse, and the user must bounce the ball
to make it collide and remove bricks from the screen.  The user has
3 turns.  If the ball falls below the bottom of the screen, the user
loses a turn.  If the user removes all bricks before their turns
run out, they win!
"""

import math
from graphics import Canvas
import random
import time

"""
Dimensions of the canvas, in pixels
These should be used when setting up the initial size of the game,
but in later calculations you should use canvas.get_canvas_width() and 
canvas.get_canvas_height() rather than these constants for accurate size information.
"""
CANVAS_WIDTH = 420
CANVAS_HEIGHT = 600

# Stage 1: Set up the Bricks

# Number of bricks in each row
NBRICK_COLUMNS = 10

# Number of rows of bricks
NBRICK_ROWS = 10

# Separation between neighboring bricks, in pixels
BRICK_SEP = 4

# Width of each brick, in pixels
BRICK_WIDTH = math.floor((CANVAS_WIDTH - (NBRICK_COLUMNS + 1.0) * BRICK_SEP) / NBRICK_COLUMNS)

# Height of each brick, in pixels
BRICK_HEIGHT = 8

# Offset of the top brick row from the top, in pixels
BRICK_Y_OFFSET = 70

# Stage 2: Create the Bouncing Ball

# Radius of the ball in pixels
BALL_RADIUS = 10

# The ball's vertical velocity.
VELOCITY_Y = 6.0

# The ball's minimum and maximum horizontal velocity; the bounds of the
# initial random velocity that you should choose (randomly +/-).
VELOCITY_X_MIN = 2.0
VELOCITY_X_MAX = 6.0

# Animation delay or pause time between ball moves (in seconds)
DELAY = 1 / 60

# Stage 3: Create the Paddle

# Dimensions of the paddle
PADDLE_WIDTH = 60
PADDLE_HEIGHT = 10

# Offset of the paddle up from the bottom
PADDLE_Y_OFFSET = 30

# Stage 5: Polish and Finishing Up

# Number of turns
NTURNS = 3

BOUNCE_SOUND = "bounce.au"


def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    canvas.set_canvas_title("Breakout")

    for y in range(NBRICK_COLUMNS):
        for x in range(NBRICK_ROWS):
            draw_brick(canvas, x, y)
    paddle = add_paddle(canvas)
    dx = random.randint(VELOCITY_X_MIN, VELOCITY_X_MAX)
    dy = VELOCITY_Y
    bricks_remaining = 100
    result = "You Lost!"

    for i in range(3):
        if bricks_remaining == 0:
            canvas.delete(ball)
            result = "You Won!"
            break
        ball = bouncing_ball(canvas)
        canvas.wait_for_click()
        clicks = canvas.get_new_mouse_clicks()
        for click in clicks:
            click = canvas.move(ball, dx, dy)
        while bricks_remaining != 0:
            mouse_x = canvas.get_mouse_x()
            if CANVAS_WIDTH - PADDLE_WIDTH > mouse_x > 0:
                canvas.moveto(paddle, mouse_x, CANVAS_HEIGHT - PADDLE_Y_OFFSET - PADDLE_HEIGHT)

            if canvas.get_top_y(ball) < 0:
                dy = dy * -1
            elif canvas.get_top_y(ball) + 2 * BALL_RADIUS > canvas.get_canvas_height():
                canvas.delete(ball)
                break
            elif canvas.get_left_x(ball) < 0:
                dx = dx * -1
            elif canvas.get_left_x(ball) + 2 * BALL_RADIUS > canvas.get_canvas_width():
                dx = dx * -1
            canvas.move(ball, dx, dy)

            ball_coords = canvas.coords(ball)
            x_1 = ball_coords[0]
            y_1 = ball_coords[1]
            x_2 = ball_coords[2]
            y_2 = ball_coords[3]
            colliding_list = canvas.find_overlapping(x_1, y_1, x_2, y_2)
            for collider in colliding_list:
                if collider == ball:
                    pass
                elif collider == paddle:
                    dy = dy * -1
                else:
                    dy = dy * -1
                    canvas.delete(collider)
                    bricks_remaining -= 1
            canvas.update()
            time.sleep(DELAY)
    canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/2, result)
    canvas.mainloop()


def draw_brick(canvas, x, y):
    top_x = x * (BRICK_WIDTH + BRICK_SEP) + BRICK_SEP
    top_y = y * (BRICK_HEIGHT + BRICK_SEP) + BRICK_SEP
    bottom_x = (x+1) * BRICK_WIDTH + x * BRICK_SEP + BRICK_SEP
    bottom_y = (y+1) * BRICK_HEIGHT + y * BRICK_SEP + BRICK_SEP
    brick = canvas.create_rectangle(top_x, top_y + BRICK_Y_OFFSET, bottom_x, bottom_y + BRICK_Y_OFFSET)
    if y < 2:
        canvas.set_fill_color(brick, 'red')
        canvas.set_outline_color(brick, 'red')
    elif 4 > y >= 2:
        canvas.set_fill_color(brick, 'orange')
        canvas.set_outline_color(brick, 'orange')
    elif 6 > y >= 4:
        canvas.set_fill_color(brick, 'yellow')
        canvas.set_outline_color(brick, 'yellow')
    elif 8 > y >= 6:
        canvas.set_fill_color(brick, 'green')
        canvas.set_outline_color(brick, 'green')
    else:
        canvas.set_fill_color(brick, 'cyan')
        canvas.set_outline_color(brick, 'cyan')
    return brick


def bouncing_ball(canvas):
    top_x = CANVAS_WIDTH/2 - BALL_RADIUS
    top_y = CANVAS_HEIGHT/2 - BALL_RADIUS
    bottom_x = CANVAS_WIDTH/2 + BALL_RADIUS
    bottom_y = CANVAS_HEIGHT/2 + BALL_RADIUS
    ball = canvas.create_oval(top_x, top_y, bottom_x, bottom_y)
    canvas.set_fill_color(ball, 'black')
    return ball


def add_paddle(canvas):
    top_x = CANVAS_WIDTH/2 - PADDLE_WIDTH/2
    top_y = CANVAS_HEIGHT - PADDLE_Y_OFFSET - PADDLE_HEIGHT
    bottom_x = CANVAS_WIDTH/2 + PADDLE_WIDTH/2
    bottom_y = CANVAS_HEIGHT - PADDLE_Y_OFFSET
    paddle = canvas.create_rectangle(top_x, top_y, bottom_x, bottom_y)
    canvas.set_fill_color(paddle, 'black')
    return paddle


if __name__ == '__main__':
    main()
