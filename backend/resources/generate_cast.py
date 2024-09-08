from flask import jsonify, request
from flask_restful import Resource
from flasgger import swag_from
from werkzeug.exceptions import BadRequest

from transformers import T5ForConditionalGeneration, T5Tokenizer


from transformers_models.generate_cast.predict import predict_cast

path_to_model = "/home/ubuntu/hackathon6/transformers_models/models_cast/checkpoint-1516"

model = T5ForConditionalGeneration.from_pretrained(path_to_model)
tokenizer = T5Tokenizer.from_pretrained(path_to_model, legacy=False)
max_length = 250


class GenerateCast(Resource):
    @swag_from("./swagger_docs/generate-cast.yml")
    def post(self):
        try:
            data = request.get_json()
            if "keywords" not in data or not isinstance(data["keywords"], str):
                raise BadRequest("Invalid 'keywords' key or value in request body.")

            predicted_cast = predict_cast(data["keywords"], model, tokenizer, max_length)
            return jsonify({"predicted_cast": predicted_cast})

        except BadRequest as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": f"An error occurred while generating cast: {e}"}, 500
