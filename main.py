from pyglet.gl import *
from pyglet.window import key
import sys
import res
import graphics
import entities
import utils

config = pyglet.gl.Config(double_buffer=True)
window = pyglet.window.Window(
    res.WIN_W, res.WIN_H, config=config, caption="Tiny ship")
fps_display = pyglet.clock.ClockDisplay()

score_label = pyglet.text.Label(text='SCORE 0',
                                font_name='Droid Sans',
                                font_size=25,
                                bold=True,
                                x=10, y=res.WIN_H - 30)

dead_label = pyglet.text.Label(text='PRESS R FOR RESTART',
                               font_name='Droid Sans',
                               font_size=40,
                               bold=True,
                               anchor_x='center', anchor_y='center',
                               x=res.HALF_WIN_W, y=res.HALF_WIN_H)


background = graphics.Stars(256)
wall = pyglet.sprite.Sprite(res.wall_animation, y=44)
wall.rotation = 90

player_ship = None
game_objects = []
animations_buffer = []
event_stack_size = 0


def reset():
    global player_ship, game_objects, event_stack_size, animations_buffer

    while event_stack_size > 0:
        window.pop_handlers()
        event_stack_size -= 1

    player_ship = entities.Player()

    game_objects = [player_ship]
    animations_buffer = []
    entities.load_asteroids(game_objects, 400)

    for handler in player_ship.event_handlers:
        window.push_handlers(handler)
        event_stack_size += 1


@window.event
def on_draw():
    window.clear()
    glClearColor(.0, .1, .2, .0)
    background.draw()

    for obj in game_objects:
        obj.draw()

    wall.draw()

    for anim in animations_buffer:
        anim.draw()

    score_label.draw()
    if player_ship.dead:
        dead_label.draw()
    # fps_display.draw()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.ESCAPE:
        sys.exit()
    if symbol == key.R:
        reset()


def update(dt):
    background.update(dt)

    score = len(player_ship.score_table)
    score_label.text = 'SCORE ' + str(score)
    entities.load_asteroids(game_objects, max(200, 300 - score // 10))

    for obj in game_objects:
        obj.update(dt)
        if obj.dead:
            animations_buffer.append(entities.DeadAnimation(x=obj.x, y=obj.y))
            obj.to_remove = True
        else:
            player_ship.collide_handle(obj)

    for to_remove in [obj for obj in game_objects if obj.to_remove]:
        game_objects.remove(to_remove)

    for i, anim in enumerate(animations_buffer):
        if anim.to_remove:
            anim.delete()
            del animations_buffer[i]

    if not player_ship.dead:
        player_ship.distance += res.WORLD_VELOCITY * dt
        for obj in game_objects[1::2]:
            nearly_distance = round(player_ship.distance, -1)
            if abs(player_ship.x - obj.x) < 5 \
                and nearly_distance not in player_ship.score_table \
                and abs(player_ship.y - obj.y) < res.ASTEROIDS_DISTANCE:
                player_ship.score_table.append(nearly_distance)


def gl_init():
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)


if __name__ == '__main__':
    gl_init()
    reset()
    pyglet.clock.schedule_interval(update, 1 / 60.0)
    pyglet.app.run()
