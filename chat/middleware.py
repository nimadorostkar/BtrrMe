from channels.middleware import BaseMiddleware
from accounts.backends.jwt_auth import JWTAuthentication
from asgiref.sync import sync_to_async
from starlette.responses import JSONResponse


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        #headers = dict(scope['headers'])
        decoded_params = scope['query_string'].decode('utf-8')
        access_token = decoded_params.split('=')[1]
        try:
            user, _ = await sync_to_async(JWTAuthentication().ws_authenticate)(access_token)
            print(user)
            scope['user'] = user
            return await super().__call__(scope, receive, send)
        except Exception as e:
            print(f'-- error in reading token: {e} --')
            response = JSONResponse({"error": "Invalid or missing token", "details": str(e)}, status_code=401)
            await response(scope, receive, send)