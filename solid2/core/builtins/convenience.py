from ...config import config
from ..object_base import ObjectBase, OperatorMixin, AccessSyntaxMixin
from .primitives import *

# =============
# = modifiers =
# =============
class ModifierBase(ObjectBase, OperatorMixin, AccessSyntaxMixin):
    def __init__(self, child=None):
        super().__init__()
        if child:
            self._children += [child]

class debug(ModifierBase):
    def _render(self):
        return "#" + super()._render()

class background(ModifierBase):
    def _render(self):
        return "%" + super()._render()

class root(ModifierBase):
    def _render(self):
        return "!" + super()._render()

class disable(ModifierBase):
    def _render(self):
        return "*" + super()._render()

# ==============
# = Directions =
# ==============
def up(z): return translate((0, 0, z))
def down(z): return translate((0, 0, -z))
def right(x): return translate((x, 0, 0))
def left(x): return translate((-x, 0, 0))
def forward(y): return translate((0, y, 0))
def fwd(y): return forward(y)
def back(y): return translate((0, -y, 0))

def translateX(x) : return translate((x, 0, 0))
def translateY(y) : return translate((0, y, 0))
def translateZ(z) : return translate((0, 0, z))

def rotateX(x): return rotate((x, 0, 0))
def rotateY(y): return rotate((0, y, 0))
def rotateZ(z): return rotate((0, 0, z))

def scaleX(x): return scale((x, 1, 1))
def scaleY(y): return scale((1, y, 1))
def scaleZ(z): return scale((1, 1, z))

if not config.use_implicit_builtins:
    def resizeX(x): return resize((x, 0, 0))
    def resizeY(y): return resize((0, y, 0))
    def resizeZ(z): return resize((0, 0, z))

    def mirrorX(): return mirror((1, 0, 0))
    def mirrorY(): return mirror((0, 1, 0))
    def mirrorZ(): return mirror((0, 0, 1))

# ==============================================
# = overwrite translate, rotate, scale, mirror =
# ==============================================
"""
    This block overwrites translate, scale, mirror and rotate from builtins
    to allow "overloading" those functions.
    As result you don't need to pass vectors in as lists, you can provide
    them as single integers / floats.

    translate([1, 2, 3])  ->   translate(1, 2, 3)
    rotate([1, 2, 3])   -> rotate(1, 2, 3)
"""
def extract_size_list(size_count, *args):
    if len(args) <= 1:
        return args

    size_list = []
    args_copy = list(args)

    while args_copy and len(size_list) < size_count:
        a = args_copy.pop(0)
        if type(a) == int or type(a) == float:
            size_list += [a]
        else:
            args_copy = [a] + args_copy
            break

    if len(size_list) == size_count:
        return [size_list] + args_copy
    else:
        return size_list + args_copy

orig_translate = translate
def translate(*args, **kwargs):
    args = extract_size_list(3, *args)
    return orig_translate(*args, **kwargs)

orig_scale = scale
def scale(*args, **kwargs):
    args = extract_size_list(3, *args)
    return orig_scale(*args, **kwargs)

orig_rotate = rotate
def rotate(*args, **kwargs):
    args = extract_size_list(3, *args)
    return orig_rotate(*args, **kwargs)

orig_square = square
def square(*args, **kwargs):
    args = extract_size_list(2, *args)
    return orig_square(*args, **kwargs)

orig_cube = cube
def cube(*args, **kwargs):
    args = extract_size_list(3, *args)
    return orig_cube(*args, **kwargs)

if not config.use_implicit_builtins:
    orig_resize = resize
    def resize(*args, **kwargs):
        args = extract_size_list(3, *args)
        return orig_resize(*args, **kwargs)

    orig_mirror = mirror
    def mirror(*args, **kwargs):
        args = extract_size_list(3, *args)
        return orig_mirror(*args, **kwargs)

