from django.contrib import admin
from django.conf.urls import url,include
from api import views
urlpatterns = [
    url(r'^(?P<version>[v1|v2]+)/auth/$', views.LoginView.as_view()),
    # 课程列表
    url(r'^(?P<version>[v1|v2]+)/course/$', views.CourseView.as_view({"get": "list"})),
    # 课程详细
    url(r'^(?P<version>[v1|v2]+)/course/(?P<pk>\d+)/$', views.CourseView.as_view({"get": "one"}),name='course'),
    # 文章列表
    url(r'^(?P<version>[v1|v2]+)/article/$', views.ArticleView.as_view({"get": "list"})),
    # 文章详细
    url(r'^(?P<version>[v1|v2]+)/article/(?P<pk>\d+)/$', views.ArticleView.as_view({"get": "one"})),
    # 文章点赞
    url(r'^(?P<version>[v1|v2]+)/article/agree/(?P<pk>\d+)/$', views.ArticleView.as_view({"get": "agree"})),
    # 文章收藏
    url(r'^(?P<version>[v1|v2]+)/article/collect/(?P<pk>\d+)/$', views.ArticleView.as_view({"get": "collect"})),
    # 文章评论
    url(r'^(?P<version>[v1|v2]+)/article/comment/(?P<pk>\d+)/$', views.ArticleView.as_view({"post": "comment"})),


    # 加入购物车
    url(r'^(?P<version>[v1|v2]+)/addcar/$', views.ShopCarView.as_view({"post": "post"})),
    # 更新购物车
    url(r'^(?P<version>[v1|v2]+)/patchcar/(?P<pk>\d+)/$', views.ShopCarView.as_view({"patch":"patch"})),
    # 删除购物车商品
    url(r'^(?P<version>[v1|v2]+)/delcar/(?P<pk>\d+)/$', views.ShopCarView.as_view({"delete":"delete"})),
    # 显示购物车
    url(r'^(?P<version>[v1|v2]+)/showcar/$', views.ShopCarView.as_view({"get": "get"})),

    # 加入结算中心
    url(r'^(?P<version>[v1|v2]+)/addjs/$', views.CountView.as_view({"post": "post"})),
    # 查看结算中心
    url(r'^(?P<version>[v1|v2]+)/showjs/$', views.CountView.as_view({"get": "get"})),
    # 更新结算的优惠卷
    url(r'^(?P<version>[v1|v2]+)/patchjs/$', views.CountView.as_view({"patch": "patch"})),

]