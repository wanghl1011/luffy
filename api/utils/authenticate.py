from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from api.models import *


class MyAuthentication(BaseAuthentication):
    def authenticate(self,request,*args,**kwargs):
        token = request.query_params.get("token")

        obj = UserAuthToken.objects.filter(token=token).first()
        if not obj:
            raise exceptions.AuthenticationFailed("用户认证失败")
        return (obj.user, None)

    def authenticate_header(self, request):
        print("认证失败")
        # return "hahahahahahahahhahah"