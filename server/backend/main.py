
from fastapi import FastAPI
from core.utils.register_router import route_registry
import routes  # noqa
from core.auth.jwt_key_manager import JWTKeyManager



app = FastAPI()


JWTKeyManager.load_keys_from_file()

for route in route_registry:
    app.include_router(route.router)