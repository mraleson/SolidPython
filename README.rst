
.. image:: https://readthedocs.org/projects/solidpython2/badge/?version=latest
    :target: http://solidpython2.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

**If you switch from the regular SolidPython:master branch to this branch, have a
look at** `Version 2.x.x`_.

SolidPython
===========

.. contents::
   
OpenSCAD for Python
-------------------

SolidPython is a generalization of Phillip Tiefenbacher's openscad
module, found on `Thingiverse <http://www.thingiverse.com/thing:1481>`__. It
generates valid OpenSCAD code from Python code with minimal overhead. Here's a
simple example:

This Python code:

.. code:: python

    from solid2 import *
    d = difference()(
        cube(10),
        sphere(15)
    )
    d.as_scad()

Generates this OpenSCAD code:

.. code:: python

    difference(){
        cube(10);
        sphere(15);
    }

That doesn't seem like such a savings, but the following SolidPython code is a
lot shorter (and I think clearer) than the SCAD code it compiles to:

.. code:: python

    from solid2 import *
    d = cube(5) + sphere(5).right(5) - cylinder(r=2, h=6)

Generates this OpenSCAD code:

.. code::

    difference(){
        union(){
            cube(5);
            translate( [5, 0,0]){
                sphere(5);
            }
        }
        cylinder(r=2, h=6);
    }

Advantages
----------

In contrast to OpenSCAD -- which is a constrained domain specific language --
Python is a full blown modern programming language and as such supports
pretty much all modern programming features. Furthermore a huge number of
libraries is available.

SolidPython lets you use all these fancy python features to generate your
constructive solid geometry models.

On the one hand it makes the generation of your models a lot easier, because
you don't need to learn another domain specific language and you can use all
the programming technique you're already familiar with. On the other hand it
gives you a lot more power, because you can use all the comprehensive python
libraries to generate your models.

I would almost say this enables you to do what ever you want with ease.
As (maybe little uncommon) example, you could write a program that:

  - looks up the mail adress of your actuall president (based on your ip address)
  - writes a mail to him or her and asks for a portrait
  - waits for a reply
  - generates a heightmap from the picture you received and maps it onto a vase

This should be pretty straight forward with SolidPython but is impossible with
pure OpenSCAD.

Furhtermore SolidPython 2.x.x is designed to be extendible. As such you can extend SolidPython itself using python. Actually parts of SolidPython itself are implemented as extensions (everything but the core one-to-one mapping of OpenScad to Python), these include operators, access style syntax, convenience functions, scad_interface and bosl2 support. Furthermore some of the SolidPython 1.x.x solid.utils features are also implemented as extensions (bill of material & part-hole).

Installing SolidPython
----------------------

-  Install latest release via
   `PyPI <https://pypi.python.org/pypi/solidpython2>`__:

   .. code:: bash

       pip install solidpython2

   (You may need to use ``sudo pip install solidpython2``, depending on
   your environment. This is commonly discouraged though. You'll be happiest 
   working in a `virtual environment <https://docs.python.org/3/tutorial/venv.html>`__ 
   where you can easily control dependencies for a given project)

- Install current master straight from Github:

  .. code:: bash

      pip install git+https://github.com/jeff-dh/SolidPython

Using SolidPython
-----------------

-  Include SolidPython at the top of your Python file:

   .. code:: python

       from solid2 import *

   (See `this issue <https://github.com/SolidCode/SolidPython/issues/114>`__ for 
   a discussion of other import styles)

-  OpenSCAD uses curly-brace blocks ({}) to create its tree. SolidPython
   uses parentheses with comma-delimited lists. 
   
   **OpenSCAD:**

   .. code::

       difference(){
           cube(10);
           sphere(15);
       }

   **SolidPython:**

   .. code::

       d = difference()(
           cube(10),  # Note the comma between each element!
           sphere(15)
       )

-  Call ``py_scad_obj.as_scad()`` to generate SCAD code. This returns
   a string of valid OpenSCAD code.
-  *or*: call ``py_scad_obj.save_as_scad("filepath.scad")`` to store
   that code in a file.
-  If ``filepath.scad`` is open in the OpenSCAD IDE and Design => 'Automatic
   Reload and Compile' is checked in the OpenSCAD IDE, running
   ``py_scad_obj.save_as_scad()`` from Python will load the object in the
   IDE.
-  Alternately, you could call OpenSCAD's command line and render
   straight to STL.

Tutorial - Example Code
-----------------------

The best way to learn how SolidPython works is to look at the included
example code. They are kind of a minimalistic SolidPython tutorial. If
you've installed SolidPython, the following line of Python will print
(the location of) the examples directory:

.. code:: python

    import os, solid2; print(os.path.dirname(solid2.__file__) + '/examples')
        

Or browse the example code on Github
`here <https://github.com/jeff-dh/SolidPython/tree/exp_solid/solid2/examples>`__

Extra syntactic sugar
=====================

Basic operators
---------------

SolidPython overrides the basic operators + and | (union), - (difference), \*
and & (intersection) and ~ (debug). So

.. code:: python

    c = cylinder(r=10, h=5) + cylinder(r=2, h=30)

is the same as:

.. code:: python

    c = union()(
        cylinder(r=10, h=5),
        cylinder(r=2, h=30)
    )

Likewise:

.. code:: python

    c = cylinder(r=10, h=5)
    c -= cylinder(r=2, h=30)

is the same as:

.. code:: python

    c = difference()(
        cylinder(r=10, h=5),
        cylinder(r=2, h=30)
    )

Access Style Syntax
-------------------

Since at least some people (including me) don't like the OpenSCAD Syntax, SolidPython 2.x.x introduces the support for the so called "Access-Style-Syntax". This enables you to call some of the SolidPython / OpenSCAD functions as member functions of any OpenSCADObject instead of wrapping it in an instance of it.

In other words, e.g. code:

.. code:: python

  up(10)(cube(1))
  #is equal to
  cube(1).up(10)

The available member functions are the following:

.. code:: python

  union, difference, intersection, translate, scale, rotate, mirror, resize,
  color, offset, hull, render, projection, surface, linear_extrude,
  rotate_extrude, debug, background, root and disable

Also the convenience functions are available:

.. code:: python

  up, down, left, right, forward, fwd, back, translateX, translateY, translateZ,
  rotateX, rotateY, rotateZ, mirrorX, mirrorY, mirrorZ, scaleX, scaleY, scaleZ,
  resizeX, resizeY, resizeZ

Furthermore you can chain these functions, because they all return the transformed OpenSCADObject, e.g.:

.. code:: python

  cube(1).up(10).back(20).rotate(10, 0, 5).mirror(1, 0, 0).color("green").root()

Convenience functions
---------------------

SolidPython includes a number of convenience functions. Currently these
include:

Directions for arranging things:

.. code:: python

  up, down, left, right, forward, fwd, back

Transformations per dimension:

.. code:: python

  translateX, translateY, translateZ, rotateX, rotateY, rotateZ, mirrorX,
  mirrorY, mirrorZ, resizeX, resizeY, resizeZ, scaleX, scaleY, scaleZ

Furthermore the operations `translate, scale, resize, mirror, rotate, cube and square` are overwritten in a way that they accept single integer or float values as first parameter. (`translate(1, 2, 3)` equals `translate([1, 2, 3])`)

.. code:: python

    cylinder().rotateY(90).up(10)

seems a lot clearer to me than:

.. code:: python

    translate([0,0,10])(
        rotate([0, 90, 0])(
          cylinder()
    ))

Features
========

BOSL2
-----

SolidPython supports -- at least -- quite a lot of the **bosl2** library. You can use it by importing the ``solid2.extensions.bosl2``. Take a look at `bosl2 example <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid2/examples/07-libs-bosl2.py>`_ and `mazebox example <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid2/examples/16-mazebox-bosl2.py>`_ to get an idea how to use it and what's possible.

I would suggest to use it as kind of a standard library for SolidPython.
Take a look at their `Wiki <https://github.com/revarbat/BOSL2/wiki>`_ to get an idea about it's features.


Animation, Customizer, custom Fonts, ImplicitCad, Extensions
------------------------------------------------------------

SolidPython supports the following features

* native **OpenSCAD customizer** support `customizer example <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid2/examples/10-customizer.py>`_ `greedy scad interface example <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid2/examples/17-greedy-scad-interface.py>`_
* native **OpenSCAD animation** support `animation example <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid2/examples/12-animation.py>`_ and `animation example 2 <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid2/examples/13-animated-bouncing-ball.py>`_
* **custom fonts** `fonts example <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid2/examples/11-fonts.py>`_
* supports **ImplicitCAD** `implicitCAD example <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid2/examples/14-implicitCAD.py>`_ `implicitCAD example 2 <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid2/examples/15-implicitCAD2.py>`_
* SolidPython is extendible `extensions example 1 <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid2/examples/08-extensions.py>`_  `extension example 2 <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid2/examples/09-code-attach-extension.py>`_

Jupyter Renderer
================

SolidPython can be rendered inside a Jupyter Notebook using ViewScad. Unfortunately the pypi version of ``viewscad`` seems to be not compatible with ``solid2``. @jreiberkyle created `this viewscad fork <https://github.com/jreiberkyle/ViewSCAD>`__ and made it work with `solid2` (`#7 <https://github.com/jeff-dh/SolidPython/issues/7>`__)

Version 2.x.x
=============

SolidPython 2.x.x is a refactored version of SolidPython 1.x.x.
The refactoring process was based on the following proposal:
https://github.com/SolidCode/SolidPython/issues/169

The goal was to

* extract the "core" from SolidPython
* make a solid package that only contains the fundamentals (+ a few convenience features) 
* make it extendible
* try to get complex libraries working properly (mcad, bosl, bosl2)
* **KISS**: ``from solid2 import *`` -> imports only ~1000 lines of source code and has (almost?) all the feautres SolidPython 1.x.x has
* be a drop in replacement for SolidPython 1.x.x -- as far as possible, see Backwards Compatibility Section
* get all kinds of nice features working (see Features section)

The result is a refactored and in some parts rewritten version of SolidPython we would like to release as SolidPython 2.x.x. The major improvement is a code base that should be better maintainable and extendible.

Besides these benefits SolidPython 2.x.x implemented quite a few nice new features (cf. Features section).

Features
--------

SolidPython 2.x.x has support for the following new features:

* **bosl2** - SolidPython is now able to handle bosl2 pretty well (don't know whether everything works, but quite a lot). `bosl2 example <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid2/examples/07-libs-bosl2.py>`_ and `mazebox example <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid2/examples/16-mazebox-bosl2.py>`_
* native **OpenSCAD customizer** support `customizer example <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid2/examples/10-customizer.py>`_ and `greedy scad interface example <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid2/examples/17-greedy-scad-interface.py>`_
* native **OpenSCAD animation** support `animation example <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid2/examples/12-animation.py>`_ and `animation example 2 <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid2/examples/13-animated-bouncing-ball.py>`_
* **custom fonts** `fonts example <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid2/examples/11-fonts.py>`_
* supports **ImplicitCAD** `implicitCAD example <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid2/examples/14-implicitCAD.py>`_ and `implicitCAD example 2 <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid2/examples/15-implicitCAD2.py>`_

Furthermore it has several minor improvements, like these which are based on ideas from *posts* from the SolidPython universe:

* use invert operator (~) as # in OpenSCAD `#167 <https://github.com/SolidCode/SolidPython/pull/167>`_
* convenience function including to pass sizes as integer parameters (``translate(10, 20, 30)``) `#63 <https://github.com/SolidCode/SolidPython/pull/63#issuecomment-688171416>`_
* *access-style* syntax: ``cube(1).up(5).rotate(45, 0, 0)`` `#66 <https://github.com/SolidCode/SolidPython/pull/66>`_ This is additional! The OpenSCAD / SolidPython style syntax is still fully supported.

Another nice little feature especially to play around and debug it is that the ``__repr__`` operator of each "OpenSCADObject" now calls ``scad_render``. With this the python shell becomes pretty good in debuging and playing around with solid code and the library itself:

.. code:: python

  >>> from solid2 import *
  >>> c = cube(5)
  >>> c.up(5)
  translate(v = [0, 0, 5]) {
          cube(size = 5);
  };
  >>> c.up(5).save_as_scad()
  '/home/xxx/xxx/xxx/SolidPython/expsolid_out.scad'
  >>>

Backwards compatibility
-----------------------

SolidPython 2.x.x should be a complete and mostly backwards compatible drop in
replacement for SolidPython 1.x.x.
The backwards compatibility is not 100% as depicted by the version number.
Somethings (and even interfaces) changed. We tried to stay as backward
compatible as possible.  The package should behave 98% the same as SolidPython
unless you do some "deep access" -- that's by 99% chance not backwards
compatible (like modifying OpenSCADObjects or import internal modules).

As long as you stick to:

.. code:: python

  from solid2 import *

you shoul be fine.

**solid.utils**

``solid.utils`` consisted of convenience functions and "modelling extensions" (kind of a small third party library like `mcad, bosl, bosl2`).
The convenience functions are now -- or the missing ones are supposed to be -- part of `solid2.extensions.convenience` and are automatically importet with the main package.

Concerning the "modelling extensions" I would actually like to get rid of them as part of the SolidPython 2.x.x package. The resons are the following:

* these modelling extensions (like `extrude_along_path, splines, screw_threads, part_hole,...`) don't align with the (core) purpose of SolidPython as I understand it (I think SolidPython is supposed to be a python "wrapper" / interface for OpenSCAD)
* these modelling extensions are "yet another implementation" of common modelling task that need to be maintained. I would prefere a SolidPython design where these features are outsourced into a third party library
* SolidPython 2.x.x has a pretty good **bosl2** support and bosl2 has all (?) the features provided by `solid.utils`:

  * extrude_along_path: https://github.com/revarbat/BOSL2/wiki/mutators.scad#module-path_extrude
  * First-class Negative Space (Holes): https://github.com/revarbat/BOSL2/wiki/attachments.scad#module-diff
  * Splines / Bezier: https://github.com/revarbat/BOSL2/wiki/beziers.scad
  * Screw threads: https://github.com/revarbat/BOSL2/wiki/screws.scad https://github.com/revarbat/BOSL2/wiki/metric_screws.scad https://github.com/revarbat/BOSL2/wiki/threading.scad
  * distributors: https://github.com/revarbat/BOSL2/wiki/distributors.scad
  * bouding boxes: https://github.com/revarbat/BOSL2/wiki/mutators.scad#module-bounding_box
  * arcs, pie slices, tubes, ...: https://github.com/revarbat/BOSL2/wiki/shapes3d.scad https://github.com/revarbat/BOSL2/wiki/drawing.scad
  * cut models in "half" / by a plane: https://github.com/revarbat/BOSL2/wiki/mutators.scad#functionmodule-half_of
  * attachments: https://github.com/revarbat/BOSL2/wiki/attachments.scad

And a looooot more.....

I don't see why SolidPython should implement and maintain its own set of these features. Furthermore I assume a third party library (like `bosl2`) is probably able to provide more sophisticated implementations than we will ever be able to provide.

Please take a look at the `bosl2` implementations. I did some very basic tests in ``examples/07-libs-bosl2.py`` and -- at least -- was able to create basic examples for the core `solid.utils` features using bosl2.

I would also be fine with a python third party library that implements these features, but I would like to seperate it from SolidPython itself. The reason is to achieve a SolidPython module which is independent from it (development, bugs, maintainance) with the goal to get an as solid and stable as possible SolidPython (core) package.

BUT, since I assume quite a few people out there are using `solid.utils` up until now and simply getting rid of it might cause some brouhaha, my suggestion for a compromise is the `solid_legay` extension.

**solid2_legacy**

The `solid2_legacy` extension is basicly everything that used to be `solid.utils`. Furhtermore it tries to "mimic" the SolidPython 1.x.x interface. This is the effort to become as backward compatible as possible. This might for example be useful when trying to get existing SolidPython 1.x.x code running.

The `solid2_legacy` extension got extracted into a seperate repo (and pip package). You should be able to just import the package if it is installed or somewhere in your import path.

If you want to use those features import the extension and take a look at it.

.. code:: python

  from solid2_legacy import *

Anyway SolidPython 1.x.x `imports` do not work with SolidPython 2.x.x! (see Interface changes - imoprt paths have changed)

I was able to get the SolidPython 1.x.x examples running just by changing the imports and they all (except for the splines example which seems to have an internal issue) worked "out of the box".


**Interface changes**

* OpenSCAD identifier escaping:
        * all *illegal* python idetifiers are escape with a single prepending underscore
        * special variables ``$fn -> _fn`` (*note*: ``segments`` still works)
        * identifier starting with a digit ``module 12ptStar() -> _12ptStar()`` (*note*: ``__12ptStar`` still works)
        * python keywords ``module import() -> _import()`` (*note*: ``import\_``  still works)

* import paths have changed (a lot)
    * as long as you only import the root package it should be fine, otherwise probably not
    
    .. code:: python
    
            from solid2 import * #fine
            from solid2 import objects #crash
            from solid2 import solidpython #crash
            from solid2 import splines #crash
            from solid2 import utils #crash

* all extensions have been moved:
    * solid.utils has been moved to ``solid2_legacy``. If you want to use them import that extension
    * there are some example implementations of the part / hole feature and
      bill of materials in ``solid2_legacy``. They seem to work but are
      not tested extensively. Take a look at ``examples/xx_legacy*``.
    * please take a look at the bosl2 example. BOSL2 provides many features which
      might be alternatives.

* OpenSCADObject internally changed a lot
    If you access it directly
    (e.g. mycube.set_modifier) this might not work. But if you import
    ``solid2_legacy`` some dummy methods will be monkey patched onto
    OpenSCADObject so you might be able to at least run the code, but it
    might render not correctly.

* maybe some more things I can't remember. Some function signatures changed
  slightly. But as long as as you stick to the regular public interface
  everything should be fine.


Contact
=======

Enjoy!

If you have any questions or bug reports please report them to the SolidPython
`GitHub page <https://github.com/jeff-dh/SolidPython>`__!



Cheers!

License
=======

This library is free software; you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation; either version 2.1 of the License, or (at
your option) any later version.

This library is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
General Public License for more details.

`Full text of the
license <http://www.gnu.org/licenses/old-licenses/lgpl-2.1.txt>`__.

Some class docstrings are derived from the `OpenSCAD User Manual
<https://en.wikibooks.org/wiki/OpenSCAD_User_Manual>`__, so 
are available under the `Creative Commons Attribution-ShareAlike License
<https://creativecommons.org/licenses/by-sa/3.0/>`__. 

