#encoding=utf-8


import logging
from common.helpers import ok_json, error_json
from common.models import ApiAuth

def check_api_token(func):
    def api_auth(request, *args, ** kwargs):
        api_token = request.META.get("HTTP_API_TOKEN")
        logging.info("api_token=%s ", api_token)
        if api_token in ["", "None", None, "unkown"]:
            return error_json("Api Token 为空", 1000)
        api_auth = ApiAuth.objects.filter(api_token=api_token).first()
        if api_auth is None:
            return error_json("Api Token 不存在", 1000)
        if api_auth.status in ['UnVerify', 'Verifing']:
            return error_json("Api Token 审核中", 1000)
        if api_auth.is_expire == "YES":
            return error_json("Api Token 已经过期", 1000)
        return func(request, *args, **kwargs)
    return api_auth
