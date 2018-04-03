# 结算中心 = {
#   user.id: {
#     policy_course_dict: {
#        课程ID: {
#           'course_id': course_id,
#           'course_name': product['name'],
#           'course_img': product['course_img'],
#           'policy_id': product['choice_policy_id'],
#           'policy_price': policy_price,
#           'policy_period': policy_period,
#           'default_coupon': 0,
#           'coupon_record_list': {
#               0: {'id': 0, 'text': '请选择优惠券'},
#               1: {'id': 1, 'type': 1, 'text': '优惠券1',..},
#               2: {'id': 2, 'type': 2, 'text': '优惠券1',..},
#               3: {'id': 3, 'type': 3, 'text': '优惠券1',..},
#            },
#        },
#        课程ID:{
#            'course_id': course_id,
#            'course_name': product['name'],
#            'course_img': product['course_img'],
#            'policy_id': product['choice_policy_id'],
#            'policy_price': policy_price,
#            'policy_': policy_period,
#            'default_coupon': 0,
#            'coupon_record_list': {
#                0: {'id': 0, 'text': '请选择优惠券'},
#                1: {'id': 1, 'type': 1, 'text': '优惠券1',..},
#                2: {'id': 2, 'type': 2, 'text': '优惠券1',..},
#                3: {'id': 3, 'type': 3, 'text': '优惠券1',..},
#             },
#        }
#   },
#   global_coupon_dict: {
#     1: {'type': 0, 'text': "通用优惠券", 'id': 1,..},
#     2: {'type': 0, 'text': "通用优惠券", 'id': 2,..},
#     3: {'type': 0, 'text': "通用优惠券", 'id': 3, ...},
#     4: {'type': 0, 'text': "通用优惠券", 'id': 4, ...},
#   },
#   global_coupon_id: 0
#   }
#
# }






# class MyType(type):
#     def __init__(self,*args,**kwargs):
#         super().__init__(*args,**kwargs)
#
#     def __call__(self, *args, **kwargs):
#         obj = self.__new__(self, *args, **kwargs)
#         obj.__init__(*args,**kwargs)
#         return obj
#
#
# class Foo(object,metaclass=MyType):
#
#     def __new__(cls, *args, **kwargs):
#         print(11111)
#         obj = super().__new__(cls, *args, **kwargs)
#         return obj
#
#     def __init__(self, *args, **kwargs):
#         print("2222")
#
# obj = Foo()
# print(obj)



# {1:
#      {
#          8:
#           {
#               'id': 8,
#               'name': '课程1折扣卷1',
#               'type': 3,
#               'money_equivalent_value': None,
#               'minimum_consume': None,
#               'off_percent': 80}},
# 2:
#     {
#       5:
#           {
#              'id': 5,
#              'name': '课程2满减卷',
#              'type': 2,
#              'money_equivalent_value': 30,
#              'minimum_consume': 299,
#              'off_percent': None},
#     13: {
#         'id': 13,
#         'name': '课程2折扣卷2',
#         'type': 3, 'money_equivalent_value': None,
#         'minimum_consume': None, 'off_percent': 90}
#     }
# }




# 1:{
#     'policy_course_dict':
#         {
#             1:
#                 {
#                     'course_id': 1,
#                     'course_name': '爬虫开发',
#                     'course_img': None,
#                     'policy_id': 1,
#                     'policy_price': 299.0,
#                     'policy_period': '1个月',
#                     'default_coupon': 0,
#                     'coupon_record_list': {
#                         0: {'id': 0, 'name': '请选择优惠卷'},
#                         8: {
#                             'id': 8,
#                             'name': '课程1折扣卷1',
#                             'type': 3,
#                             'money_equivalent_value': None,
#                             'minimum_consume': None,
#                             'off_percent': 80}
#                     }
#                 },
#             2:
#                 {
#                     'course_id': 2,
#                     'course_name': 'CRM客户关系管理系统实战开发',
#                     'course_img': None,
#                     'policy_id': 5,
#                     'policy_price': 399.0,
#                     'policy_period': '1个月',
#                     'default_coupon': 0,
#                     'coupon_record_list': {
#                         0: {'id': 0, 'name': '请选择优惠卷'},
#                         5: {
#                             'id': 5,
#                             'name': '课程2满减卷',
#                             'type': 2,
#                             'money_equivalent_value': 30,
#                             'minimum_consume': 299,
#                             'off_percent': None},
#                         13: {
#                             'id': 13,
#                             'name': '课程2折扣卷2',
#                             'type': 3,
#                             'money_equivalent_value': None,
#                             'minimum_consume': None,
#                             'off_percent': 90}}}
#         },
#     'global_coupon_dict':
#         {
#             1: {'id': 1, 'name': '双十一通用卷', 'money_equivalent_value': 100},
#             2: {'id': 2, 'name': '双十二通用卷', 'money_equivalent_value': 150}
#         },
#     'global_coupon_id': 0
# }

#
#
#
# class Field(object):
#     pass
#
# class CharField(Field):
#     pass
#
# class EmailField(Field):
#     pass
# obj_list = [EmailField(),CharField(),dict(),Field()]
# # for item in obj_list:
# #     if isinstance(item,CharField):
# #         print(666)
# #     elif isinstance(item, EmailField):
# #         print(999)
# #     elif isinstance(item, dict):
# #         print(123)
# for item in obj_list:
#     # print(type(item))
#     print(issubclass(type(item),Field))
#     # if isinstance(item,Field):
#     #     print(888)
#     if type(item) == Field:
#         print(888)
#     # elif isinstance(item, dict):
#     #     print(123)
#     elif type(item) == dict:
#         print(123)


# s = 1
# print(id(s))
# s = 2
# print(id(s))

# li = [1,2,[1,2]]
# print(id(li))
# print(id(li[2]))
# li[2].append(123)
# print(id(li[2]))


# import datetime
# ctime = datetime.datetime.now()
# print(ctime.date().day)
# print(ctime+datetime.timedelta(days=30))


class Foo(object):
    def __init__(self,name):
        self.name = name
# o1=Foo('alex')
# o2=Foo('aaaa')
# print(o1)
# print(o2)
# print(id(Foo('alex')))
# print(id(Foo('aaaa')))
print(Foo("alex"))
print(Foo("aaaa"))



# print(Foo("whl"),type(Foo('alex')))
# print(id(Foo("whl")))
# obj = Foo("whl")
# print(obj,type(obj))










