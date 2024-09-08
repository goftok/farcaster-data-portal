from flask import make_response
from flask_restful import Resource
from flasgger import swag_from


class HomePage(Resource):
    @swag_from("./swagger_docs/home.yml")
    def get(self):
        html = """
        <h1>Hi, welcome to the Farcaster Data Portal!</h1>
        <h3>If you see this, that means the backend is working properly.</h3>
        <h5>
            See docs: <br>
            <a href="/apidocs">/apidocs</a> <br>

        </h5>

        """
        response = make_response(html)
        response.headers["Content-Type"] = "text/html"
        return response
