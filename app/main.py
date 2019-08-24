import json
import os
import bottle
import numpy as np
import random

from api import ping_response, start_response, move_response, end_response
from random import *


def IsInBounds(coord, min_val, max_val):
    return ((min_val <= coord[0] < max_val) and (min_val <= coord[1] < max_val))


def GetManhatten(p1, p2):
    return abs((p1[0] - p2[0]) + (p1[1] - p2[1]))


def GetDir(to_coord, from_coord):
    diff = tuple(np.subtract(to_coord, from_coord))
    if(diff == (-1, 0)):
        return 'up'
    elif (diff == (1, 0)):
        return 'down'
    elif (diff == (0, -1)):
        return 'left'
    else:
        return 'right'


def ToFood(start, food):
    if food[1] > start[1]:
        return 'right'
    elif food[1] < start[1]:
        return 'left'


@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''


@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')


@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()


@bottle.post('/start')
def start():
    data = bottle.request.json

    # print(json.dumps(data))

    color = "#736CCB"

    return start_response(color)


@bottle.post('/move')
def move():

    data = bottle.request.json

    me = data['you']['body']
    width = data['board']['width']
    height = data['board']['height']
    board = np.full((width, height), 2)
    food = data['board']['food']
    snakes = data['board']['snakes']

    if len(snakes) > 0:
        snakes = ([(d['y'], d['x']) for dd in snakes if dd['id']
                   != data['you']['id'] for d in dd['body']])
        for s in snakes:
            if s == snakes[0]:
                for i in [-1, 1]:
                    new_coord = (s[0]+i, s[1])
                    if(IsInBounds(new_coord, 0, width)):
                        board[new_coord] = 0
                    new_coord = (s[0], s[1]+i)
                    if(IsInBounds(new_coord, 0, width)):
                        board[new_coord] = 0
            board[s] = 0
    food = [(d['y'], d['x']) for d in food]

    for f in food:
        board[f] = 3

    head = me[0]
    neck = me[1]

    direction = (head['x'] - neck['x'], head['y'] - neck['y'])

    meX = []
    meY = []

    for limb in me:
        board[limb['y'], limb['x']] = -1
        meX.append(limb['x'])
        meY.append(limb['y'])

    possible_coords = []

    for i in [-1, 1]:
        possible_coords.append((me[0]['y'] + i, me[0]['x']))
        possible_coords.append((me[0]['y'], me[0]['x'] + i))
    possible_coords = [i for i in possible_coords if IsInBounds(i, 0, width)]
    possible_moves = []

    for p in possible_coords:
        possible_moves.append(
            {'dir': GetDir(p, (me[0]['y'], me[0]['x'])), 'score': board[p], 'coord': p})

    # for p in possible_moves:
    #     foodDistances = []
    #     for f in food:
    #         foodDistances.append(GetManhatten(p['coord'], f))
    #     print(foodDistances)
    #     p['score'] += 1 / min(foodDistances)

    possible_moves = sorted(
        possible_moves, key=lambda i: i['score'], reverse=True)

    if(possible_moves[0]['score'] == possible_moves[1]['score'] and possible_moves[1]['score'] == possible_moves[2]['score']):
        return move_response(possible_moves[randint(0, 2)]['dir'])
    else:
        return move_response(possible_moves[0]['dir'])


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    # print(json.dumps(data))

    return end_response()


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
