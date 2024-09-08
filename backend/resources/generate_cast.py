from flask import jsonify, request
from flask_restful import Resource
from flasgger import swag_from
from werkzeug.exceptions import BadRequest


from transformers_models.generate_cast.predict import predict_cast


class Generate_Cast(Resource):
    @swag_from("./swagger_docs/generate-cast.yml")
    def post(self):
       try:
            data = request.get_json()
            if "keywords" not in data or not isinstance(data["keywords"], str):
                raise BadRequest("Invalid 'keywords' key or value in request body.")

            predicted_cast= predict_cast(data["keywords"])
            return jsonify({"predicted_cast": predicted_cast})

        except BadRequest as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": f"An error occurred while generating cast: {e}"}, 500
