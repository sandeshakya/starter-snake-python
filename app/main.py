import json
import os
import bottle
import numpy as np

from api import ping_response, start_response, move_response, end_response


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

    me = data['you']['body']

    # Variable initalization
    width = data['board']['width']
    height = data['board']['height']

    board = np.full((width + 1, height + 1), 2)

    for limb in me:
        board[limb['y'], limb['x']] = -1




    


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
