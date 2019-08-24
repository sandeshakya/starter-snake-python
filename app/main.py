import json
import os
import random
import bottle
import numpy as np

from app.api import ping_response, start_response, move_response, end_response


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
    print('in start------------------------------------------------------')
    data = bottle.request.json

    print(json.dumps(data))

    color = "#736CCB"

    print('exiting start------------------------------------------------')

    return start_response(color)


@bottle.post('/move')
def move():
    print('turn --------------------------------------------------------')
    data = bottle.request.json

    # Variable initalization
    width = data['board']['width']
    height = data['board']['height']
    board = np.full((width + 1, height + 1), 2)
    headX = int(json.dumps(data['you']['body'][0]['x']), 10) + 1
    headY = int(json.dumps(data['you']['body'][0]['y']), 10) + 1

    neckX = int(json.dumps(data['you']['body'][1]['x']), 10) + 1
    neckY = int(json.dumps(data['you']['body'][1]['y']), 10) + 1

    # set edge values to zero so we dont move there
    board[:, 0] = 0
    board[0, :] = 0
    board[:, height] = 0
    board[width, :] = 0

    def lookFoward(head, neck):
        if (head[1] == neck[1]) and (head[0] < neck[0]):
            forwardGridVal = board[head[0]-1, head[1]].item()
            direction = 'left'
            return forwardGridVal, direction
        elif (head[1] == neck[1]) and (head[0] > neck[0]):
            forwardGridVal = board[head[0]+1, head[1]].item()
            direction = 'right'
            return forwardGridVal, direction
        elif (head[0] == neck[0]) and (head[1] < neck[1]):
            forwardGridVal = board[head[0], head[1]-1].item()
            direction = 'up'
            return forwardGridVal, direction
        elif (head[0] == neck[0]) and (head[1] > neck[1]):
            forwardGridVal = board[head[0], head[1]+1].item()
            direction = 'down'
            return forwardGridVal, direction

    def lookRight(head, neck):
        if (head[1] == neck[1]) and (head[0] < neck[0]):
            forwardGridVal = board[head[0], head[1]+1].item()
            direction = 'down'
            return forwardGridVal, direction
        elif (head[1] == neck[1]) and (head[0] > neck[0]):
            forwardGridVal = board[head[0], head[1]-1].item()
            direction = 'up'
            return forwardGridVal, direction
        elif (head[0] == neck[0]) and (head[1] < neck[1]):
            forwardGridVal = board[head[0]-1, head[1]].item()
            direction = 'left'
            return forwardGridVal, direction
        elif (head[0] == neck[0]) and (head[1] > neck[1]):
            forwardGridVal = board[head[0]+1, head[1]].item()
            direction = 'right'
            return forwardGridVal, direction

    def lookLeft(head, neck):
        if (head[1] == neck[1]) and (head[0] < neck[0]):
            forwardGridVal = board[head[0], head[1] - 1].item()
            direction = 'left'
            return forwardGridVal, direction
        elif (head[1] == neck[1]) and (head[0] > neck[0]):
            forwardGridVal = board[head[0], head[1] + 1].item()
            direction = 'right'
            return forwardGridVal, direction
        elif (head[0] == neck[0]) and (head[1] < neck[1]):
            forwardGridVal = board[head[0] + 1, head[1]].item()
            direction = 'up'
            return forwardGridVal, direction
        elif (head[0] == neck[0]) and (head[1] > neck[1]):
            forwardGridVal = board[head[0] - 1, head[1]].item()
            direction = 'down'
            return forwardGridVal, direction

    print(data['turn'])
    print('----------------------------------------------')
    forwardTuple = lookFoward((headX, headY), (neckX, neckY))
    leftTuple = lookLeft((headX, headY), (neckX, neckY))
    rightTuple = lookRight((headX, headY), (neckX, neckY))

    print(forwardTuple)
    print(leftTuple)
    print(rightTuple)
    print('-----------------------------------------------')

    if int(forwardTuple[0]) == 0:
        return move_response('right')
    else:
        return move_response(forwardTuple[1])


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

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
