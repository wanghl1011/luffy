import time
from django.contrib.auth.models import AnonymousUser
VISIT_RECORD = {}


# 自定义节流类
class VisitThrottle(object):
    def __init__(self):
        self.history = None
        self.seconds = 120
        self.num = 100

    # 具体做节流控制
    def allow_request(self, request, view):
        if isinstance(request.user,AnonymousUser):
            print("IS AnonymousUser")
            self.seconds =20
            self.num = 3
        # 1. 获取用户IP
        remote_addr = request.META.get('REMOTE_ADDR')
        # print("IPIPIPIPIPIPIPIPIPIP",remote_addr)
        ctime = time.time()
        if remote_addr not in VISIT_RECORD:
            VISIT_RECORD[remote_addr] = [ctime, ]
            return True
        history = VISIT_RECORD.get(remote_addr)
        self.history = history

        while history and history[-1] < ctime - self.seconds:
            history.pop()

        if len(history) < self.num:
            history.insert(0, ctime)
            return True
    def wait(self):
        ctime = time.time()
        return self.seconds - (ctime - self.history[-1])