from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth.models import AnonymousUser
from accounts.backends.jwt_auth import JWTAuthentication
from django.core.exceptions import SynchronousOnlyOperation
from asgiref.sync import sync_to_async
from starlette.responses import JSONResponse



class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        try:
            token_name, token_key = headers.get(b'authorization').decode().split()
            if token_name == 'Bearer':
                user, _ = await sync_to_async(JWTAuthentication().ws_authenticate)(scope)
                scope['user'] = user
            return await super().__call__(scope, receive, send)

        except Exception as e:
            print('-- error in readin headers --')
            response = JSONResponse({"error": "Invalid or missing token", "details": str(e)}, status_code=401)
            await response(scope, receive, send)