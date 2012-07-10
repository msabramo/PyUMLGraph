# $Id: TestClasses.py,v 1.2 2003/10/16 17:25:26 adamf Exp $

class TestClassOne:
   def __init__(self):
      self.one = "a"
      self.two = "b"
      foo = "bar"
      self.three = 3
      self.pi = 3.141592
      self.list = []
      self.dict = {}

   def methodOne(self, methodOneArgOne = "defaultA"):
      self.vegetable = "rutabaga"
      return methodOneArgOne

   def methodTwo(self, methodTwoArgOne = None, methodTwoArgTwo = 1.614):
      self.two = []
      self.three = "three"
      return None


class TestClassTwo(TestClassOne):
   def __init__(self):
      TestClassOne.__init__(self)
      self.three = "c"
      baz = 9876

   def methodOne(self):
      self.four = "d"

   def methodTwo(self, methodTwoArgOne = TestClassOne()):
      pass


class TestClassThree:
   def __init__(self):
      pass

   def publicMethod(self):
      return None

   def privateMethod(self):
      "private"
      return TestClassOne()


class TestClassFour:
   def __init__(self):
      foo = TestClassThree()
      self.bar = TestClassTwo()

   def methodOne(self, methodOneArgOne, methodOneArgTwo, methodOneArgThree = "bar"):
      return
   
