from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet,ViewSetMixin
from django.db import transaction
from django.urls import reverse
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from api.models import *
from django.db import transaction
from api.utils.serializer import *
from api.utils.pagenation import MyPageNumberPagination
import json,time,hashlib
from django.db.models import F
from rest_framework.response import Response
import datetime
# @method_decorator(csrf_exempt,name='dispatch')
class LoginView(APIView):
    authentication_classes = []

    # def md5(self,user):
    #     ret = hashlib.md5(bytes(user.username, encoding="utf-8"))
    #     ret.update(bytes(user.uid, encoding='utf-8'))
    #     m = ret.hexdigest()
    #     return m
    def post(self, request, *args, **kwargs):
        ret = {"id":None,"name": None, "code": 1000, "token": None, "msg": "success"}
        try:
            name = request.data.get("username")
            pwd = request.data.get("password")
            user = Account.objects.filter(username=name, password=pwd).first()
            if not user:
                ret["code"] = 1001
                ret["msg"] = "用户名或密码错误"
                return Response(ret)
            user_token, status = UserAuthToken.objects.update_or_create(user_id=user.pk)
            ret["id"] = user.pk
            ret["token"] = user_token.token
            ret["name"]=name
            # ret["url"] = reverse(viewname="user", kwargs={"version":request.version,"pk":user.pk})
        except Exception as e:
            print("Exception>>>>>>>>>>>", e)
            ret["code"] = 1002
            ret["msg"] = "异常"
        response = Response(ret)
        return response


# @method_decorator(csrf_exempt,name='dispatch')
class CourseView(GenericViewSet):
    def list(self,request,*args,**kwargs):
        ret = {"code":2000,"JsonData":None,"msg":"success"}
        try:
            queryset = Course.objects.all()
            pg = MyPageNumberPagination()
            result = pg.paginate_queryset(queryset=queryset,request=request,view=self)
            ser = MyCourseserializer(instance=result,many=True, context={'request': request})
            ret["JsonData"]=ser.data
        except Exception as e:
            ret["code"] = 2001
            ret["msg"] = "发生错误"
            print("Exception>>>>>>>>>>>", e)
        finally:
            response = Response(ret)
            return response
    def one(self,request,*args,**kwargs):
        ret = {"code": 3000, "JsonData": None, "msg": "success"}
        try:
            s_pk = kwargs.get("pk")
            course_obj=Course.objects.filter(pk=s_pk).first()
            ser = MyCourseserializer(instance=course_obj, many=False, context={'request': request})
            ret["JsonData"]=ser.data
        except Exception as e:
            ret["code"]=3001
            ret["msg"] = "发生错误"
            print("Exception>>>>>>>>>>", e)
        finally:
            print("data",ret["JsonData"])
            response = Response(ret)
            return response


class ArticleView(GenericViewSet):
    serializer_class = MyCommentserializer

    def list(self,request,*args,**kwargs):
        print("这里")
        ret = {"code": 2000, "JsonData": None, "msg": "success"}
        try:
            queryset = Article.objects.all()
            pg = MyPageNumberPagination()
            result = pg.paginate_queryset(queryset=queryset, request=request, view=self)
            ser = MyArticleserializer(instance=result, many=True)
            ret["JsonData"] = ser.data
        except Exception as e:
            ret["code"] = 2001
            ret["msg"] = "发生错误"
            print("Exception>>>>>>>>>>>", e)
        finally:
            response = Response(ret)
            return response
    def one(self,request,*args,**kwargs):
        ret = {"code": 3000, "JsonData": None, "msg": "success"}
        try:
            s_pk = kwargs.get("pk")
            course_obj=Article.objects.filter(pk=s_pk).first()
            ser = MyArticleserializer(instance=course_obj, many=False)
            ret["JsonData"]=ser.data
        except Exception as e:
            ret["code"]=3001
            ret["msg"] = "发生错误"
            print("Exception>>>>>>>>>>", e)
        finally:
            print("one>>><><><><><><",ret["JsonData"])
            response = Response(ret)
            return response
    def agree(self,request,*args,**kwargs):
        ret={"code":2100,"msg":"success"}
        try:
            # print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            article_id = kwargs.get("pk")
            Article.objects.filter(pk=article_id).update(agree_num=F("agree_num")+1)
        except Exception as e :
            ret["code"]=2101
            ret["msg"]="点赞失败"
            print("Exception>>>>>>>>",e)
        finally:
            return Response(ret)
    def collect(self,request,*args,**kwargs):
        # print("collect>>>>>>>>>>>>")
        ret={"code":3100,"msg":"success"}
        try:
            article_id = kwargs.get("pk")
            article_obj=Article.objects.get(pk=article_id)
            # print("obj________",article_obj)
            with transaction.atomic():
                if article_obj.collection.filter(account=request.user).exists():
                    ret['code']=3102
                    ret["msg"]="您已经收藏过"
                else:
                    Collection.objects.create(account=request.user,content_object=article_obj)
                    Article.objects.filter(pk=article_id).update(collect_num=F("collect_num")+1)
        except Exception as e :
            ret["code"]=3101
            ret["msg"]="收藏失败"
            print("collectException>>>>>>>>",e)
        finally:
            return Response(ret)

    # def op(self,request,*args,**kwargs):
    #     return Response('')
    def comment(self,request,*args,**kwargs):
        # self.get_serializer()
        # return Response('...')
        # print("comment>>>>>>>")
        ret = {"code": 4100, "date":None, "username":None,"msg": "success"}
        try:
            article_id = kwargs.get("pk")
            content = request.data.get("content")
            # print(content)
            article_obj = Article.objects.get(pk=article_id)
            with transaction.atomic():
                comment_obj=Comment.objects.create(account=request.user,content=content,content_object=article_obj)
                Article.objects.filter(pk=article_id).update(comment_num=F("comment_num")+1)
                ret["date"]="%s-%s-%s %s:%s"%(comment_obj.date.year,comment_obj.date.month,comment_obj.date.day,comment_obj.date.hour+8,comment_obj.date.minute)
                ret["username"]=comment_obj.account.username
        except Exception as e:
            ret["code"] = 4101
            ret["msg"] = "评论失败"
            print("collectException>>>>>>>>", e)
        finally:
            return Response(ret)
# 购物车 = {
# 					1:{
# 						课程ID1:{
# 							name: "Python开发21天入门必备",
# 							img: '',
# 							default_price_policy:2,
# 							price_policy:{
# 								2: {...},
# 								3: {...},
# 							}
# 						},
# 					}
# 				}
SHOPPING_CAR = {}

class ShopCarView(ViewSetMixin,APIView):
    def post(self,request,*args,**kwargs):
        ret = {"code":1100,"JsonDate":None,"msg":"success"}
        # 要考虑重复选同一门课程的不同策略，要做更新
        user_id = request.user.pk
        print('user_id',user_id,type(user_id))
        course_id = request.data.get("cid")
        print("course_id",course_id,type(course_id))
        price_policy_id = request.data.get("ppid")
        print("price_policy_id",price_policy_id,type(price_policy_id))
        # price_list = request.data.get("price_list")
        # course_name = request.data.get("course_name")
        # price_dict = {price.get("id"):price for price in json.loads(price_list)}
        # print("price_dict",price_dict)
        # print(5555555555555,price_dict,type(price_dict))
        try:
            # 课程对象
            course_obj = Course.objects.get(pk=course_id)
            # 价格策略对象
            policy_obj = PricePolicy.objects.get(pk=price_policy_id)
            if not policy_obj:
                ret["code"] = 1103
                ret["msg"] = "价格策略不存在"
            # # 课程对应的所有价格策略对象
            course_policy_list=course_obj.price_policy.all()
            # # 先对课程和价格策略做检验
            if policy_obj not in course_policy_list:
                ret["code"] = 1102
                ret["msg"] = "价格策略与课程不对应"
                return Response(ret)
            pricepolicy_dict = {item.pk:{"id":item.pk,"price":item.price,"period":item.get_valid_period_display(),"period_id":item.valid_period} for item in course_policy_list}
            temp = {
                        "name":course_obj.name,
                        "img": None,
                        "default_price_policy":price_policy_id,
                        "price_policy": pricepolicy_dict
                    }

            if SHOPPING_CAR.get(user_id):
                SHOPPING_CAR[user_id] = json.loads(SHOPPING_CAR[user_id])
                print(333,SHOPPING_CAR[user_id])
                # 更新原有课程的价格策略
                if str(course_id) in SHOPPING_CAR[user_id]:

                    print(1)
                    SHOPPING_CAR[user_id][str(course_id)]["default_price_policy"] = price_policy_id
                # 创建新的课程和价格策略
                else:
                    print(2)
                    SHOPPING_CAR[user_id][course_id] = temp
                SHOPPING_CAR[user_id] = json.dumps(SHOPPING_CAR[user_id],ensure_ascii=False)
            else:
                # 创建操作
                print(3)
                user_shop_car={}
                user_shop_car[course_id] = temp
                SHOPPING_CAR[user_id] = user_shop_car
                print(444,SHOPPING_CAR)
                SHOPPING_CAR[user_id] = json.dumps(SHOPPING_CAR[user_id],ensure_ascii=False)
            ret["JsonDate"]=SHOPPING_CAR
            print(2222222222222222,SHOPPING_CAR)
        except Exception as e:
            ret["msg"] = "发生错误"
            print("Exception>>>>>>>>>>>>",e)
        finally:
            return JsonResponse(ret)

    def get(self, request, *args, **kwargs):
        print(request._request.get_full_path())
        print(request._request.path_info)
        print(request._request.path)
        ret={"code":1200,"msg":"success","data":None}
        try:
            my_car = SHOPPING_CAR.get(request.user.pk)
            print(type(my_car))

            my_car_dict = json.loads(my_car)
            ret["data"]=my_car_dict
        except Exception as e :
            ret["msg"] = "出错了"
            print("Exception>>>>>>>>>>>",e)
        finally:
            return Response(ret)

    def delete(self,request,*args,**kwargs):
        course_id = kwargs.get("pk")
        ret={
            "code":1300,
            "msg":"success"
        }
        try:
            my_car = SHOPPING_CAR.get(request.user.pk)
            my_car_dict = json.loads(my_car)
            if str(course_id) in my_car_dict:
                del my_car_dict[str(course_id)]
                SHOPPING_CAR[request.user.pk] = json.dumps(my_car_dict,ensure_ascii=False)
            else:
                ret["code"] = 1301
                ret["msg"] = "购物车不存在该课程"
        except Exception as e:
            ret["msg"] = "出现错误"
            print("Exception>>>>>>>>>>>",e)
        finally:
            print("delete>>>>",SHOPPING_CAR)
            return Response(ret)

    def patch(self,request,*args,**kwargs):
        course_id = kwargs.get("pk")
        price_policy_id = request.data.get("ppid")
        ret = {
            "code": 1400,
            "msg": "success",
            "data":None
        }
        try:
            my_car = SHOPPING_CAR.get(request.user.pk)
            my_car_dict = json.loads(my_car)
            if str(course_id) in my_car_dict:
                if str(price_policy_id) in my_car_dict[str(course_id)]["price_policy"]:
                    my_car_dict[str(course_id)]["default_price_policy"] = price_policy_id
                    SHOPPING_CAR[request.user.pk] = json.dumps(my_car_dict, ensure_ascii=False)
                else:
                    ret["code"] = 1402
                    ret["msg"] = "课程不存在此价格策略"
            else:
                ret["code"] = 1401
                ret["msg"] = "购物车不存在该课程"
        except Exception as e:
            ret["msg"] = "出现错误"
            print("Exception>>>>>>>>>>>", e)
        finally:
            print("patch>>>>", SHOPPING_CAR)
            return Response(ret)


JS_CENTER = {}
class CountView(ViewSetMixin, APIView):
    def post(self, request, *args, **kwargs):
        ret={"code":2100,"msg":"success","data":None}
        user_id = request.user.pk
        try:
            course_ids = request.data.get("cids")
            # 获取该用户的购物车
            my_car_dict = json.loads(SHOPPING_CAR.get(request.user.pk))
            # 校验课程id是否在购物车中
            for course_id in course_ids:
                if str(course_id) not in my_car_dict:
                    ret["code"] = 2101
                    ret["msg"] = "请先加入购物车"
                    ret["data"] = course_id
                    return JsonResponse(ret)
            # 获取到该用户所有可用的以及和课程对应的优惠卷
            course_coupon_list = Coupon.objects.filter(couponrecord__account=request.user, couponrecord__status=1, object_id__in=course_ids, content_type__model="course")
            course_coupon_dict = {}
            for coupon in course_coupon_list:
                coupon_dict = {
                    "id":coupon.pk,
                    "name":coupon.name,
                    "type":coupon.coupon_type,
                    # 满减额度
                    "money_equivalent_value":coupon.money_equivalent_value if coupon.coupon_type == 2 or coupon.coupon_type == 1 else None,
                    # 满减最低消费
                    "minimum_consume":coupon.minimum_consume if coupon.coupon_type == 2 else None,
                    # 折扣额度
                    "off_percent":coupon.off_percent if coupon.coupon_type == 3 else None
                }
                cid = coupon.object_id
                if cid in course_coupon_dict:
                    course_coupon_dict[cid][coupon.pk]=coupon_dict
                else:
                    course_coupon_dict[cid]={
                        0: {"id":0,"name":"课程优惠卷"},
                        coupon.pk: coupon_dict
                    }
            print("course_coupon_dict======",course_coupon_dict)
            # 获取全站优惠卷
            full_coupon_list = Coupon.objects.filter(couponrecord__account=request.user, couponrecord__status=1, object_id__isnull=True,content_type_id__isnull=True)
            full_coupon_dict = {}
            for coupon in full_coupon_list:
                full_coupon_dict[coupon.pk]={
                    "id":coupon.pk,
                    "name":coupon.name,
                    "type":coupon.coupon_type,
                    # 满减额度
                    "money_equivalent_value": coupon.money_equivalent_value if coupon.coupon_type == 2 or coupon.coupon_type == 1 else None,
                    # 满减最低消费
                    "minimum_consume": coupon.minimum_consume if coupon.coupon_type == 2 else None,
                    # 折扣额度
                    "off_percent": coupon.off_percent if coupon.coupon_type == 3 else None

                }
            # 构建用户自己的结算中心
            my_js_dict = {}
            policy_course_dict={}
            global_coupon_dict = full_coupon_dict
            for course_id in course_ids:
                # 价格策略id，价格，时间
                policy_id = my_car_dict[str(course_id)]["default_price_policy"]
                policy_price = my_car_dict[str(course_id)]["price_policy"][str(policy_id)]["price"]
                policy_period = my_car_dict[str(course_id)]["price_policy"][str(policy_id)]["period"]
                policy_period_id = my_car_dict[str(course_id)]["price_policy"][str(policy_id)]["period_id"]
                # 用户拥有的该课程对应的优惠卷
                policy_course_dict[course_id] = {
                    "course_id":course_id,
                    "course_name": my_car_dict[str(course_id)]["name"],
                    "course_img": my_car_dict[str(course_id)]["img"],
                    "policy_id":policy_id,
                    "policy_price":policy_price,
                    "policy_period":policy_period,
                    "period_id":policy_period_id,
                    "default_coupon":0,
                    "coupon_record_list":course_coupon_dict.get(course_id)
                }
            my_js_dict["policy_course_dict"] = policy_course_dict
            my_js_dict["global_coupon_dict"] = global_coupon_dict
            my_js_dict["default_global_coupon_id"] = 0
            print("my_js_dict========",my_js_dict)
            JS_CENTER[user_id] = json.dumps(my_js_dict,ensure_ascii=False)
        except Exception as e :
            ret["msg"] = '出错了'
            print("Exception========", e)
        return JsonResponse(ret)

    def get(self, request, *args, **kwargs):
        ret={"code":2200,"msg":"success","data":None}
        try:
            my_js_center_json = JS_CENTER.get(request.user.pk)
            if not my_js_center_json:
                raise Exception("出错了")
            my_js_center = json.loads(my_js_center_json)
            ret["data"]=my_js_center
        except Exception as e :
            ret["msg"] = "出错了"
            print("Exception>>>>>>>>>>>",e)
        finally:
            return JsonResponse(ret)

    def patch(self, request, *args, **kwargs):
        ret = {"code": 2200, "msg": "success"}
        course_id = request.data.get("course_id")
        coupon_id = request.data.get("coupon_id")
        # 校验课程id和优惠卷id是否合格
        if not CouponRecord.objects.filter(account=request.user, coupon_id=coupon_id, coupon__object_id=course_id,coupon__content_type='course').exists():
            ret["msg"] = "数据有错误"
            return JsonResponse(ret)
        try:
            # 获取当前用户的结算中心
            my_js_center = json.loads(JS_CENTER.get(request.user.pk))
            # 更新非全站优惠卷
            if course_id != 0 :
                # 找到课程对应的数据
                dic = my_js_center.get("policy_course_dict")
                course_dict = dic.get(str(course_id))
                course_dict["default_coupon"] = coupon_id
            # 更新全站优惠卷
            else:
                if str(coupon_id) in my_js_center.get("global_coupon_dict"):
                    my_js_center["default_global_coupon_id"] = coupon_id
                else:
                    ret['msg'] = "优惠卷不存在"
            JS_CENTER[request.user.pk] = json.dumps(my_js_center)
            print("my_js_center=======",my_js_center)
        except Exception as e :
            print("Exception========",e)
            ret["msg"] = "出错了"
        finally:
            return JsonResponse(ret)


class PayView(ViewSetMixin, APIView):
    def pay(self,request,*args, **kwargs):
        ret={"code":3300,"msg":None}
        try:
            # 获取用户提交的数据
            # 贝里数
            # 支付金额
            balance = request.data.get("bs")
            alipay = request.data.get('ap')
            # 获取当前用户结算中心的课程和优惠卷
            my_js_center = json.loads(JS_CENTER.get(request.user.pk))
            if not my_js_center:
                raise Exception('用户不对')
            # 课程的原总价
            total_price = 0
            # 课程使用优惠卷抵扣的总金额
            discount = 0
            # 用户结算中心的所有课程
            my_js_course_dict = my_js_center.get("policy_course_dict")
            if not my_js_course_dict:
                raise Exception("课程列表出错了")
            # 已使用的优惠卷列表
            used_coupon_list =[]
            # 已购买的课程字典
            payed_course_dict = {}
            # 处理课程优惠卷
            for course_id,course_dict in my_js_course_dict.items():
                # 校验课程是否已经下架
                if Course.objects.filter(id=course_id,status=2).exists():
                    raise Exception("课程已下架")
                # 判断是否该课程有可用的优惠卷
                if not course_dict["default_coupon"]:
                    payed_course_dict[course_id]={
                        "original_price":course_dict["policy_price"],
                        "price":course_dict["policy_price"],
                        "policy_period":course_dict["policy_period"],
                        "policy_period_id":course_dict["period_id"],
                    }
                    total_price += course_dict["policy_price"]
                else:
                    # 有可用的优惠卷
                    # 校验优惠卷是否过期
                    if CouponRecord.objects.filter(coupon_id=course_dict["default_coupon"],account=request.user,status=3).exists():
                        raise Exception("课程优惠卷已过期")
                    else:
                        # 优惠卷没有过期
                        used_coupon_list.append(course_dict["default_coupon"])
                        total_price += course_dict["policy_price"]
                        # 不同类型优惠卷做不同处理
                        coupon_id = course_dict["default_coupon"]
                        coupon_dict = course_dict["coupon_record_list"][str(coupon_id)]
                        coupon_type = coupon_dict["type"]
                        # 通用卷
                        if coupon_type == 1:
                            if coupon_dict["money_equivalent_value"] > course_dict["policy_price"]:
                                discount += course_dict["policy_price"]
                            else:
                                discount += coupon_dict["money_equivalent_value"]
                        # 满减卷
                        elif coupon_type ==2:
                            if course_dict["policy_price"] > coupon_dict["minimum_consume"]:
                                discount +=  coupon_dict["money_equivalent_value"]
                        # 折扣卷
                        elif coupon_type == 3:
                            discount += (100-coupon_dict["off_percent"])*0.01*course_dict["policy_price"]
                        payed_course_dict[course_id]={
                            "original_price":course_dict["policy_price"],
                            "price": course_dict["policy_price"] - discount,
                            "policy_period": course_dict["policy_period"],
                            "policy_period_id": course_dict["period_id"],
                        }
            # 处理全站优惠卷
            global_coupon_id = my_js_center["default_global_coupon_id"]
            # 校验优惠卷是否已过期
            if CouponRecord.objects.filter(coupon_id=global_coupon_id,account=request.user,status=3).exists():
                raise Exception("全站优惠卷过期")
            # 没有过期
            # 处理优惠卷类型
            used_coupon_list.append(my_js_center["global_coupon_id"])
            global_coupon_type = my_js_center["global_coupon_dict"][str(global_coupon_id)]["type"]
            global_coupon_dict = my_js_center["global_coupon_dict"][str(global_coupon_id)]
            # 通用卷
            if global_coupon_type == 1:
                if global_coupon_dict["money_equivalent_value"] > global_coupon_dict["policy_price"]:
                    discount += global_coupon_dict["policy_price"]
                else:
                    discount += global_coupon_dict["money_equivalent_value"]
            # 满减卷
            elif global_coupon_type == 2:
                if global_coupon_dict["policy_price"] > global_coupon_dict["minimum_consume"]:
                    discount += global_coupon_dict["money_equivalent_value"]
            # 折扣卷
            elif global_coupon_type == 3:
                discount += (100 - global_coupon_dict["off_percent"]) * 0.01 * global_coupon_dict["policy_price"]
            # 判断金额是否正确
            if balance + alipay + discount != total_price:
                raise Exception("金额出错了")
            ctime = datetime.datetime.now()
            # 生成订单
            with transaction.atomic():
                if alipay == 0 :
                    # 还要判断支付的类型
                    order_obj=Order.objects.create(account=request.user,status=1)
                else:
                    order_obj=Order.objects.create(account=request.user,status=2)
                # 生成订单详细
                for course_id,course_price in payed_course_dict:
                    # 生成订单详细
                    orderdetail_obj=OrderDetail.objects.create(
                        order=order_obj,
                        content_type__model='course',
                        object_id=course_id,
                        original_price=course_price["course_price"],
                        price = course_price["price"],
                        valid_period_display=course_price["policy_period"],
                        valid_period=course_price["policy_period_id"]
                    )
                    # 生成已报名课程记录
                    EnrolledCourse.objects.create(
                        order_detail=orderdetail_obj,
                        account=request.user,
                        course_id = course_id,
                        valid_begin_date=ctime.date(),
                        valid_end_date = ctime+datetime.timedelta(days=course_price["policy_period_id"])
                    )
                # 改变优惠卷状态
                CouponRecord.objects.filter(pk__in=used_coupon_list).update(status=2,order=order_obj)
                # 生成贝里交易记录
                TransactionRecord.objects.create(
                    account=request.user,
                    amount=balance,
                    balance=request.user.balance,
                    transaction_type=1,
                    content_object=order_obj,
                    transaction_number='xxxxx'
                )
                # 更新用户贝里
                Account.objects.filter(pk=request.user.pk).update(balance=F("balance")-balance)
                # 生成支付URL
                if alipay:
                    pass
        except Exception as e:
            ret["code"] = 3301
            ret["msg"] = e
        finally:
            return JsonResponse(ret)







