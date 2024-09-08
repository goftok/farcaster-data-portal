from flask_restful import Resource
from flasgger import swag_from


class HealthyCheck(Resource):
    @swag_from("./swagger_docs/healthy-check.yml")
    def get(self):
        return {"status": "healthy"}, 200
