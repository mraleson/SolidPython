from solid2.core.object_base import OpenSCADConstant as _OpenSCADConstant
from solid2.core.scad_import import extra_scad_include as _extra_scad_include
from pathlib import Path as _Path

from .bosl2_base import Bosl2Base as _Bosl2Base

_extra_scad_include(f"{_Path(__file__).parent.parent / 'bosl2/BOSL2/color.scad'}", use_not_include=False)

class hsl(_Bosl2Base):
    def __init__(self, h=None, s=None, l=None, a=None, **kwargs):
       super().__init__("hsl", {"h" : h, "s" : s, "l" : l, "a" : a, **kwargs})

class hsv(_Bosl2Base):
    def __init__(self, h=None, s=None, v=None, a=None, **kwargs):
       super().__init__("hsv", {"h" : h, "s" : s, "v" : v, "a" : a, **kwargs})

class recolor(_Bosl2Base):
    def __init__(self, c=None, **kwargs):
       super().__init__("recolor", {"c" : c, **kwargs})

class color_this(_Bosl2Base):
    def __init__(self, c=None, **kwargs):
       super().__init__("color_this", {"c" : c, **kwargs})

class rainbow(_Bosl2Base):
    def __init__(self, list=None, stride=None, maxhues=None, shuffle=None, seed=None, **kwargs):
       super().__init__("rainbow", {"list" : list, "stride" : stride, "maxhues" : maxhues, "shuffle" : shuffle, "seed" : seed, **kwargs})

class hsl(_Bosl2Base):
    def __init__(self, h=None, s=None, l=None, a=None, **kwargs):
       super().__init__("hsl", {"h" : h, "s" : s, "l" : l, "a" : a, **kwargs})

class hsv(_Bosl2Base):
    def __init__(self, h=None, s=None, v=None, a=None, **kwargs):
       super().__init__("hsv", {"h" : h, "s" : s, "v" : v, "a" : a, **kwargs})

