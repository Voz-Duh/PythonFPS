import time
import tkinter as tk
import vectors as vec

class Triangle:
    pos0, pos1, pos2 = vec.tor2(0, 0), vec.tor2(0, 0), vec.tor2(0, 0)

class Input:
    mouse_pos = vec.tor2(0, 0)
    buttons = {}

class Color:
    r, g, b = 0, 0, 0
    hex = ''

    def __init__(self, **kwargs):
        if kwargs.__contains__('hex'):
            self.hex = kwargs.get('hex')
            rgb = from_hex(self.hex)
            self.r = rgb.r
            self.g = rgb.g
            self.b = rgb.b
        else:
            if kwargs.__contains__('r'): self.r = kwargs.get('r')
            if kwargs.__contains__('g'): self.g = kwargs.get('g')
            if kwargs.__contains__('b'): self.b = kwargs.get('b')
            self.hex = from_rgb(self.r, self.g, self.b)

    def clone(self):
        return Color(r=self.r, g=self.g, b=self.b)

    def update_hex(self):
        self.hex = from_rgb(self.r, self.g, self.b)

def from_hex(hex):
    hex = hex.lstrip('#')
    rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
    return Color(r=rgb[0], g=rgb[1], b=rgb[2])

def clamp(x):
    return int(max(0, min(x, 255)))

def from_rgb(r, g, b):
    return "#{0:02x}{1:02x}{2:02x}".format(clamp(r), clamp(g), clamp(b))

def pressed(key):
    try:
        return Input.buttons[key.upper()][0]
    except KeyError:
        return False


class Window:
    def __init__(self, title: str, width: int, height: int, background_color: str):
        self.background_color = background_color
        self.height = height
        self.width = width

        self.root = tk.Tk()
        self.root.title(title)

        self.canvas = tk.Canvas(self.root)
        self.canvas.destroy()

        self.root.geometry('{0}x{1}'.format(width, height))

        def motion(event):
            Input.mouse_pos = vec.tor2(event.x, event.y)
        self.root.bind('<Motion>', motion)

        def any_click(event):
            but = f'MOUSE{event.num}'

            Input.buttons[but] = [True, 6]

        self.root.bind("<Button>", any_click)

        def any_key(event):
            but = event.char.upper()

            Input.buttons[but] = [True, 6]
        self.root.bind("<Key>", any_key)

        self.window_size = vec.tor2(width, height)
        self.camera = vec.tor2(0, 0)
        self.old_ms = time.time()

    def update(self, _self, dt) -> None:
        return None

    def draw(self, _self) -> None:
        return None

    def from_ui(self, pos):
        return pos + self.camera - self.window_size / 2

    def draw_circle(self, pos, r, **kwargs):
        pos = pos - self.camera + self.window_size / 2
        return self.canvas.create_oval(pos.x - r, pos.y - r, pos.x + r, pos.y + r, **kwargs)

    def draw_rectangle(self, pos, size, **kwargs):
        pos = pos - self.camera + self.window_size / 2
        return self.canvas.create_rectangle(pos.x - size.x, pos.y - size.y, pos.x + size.x, pos.y + size.y, **kwargs)

    def draw_rectangle_from_to(self, pos0, pos1, **kwargs):
        pos0 = pos0 - self.camera + self.window_size / 2
        pos1 = pos1 - self.camera + self.window_size / 2
        return self.canvas.create_rectangle(pos0.x, pos0.y, pos1.x, pos1.y, **kwargs)

    def draw_text(self, pos, text, **kwargs):
        pos = pos - self.camera + self.window_size / 2
        return self.canvas.create_text(pos.x, pos.y, text=text, **kwargs)

    def start(self):
        while True:
            t_ms = time.time()
            dt = self.old_ms - t_ms
            self.old_ms = t_ms

            self.update(self, dt)

            self.canvas = tk.Canvas(self.root, width=self.root.winfo_width(), height=self.root.winfo_height(), borderwidth=0, highlightthickness=0, bg=self.background_color)
            self.canvas.grid()
            #print(dir(self.canvas))
            #break

            self.draw(self)

            self.root.update_idletasks()
            for but in Input.buttons:
                if Input.buttons[but][1] != 0:
                    Input.buttons[but][1] -= 1
                else:
                    Input.buttons[but][0] = False
            self.root.update()

            self.window_size = vec.tor2(self.canvas.winfo_width(), self.canvas.winfo_height())
            self.canvas.destroy()
