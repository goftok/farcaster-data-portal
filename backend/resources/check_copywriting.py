from flask import jsonify, request
from flask_restful import Resource
from flasgger import swag_from
from werkzeug.exceptions import BadRequest


from copywriting.check_copywriting import check_cast_for_copyright


class CheckCopywriting(Resource):
    @swag_from("./swagger_docs/check-copywriting.yml")
    def post(self):
       try:
            data = request.get_json()
            if "cast_text" not in data or not isinstance(data["cast_text"], str):
                raise BadRequest("Invalid 'cast_text' key or value in request body.")

            casts , casts_count = check_cast_for_copyright(data["cast_text"])
            return jsonify({"casts": casts, "casts_count": casts_count})

        except BadRequest as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": f"An error occurred while checking copywriting: {e}"}, 500
