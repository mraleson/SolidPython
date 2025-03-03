from .access_syntax_mixin import AccessSyntaxMixin
from .operator_mixin import OperatorMixin

#don't do relative imports on the global scope to be able to import this file
#from "everywhere"

class RenderMixin:
    def __repr__(self):
        return self.as_scad()

    def as_scad(self):
        from ..scad_render import scad_render
        return scad_render(self)[:-1]

    def save_as_scad(self, filename='', outdir=''):
        from ..scad_render import scad_render_to_file
        return scad_render_to_file(self, filename, outdir)

    def save_as_stl(self, filename=None):
        from ..scad_render import render_to_stl_file
        return render_to_stl_file(self, filename)

class ObjectBase(RenderMixin):
    def __init__(self):
        self._children = []

    def add(self, c):
        def _add(c):
            assert(hasattr(c, "_render"))
            self._children += [c]

        if isinstance(c, list):
            for cc in c:
                _add(cc)
        else:
            _add(c)

        return self

    def _render(self):
        s = ''
        for c in self._children:
            s += c._render()
        return s

    def __call__(self, *args):
        #translate(...)(cube())
        #this adds cube() to translate._children
        for a in args:
            self.add(a)
        return self


class BareOpenSCADObject(ObjectBase):
    def __init__(self, name, params):
        super().__init__()
        self._name = name
        self._params = params

    def _render(self):
        """
            returns the scad code for a given node tuple consiting of name,
            params and children list.

            -> translate(v = [1, 2, 3]) {children[0]; children[1]; ...};\n
        """
        from ..utils import indent
        renderedChildsList = [indent(child._render()) for child in self._children]
        if renderedChildsList:
            renderedChilds = f" {{\n{''.join(renderedChildsList)}}}\n"
        else:
            renderedChilds = ";\n"

        return self._generate_scad_head() + renderedChilds

    def _generate_scad_head(self):
        """
            for a given function name and dict of params it returns:
                {name}(p1=v1, p2=v2,...)
                -> translate(v = [1, 2, 3])
        """
        from ..utils import unescape_openscad_identifier, py2openscad
        from ...config import config

        param_strings = []
        for p in sorted(self._params.keys()):
            if self._params[p] is None:
                continue

            if config.use_implicit_builtins and \
                        isinstance(self._params[p], OpenSCADParameterFunction):

                param_strings.append(self._params[p]._render())
            else:
                scad_value = py2openscad(self._params[p])
                scad_identifier = unescape_openscad_identifier(p)

                param_strings.append(f'{scad_identifier} = {scad_value}')

        scad_identifier = unescape_openscad_identifier(self._name)
        param_str = ", ".join(param_strings)

        return f'{scad_identifier}({param_str})'

class OpenSCADObject(AccessSyntaxMixin, OperatorMixin, BareOpenSCADObject):
    pass

class OpenSCADConstant:
    def __init__(self, value):
        self.value = value

        from ..utils import escape_openscad_identifier
        self.__doc__ = escape_openscad_identifier(value)

    def __repr__(self):
        return f'{self.value}'

    def __operator_base__(self, op, other):
        return OpenSCADConstant(f'({self} {op} {other})')

    def __roperator_base__(self, op, other):
        return OpenSCADConstant(f'({other} {op} {self})')

    def __unary_operator_base__(self, op):
        return OpenSCADConstant(f'({op}{self})')

    def __illegal_operator__(self):
       raise Exception("You can't compare a OpenSCADConstant with something else, " +\
                       "because we don't know the customized value at " +\
                       "SolidPythons runtime because it might get customized " +\
                       "at OpenSCAD runtime.")

    #basic operators +, -, *, /, %, **
    def __add__(self, other): return self.__operator_base__("+", other)
    def __sub__(self, other): return self.__operator_base__("-", other)
    def __mul__(self, other): return self.__operator_base__("*", other)
    def __mod__(self, other): return self.__operator_base__("%", other)
    def __pow__(self, other): return self.__operator_base__("^", other)
    def __truediv__(self, other): return self.__operator_base__("/", other)

    def __radd__(self, other): return self.__roperator_base__("+", other)
    def __rsub__(self, other): return self.__roperator_base__("-", other)
    def __rmul__(self, other): return self.__roperator_base__("*", other)
    def __rmod__(self, other): return self.__roperator_base__("%", other)
    def __rpow__(self, other): return self.__roperator_base__("^", other)
    def __rtruediv__(self, other): return self.__roperator_base__("/", other)

    #unary operators
    def __neg__(self): return self.__unary_operator_base__("-")

    #other operators
    def __abs__(self): return OpenSCADConstant(f'abs({self})')

    #"illegal" operators
    def __eq__(self, _): return self.__illegal_operator__()
    def __ne__(self, _): return self.__illegal_operator__()
    def __le__(self, _): return self.__illegal_operator__()
    def __ge__(self, _): return self.__illegal_operator__()
    def __lt__(self, _): return self.__illegal_operator__()
    def __gt__(self, _): return self.__illegal_operator__()

    #do not allow to evaluate to bool
    def __bool__(self):
        raise Exception("You can't use scad variables as truth statement because " +\
                        "we don't know the value of a customized variable at " +\
                        "SolidPython runtime.")

    def _render(self):
        from textwrap import dedent
        return dedent(self.value)

import math
sin = lambda x: OpenSCADConstant(f'sin({x})') if isinstance(x, OpenSCADConstant) else math.sin(x)
cos = lambda x: OpenSCADConstant(f'cos({x})') if isinstance(x, OpenSCADConstant) else math.cos(x)
tan = lambda x: OpenSCADConstant(f'tan({x})') if isinstance(x, OpenSCADConstant) else math.tan(x)
asin = lambda x: OpenSCADConstant(f'asin({x})') if isinstance(x, OpenSCADConstant) else math.asin(x)
acos = lambda x: OpenSCADConstant(f'acos({x})') if isinstance(x, OpenSCADConstant) else math.acos(x)
atan = lambda x: OpenSCADConstant(f'atan({x})') if isinstance(x, OpenSCADConstant) else math.atan(x)
sqrt = lambda x: OpenSCADConstant(f'sqrt({x})') if isinstance(x, OpenSCADConstant) else math.sqrt(x)
not_ = lambda x: OpenSCADConstant(f'!{x}')

def scad_inline(code):
    return OpenSCADConstant(code)

class OpenSCADParameterFunction(OpenSCADConstant):
    pass

def scad_inline_parameter_func(code):
    return OpenSCADParameterFunction(code)

