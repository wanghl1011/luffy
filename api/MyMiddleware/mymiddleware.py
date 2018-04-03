from django.utils.deprecation import MiddlewareMixin

class MyCorsMiddleWare(MiddlewareMixin):

    def process_response(self, request, response):

        response["Access-Control-Allow-Origin"] = "http://localhost:8080"
        response["Access-Control-Allow-Headers"] = "content-type"
        response["Access-Control-Allow-Methods"] = "*"

        return response