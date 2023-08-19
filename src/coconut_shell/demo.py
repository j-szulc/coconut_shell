from . import coco_app

class Incrementer(coco_app.CocoAppIO):

    def set_input(self, src):
        self.number = src

    def get_output(self):
        return self.number + 1

    def print_output(self):
        print(self.get_output())
