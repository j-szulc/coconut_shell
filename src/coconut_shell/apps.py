from . import coco_app

class Decode(coco_app.CocoAppIO):

    def __init__(self, encoding="utf-8"):
        self.encoding = encoding

    def set_input(self, src):
        self.src = src

    def get_output(self):
        return self.src.decode(self.encoding)