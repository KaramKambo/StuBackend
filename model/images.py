from sqlalchemy import Column, Integer, String, Text, LargeBinary
from sqlalchemy.exc import IntegrityError
from pathlib import Path
import sqlite3
from __init__ import app, db

class Images(db.Model):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    imagePath = Column(String(255), nullable=False)

    def __init__(self, imagePath):
        self.imagePath = imagePath

    def __repr__(self):
        return "<image(id='%s', imagePath='%s')>" % (
            self.id,
            self.imagePath
        )

    def to_dict(self):
        return {"id": self.id, "imagePath": self.imagePath}

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def read(self):
        return {
            "path": self.imagePath
        }

    def update(self, path=""):
        if path:
            self.imagePath = path
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None
    
def initEasyImages():
    with app.app_context():
        db.create_all()
        image_dir = Path.cwd()/"images"
        images_paths = [i.name for i in image_dir.iterdir()]
        images = [Images("images" + image) for image in images_paths]
        for image in images:
            try:
                image.create()
                print("Successfully added entry")
            except:
                db.session.remove()
                print("Error adding image: ", image.imagePath)
