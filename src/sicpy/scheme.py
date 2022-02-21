from __future__ import annotations
from functools import singledispatch
import types
import typing
import collections.abc
from dataclasses import dataclass
import builtins as py

class SchemeError(Exception):
  def __init__(self, msg, *args, **kwargs):
    if kwargs:
      super().__init__(msg, *args, kwargs)
    else:
      super().__init__(msg, *args)

def error(msg, *args, **kwargs):
  raise SchemeError(msg, *args, **kwargs)

@singledispatch
def length(x):
  raise TypeError(f"Can't take length of {type(x)}")

@length.register
def _(x: collections.abc.Sized):
  return len(x)

@singledispatch
def null(x):
  return False

@null.register
def _(x: types.NoneType):
  return x is None

@null.register
def _(x: collections.abc.Sized):
  return length(x) <= 0

@singledispatch
def car(l):
  raise TypeError(f"Can't take car of {type(l)}")

@singledispatch
def cdr(l):
  raise TypeError(f"Can't take cdr of {type(l)}")

@car.register
def _(x: types.NoneType):
  return None

@cdr.register
def _(x: types.NoneType):
  return None


@car.register
def _(x: collections.abc.Sequence):
  return x[0]

@cdr.register
def _(x: collections.abc.Sequence):
  return x[1:]

@singledispatch
def set_car(l, x):
  l[0] = x

@singledispatch
def set_cdr(l, x):
  return error(f"Can't set_cdr for {type(l)}", l, x)
  # del l[1:]
  # l.extend(x)


@dataclass
class Cons:
  car: typing.Any
  cdr: typing.Any

  def __repr__(self):
    s = "("
    sep = ""
    l = self
    while consp(l):
      s += sep + repr(car(l))
      sep = " "
      l = cdr(l)
    if not null(l):
      s += " . " + repr(l)
    s += ")"
    return s

@singledispatch
def repr(x):
  return py.repr(x)

@repr.register
def _(x: str):
  if x.isidentifier():
    return x
  else:
    return py.repr(x)

@repr.register
def _(x: types.NoneType):
  return "()"

repr.register(Cons)(Cons.__repr__)

# @singledispatch
# def cons(a, b):
#   return [a, *b]
def cons(a, b):
  return Cons(a, b)

def consp(x):
  return isinstance(x, Cons)

def for_each_tail(l: Cons):
  while consp(l):
    yield l
    l = cdr(l)

def list(*args):
  if args:
    return Cons(args[0], list(*args[1:]))

car.register(Cons)(lambda x: x.car)
cdr.register(Cons)(lambda x: x.cdr)

@set_car.register
def _(l: Cons, x):
  l.car = x

@set_cdr.register
def _(l: Cons, x):
  l.cdr = x

@length.register
def _(l: Cons):
  i = 0
  for x in for_each_tail(l):
    i += 1
  return i

@dataclass
class View:
  value: collections.abc.Sequence
  offset: int
  def __init__(self, l, offset=0):
    if isinstance(l, View):
      offset += l.offset
      l = l.value
    self.value = l
    self.offset = offset

  def car(self):
    return self.value[self.offset]

  def cdr(self):
    return View(self.value, self.offset + 1)

  def set_car(self, x):
    self.value[self.offset] = x

  def set_cdr(self, l):
    self.value[self.offset + 1:] = l

car.register(View)(View.car)
cdr.register(View)(View.cdr)
set_car.register(View)(View.set_car)
set_cdr.register(View)(View.set_cdr)


def display(x):
  print(x, end='', flush=True)

def newline():
  display("\n")