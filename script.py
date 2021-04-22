

class Animals:

    def is_alive(self):
        print('Iam alive!')


class Cat(Animals):

    name = 'Mysia'

    def __init__(self, color):
        self.color = color

    def get_voice(self):
        print('Meou, meou, meou...')



