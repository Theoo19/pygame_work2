from ..change.timeline import TimeLine as _TimeLine
from .display import Display as _Display
from ..pc_input.mouse import Mouse as _Mouse
from ..pc_input.event import Events as _Events
from ..pc_input.keyboard import Keyboard as _Keyboard
from ..logic.constants import Default as _Default
from ..logic.time import Time as _Time
from pygame import VIDEORESIZE as _VIDEORESIZE, QUIT as _QUIT, MOUSEBUTTONUP as _MOUSEBUTTONUP, MOUSEBUTTONDOWN as \
     _MOUSEBUTTONDOWN, KEYDOWN as _KEYDOWN, KEYUP as _KEYUP, init as _pygame_init, get_init as _pygame_get_init, \
     quit as _pygame_quit, K_F4 as _K_F4, K_LALT as _K_LALT, K_RALT as _K_RALT
from pygame.time import Clock as _Clock


class _ShapeList:
    def __init__(self, shapes):
        self.__shapes = shapes
        self.__loop_behavior_shapes = list()
        self.__update_alignment_shapes = list()

        self.__reload_loop_behavior_shapes()
        self.__reload_update_alignment_shapes()

    def __reload_loop_behavior_shapes(self):
        self.__loop_behavior_shapes = list(shape for shape in self.__shapes if hasattr(shape, "loop_behavior"))

    def __reload_update_alignment_shapes(self):
        self.__update_alignment_shapes = list(shape for shape in self.__shapes if hasattr(shape, "update_alignment"))

    def __append_shape_update(self, shape):
        if hasattr(shape, "loop_behavior"):
            self.__loop_behavior_shapes.append(shape)
        if hasattr(shape, "update_alignment"):
            self.__update_alignment_shapes.append(shape)

    def get_loop_behavior_shapes(self):
        return self.__loop_behavior_shapes

    def get_update_alignment_shapes(self):
        return self.__update_alignment_shapes

    def append(self, shape):
        self.__shapes.append(shape)
        self.__append_shape_update(shape)

    def clear(self):
        self.__shapes.clear()
        self.__loop_behavior_shapes.clear()
        self.__update_alignment_shapes.clear()

    def count(self, shape):
        return self.__shapes.count(shape)

    def extend(self, shapes):
        self.__shapes.extend(shapes)
        self.__loop_behavior_shapes.extend(shape for shape in shapes if hasattr(shape, "loop_behavior"))
        self.__update_alignment_shapes.extend(shape for shape in shapes if hasattr(shape, "update_alignment"))

    def index(self, shape):
        return self.__shapes.index(shape)

    def insert(self, index, shape):
        self.__shapes.insert(index, shape)
        self.__append_shape_update(shape)

    def pop(self, index):
        self.__shapes.pop(index)
        self.__reload_loop_behavior_shapes()
        self.__reload_update_alignment_shapes()

    def remove(self, shape):
        self.__shapes.remove(shape)
        self.__reload_loop_behavior_shapes()
        self.__reload_update_alignment_shapes()

    def reverse(self):
        self.__shapes.reverse()
        self.__loop_behavior_shapes.reverse()
        self.__update_alignment_shapes.reverse()

    def sort(self):
        pass

    def __len__(self):
        return len(self.__shapes)

    def __getitem__(self, key):
        return self.__shapes[key]

    def __setitem__(self, key, value):
        self.__shapes[key] = value
        self.__reload_loop_behavior_shapes()
        self.__reload_update_alignment_shapes()

    def __delitem__(self, key):
        pass

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        if self.__index < len(self.__shapes):
            shape = self.__shapes[self.__index]
            self.__index += 1
            return shape
        else:
            raise StopIteration


class Page:
    def __init__(self, name, shapes, **variables):
        self.name = name
        self.shapes = _ShapeList(shapes)
        self.variables = variables
        self.running = False
        self.background_color = _Default.background_color
        self.timeline = _TimeLine()

    def init(self):
        self.update_shapes_pos()

    def loop(self):
        while self.running:
            _Display.fill(self.background_color)
            for shape in self.shapes.get_loop_behavior_shapes():
                shape.loop_behavior()
            for shape in self.shapes:
                shape.draw(_Display.surface)
            self.loop_function()
            self.timeline.update()
            Application.update()

    def quit(self):
        pass

    def loop_function(self):
        pass

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def set_shapes(self, shapes):
        self.shapes = _ShapeList(shapes)

    def update_shapes_pos(self):
        _Display.update_shapes_pos(self.shapes.get_update_alignment_shapes())

    def __getitem__(self, item):
        return self.variables[item]


class Application:
    pages = dict()
    selected_name = None
    selected_page = None
    running = True
    clock = _Clock()
    ticks = _Default.ticks

    @staticmethod
    def init(page_name, ticks=_Default.ticks):
        if not _pygame_get_init():
            _pygame_init()
        Application.set_ticks(ticks)
        Application.selected_name = page_name

    @staticmethod
    def quit():
        _pygame_quit()

    @staticmethod
    def set_ticks(ticks):
        Application.ticks = ticks
        _Time.application_factor = ticks

    @staticmethod
    def set_page(page_name):
        Application.selected_name = page_name
        Application.update_page()

    @staticmethod
    def update_page():
        if hasattr(Application.selected_page, "stop"):
            Application.selected_page.stop()
        Application.selected_page = Application.pages[Application.selected_name]
        if hasattr(Application.selected_page, "start"):
            Application.selected_page.start()

    @staticmethod
    def get_page(page_name):
        return Application.pages[page_name]

    @staticmethod
    def get_current_page():
        return Application.selected_page

    @staticmethod
    def add_page(page, name=None):
        if name is None:
            name = page.name
        Application.pages[name] = page

    @staticmethod
    def add_pages(*pages):
        for page in pages:
            Application.pages[page.name] = page

    @staticmethod
    def update():
        _Mouse.update()
        _Keyboard.update()
        _Display.flip()
        _Events.update()
        Application.clock.tick(Application.ticks)

    @staticmethod
    def loop():
        while Application.running:
            Application.update_page()
            Application.selected_page.init()
            Application.selected_page.loop()
            Application.selected_page.quit()

    @staticmethod
    @_Events.new(_VIDEORESIZE)
    def update_screen():
        event = _Events.get_current()
        _Display.set_size(event.w, event.h)
        if hasattr(Application.selected_page, "update_shapes_pos"):
            Application.selected_page.update_shapes_pos()

    @staticmethod
    @_Events.new(_QUIT)
    @_Keyboard.key_bind_down(_K_LALT, _K_F4)
    @_Keyboard.key_bind_down(_K_RALT, _K_F4)
    def stop():
        if hasattr(Application.selected_page, "stop"):
            Application.selected_page.stop()
        Application.running = False

    @staticmethod
    @_Events.new(_MOUSEBUTTONDOWN)
    def update_mouse_button_down():
        button = _Events.get_current().button
        _Mouse.update_button_down(button)

    @staticmethod
    @_Events.new(_MOUSEBUTTONUP)
    def update_mouse_button_up():
        button = _Events.get_current().button
        _Mouse.update_button_up(button)

    @staticmethod
    @_Events.new(_KEYDOWN)
    def update_keyboard_down():
        _Keyboard.key_press_down(_Events.get_current())

    @staticmethod
    @_Events.new(_KEYUP)
    def update_keyboard_up():
        _Keyboard.key_press_up(_Events.get_current())
