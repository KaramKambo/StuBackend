from model.images import Images
import random
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from __init__ import db, project_path
import base64

class ImagesAPI:
    class _EasyImages(Resource):
        def get(self):
            def get_random_easy_image():
                images = Images.query.filter_by(_difficulty=0).all()
                image = random.choice(images)
                return image
            
            image = get_random_easy_image()
            json_data = {}
            if image:
                image_path = project_path + "/" + image.imagePath
                with open(image_path, "rb") as image_file:
                    json_data["bytes"] = str(base64.b64encode(image_file.read()))[2:][:-1]
                json_data["xCoord"] = image.xCoord
                json_data["yCoord"] = image.yCoord
            return jsonify(json_data)
    
    