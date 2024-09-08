from art import tprint

from rich.console import Console
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flasgger import Swagger

from backend.resources.home_page import HomePage
from backend.resources.healthy_check import HealthyCheck
from backend.resources.check_copywriting import CheckCopywriting
from backend.resources.generate_cast import GenerateCast
from backend.resources.get_most_warps_tipped import GetMostWarpsTipped
from backend.resources.get_ens_for_the_user import GetEnsForTheUser
from backend.env_links import MODEL_PATH

console = Console()


def print_config():
    tprint("Farcaster Data Portal")
    console.print(f"Models path: {MODEL_PATH}")


def create_app():
    app = Flask(__name__)
    CORS(app, methods=["GET", "POST"])

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec_1",
                "route": "/apispec_1.json",
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "title": "Farcaster Data Portal API",
        "version": "1.0.0",
        "description": "API for accessing and manipulating Farcaster data",
        "termsOfService": "Terms of service",
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",
    }

    Swagger(app, config=swagger_config)

    api = Api(app)
    api.add_resource(HomePage, "/")
    api.add_resource(HealthyCheck, "/health-check")
    api.add_resource(CheckCopywriting, "/check-copywriting")
    api.add_resource(GenerateCast, "/generate-cast")
    api.add_resource(GetMostWarpsTipped, "/get-most-warps-tipped")
    api.add_resource(GetEnsForTheUser, "/get-ens-for-the-user")

    return app


app = create_app()
print_config()

if __name__ == "__main__":
    app.run(debug=False)
