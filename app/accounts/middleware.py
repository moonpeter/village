from django.utils.deprecation import MiddlewareMixin


class CustomHeaderMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # 기존 헤더의 토큰
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        # 검증하여 반환된 토큰
        auth = request.__dict__.get("auth")
        # 반환된 토큰중 invalid 체킹용 변수
        auth_invalid_list = {"Expired", "Invalid", "NotUser"}
        # 유저가 인증 안됐으면
        if not request.user.is_authenticated:
            # 검증 토큰이 invalid list에 존재하면
            if auth in auth_invalid_list:
                # 헤더에 어떤 토큰 에러인지 반환
                response.headers["Token-Error"] = auth
            return response
        # 토큰이 있고
        if auth_header:
            try:
                token = auth_header.split()[1]
                # 토큰이 검증이 됐고, 기존 토큰과 검증 토큰이 다르다면
                if auth and token != str(auth) and auth != None and auth != "Expired":
                    # 헤더에 새로운 토큰 반환
                    response.headers["Authorization"] = f"Bearer {auth}"
            # 토큰 길이가 다르면
            except IndexError:
                # 무시하고 반환
                return response
        return response
