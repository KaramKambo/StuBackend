from model.images import Images
import random
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse # used for REST API building
from __init__ import db, project_path
import base64


def get_image():
    images = Images.query.all()
    return images


images_bp = Blueprint("images", __name__, url_prefix='/api/images')
images_api = Api(images_bp)

class ImagesAPI:
    class _ReturnImages(Resource):
        def get(self):
            image = get_image()
            json_data = {}
            if image:
                image_path = project_path + "/" + image.imagePath
                with open(image_path, "rb") as image_file:
                    json_data["bytes"] = str(base64.b64encode(image_file.read()))[2:][:-1]
            return jsonify(json_data)

    class _PostImages(Resource):
        def post(self):
            json_data = request.get_json()
            if "base64_string" and "name" in json_data:
                base64_string = json_data["base64_string"]
                name = json_data["name"]
                image_data = base64.b64decode(base64_string)
                # Save the image to the database
                image = Images(imagePath=f"{project_path}/images/{name}.jpg", imageData=image_data)
                db.session.add(image)
                db.session.commit()
                return jsonify({"message": "Image saved successfully"})
            else:
                return jsonify({"error": "Invalid request"})
            
    images_api.add_resource(_ReturnImages, "/")
    images_api.add_resource(_PostImages, "/upload")
            

        

            
    
    