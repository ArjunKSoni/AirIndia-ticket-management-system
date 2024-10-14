import jwt
from django.conf import settings
from django.http import JsonResponse

class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'AUTHORIZATION' in request.headers:
            token = request.headers['AUTHORIZATION']
            try:
                data = jwt.decode(token, key=settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
                request.user = data
            except Exception as e:
                print(e)
                return JsonResponse({"error":"Invalid token"})
        response = self.get_response(request)
        return response