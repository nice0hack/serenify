from fastapi import APIRouter

class BaseRoutes:
    def __init__(self):
        self.router = APIRouter()
        self._register_routes()

    def _register_routes(self):
        """Register API routes."""
        pass