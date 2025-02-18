from .base import BaseService

class HealthCheckService(BaseService):

    def handle(self):
        return {
            "status": 200,
            "message": "healthy"
        }