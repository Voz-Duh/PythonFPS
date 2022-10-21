import math
import random
import time

import render
import vectors as vec


class Player:
    name = ''
    health = 5
    position = vec.tor2(0, 0)
    direction = 0

    def __init__(self, name: str, health: int, position: vec.tor2, direction: float):
        self.name = name
        self.health = health
        self.position = position
        self.direction = direction


class Tile:
    def __init__(self, color, black_color, **kwargs):
        self.black_color = black_color
        self.color = color
        if kwargs.__contains__('mirror'): self.mirror = kwargs.get('mirror')


class RaycastResult:
    obj = Tile('', '')
    distance = 0

    def __init__(self, obj, distance):
        self.obj = obj
        self.distance = distance


window = render.Window('3DGame', 400, 400, 'black')

quality = 100# max(int(input('Quality of game: ')), 20)

fov = 40
fov_plane = 0.1

ora = Tile(render.Color(hex='#D8683C'), render.Color(hex='#6B3017'))
gre = Tile(render.Color(hex='#60F243'), render.Color(hex='#116800'))
whi = Tile(render.Color(hex='#D2EFEF'), render.Color(hex='#116800'))
yel = Tile(render.Color(hex='#FFCF42'), render.Color(hex='#99550D'))
play_map = [
    [yel, yel, yel, yel, yel, yel, yel, yel, yel, yel, ora, ora, ora, ora, ora, ora, ora, ora, ora, ora, ora, ora, ora],
    [yel, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', yel, ora, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ora],
    [yel, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ora],
    [yel, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', yel, ora, ' ', ' ', whi, whi, whi, ' ', whi, whi, whi, ' ', ' ', ora],
    [yel, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', yel, ora, ' ', ' ', whi, ' ', ' ', ' ', ' ', ' ', whi, ' ', ' ', ora],
    [yel, yel, ' ', yel, ' ', yel, yel, yel, yel, yel, ora, ' ', ' ', whi, ' ', ' ', ' ', ' ', ' ', whi, ' ', ' ', ora],
    [ora, ora, ' ', ora, ' ', ora, ora, ora, ora, ora, ora, ' ', ' ', whi, ' ', ' ', ' ', ' ', ' ', whi, ' ', ' ', ora],
    [gre, ' ', ' ', ' ', ' ', ' ', gre, ora, ' ', ' ', ora, ' ', ' ', whi, ' ', ' ', ' ', ' ', ' ', whi, ' ', ' ', ora],
    [gre, ' ', ' ', ' ', ' ', ' ', gre, ora, ' ', ' ', ' ', ' ', ' ', whi, ' ', ' ', ' ', ' ', ' ', whi, ' ', ' ', ora],
    [gre, ' ', ' ', ' ', ' ', ' ', ' ', ora, ' ', ' ', ora, ' ', ' ', whi, ' ', gre, gre, gre, ' ', whi, ' ', ' ', ora],
    [gre, ' ', ' ', ' ', ' ', ' ', ' ', ora, ' ', ' ', ora, ora, ' ', ora, ora, ora, ora, ora, ora, ora, ora, ' ', ora],
    [gre, ' ', ' ', ' ', ' ', ' ', ' ', ora, ' ', ' ', ora, ' ', ' ', ora, ' ', ' ', ' ', ' ', ' ', ora, ' ', ' ', ora],
    [gre, ' ', ' ', ' ', ' ', ' ', ' ', ora, ' ', ' ', ora, ' ', ' ', ora, ' ', ' ', ' ', ' ', ' ', ora, ' ', ' ', ora],
    [gre, ' ', ' ', ' ', ' ', ' ', ' ', ora, ' ', ' ', ora, ' ', ' ', ora, ' ', ' ', ' ', ' ', ' ', ora, ' ', ' ', ora],
    [gre, ' ', ' ', ' ', ' ', ' ', ' ', ora, ' ', ' ', ora, ' ', ' ', ora, ' ', ' ', ' ', ' ', ' ', ora, ' ', ' ', ora],
    [gre, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ora, ' ', ' ', ora],
    [gre, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ora, ' ', ora, ora],
    [gre, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ora, ' ', ' ', ora],
    [gre, ' ', ' ', ' ', ' ', ' ', ' ', ora, ' ', ' ', ora, ' ', ' ', ora, ' ', ' ', ' ', ' ', ' ', ora, ' ', ' ', ora],
    [gre, ' ', ' ', ' ', ' ', ' ', ' ', ora, ' ', ' ', ora, ' ', ' ', ora, ' ', ' ', ' ', ' ', ' ', ora, ' ', ' ', ora],
    [gre, ' ', ' ', ' ', ' ', ' ', ' ', ora, ' ', ' ', ora, ' ', ' ', ora, ' ', ' ', ' ', ' ', ' ', ora, ' ', ' ', ora],
    [gre, ' ', ' ', ' ', ' ', ' ', ' ', ora, ' ', ' ', ora, ' ', ' ', ora, ' ', ' ', ' ', ' ', ' ', ora, ' ', ' ', ora],
    [gre, ' ', ' ', ' ', ' ', ' ', ' ', ora, ' ', ' ', ora, ora, ' ', ora, ora, ora, ora, ora, ora, ora, ora, ' ', ora],
    [gre, ' ', ' ', ' ', ' ', ' ', ' ', ora, ' ', ' ', ora, ' ', ' ', whi, ' ', gre, gre, gre, ' ', whi, ' ', ' ', ora],
    [gre, ' ', ' ', ' ', ' ', ' ', ' ', ora, ' ', ' ', ' ', ' ', ' ', whi, ' ', ' ', ' ', ' ', ' ', whi, ' ', ' ', ora],
    [yel, ' ', yel, yel, ' ', ' ', ' ', ora, ' ', ' ', ora, ' ', ' ', whi, ' ', ' ', ' ', ' ', ' ', whi, ' ', ' ', ora],
    [yel, ' ', ' ', yel, ' ', ' ', ' ', ora, ora, ora, ora, ' ', ' ', whi, ' ', ' ', ' ', ' ', ' ', whi, ' ', ' ', ora],
    [yel, ' ', ' ', yel, ' ', ' ', ' ', ' ', ' ', ' ', ora, ' ', ' ', whi, ' ', ' ', ' ', ' ', ' ', whi, ' ', ' ', ora],
    [yel, ' ', ' ', yel, ' ', ' ', ' ', ' ', ' ', ' ', ora, ' ', ' ', whi, ' ', ' ', ' ', ' ', ' ', whi, ' ', ' ', ora],
    [yel, ' ', ' ', yel, ' ', ' ', ' ', ' ', ' ', ' ', ora, ' ', ' ', whi, whi, whi, ' ', whi, whi, whi, ' ', ' ', ora],
    [yel, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ora, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ora],
    [yel, ' ', ' ', yel, ' ', ' ', ' ', gre, gre, gre, ora, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ora],
    [yel, yel, yel, yel, gre, gre, gre, gre, gre, gre, ora, ora, ora, ora, ora, ora, ora, ora, ora, ora, ora, ora, ora],
]
spawn_points = [vec.tor2(16, 6), vec.tor2(16, 16), vec.tor2(16, len(play_map) - 6), vec.tor2(2, len(play_map) - 3), vec.tor2(5, len(play_map)/2)]

window.current_player = 0
window.players = []
for i in range(0, 4):
    point = spawn_points[random.randint(0, len(spawn_points) - 1)]
    spawn_points.remove(point)
    get_player = input('Player {0} name: '.format(i + 1))
    if get_player == '':
        break
    window.players.append(Player(get_player, 5, point, random.randrange(0, 360)))

max_step = int(max(len(play_map[0]), len(play_map)) * 5)
step_range = 0.2
view_distance = max_step * step_range/2


def clamp(v, s, e):
    return min(max(v, s), e)


def get_box_dist(_from, to):
    return vec.tor2(clamp(_from.x, to.x - 0.5, to.x + 0.5), clamp(_from.y, to.y - 0.5, to.y + 0.5)).len_to(_from)

def dot(a, b):
    return a.x * b.x + a.y * b.y


def reflect(incident_direction, normal):
    return incident_direction - (normal * dot(incident_direction, normal)) * 2

def raycast(direction, origin: vec.tor2, not_player):
    _origin = origin.clone()
    old_origin = _origin.clone()
    for i in range(0, max_step):
        _origin += vec.tor2(vec.dcos(direction) * step_range, vec.dsin(direction) * step_range)

        map_orig_x = math.floor(_origin.x)
        map_orig_y = math.floor(_origin.y)

        for p in range(0, len(window.players)):
            if p != not_player:
                pp_x = window.players[p].position.x
                pp_y = window.players[p].position.y
                if pp_x - 0.5 < _origin.x < pp_x + 0.5:
                    if pp_y - 0.5 < _origin.y < pp_y + 0.5:
                        _origin = vec.tor2(clamp(old_origin.x, pp_x - 0.5, pp_x + 0.5),
                                           clamp(old_origin.y, pp_y - 0.5, pp_y + 0.5))
                        return RaycastResult(Tile(render.Color(r=255), render.Color(r=100)), clamp(origin.len_to(_origin) / view_distance, 0, 1))

        if 0 <= map_orig_x < len(play_map[0]) and 0 <= map_orig_y < len(play_map):
            if play_map[map_orig_y][map_orig_x] != ' ':
                _origin = vec.tor2(clamp(old_origin.x, map_orig_x, map_orig_x + 1),
                                   clamp(old_origin.y, map_orig_y, map_orig_y + 1))
                return RaycastResult(play_map[map_orig_y][map_orig_x], clamp(origin.len_to(_origin) / view_distance, 0, 1))
        old_origin = _origin.clone()
    return None

def shoot(self, direction, origin, not_player):
    _origin = origin.clone()
    distance = 0
    for i in range(0, max_step):
        for p in range(0, len(window.players)):
            if p != not_player:
                if window.players[p].position.x - 0.5 <= _origin.x < window.players[p].position.x + 0.5:
                    if window.players[p].position.y - 0.5 <= _origin.y < window.players[p].position.y + 0.5:
                        window.players[p].health -= 1
                        self.input_event =\
                            'PLAYER {0} GET HIT\nRIGHT MOUSE BUTTON TO CONTINUE'.format(window.players[p].name.upper())
                        if window.players[p].health <= 0:
                            window.players.remove(window.players[p])
                        return RaycastResult(p, distance / (max_step * step_range))
        _origin += vec.tor2(vec.dcos(direction) * step_range,
                            vec.dsin(direction) * step_range)
        distance += step_range
    return RaycastResult(Tile(render.Color(), render.Color()), distance / (max_step * step_range))


def raycast_step(direction, origin, max_step, step_range):
    _origin = origin.clone()
    distance = 0
    for i in range(0, max_step):
        map_orig_x = math.floor(_origin.x)
        map_orig_y = math.floor(_origin.y)

        if 0 <= map_orig_x < len(play_map[0]):
            if 0 <= map_orig_y < len(play_map):
                if play_map[map_orig_y][map_orig_x] != ' ':
                    return '0'
        _origin.x += vec.dcos(direction) * step_range
        _origin.y += vec.dsin(direction) * step_range
        distance += step_range
    return ' '


player_steps = 100
window.current_steps = player_steps


def move_player(player, speed) -> int:
    last_pos = player.position.clone()
    player.position.x += vec.dcos(player.direction) * speed
    player.position.y += vec.dsin(player.direction) * speed

    map_orig_x = math.floor(player.position.x)
    map_orig_y = math.floor(player.position.y)

    if 0 <= map_orig_x < len(play_map[0]):
        if 0 <= map_orig_y < len(play_map):
            if play_map[map_orig_y][map_orig_x] != ' ':
                player.position = last_pos
                return 0
    return -1


window.input_event = ''
window.input_func = None

def win_draw(self: render.Window):
    if self.input_event != '':
        self.draw_text(vec.tor2(0, 0), self.input_event, fill=render.Color(r=40, g=120, b=200).hex)
        return

    hits = []
    for f in range(0, quality):
        direction = self.players[self.current_player].direction
        view_power = (f / quality - 0.5) * 2
        hits.append(raycast(direction + view_power * fov,
                    self.players[self.current_player].position +
                    vec.tor2(vec.dsin(direction) * view_power * -fov_plane, vec.dcos(direction) * view_power * -fov_plane),
                    self.current_player))

    self.draw_rectangle_from_to(vec.tor2(-self.window_size.x / 2, self.window_size.y / 6),
                                vec.tor2(self.window_size.x / 2, self.window_size.y / 2),
                                fill=render.Color(hex='#4c1e0a').hex)
    for f in range(0, quality):
        if hits[f] is None:
            continue
        color = hits[f].obj.color.clone()
        black_color = hits[f].obj.black_color.clone()
        color.r = vec.lerp(color.r, black_color.r, hits[f].distance)
        color.g = vec.lerp(color.g, black_color.g, hits[f].distance)
        color.b = vec.lerp(color.b, black_color.b, hits[f].distance)
        color.update_hex()
        self.draw_rectangle(vec.tor2(-self.window_size.x / 2 + (self.window_size.x * (f / float(quality))), hits[f].distance * self.window_size.y / 6),
                            vec.tor2(self.window_size.x * (0.5 / quality),
                                     (1 - hits[f].distance) * self.window_size.y / 2),
                            fill=color.hex, outline='')
    self.draw_text(vec.tor2(0, self.window_size.y / 2 - 40),
                   'Player {0}; Health {1}; Steps: {2}; Can shoot: {3};'
                   .format(self.players[self.current_player].name, self.players[self.current_player].health,
                           self.current_steps, self.current_steps > 20), fill=render.Color().hex)
    #time.sleep(0.1)


def win_update(self: render.Window, dt):
    if self.input_event != '':
        if render.pressed('mouse3'):
            self.input_event = ''
            if self.input_func is not None: self.input_func(self)
            self.input_func = None
        return

    if render.pressed('d'):
        self.players[self.current_player].direction += 1
    if render.pressed('a'):
        self.players[self.current_player].direction -= 1

    speed = 0.1
    if render.pressed('w'):
        self.current_steps += move_player(self.players[self.current_player], speed)
    if render.pressed('s'):
        self.current_steps += move_player(self.players[self.current_player], -speed)

    if render.pressed('mouse1') and self.current_steps > 20:
        shoot(self, self.players[self.current_player].direction, self.players[self.current_player].position,
              self.current_player)
        self.current_steps = 20
        players_count = 0
        __player = None
        for _player in self.players:
            players_count += 1

        if players_count == 1 and __player is Player:
            self.input_event = f'PLAYER {__player.name.upper()} WIN\nRIGHT MOUSE BUTTON TO EXIT'

            def ex(self):
                exit()
            self.input_func = ex

    if self.current_steps == 0:
        self.current_player += 1
        if self.current_player >= len(self.players):
            self.current_player = 0
        self.current_steps = player_steps

        self.input_event = 'NEXT TURN\nRIGHT MOUSE BUTTON TO CONTINUE'


window.draw = win_draw
window.update = win_update

window.start()
