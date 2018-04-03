from django.contrib import admin
from api.models import *
# Register your models here.

# #################课程相关
admin.site.register(CourseCategory)
admin.site.register(CourseSubCategory)
admin.site.register(DegreeCourse)
admin.site.register(Teacher)
admin.site.register(Scholarship)
admin.site.register(Course)
admin.site.register(CourseDetail)
admin.site.register(OftenAskedQuestion)
admin.site.register(CourseOutline)
admin.site.register(CourseChapter)
admin.site.register(CourseSection)
admin.site.register(Homework)
admin.site.register(PricePolicy)

# ####################账户相关
admin.site.register(Account)
admin.site.register(UserAuthToken)
admin.site.register(Province)
admin.site.register(City)
admin.site.register(Industry)
admin.site.register(Profession)
admin.site.register(Feedback)
admin.site.register(Tags)

# #####################深科技相关
admin.site.register(ArticleSource)
admin.site.register(Article)
admin.site.register(Collection)
admin.site.register(Comment)

# ####################购买相关
admin.site.register(CouponRecord)
admin.site.register(Coupon)
