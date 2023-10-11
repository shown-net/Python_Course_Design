class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def say_hello(self):
        print("Hello, my name is ", self.name, ". I am ", self.age, " years old.")


p = Person("Tom", 20)
p.say_hello()