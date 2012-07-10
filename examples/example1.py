#!/usr/bin/env python

class A:
   def __init__(self):
      self.an_int = 1
      self.a_float = 3.14
      self.foo_method()
      bar = 2
      
   def foo_method(self):
      return "arg!"


class B(A):
   def foo_method(self):
      self.d_ref = D()
      self.str = "string"
      baz = "baz"
      return 1


class C:
   def __init__(self):
      self.b = B()

class D:
   def __init__(self):
      self.some_dict = {}
      self.a_list = []
      blah = []

   def bar_method(self, options):
      return []

class E:
   def __init__(self):
      temp1 = D()
      temp2 = A()
      temp3 = ""
      temp4 = []


if __name__ == "__main__":
   a = A()
   b = B()
   c = C()
   d = D()
   e = E()

