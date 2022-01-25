def my_jwt_response_payload_handler(token, user, request):
    """
    登录响应内容
    """
    return {
        "token":token,
        "username":user.username,
        "id":user.id
    }