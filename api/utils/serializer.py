from rest_framework import serializers
from api.models import *


class MyCourseserializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="pk")
    level = serializers.CharField(source="get_level_display")
    recommend = serializers.SerializerMethodField()
    jieshao = serializers.CharField(source='coursedetail.video_brief_link')
    course_url = serializers.HyperlinkedIdentityField(view_name="course",lookup_field="id",lookup_url_kwarg="pk")
    comment = serializers.SerializerMethodField()
    zhangjie = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    questions = serializers.SerializerMethodField()

    def get_questions(self,row):
        queryset = row.oaq.all()
        temp = [{"question": item.question,"answer": item.answer} for item in queryset]
        return temp

    def get_price(self,row):
        queryset = row.price_policy.all()
        temp = [{"id":item.pk,"period": item.get_valid_period_display(),"price": item.price} for item in queryset]
        return temp

    def get_recommend(self,row):
        # print(">>>>>>>>>>>",row)
        queryset = row.coursedetail.recommend_courses.all()
        temp = [{"name":item.name,"id":item.pk} for item in queryset]
        return temp

    def get_zhangjie(self,row):
        print(">>>>>>>>>>>",type(row))
        queryset = row.course_chapters.all()
        temp = []
        for item in queryset:
            dic = {}
            dic["chapter"]=item.chapter
            dic["title"]=item.name
            dic["sections"]=[{"name":i.name,"time":i.video_time} for i in item.course_sections.all()]
            if not dic["sections"]:
                dic["sections"]=None
            temp.append(dic)
        return temp
    def get_comment(self,row):
        # print(">>>>>>>>>>>",row)
        queryset = row.comment.all()
        temp = [{"name":item.account.username,"content":item.content} for item in queryset]
        if temp:
            return temp
        else:
            return None
    class Meta:
        model = Course
        fields = [
            "course_url","id","name","brief",
            'recommend',
            'level',
            "jieshao",
            "comment",
            "zhangjie",
            "price",
            "questions"]


class MyArticleserializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="pk")
    tags = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    def get_tags(self,row):
        queryset = row.tags.all()
        temp = [{"name":item.name,"id":item.pk} for item in queryset]
        return temp
    def get_comment(self,row):
        queryset = row.comment.all().extra(select={"time":"strftime('%%Y-%%m-%%d %%H:%%M',date)"})
        temp = [{"name": item.account.username,"time":item.time, "content": item.content} for item in queryset]
        if not temp :
            temp = None
        return temp
    class Meta:
        model = Article
        fields = ["id","title",'brief',"view_num","comment_num","collect_num","content","tags","agree_num",'comment']


class MyShopCarserializer(serializers.ModelSerializer):
    data_list = serializers.SerializerMethodField()
    def get_data_list(self,row):
        queryset = row.course.all()
        temp=[]

        for course in queryset:
            dic={}
            dic["course_name"] = course.name
            dic["price_list"]=[
                {"period":item.get_valid_period_display(),"price":item.price,"selected": 1 if item == row.price_policy else 0} for item in course.price_policy.all]
            temp.append(dic)


        return temp

    class Meta:
        model = Article
        fields = ["pk", "data_list",]

class MyCommentserializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"