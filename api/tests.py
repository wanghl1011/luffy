# from django.test import TestCase

# Create your tests here.
# import threading
#
# lock = threading.Lock()
#
# class Singleton(type):
#     def __call__(cls, *args, **kwargs):
#         if not hasattr(cls, 'instance'):
#             with lock:
#                 # if not hasattr(cls,'instance'):
#                 obj = cls.__new__(cls,*args, **kwargs)
#                 obj.__init__(*args, **kwargs)
#                 setattr(cls,'instance',obj)
#                 return getattr(cls,'instance')
#         return getattr(cls, 'instance')
#
#
# class Foo(object,metaclass=Singleton):
#     def __init__(self):
#         self.name = 'alex'

# obj1 = Foo()
# obj2 = Foo()

# def w():
#     print("=====",Foo())
#     print("id====",id(Foo()))
#
# if __name__ == "__main__":
#     for i in range(20):
#         r = threading.Thread(target=w,)
#         r.start()


# print(obj1)
# print(obj2)